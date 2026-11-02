# -*- coding: utf-8 -*-
"""
HAOS Auto-Brain - destilador de aprendizados (referencia generica)

Creditos: inspirado nas ideias do GBrain de Garry Tan
(github.com/garrytan/gbrain, MIT): ingestao automatica, create_safety
(anti-duplicata) e gap analysis. Esta e uma reimplementacao adaptada ao
stack HAOS (memoria markdown + 1 LLM barato via API compativel com OpenAI),
nao o codigo do GBrain.

O QUE FAZ:
  Le o inbox JSONL do dia (prompts capturados pelo bloco de captura) + o
  indice da memoria + a lista de arquivos de memoria existentes (anti-duplicata).
  Faz 1 chamada barata a um LLM pedindo APRENDIZADOS DURAVEIS que ainda nao
  estao na memoria. Aplica os de alta confianca (cria/atualiza .md no padrao
  de frontmatter + ponteiro no indice) e joga os de baixa confianca / gaps
  numa fila de revisao humana.

SALVAGUARDAS:
  - Tudo LOCAL. Manda ao LLM SO os prompts do usuario + o indice da memoria.
    NUNCA dados sensiveis de terceiros (CRM, financeiro, PII).
  - 1 call barata por execucao. Sem daemon, sem loop.
  - Kill-switch global: arquivo .brain_off no HAOS_BRAIN_DIR desliga tudo.
  - Fail-safe: qualquer erro -> loga e sai 0 (nunca quebra o fechamento).
  - Idempotente: registra prompts ja processados; nao reprocessa.
  - Nunca embute segredos. Le a chave de API de variavel de ambiente.

CONFIG (tudo por variavel de ambiente, sem path de maquina, sem segredo):
  HAOS_MEMORY_DIR     -> pasta da memoria markdown (.md + indice). OBRIGATORIA.
  HAOS_BRAIN_DIR      -> pasta de trabalho do brain. Default: <MEMORY_DIR>/_brain
  HAOS_MEMORY_INDEX   -> nome do arquivo de indice. Default: MEMORY.md
  OPENROUTER_API_KEY  -> chave do provedor compativel com OpenAI. OBRIGATORIA.
  HAOS_BRAIN_BASE_URL -> endpoint chat/completions. Default: OpenRouter.
  HAOS_BRAIN_MODEL    -> id do modelo barato. Default: um "flash-lite".

USO:
  python distiller.py [--date YYYY-MM-DD] [--session <id>] [--dry-run]
  Sem --date, usa o inbox de hoje. --dry-run mostra o JSON sem gravar nada.
"""
import os
import sys
import json
import re
import argparse
import datetime
import urllib.request
import urllib.error

# ----------------------------------------------------------------------------
# Caminhos / config (tudo via env, nada hardcoded)
# ----------------------------------------------------------------------------
MEMORY_DIR = os.environ.get("HAOS_MEMORY_DIR")
BRAIN_DIR = os.environ.get(
    "HAOS_BRAIN_DIR",
    os.path.join(MEMORY_DIR, "_brain") if MEMORY_DIR else os.path.join(os.getcwd(), "_brain"),
)
MEMORY_INDEX_NAME = os.environ.get("HAOS_MEMORY_INDEX", "MEMORY.md")
MEMORY_INDEX = os.path.join(MEMORY_DIR, MEMORY_INDEX_NAME) if MEMORY_DIR else None

BRAIN_OFF = os.path.join(BRAIN_DIR, ".brain_off")
PENDING = os.path.join(BRAIN_DIR, "pending-review.md")
LOG = os.path.join(BRAIN_DIR, "consolidation-log.jsonl")
PROCESSED = os.path.join(BRAIN_DIR, "processed.json")

OPENROUTER_URL = os.environ.get(
    "HAOS_BRAIN_BASE_URL", "https://openrouter.ai/api/v1/chat/completions"
)
MODEL = os.environ.get("HAOS_BRAIN_MODEL", "google/gemini-2.5-flash-lite")

VALID_TYPES = ("user", "feedback", "project", "reference")


