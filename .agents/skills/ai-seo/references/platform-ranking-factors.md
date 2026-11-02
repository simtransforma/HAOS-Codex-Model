# How Each AI Platform Picks Sources

Revisão local HAOS: 2026-10-01.2. Referência de evidências e limites, não tabela de pesos de ranking.

## Proveniência

A referência anterior atribuía alegações ao estudo GEO (KDD 2024), a análises SE Ranking e ZipTie. A atribuição histórica é preservada aqui; números sem fonte primária rastreável e extrapolações foram retirados. Isso não valida as conclusões anteriormente atribuídas a essas fontes. Não alteradas licenças ou autoria do pacote.

## Como classificar afirmações

- **FATO:** documentação primária datada, no produto e modo pertinentes.
- **OBSERVAÇÃO:** amostra reproduzível com consultas, idioma/localidade, data, modo de busca e URLs.
- **HIPÓTESE:** interpretação editorial ou possível mecanismo ainda não demonstrado.

Não converter um backend observado em índice exclusivo permanente, nem correlação em peso de ranking. Nenhuma plataforma recebe prioridade automática: escolher pela audiência e evidência disponíveis.

## Google Search: AI Overviews e AI Mode

Fonte consultada em 2026-10-01: [guia oficial de otimização para IA](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), atualizado em 2026-07-10.

A orientação é manter fundamentos de SEO e conteúdo útil. Não há ganho documentado nesta referência por schema especial, tamanho fixo ou llms.txt. Fan-out não elimina intenção específica.

O guia atual aponta relatório de IA generativa no Search Console. Conferir a propriedade, acesso e métricas disponíveis antes de montar o plano; não repetir a antiga afirmação de inexistência. A documentação pode mudar: registrar data e resolver divergências pela fonte específica mais recente, sem supor disponibilidade na conta.

## OpenAI / ChatGPT

Fonte: [Overview of OpenAI Crawlers](https://developers.openai.com/api/docs/bots), consultada em 2026-10-01.

- OAI-SearchBot: descoberta para busca.
- GPTBot: coleta para possível treinamento.
- ChatGPT-User: acesso a pedido do usuário, não equivalente a rastreamento automático.

Busca e treinamento possuem controles separados. Bloquear GPTBot não equivale a bloquear OAI-SearchBot. Não deduzir ausência absoluta de links a partir de robots; acessos solicitados pelo usuário têm regras próprias.

## Anthropic / Claude

Fonte: [documentação dos crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), consultada em 2026-10-01.

ClaudeBot, Claude-SearchBot e Claude-User distinguem treinamento, busca e acesso pelo usuário. Não usar o antigo par ClaudeBot/anthropic-ai como recomendação genérica de busca. Não presumir dependência exclusiva de Brave nem pesos de seleção não publicados.

## Google-Extended não é Google Search

Fonte: [Google common crawlers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended), consultada em 2026-10-01.

Google-Extended trata usos de treinamento e grounding nos produtos Gemini especificados pela documentação; não controla inclusão ou ranking no Google Search. Googlebot e controles de Search devem ser analisados separadamente. Não confundir esses produtos ao recomendar permissões.

## Perplexity e Microsoft Copilot

Nesta revisão não foi estabelecida uma política operacional completa com documentação primária atual desses produtos. Antes de propor regras, conferir a finalidade atual de PerplexityBot/Bingbot e os controles oficiais do serviço exato.

Permanecem NÃO COMPROVADAS aqui: pesos de autoridade, favorecimento automático de PDFs/FAQ, dependência exclusiva de um índice, bônus por LinkedIn/GitHub e um limiar universal de velocidade. Não usar essas hipóteses como checklist obrigatório ou motivo para publicar conteúdo.

## Decisão de robots em site próprio

1. Confirmar propriedade do domínio e escopo autorizado.
2. Ler regras atuais, controles de indexação e intenção do proprietário.
3. Separar treinamento, descoberta por busca e acessos a pedido do usuário.
4. Consultar a documentação de cada agente envolvido; não liberar todos por padrão.
5. Apresentar diff proposto e riscos. Escrita depende de autorização; verificar o estado efetivo depois.
6. Não tratar robots como autenticação, remoção retroativa de treinamento ou garantia de citação.

No YouTube, o dono do canal não administra robots de youtube.com. Não colocar regras de bots, JSON-LD, GTM ou llms.txt em descrições. Site próprio ou embed exige escopo distinto.

## O que o estudo GEO permite afirmar

Fonte: [GEO, KDD 2024, versão 3](https://arxiv.org/html/2311.09735v3).

É um experimento com métricas próprias de visibilidade, não uma documentação de pesos de Google AI Overviews. Exemplos de citações e tom autoritativo na tabela de casos não são efeitos médios transferíveis. Não transportar seus resultados para audiência, CTR ou ranking de lives.

Uma hipótese derivada deve nomear intervenção, população e métrica, além de prever resultado inconclusivo. Não adicionar números ou referências artificiais ao conteúdo para reproduzir o experimento.

## Método e evidência editorial

Preencher intenção específica e conteúdo entregue por ativo. Fazer o teste de troca de parágrafos definido em SKILL.md: se aberturas continuam intercambiáveis ao retirar nomes, revisar sua especificidade sem inventar diferenças.

Distinguir menção, URL citada e tráfego referido. Medir consultas repetidas sob condições comparáveis; uma amostra não representa todas as respostas de uma plataforma.

Preservar CTAs aprovados e exigir readback de campos salvos após qualquer escrita autorizada. Melhoria editorial não comprova ganho de distribuição.
