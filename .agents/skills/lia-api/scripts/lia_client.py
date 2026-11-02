"""Cliente minimo da API da Lia EdTech (external-api.lia.com.br/external_api/v1).

Auth por header Authorization: Bearer <LIA_API_KEY>. Token lido do MASTER.env
(NUNCA hardcode). Cobre o que a integracao usa de fato: listar/buscar produtos
e listar/criar webhooks (POST /webhooks e ADITIVO). Os outros endpoints seguem
o mesmo padrao: usar self._get / self._request.

Uso:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.home() / ".claude" / "skills" / "lia-api" / "scripts"))
    from lia_client import LiaClient

    lia = LiaClient.from_master_env()
    produtos = lia.list_products()
    lia.create_webhook(name="...", url="https://service.example.invalid", entity="order",
                       events=["finished", "canceled"])
"""

raise RuntimeError('requires_user_config: render placeholders, review bindings and remove this guard only after local validation')


import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PROD_BASE = "https://external-api.lia.com.br/external_api/v1"
SANDBOX_BASE = "https://external-api-sandbox.lia.com.br/external_api/v1"

# Caminho canonico do MASTER.env (AGENTS.md secao 11)
MASTER_ENV = (
    Path.home()
    / "OneDrive"
    / "Documentos"
    / "Projetos"
    / "Agencia HAU - Solucoes Digitais"
    / "HAO IA Operation System"
    / "_secrets"
    / "MASTER.env"
)


def _load_master_env(path=None):
    """Le o MASTER.env e devolve dict (sem persistir nada em log)."""
    env = {}
    p = Path(path) if path else MASTER_ENV
    if not p.exists():
        # fallback: pode ja estar no ambiente
        return env
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        env[key.strip()] = val.strip().strip('"').strip("'")
    return env


class LiaClient:
    def __init__(self, api_key, base=PROD_BASE, timeout=30):
        if not api_key:
            raise ValueError("LIA_API_KEY ausente (MASTER.env)")
        self.api_key = api_key
        self.base = base.rstrip("/")
        self.timeout = timeout

    @classmethod
    def from_master_env(cls, sandbox=False, master_path=None):
        env = _load_master_env(master_path)
        key = (
            env.get("LIA_API_KEY")
            or os.environ.get("LIA_API_KEY")
            or env.get("LIA_TOKEN")
            or os.environ.get("LIA_TOKEN")
        )
        return cls(key, base=SANDBOX_BASE if sandbox else PROD_BASE)

    # ----- HTTP base -----
    def _request(self, method, path, params=None, body=None, _retries=3):
        url = self.base + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Accept": "application/json",
        }
        if data is not None:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        for attempt in range(_retries):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    raw = resp.read().decode("utf-8")
                    return json.loads(raw) if raw else {}
            except urllib.error.HTTPError as exc:
                # backoff em 429 / 5xx
                if exc.code in (429, 500, 502, 503, 504) and attempt < _retries - 1:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                detail = exc.read().decode("utf-8", errors="ignore")
                raise RuntimeError(
                    "Lia API %s %s -> HTTP %s: %s"
                    % (method, path, exc.code, detail[:500])
                ) from None
            except urllib.error.URLError:
                if attempt < _retries - 1:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                raise
        return {}

    def _get(self, path, params=None):
        return self._request("GET", path, params=params)

    def _get_paginated(self, path, params=None, per_page=100, page_param="page"):
        """Pagina ate esvaziar. A Lia usa page/per_page; o array de itens vem
        em chave variavel (data/items/results) ou e a propria lista."""
        params = dict(params or {})
        params["per_page"] = per_page
        out = []
        page = 1
        while True:
            params[page_param] = page
            resp = self._get(path, params)
            items = _extract_items(resp)
            if not items:
                break
            out.extend(items)
            if len(items) < per_page:
                break
            page += 1
        return out

    # ----- Produtos -----
    def list_products(self, search=None, availability=None):
        params = {}
        if search:
            params["search"] = search
        if availability is not None:
            params["availability"] = availability
        return self._get_paginated("/products", params)

    def get_product(self, product_id):
        return self._get("/products/%s" % product_id)

    # ----- Webhooks -----
    def list_webhooks(self):
        resp = self._get("/webhooks")
        return _extract_items(resp) or resp

    def create_webhook(self, name, url, entity, events, target="standard", verb="post"):
        """POST /webhooks (ADITIVO, nao substitui existentes).
        entity: 'bill' | 'billing' | 'order'. events: lista de strings."""
        if entity not in ("bill", "billing", "order"):
            raise ValueError("entity invalida: %r (use bill/billing/order)" % entity)
        body = {
            "name": name,
            "url": url,
            "entity": entity,
            "events": list(events),
            "target": target,
            "verb": verb,
        }
        return self._request("POST", "/webhooks", body=body)

    def delete_webhook(self, webhook_id):
        return self._request("DELETE", "/webhooks/%s" % webhook_id)

    # ----- Pedidos / financeiro (leitura) -----
    def list_orders(self, status=None, search=None,
                    created_at_start=None, created_at_end=None):
        params = {}
        if status:
            params["status"] = status
        if search:
            params["search"] = search
        if created_at_start:
            params["created_at_start"] = created_at_start
        if created_at_end:
            params["created_at_end"] = created_at_end
        return self._get_paginated("/orders", params)

    def get_order(self, order_id):
        return self._get("/orders/%s" % order_id)

    def list_bills(self):
        return self._get_paginated("/bills")

    def list_billings(self):
        return self._get_paginated("/billings")


