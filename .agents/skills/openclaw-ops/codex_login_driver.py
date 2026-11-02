#!/usr/bin/env python3
"""Driver pty para re-login OAuth codex no OpenClaw (headless/VPS).
Uso (dentro do container `openclaw`):
  1. docker exec -i openclaw tee /tmp/codex_login_driver.py < this_file
  2. docker exec openclaw bash -lc 'setsid bash -c "python3 /tmp/codex_login_driver.py" >/dev/null 2>&1 &'
  3. ler URL: sed -e "s/\\x1b\\[[0-9;?]*[a-zA-Z]//g" /tmp/codex_login2.out | grep -aoE "https://service.example.invalid ]*" | head -1
  4. Gian autoriza no browser -> devolve a redirect URL como TEXTO
  5. docker exec -i openclaw bash -lc 'cat > /tmp/codex_answer.txt'   (heredoc com a URL)
  6. conferir: grep -aiE "ANSWER SENT|Auth profile|error|EXIT" no /tmp/codex_login2.out
Mata por pidfile: kill $(cat /tmp/codex_driver.pid). NUNCA pkill -f com padrao na propria cmdline.
"""

raise RuntimeError('requires_user_config: render placeholders, review bindings and remove this guard only after local validation')

import os, pty, subprocess, time, select

OUT = "/tmp/codex_login2.out"
ANSWER = "/tmp/codex_answer.txt"
for f in (OUT, ANSWER):
    try: os.remove(f)
    except OSError: pass
open(ANSWER, "w").close()
open("/tmp/codex_driver.pid", "w").write(str(os.getpid()))

logf = open(OUT, "wb", buffering=0)
master, slave = os.openpty()
p = subprocess.Popen(
    ["openclaw", "models", "auth", "--agent", "main", "login", "--provider", "openai-codex"],
    stdin=slave, stdout=slave, stderr=slave, close_fds=True, preexec_fn=os.setsid,
)
os.close(slave)
open("/tmp/codex_login.pid", "w").write(str(p.pid))

buf = b""
sent = False
deadline = time.time() + 900
while True:
    if time.time() > deadline:
        logf.write(b"\n[DRIVER] TIMEOUT\n"); break
    r, _, _ = select.select([master], [], [], 1.0)
    if master in r:
        try:
            chunk = os.read(master, 4096)
        except OSError:
            break
        if not chunk:
            break
        buf += chunk
        logf.write(chunk)
    if (not sent) and (b"authorization code" in buf or b"redirect URL" in buf):
        try:
            ans = open(ANSWER).read().strip()
        except Exception:
            ans = ""
        if ans:
            time.sleep(0.5)
            os.write(master, ans.encode() + b"\r")
            sent = True
            logf.write(b"\n[DRIVER] ANSWER SENT len=%d\n" % (len(ans),))
    if p.poll() is not None:
        try:
            while True:
                r2, _, _ = select.select([master], [], [], 0.5)
                if master in r2:
                    c = os.read(master, 4096)
                    if not c: break
                    logf.write(c)
                else:
                    break
        except OSError:
            pass
        logf.write(b"\n[DRIVER] EXIT %d\n" % (p.poll(),))
        break
logf.flush(); logf.close()