# ----------------------------------------------------------------------------
# Util
# ----------------------------------------------------------------------------
def log(event, **kw):
    """Append fail-safe no log de consolidacao."""
    try:
        os.makedirs(BRAIN_DIR, exist_ok=True)
        rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), "event": event}
        rec.update(kw)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def read_api_key():
    """Le a chave de API de variavel de ambiente. Nunca imprime o valor."""
    return os.environ.get("OPENROUTER_API_KEY")


def slugify(title, mtype):
    """Gera nome de arquivo no padrao <type>_<slug>.md"""
    base = title.lower()
    base = re.sub(r"[à-ÿ]", lambda m: {
        "á": "a", "à": "a", "â": "a", "ã": "a",
        "é": "e", "ê": "e", "í": "i", "ó": "o",
        "ô": "o", "õ": "o", "ú": "u", "ç": "c",
    }.get(m.group(0), ""), base)
    base = re.sub(r"[^a-z0-9]+", "_", base).strip("_")[:50]
    prefix = mtype if mtype in VALID_TYPES else "reference"
    return "%s_%s.md" % (prefix, base or "auto")


def existing_memory_files():
    try:
        return sorted(
            f for f in os.listdir(MEMORY_DIR)
            if f.endswith(".md") and f != MEMORY_INDEX_NAME
        )
    except Exception:
        return []


