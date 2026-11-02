# Autorização e segurança operacional

## Campos mínimos

- Proprietário legal e responsável técnico
- Evidência de autorização e período de validade
- Domínios, IPs, APIs, aplicativos e tenants incluídos
- Produção, homologação ou laboratório
- Contas, papéis e dados sintéticos permitidos
- Limites de taxa, concorrência e volume
- Técnicas proibidas e fornecedores fora do escopo
- Contatos de emergência e canal de comunicação
- Retenção, criptografia e descarte das evidências

## Regras de parada

Interromper imediatamente em caso de indisponibilidade, alteração de dados reais, acesso a PII além do mínimo, efeito financeiro, exposição de segredo, alcance a terceiro ou dúvida sobre autorização. Preservar evidência mínima e notificar o contato definido.

## Default seguro

Começar por documentação, código, OpenAPI, headers e navegação normal. Usar contas sintéticas e ambiente de homologação. Não fazer DoS, força bruta, credential stuffing, phishing, persistência, exfiltração ou execução remota.
