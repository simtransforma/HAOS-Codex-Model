# Variações: combinado multi-tag, compartilhar entre contas, Lookalike

Padrões validados em produção 19/06/2026 (públicos QRcode/369flix, BM01).
O `run_pipeline.py` cobre **1 tag → 1 audience + auto-sync + doc**. Estas são as extensões.

## 1. Público COMBINADO (várias tags → 1 audience, deduplicado)

Reusa as funções do `run_pipeline.py` (não reimplementar hash/normalização):

```python
import sys; sys.path.insert(0, r"${HAOS_PRIVATE_ROOT}")
import run_pipeline as rp
env = rp.load_env()
tags = {"Tag_A":"<tag_id_a>", "Tag_B":"<tag_id_b>", ...}   # nome: id (resolver id com rp.clint_resolve_tag_id se preciso)
seen=set(); records=[]
for name,tid in tags.items():
    for c in rp.clint_fetch_contacts_by_tag(env, tid):
        n = rp.normalize_contact(c)
        if not n: continue
        key=(n.get('email') or '', n.get('phone') or '')
        if key in seen: continue
        seen.add(key); records.append(n)
aid = rp.meta_create_audience(env, "${RESOURCE_ID}", "BM01", "<Nome>", "<desc>")
rp.meta_upload_users(env, "BM01", aid, records)
```

- **Auto-sync do combinado:** o `run_pipeline` é 1-tag. Pro combinado, ou (a) rodar N clones de `rp.n8n_duplicate_workflow` apontando todos pra MESMA audience_id (proven, mas N workflows), ou (b) 1 job diário multi-tag (n8n custom ou cron Hetzner). LAL refresha a cada poucos dias, então diário basta.
- **Pegadinha Clint:** a paginação do `/contacts?tag_ids=` às vezes engasga e devolve menos que o real (vi 400 vs 695 numa tag). Conferir contagem; o refresh diário completa.

## 2. Compartilhar audience entre contas de anúncio (mesma BM)

Custom audience é dona da conta que criou. Pra usar em outra conta da MESMA BM, compartilhar:

```python
POST https://graph.facebook.com/v21.0/{audience_id}/adaccounts
  adaccounts = json.dumps(["${RESOURCE_ID}"])   # numerico, SEM 'act_'
  access_token = ${USER_SECRET}
# resposta OK: {"success": true, "sharing_data":[{"ad_acct_id":"...","audience_share_status":"shared"}]}
```

Funciona pra custom audiences E lookalikes. Compartilhar a SEMENTE não basta pra LAL; compartilhe o LAL também.

## 3. Lookalike 1% (BR) a partir de uma seed

```python
POST https://graph.facebook.com/v21.0/{ad_account}/customaudiences
  name="<Nome> , LAL 1% BR"
  subtype="LOOKALIKE"
  origin_audience_id="<seed_audience_id>"   # a combinada é a melhor seed (maior)
  lookalike_spec=json.dumps({"ratio":0.01,"country":"BR","type":"similarity"})
```

- LAL leva **algumas horas** pra calcular (`operation_status="Atualizando"`, `delivery_status` fica "muito pequeno" até terminar). Depois ~2M de alcance no BR.
- Seed precisa de match suficiente (>100; ideal 1.000-50.000). A combinada de várias tags é a melhor semente.

## 4. Verificar estado dos públicos

```python
GET /{aid}?fields=name,subtype,operation_status,approximate_count_lower_bound,delivery_status
```
`delivery_status.description` = "pronto para uso" / "muito pequeno". `operation_status` = "Atualizando" enquanto calcula.

## Naming usado (QRcode/369flix)
- Por produto: `[Clint] [QRcode] <Produto>`
- Combinado: `[Clint] [369flix] QRcode (todos)`
- LAL: `[Clint] [369flix] QRcode , LAL 1% BR`

