# Metodologia de qualidade para listas comerciais

## Ordem de operação

1. Backup.
2. Auditoria de estrutura e completude.
3. Normalização.
4. Deduplicação.
5. Qualificação por público ideal.
6. Validação e enriquecimento.
7. Pontuação, segmentação e próxima ação.
8. Verificação final e log.

Deduplicar antes de enriquecer evita pesquisa e créditos repetidos.

## Hierarquia de fontes

1. Site oficial da organização.
2. Perfil institucional verificado.
3. Diretório oficial, associação setorial, governo ou instituição de ensino.
4. Diretório comercial reconhecido.
5. Agregadores, buscadores e redes sociais não verificadas apenas como pista.

Registrar URL e data. Não elevar uma pista a dado confirmado.

## Chaves de deduplicação

- Fortes: e-mail exato, telefone normalizado exato, CNPJ ou identificador oficial.
- Médias: domínio + nome; Instagram + localização; nome + cidade + setor.
- Fracas: nome parecido isoladamente.

Mesclar automaticamente apenas chaves fortes. Revisar chaves médias e fuzzy.

## Pontuação recomendada

Modelo de 100 pontos, ajustável ao projeto:

- evidência pública e domínio compatível: 25;
- aderência ao segmento/público ideal: 25;
- proximidade geográfica ou operacional: 15;
- e-mail tecnicamente válido: 10;
- telefone utilizável: 10;
- contato-alvo identificado: 5;
- perfil institucional: 5;
- sinal de relacionamento anterior: 5.

Aplicar teto de prioridade quando a identidade estiver em revisão.

## Metas de saúde

- duplicidade: abaixo de 2%;
- campos críticos completos: acima de 90%;
- e-mail verificado por ferramenta própria antes de disparo: acima de 80%;
- bounce após o primeiro envio: abaixo de 3%;
- dados ativos revisados nos últimos 90 dias.

## Referências abertas

- Sales Data Hygiene: https://github.com/sales-skills/sales/tree/main/skills/sales-data-hygiene
- Sales Enrich: https://github.com/sales-skills/sales/tree/main/skills/sales-enrich
- Sales Prospect List: https://github.com/sales-skills/sales/tree/main/skills/sales-prospect-list
- dedupe: https://github.com/dedupeio/dedupe
- OpenRefine: https://github.com/OpenRefine/OpenRefine
- Email Verifier: https://github.com/umuterturk/email-verifier
