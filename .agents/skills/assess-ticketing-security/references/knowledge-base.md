# Base consultável

## Taxonomia principal

- Identidade: cadastro, login, MFA, recuperação, SSO e vinculação de conta.
- Sessão: cookies, tokens, revogação, rotação e isolamento entre tenants.
- Autorização: BOLA/IDOR, função, propriedade, organizador, operador e participante.
- API: inventário, versionamento, mass assignment, exposição excessiva e consumo de recursos.
- Entrada e saída: injeções, XSS, SSRF, upload, exportação, CSV e templates.
- Infraestrutura: TLS, CORS, headers, cache, erros, storage e segredos.
- Integrações: pagamentos, webhooks, e-mail, QR/barcode, antifraude e analytics.
- Lógica: reserva, estoque, preço, cupom, reembolso, transferência e check-in.

## Fontes primárias no GitHub

- OWASP WSTG: https://github.com/OWASP/wstg
- OWASP ASVS: https://github.com/OWASP/ASVS
- OWASP API Security: https://github.com/OWASP/API-Security
- OWASP Cheat Sheet Series: https://github.com/OWASP/CheatSheetSeries
- OWASP crAPI, laboratório local: https://github.com/OWASP/crAPI
- OWASP Juice Shop, laboratório local: https://github.com/juice-shop/juice-shop
- ZAP: https://github.com/zaproxy/zaproxy
- Nuclei templates: https://github.com/projectdiscovery/nuclei-templates

Tratar scanners como apoio, nunca como prova. Fixar versão/commit ao citar requisito ou cenário. Executar laboratórios vulneráveis somente isolados/localmente.

## Evidência por achado

Registrar ID, data, ambiente, papel, pré-condição, sequência mínima, resultado esperado, resultado observado, objeto afetado, impacto, evidência redigida, classificação CWE/OWASP, correção e reteste. Nunca guardar tokens, cookies ou PII bruta.
