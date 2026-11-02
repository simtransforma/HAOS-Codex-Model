#!/usr/bin/env python3
import argparse
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

EMAIL_ALIASES = {"email", "e-mail", "e mail", "mail"}
PHONE_ALIASES = {"telefone", "phone", "celular", "whatsapp", "fone"}
NAME_ALIASES = {"nome", "empresa", "instituicao", "instituição", "company", "contato"}
CITY_ALIASES = {"cidade", "city", "municipio", "município"}


def norm(value):
    text = "" if value is None else str(value).strip()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def detect_column(columns, aliases):
    normalized = {norm(c): c for c in columns}
    for alias in aliases:
        if norm(alias) in normalized:
            return normalized[norm(alias)]
    for alias in aliases:
        wanted = norm(alias)
        for normalized_name, original in normalized.items():
            if normalized_name.startswith(wanted + " "):
                return original
    return None


def load(path):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return {"CSV": pd.read_csv(path, dtype=str, keep_default_na=False)}
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=None, dtype=str, keep_default_na=False)
    raise SystemExit("Formato não suportado. Use CSV, XLSX ou XLS.")


def main():
    parser = argparse.ArgumentParser(description="Audita estrutura e duplicidades de uma lista de prospecção.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("prospect_audit"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    frames = []
    sheet_stats = []
    for sheet, df in load(args.input).items():
        df = df.copy()
        df["__source_sheet"] = sheet
        frames.append(df)
        sheet_stats.append({"sheet": sheet, "rows": len(df), "columns": list(df.columns)})
    all_rows = pd.concat(frames, ignore_index=True, sort=False).fillna("")

    email_col = detect_column(all_rows.columns, EMAIL_ALIASES)
    phone_col = detect_column(all_rows.columns, PHONE_ALIASES)
    name_col = detect_column(all_rows.columns, NAME_ALIASES)
    city_col = detect_column(all_rows.columns, CITY_ALIASES)
    usable_columns = [c for c in [name_col, email_col, phone_col] if c]
    if usable_columns:
        usable_mask = all_rows[usable_columns].astype(str).apply(
            lambda col: col.str.strip().ne("")
        ).any(axis=1)
        all_rows = all_rows.loc[usable_mask].copy()

    all_rows["__email_normalized"] = all_rows[email_col].map(lambda x: str(x).strip().lower()) if email_col else ""
    all_rows["__phone_normalized"] = all_rows[phone_col].map(lambda x: re.sub(r"\D", "", str(x))) if phone_col else ""
    all_rows["__name_normalized"] = all_rows[name_col].map(norm) if name_col else ""
    all_rows["__city_normalized"] = all_rows[city_col].map(norm) if city_col else ""

    strong_key = []
    for _, row in all_rows.iterrows():
        if row["__email_normalized"]:
            strong_key.append("email:" + row["__email_normalized"])
        elif row["__phone_normalized"]:
            strong_key.append("phone:" + row["__phone_normalized"])
        elif row["__name_normalized"]:
            strong_key.append("namecity:" + row["__name_normalized"] + "|" + row["__city_normalized"])
        else:
            strong_key.append("")
    all_rows["__dedupe_key"] = strong_key
    dup_mask = all_rows["__dedupe_key"].ne("") & all_rows.duplicated("__dedupe_key", keep=False)

    email_valid = (
        all_rows["__email_normalized"].str.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        if email_col else pd.Series(False, index=all_rows.index)
    )
    all_rows["__email_syntax"] = email_valid.map({True: "válida", False: "ausente/inválida"})

    duplicates = all_rows.loc[dup_mask].copy()
    clean = all_rows.loc[~dup_mask].copy()
    review = all_rows.loc[dup_mask | ~email_valid].copy()

    all_rows.to_csv(args.output_dir / "audit_all_rows.csv", index=False, encoding="utf-8-sig")
    clean.to_csv(args.output_dir / "prospects_without_strong_duplicates.csv", index=False, encoding="utf-8-sig")
    review.to_csv(args.output_dir / "prospects_review.csv", index=False, encoding="utf-8-sig")
    duplicates.to_csv(args.output_dir / "duplicate_candidates.csv", index=False, encoding="utf-8-sig")

    summary = {
        "input": str(args.input),
        "sheets": sheet_stats,
        "rows": len(all_rows),
        "duplicate_candidates": int(dup_mask.sum()),
        "email_syntax_valid": int(email_valid.sum()),
        "email_missing_or_invalid": int((~email_valid).sum()),
        "detected_columns": {
            "name": name_col, "email": email_col, "phone": phone_col, "city": city_col
        },
        "warning": "Candidatos fuzzy e caixas de e-mail exigem revisão/verificador próprio; não auto-mesclar.",
    }
    (args.output_dir / "audit_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
