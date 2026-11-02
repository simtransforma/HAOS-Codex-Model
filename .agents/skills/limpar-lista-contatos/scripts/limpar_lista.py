#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
limpar_lista.py - Limpa listas de contatos de planilhas e exporta CSV (nome, email, numero).

Normaliza o telefone para E.164 sem o "+", com codigo de pais (default Brasil 55).
Limpeza mecanica: remove tudo que nao e digito, remove prefixos de discagem
(00 internacional e 0 de troncal de DDD) e prefixa o codigo do pais quando ausente.
NAO valida se o DDD existe e NAO inventa/remove digitos do assinante.

Uso:
  python limpar_lista.py ENTRADA [--sheet ABA | --all-sheets] [--out SAIDA.csv]
         [--nome COL] [--email COL] [--fone COL] [--country 55] [--dedup]

Exemplos:
  python limpar_lista.py base.xlsx --sheet Master --out Master_PNL.csv
  python limpar_lista.py base.xlsx --all-sheets
  python limpar_lista.py contatos.csv --fone Celular --out limpo.csv --dedup
"""
import argparse
import os
import re
import sys

import pandas as pd

# Heuristica de auto-deteccao de colunas pelo nome do cabecalho (minusculo).
CAND_NOME = ["nome", "name", "cliente", "contato", "nome completo", "full name"]
CAND_EMAIL = ["email", "e-mail", "e mail", "mail", "correio"]
CAND_FONE = ["numero", "telefone", "celular", "whatsapp", "fone", "tel",
             "mobile", "phone", "contato", "cel"]


def achar_col(cols, candidatos):
    """Acha a coluna cujo header bate com algum candidato (exato e depois parcial)."""
    low = {str(c).lower().strip(): c for c in cols}
    for cand in candidatos:               # match exato primeiro
        if cand in low:
            return low[cand]
    for cand in candidatos:               # depois match parcial
        for lc, orig in low.items():
            if cand in lc:
                return orig
    return None


def normaliza_fone(valor, country="55"):
    """Limpa e normaliza um telefone para 'country + nacional' (E.164 sem o +)."""
    d = re.sub(r"\D", "", "" if valor is None else str(valor))
    if not d:
        return ""
    if d.startswith("00"):                # saida internacional 00 -> remove
        d = d[2:]
    if d.startswith("0"):                 # troncal de DDD (011 -> 11) -> remove
        d = d.lstrip("0")
    if not d:
        return ""
    # Ja tem o codigo do pais na frente? (codigo + 10 digitos no minimo)
    if d.startswith(country) and len(d) >= len(country) + 10:
        return d
    return country + d


def carregar(entrada, sheet=None, all_sheets=False):
    """Le xlsx/csv e retorna dict {nome_aba: DataFrame} com tudo como string."""
    ext = os.path.splitext(entrada)[1].lower()
    if ext in (".xlsx", ".xls", ".xlsm"):
        if all_sheets:
            return pd.read_excel(entrada, sheet_name=None, dtype=str)
        nome = sheet if sheet is not None else 0
        return {sheet or "aba": pd.read_excel(entrada, sheet_name=nome, dtype=str)}
    # CSV: detecta o separador automaticamente.
    df = pd.read_csv(entrada, dtype=str, sep=None, engine="python", encoding="utf-8-sig")
    return {"limpo": df}


def processar(df, args):
    cols = list(df.columns)
    c_nome = args.nome or achar_col(cols, CAND_NOME)
    c_email = args.email or achar_col(cols, CAND_EMAIL)
    c_fone = args.fone or achar_col(cols, CAND_FONE)
    if not c_fone:
        sys.exit(f"ERRO: nao achei a coluna de telefone em {cols}. Use --fone NOME_DA_COLUNA.")
    out = pd.DataFrame(index=df.index)
    out["nome"] = df[c_nome].fillna("").astype(str).str.strip() if c_nome else ""
    out["email"] = df[c_email].fillna("").astype(str).str.strip() if c_email else ""
    out["numero"] = df[c_fone].apply(lambda v: normaliza_fone(v, args.country))
    out = out.reset_index(drop=True)
    if args.dedup:
        out = (out[out["numero"] != ""]
               .drop_duplicates(subset=["numero"])
               .reset_index(drop=True))
    return out, (c_nome, c_email, c_fone)


def main():
    ap = argparse.ArgumentParser(
        description="Limpa lista de contatos de planilha e exporta CSV (nome, email, numero).")
    ap.add_argument("entrada", help="arquivo .xlsx/.xls/.csv de entrada")
    ap.add_argument("--sheet", help="aba especifica (Excel)")
    ap.add_argument("--all-sheets", action="store_true", help="processa todas as abas")
    ap.add_argument("--out", help="arquivo .csv de saida")
    ap.add_argument("--nome", help="forca o nome da coluna de nome")
    ap.add_argument("--email", help="forca o nome da coluna de email")
    ap.add_argument("--fone", help="forca o nome da coluna de telefone")
    ap.add_argument("--country", default="55", help="codigo do pais (default 55)")
    ap.add_argument("--dedup", action="store_true", help="remove telefones duplicados")
    args = ap.parse_args()

    if not os.path.isfile(args.entrada):
        sys.exit(f"ERRO: arquivo nao encontrado: {args.entrada}")

    sheets = carregar(args.entrada, args.sheet, args.all_sheets)
    base = os.path.splitext(args.entrada)[0]
    for nome_aba, df in sheets.items():
        out, usadas = processar(df, args)
        if args.out and not args.all_sheets:
            saida = args.out
        else:
            saida = f"{base}_{nome_aba}.csv"
        out.to_csv(saida, index=False, encoding="utf-8-sig")
        vazios = int((out["numero"] == "").sum())
        print(f"[OK] {nome_aba}: {len(out)} linhas -> {saida} "
              f"| colunas usadas (nome,email,fone)={usadas} | sem numero: {vazios}")


if __name__ == "__main__":
    main()