def _extract_items(resp):
    """Normaliza o no de lista que a Lia devolve."""
    if isinstance(resp, list):
        return resp
    if isinstance(resp, dict):
        for key in ("data", "items", "results", "records"):
            val = resp.get(key)
            if isinstance(val, list):
                return val
    return []


# ----- Helpers de payload (espelham references/payload.md) -----
REAL_PRODUCT_IDS = {
    "${USER_RESOURCE_000006}",  # Practitioner principal
    "${USER_RESOURCE_000008}",  # Aguias do Protocolo
    "${USER_RESOURCE_000009}",  # Bolsa Social
}
GENERIC_FINANCING_PRODUCT_ID = "${USER_RESOURCE_000007}"  # parcelas


def normalize_payload(body):
    """Extrai os campos uteis de um webhook da Lia (target standard)."""
    data = (body or {}).get("data", {}) or {}
    contact = (
        data.get("contact")
        or data.get("customer")
        or data.get("buyer")
        or data.get("student")
        or data.get("payer")
        or data.get("client")
        or {}
    )
    offer = data.get("offer") or {}
    product = offer.get("product") or data.get("product") or {}
    payments = data.get("payments") or []
    pay = payments[0] if payments else {}
    cents = (
        data.get("current_amount_cents")
        or data.get("amount_cents")
        or offer.get("amount_cents")
        or 0
    )
    return {
        "event": (body or {}).get("event"),
        "status": data.get("status"),
        "product_id": product.get("id"),
        "product_name": product.get("name"),
        "name": contact.get("name") or data.get("customer_name"),
        "email": contact.get("email"),
        "phone": contact.get("phone") or contact.get("cellphone"),
        "value": cents / 100 if cents else 0,
        "method": pay.get("payment_method"),
        "boleto_url": pay.get("url"),
        "barcode": pay.get("barcode"),
        "paid_at": pay.get("paid_at"),
        "tx_id": data.get("id") or data.get("uuid") or data.get("bill_id"),
        "doc": data.get("customer_document"),  # so no order
        "address": data.get("address") or {},  # so no order
        "utm_source": (data.get("metadata") or {}).get("utm_source"),  # se mandar
        "is_installment": data.get("bill_type") == "installment",
    }


def is_real_product(product_id):
    """True se for um produto real (descarta parcela com produto generico)."""
    return product_id in REAL_PRODUCT_IDS


def _mask(value):
    """Mascara PII para log (email/phone/cpf)."""
    if not value:
        return value
    s = str(value)
    if "@" in s:
        user, _, dom = s.partition("@")
        return (user[:3] + "***@" + dom) if user else "***@" + dom
    digits = re.sub(r"\D", "", s)
    if len(digits) >= 7:
        return digits[:4] + "***" + digits[-2:]
    return "***"