def load_processed():
    try:
        with open(PROCESSED, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_processed(s):
    try:
        os.makedirs(BRAIN_DIR, exist_ok=True)
        with open(PROCESSED, "w", encoding="utf-8") as f:
            json.dump(sorted(s), f, ensure_ascii=False)
    except Exception:
        pass


# ----------------------------------------------------------------------------
# Inbox
# ----------------------------------------------------------------------------
def load_inbox(date_str, session_filter, processed):
    """Le inbox do dia. Retorna lista de (key, record) ainda nao processados."""
    inbox = os.path.join(BRAIN_DIR, "inbox-%s.jsonl" % date_str)
    out = []
    if not os.path.exists(inbox):
        return out
    try:
        with open(inbox, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if session_filter and rec.get("session_id") != session_filter:
                    continue
                key = "%s|%s" % (rec.get("ts", ""), (rec.get("prompt", "") or "")[:80])
                if key in processed:
                    continue
                out.append((key, rec))
    except Exception:
        pass
    return out


# ----------------------------------------------------------------------------
# LLM
# ----------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "Voce e um destilador de memoria de longo prazo. Recebe prompts recentes do "
    "usuario e o indice atual da memoria. Sua tarefa: extrair APENAS "
    "APRENDIZADOS DURAVEIS (preferencias, regras, fatos sobre o usuario/operacao, "
    "correcoes) que AINDA NAO estejam na memoria. Ignore o efemero/operacional "
    "(tarefas pontuais, perguntas, comandos). Responda SOMENTE JSON valido, sem "
    "texto fora do JSON, sem markdown. Escreva em portugues do Brasil. NUNCA use "
    "o caractere travessao."
)


def build_user_prompt(prompts, index_text, file_list):
    lines = ["PROMPTS RECENTES DO USUARIO:"]
    for i, p in enumerate(prompts, 1):
        lines.append("%d. %s" % (i, p))
    lines.append("")
    lines.append("ARQUIVOS DE MEMORIA EXISTENTES (nao duplicar):")
    lines.append(", ".join(file_list) if file_list else "(nenhum)")
    lines.append("")
    lines.append("INDICE DA MEMORIA:")
    lines.append(index_text[:6000])
    lines.append("")
    lines.append(
        "Responda um JSON com este formato EXATO:\n"
        "{\n"
        '  "learnings": [\n'
        "    {\n"
        '      "title": "titulo curto",\n'
        '      "type": "user|feedback|project|reference",\n'
        '      "body": "1 a 3 frases com a regra/fato/preferencia",\n'
        '      "action": "CREATE|UPDATE <arquivo-existente.md>|SKIP",\n'
        '      "confidence": "high|low"\n'
        "    }\n"
        "  ],\n"
        '  "gaps": ["ambiguidade ou ponto a confirmar com o usuario"]\n'
        "}\n"
        "Se nada novo, retorne learnings vazio. Use confidence=high so quando o "
        "aprendizado for claramente duravel e inequivoco; caso contrario low."
    )
    return "\n".join(lines)


def call_llm(key, user_prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 1500,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OPENROUTER_URL, data=data,
        headers={
            "Authorization": "Bearer %s" % key,
            "Content-Type": "application/json",
            "X-Title": "HAOS Auto-Brain",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
    obj = json.loads(body)
    return obj["choices"][0]["message"]["content"]


def parse_llm_json(text):
    """Extrai o objeto JSON da resposta (tolerante a cercas de markdown)."""
    t = text.strip()
    t = re.sub(r"^```(json)?", "", t).strip()
    t = re.sub(r"```$", "", t).strip()
    m = re.search(r"\{.*\}", t, re.DOTALL)
    if m:
        t = m.group(0)
    return json.loads(t)


# ----------------------------------------------------------------------------
# Aplicacao na memoria (anti-duplicata = create_safety, ideia do GBrain)
# ----------------------------------------------------------------------------
def write_memory_file(item, session_id):
    """Cria/atualiza arquivo .md no padrao de frontmatter. Retorna o nome."""
    mtype = item.get("type", "reference")
    if mtype not in VALID_TYPES:
        mtype = "reference"
    action = item.get("action", "CREATE")
    today_br = datetime.date.today().strftime("%d/%m/%Y")
    today_iso = datetime.date.today().isoformat()

    fname = None
    upd = re.match(r"UPDATE\s+(.+\.md)", action, re.IGNORECASE)
    if upd:
        # create_safety: so casa UPDATE se o arquivo realmente existir.
        cand = os.path.basename(upd.group(1).strip())
        if os.path.exists(os.path.join(MEMORY_DIR, cand)):
            fname = cand
    if not fname:
        fname = slugify(item.get("title", "auto"), mtype)

    path = os.path.join(MEMORY_DIR, fname)
    body = item.get("body", "").strip()
    origin = "(captado automaticamente em %s pelo Auto-Brain HAOS)" % today_br

    if os.path.exists(path):
        # UPDATE: anexa a regra no fim, sem reescrever o frontmatter.
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n\n## Atualizacao %s\n%s\n%s\n" % (today_br, body, origin))
        except Exception as e:
            log("write_error", file=fname, error=str(e))
            return None
    else:
        slug = fname[:-3]
        desc = body.replace('"', "'")[:200]
        content = (
            "---\n"
            "name: %s\n"
            'description: "%s"\n'
            "metadata:\n"
            "  node_type: memory\n"
            "  type: %s\n"
            "  created: %s\n"
            "  originSessionId: %s\n"
            "  source: auto-brain\n"
            "---\n"
            "%s\n\n"
            "%s\n"
        ) % (slug, desc, mtype, today_iso, session_id or "auto", body, origin)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            log("write_error", file=fname, error=str(e))
            return None
    return fname


def update_index(fname, title, body):
    """Adiciona ponteiro no indice se ainda nao existir (create_safety)."""
    try:
        with open(MEMORY_INDEX, "r", encoding="utf-8") as f:
            content = f.read()
        if "(%s)" % fname in content:
            return  # ja referenciado, nao duplica
        short = body.strip().split(".")[0][:160]
        line = "- %s (dependency not bundled: %s) - %s (auto-brain)\n" % (title, fname, short)
        if not content.endswith("\n"):
            content += "\n"
        content += line
        with open(MEMORY_INDEX, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        log("index_error", file=fname, error=str(e))


def append_pending(items, gaps):
    """Escreve itens de baixa confianca + gaps na fila de revisao humana."""
    try:
        os.makedirs(BRAIN_DIR, exist_ok=True)
        today_br = datetime.date.today().strftime("%d/%m/%Y")
        chunks = []
        if not os.path.exists(PENDING):
            chunks.append(
                "# Auto-Brain - Fila de revisao\n\n"
                "Itens de BAIXA confianca e gaps detectados pelo destilador. "
                "Nao foram gravados na memoria. Revise e confirme/descarte.\n"
            )
        chunks.append("\n## Revisao de %s\n" % today_br)
        for it in items:
            chunks.append(
                "- [ ] (%s) **%s** - %s\n"
                % (it.get("type", "?"), it.get("title", "?"), it.get("body", "").strip())
            )
        for g in gaps:
            chunks.append("- [ ] (gap) %s\n" % g)
        with open(PENDING, "a", encoding="utf-8") as f:
            f.write("".join(chunks))
    except Exception as e:
        log("pending_error", error=str(e))


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--session", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not MEMORY_DIR:
        print("[brain] defina HAOS_MEMORY_DIR. Saindo sem erro.")
        return 0

    # Kill-switch
    if os.path.exists(BRAIN_OFF):
        log("skip", reason="brain_off")
        print("[brain] kill-switch .brain_off ativo, nada a fazer.")
        return 0

    processed = load_processed()
    items = load_inbox(args.date, args.session, processed)
    if not items:
        log("skip", reason="empty_inbox", date=args.date)
        print("[brain] sem prompts novos no inbox de %s, sem custo." % args.date)
        return 0

    # Foco nos candidatos a aprendizado (economiza tokens), mas se nao houver
    # candidato, ainda marca como processado para nao reanalisar.
    candidates = [r for (_, r) in items if r.get("learning_candidate")]
    prompts = [r.get("prompt", "") for r in candidates]
    keys = [k for (k, _) in items]

    if not prompts:
        if not args.dry_run:
            processed.update(keys)
            save_processed(processed)
        log("skip", reason="no_learning_candidates", n=len(items))
        print("[brain] %d prompts, nenhum candidato. Marcados como vistos." % len(items))
        return 0

    # Contexto da memoria
    try:
        with open(MEMORY_INDEX, "r", encoding="utf-8") as f:
            index_text = f.read()
    except Exception:
        index_text = ""
    file_list = existing_memory_files()

    key = read_api_key()
    if not key:
        log("error", reason="no_api_key")
        print("[brain] OPENROUTER_API_KEY nao definida no ambiente. Saindo sem erro.")
        return 0

    user_prompt = build_user_prompt(prompts, index_text, file_list)

    try:
        raw = call_llm(key, user_prompt)
        result = parse_llm_json(raw)
    except urllib.error.HTTPError as e:
        log("error", reason="http_error", code=getattr(e, "code", "?"))
        print("[brain] erro HTTP no LLM (%s). Saindo sem quebrar." % getattr(e, "code", "?"))
        return 0
    except Exception as e:
        log("error", reason="llm_call", error=str(e))
        print("[brain] erro na chamada/parse do LLM: %s. Saindo sem quebrar." % e)
        return 0

    learnings = result.get("learnings", []) or []
    gaps = result.get("gaps", []) or []

    high = [l for l in learnings
            if l.get("confidence") == "high"
            and str(l.get("action", "")).upper() != "SKIP"]
    low = [l for l in learnings
           if l.get("confidence") != "high"
           and str(l.get("action", "")).upper() != "SKIP"]

    session_id = candidates[0].get("session_id", "") if candidates else ""

    # ---- DRY RUN: so mostra o JSON, nao grava nada ----
    if args.dry_run:
        print("=== [brain] DRY-RUN ===")
        print("Candidatos analisados: %d" % len(prompts))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("\nAplicaria (high): %d | pending (low+gaps): %d + %d gaps"
              % (len(high), len(low), len(gaps)))
        return 0

    # ---- APLICACAO ----
    applied = []
    for item in high:
        fname = write_memory_file(item, session_id)
        if fname:
            update_index(fname, item.get("title", "Aprendizado"), item.get("body", ""))
            applied.append({"file": fname, "title": item.get("title"), "action": item.get("action")})

    if low or gaps:
        append_pending(low, gaps)

    processed.update(keys)
    save_processed(processed)

    log("consolidated",
        date=args.date,
        candidates=len(prompts),
        applied=[a["file"] for a in applied],
        pending=len(low),
        gaps=len(gaps))

    print("[brain] consolidado: %d aplicados, %d pending, %d gaps."
          % (len(applied), len(low), len(gaps)))
    for a in applied:
        print("   + %s (%s)" % (a["file"], a["action"]))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:
        # Fail-safe absoluto: nunca derruba o fechamento.
        try:
            log("fatal", error=str(e))
        except Exception:
            pass
        print("[brain] erro inesperado (ignorado): %s" % e)
        sys.exit(0)

