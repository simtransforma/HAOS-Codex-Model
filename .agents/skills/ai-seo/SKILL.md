---
name: ai-seo
description: "Use quando o usuário quiser otimizar conteúdo para buscadores de IA, ser citado por LLMs ou aparecer em respostas geradas por IA. Use também quando ele mencionar 'AI SEO', 'AEO', 'GEO', 'LLMO', 'answer engine optimization', 'generative engine optimization', 'otimização para LLM', 'AI Overviews', 'otimizar para ChatGPT', 'otimizar para Perplexity', 'citações de IA', 'visibilidade em IA', 'busca zero-click', 'como apareço nas respostas de IA', 'menções em LLM' ou 'otimizar para Claude/Gemini'. Use sempre que alguém quiser que o conteúdo seja citado pelos assistentes e buscadores de IA. Para SEO técnico e on-page tradicional, veja seo-optimizer. Para dados estruturados, veja schema."
---

# AI SEO (HAOS)

Orientação para descoberta e citação em busca por IA, sem promessa de ranking, audiência ou recomendação. Responder em PT-BR. Melhorar a utilidade do conteúdo é uma decisão editorial; efeito em descoberta precisa ser medido.

## Origem e adaptação local

Revisão HAOS 2026-10-01.2 da versão local 2.0.1. Preservados autoria, marca e atribuições existentes; esta revisão não altera licenças nem declara origem upstream não comprovada. Removidas extrapolações percentuais e equivalências incorretas entre treinamento e busca. Revalidar o diff antes de atualizar a skill.

HAOS, consentimento e escopo prevalecem. A skill não autoriza publicação, alterações de robots, acesso a credenciais, instalação de ferramentas, gastos ou criação de memória independente. Não pressupor GTM, Analytics, domínio próprio ou acesso administrativo.

## Antes de começar

Ler o contexto de produto existente quando pertinente: `${USER_PROJECT_ROOT}/.agents/product-marketing.md`, `.claude/product-marketing.md` ou o legado `product-marketing-context.md`. Não criar contexto paralelo.

Confirmar:
- Ativo, URL/ID, canal ou domínio, idioma, público e conteúdo real.
- Superfície: site próprio, descrição YouTube ou outra plataforma hospedada.
- Objetivo observável: responder a uma intenção, conseguir visitas qualificadas ou acompanhar citações; não apenas inserir palavras.
- Consultas reais e evidência disponível. Sem Analytics ou pesquisa, declarar a intenção proposta como HIPÓTESE, não como demanda comprovada.
- Campos autorizados para edição e elementos que devem permanecer intactos.
- Baseline, ferramentas já disponíveis e limitações de acesso. Não contratar serviços.

## Fatos, observações e hipóteses

| Classe | Evidência necessária | Uso |
| --- | --- | --- |
| FATO | Fonte primária pertinente, URL e data de consulta | Funcionamento documentado, limites e requisitos |
| OBSERVAÇÃO | Amostra identificada, data e método | Estado da UI, Analytics ou respostas coletadas |
| HIPÓTESE | Justificativa editorial e teste proposto | Possível efeito de título, clareza ou organização |

Para qualquer número, registrar fonte, data, população/amostra, plataforma, métrica e denominador. Correlação não demonstra causalidade. Não transformar percentuais de um estudo em previsão para outro canal ou produto. Não inventar estatísticas, credenciais, depoimentos ou citações para tornar conteúdo "citável".

## Como funciona a busca por IA

Separar busca/recuperação atual, visita solicitada pelo usuário e treinamento de modelos. Uma resposta pode mencionar uma marca sem citar seu site; um link pode existir sem gerar clique. Não inferir o caminho de recuperação apenas pelo nome do produto.

### Google

Segundo o [guia oficial](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), consultado em 2026-10-01:
- SEO e conteúdo útil continuam relevantes; elegibilidade não garante exibição.
- Não há exigência de tamanho ideal, fragmentação para IA ou schema especial. Google Search não usa `llms.txt` como vantagem de visibilidade.
- Query fan-out pode explorar consultas relacionadas. Isso não prova que intenção específica perdeu importância nem que páginas abrangentes sempre superam páginas focadas.
- O guia documenta relatório de desempenho de IA generativa no Search Console. Verificar acesso, métricas e disponibilidade na propriedade; não presumir que o relatório esteja presente na conta.

Não generalizar essas regras para todos os assistentes. Para outros produtos, verificar documentação e comportamento observado; não afirmar índices exclusivos, pesos secretos, preferência por PDF ou formatos universais sem fonte.

### Limites do estudo GEO

O [artigo GEO, KDD 2024, versão 3](https://arxiv.org/html/2311.09735v3) avaliou intervenções em um benchmark, com motor experimental baseado em recuperação de fontes e geração, além de avaliação no Perplexity. Suas medidas de visibilidade textual não são CTR, audiência YouTube ou ranking no Google atual.

Os resultados dependem de método, métrica e contexto. Exemplos individuais não representam efeitos médios; tom autoritativo não mostrou melhora agregada significativa. Não reproduzir a antiga tabela de ganhos fixos. Usar o estudo como motivação para hipóteses verificáveis, não como receita ou promessa para lives.

## Auditoria de visibilidade

1. Definir conjunto estável de consultas por intenção e registrar como foi escolhido.
2. Para cada execução, anotar plataforma/produto, modelo quando visível, modo de busca, idioma/localidade, data/hora e condições de sessão. Não usar perfil pessoal ou dados privados sem escopo.
3. Registrar se houve resposta de IA, menção, URL citada, trecho e relevância. Ausência de resposta de IA não é igual a resposta sem citação.
4. Repetir em condições comparáveis e informar tamanho da amostra e variação. Não apresentar uma consulta isolada como participação de mercado.
5. Examinar as fontes encontradas: o que responde à intenção, que evidência trazem e o que falta ao ativo auditado. Padrões observados não revelam pesos internos do motor.

## Acesso de bots: apenas em domínio controlado

Não usar "permitir todos" como padrão. Separar decisão de busca da decisão de treinamento e conferir configuração completa antes de propor alteração.

| Agente/controle | Finalidade documentada |
| --- | --- |
| OAI-SearchBot | Busca OpenAI |
| GPTBot | Coleta que pode ser usada no treinamento de modelos OpenAI |
| ChatGPT-User | Acesso solicitado pelo usuário, distinto do crawl automático |
| Claude-SearchBot | Busca Anthropic |
| ClaudeBot | Treinamento Anthropic |
| Claude-User | Acesso solicitado pelo usuário Anthropic |
| Googlebot | Rastreamento para Google Search |
| Google-Extended | Controle de treinamento e grounding em produtos Gemini descritos na documentação; não determina inclusão/ranking no Search |

Fontes: [OpenAI](https://developers.openai.com/api/docs/bots), [Anthropic](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), [Google](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended).

É possível separar permissão ao OAI-SearchBot e bloqueio ao GPTBot. Não prometer ausência absoluta de links, citações ou uso histórico com base em robots. Visitas solicitadas pelo usuário possuem regras próprias; robots não é controle de autenticação.

Para Perplexity, Bing e outros, consultar a documentação atual antes de escrever regras; não substituir nomes por agentes de outro fornecedor. Ver [referência de plataformas](references/platform-ranking-factors.md).

## Método editorial concreto

### 1. Intenção específica

Preencher por ativo: **quem procura + o que quer encontrar/fazer + situação de uso + conteúdo que realmente será entregue + evidência**. Não escolher formato ou palavras por um suposto "favoritismo da IA".

Exemplo hipotético de escopo: procurar uma faixa musical específica em repetição é diferente de procurar uma explicação sobre afirmações. Só associar a intenção a uma live após conferir sua mídia; não preencher lacunas com benefícios inventados.

### 2. Estrutura, autoridade e presença

- **Estrutura:** abertura direta e organização legível. Escolher prosa, lista, tabela ou FAQ conforme a intenção, sem contagem ideal de palavras ou formato obrigatório.
- **Autoridade:** fatos verificáveis, autoria real e referências pertinentes. Atualizar quando a informação mudar, sem trocar apenas a data ou impor calendário de "frescor".
- **Presença:** identificar onde o público realmente procura. Menções legítimas podem ser acompanhadas; não gerar spam, prova social ou citações artificiais.

### 3. Teste de troca de parágrafos

Trocar, apenas no rascunho, a abertura e os parágrafos específicos entre dois ativos; desconsiderar seus nomes próprios e o bloco comum de CTA. Se continuarem igualmente adequados, a copy está genérica. Reescrever usando diferenças reais de conteúdo, formato ou intenção.

Este é um teste de especificidade editorial, não um experimento de ranking. Não fabricar diferenças para "passar". Quando os ativos forem realmente equivalentes, registrar essa limitação; CTAs compartilhados não precisam ser artificialmente diferentes.

### 4. Preservação e readback

Capturar texto atual e separar bloco editorial de links/CTAs aprovados. Preservar URLs, parâmetros, ordem e texto dos CTAs salvo autorização para alterá-los. Entregar diff com justificativa por mudança.

Após escrita externa autorizada pelo executor, reler os campos efetivamente salvos no ativo correto. Comparar com a proposta e confirmar preservação dos CTAs. Clique em "Salvar" sem readback não comprova conclusão; divergência fica pendente, sem repetir escrita às cegas.

## YouTube e lives contínuas

Aplicar também `youtube-seo`. Tratar EU SOU, RIQUEZA e EU RECEBO separadamente quando fizerem parte do briefing; nunca presumir IDs, conteúdo ou estado atual.

- Escopo editorial: título, descrição, tags, thumbnail e medição.
- O criador não controla robots, HTML, JSON-LD ou arquivos raiz de `youtube.com`. Não recomendar `llms.txt`, GTM ou schema na descrição.
- Não presumir acesso Search Console à propriedade YouTube a partir da posse do canal.
- Informar repetição quando aplicável, sem simular presença ou interação humana ao vivo.
- Não inventar letras, transcrições, capítulos ou resultados de saúde/finanças.
- Thumbnail específica e legível é orientação editorial, não obrigação técnica de upload deduzida desta skill.
- Preservar encoder, evento, chaves, privacidade, monetização, anúncios e demais configurações. SEO não autoriza operações nessas superfícies.

## Sites próprios: schema e arquivos auxiliares

Somente quando houver controle do site e escopo autorizado. Usar schema que represente conteúdo visível e atender à documentação do recurso pretendido; não prometer aumento de citações. Não inserir FAQ ou estatísticas apenas para preencher marcação.

Arquivos como `llms.txt` ou Markdown podem atender integrações documentadas específicas, mas não são requisito universal de descoberta. Avaliar consumidor, manutenção e necessidade; não criar automaticamente páginas paralelas, preços ou integrações.

## Medição e aceite

| Medida | Registro mínimo |
| --- | --- |
| Menção | Nome/entidade presente e contexto |
| Citação | URL realmente ligada à resposta |
| Clique referido | Visita atribuída pelo sistema de analytics; não equivale ao total de citações |
| Frequência na amostra | Numerador, denominador, consultas e condições; não chamar de quota global |
| Resultado editorial YouTube | Impressões, CTR, duração média, tempo assistido e fontes comparáveis |

Definir baseline, hipótese, variável alterada, janela de observação e critério de decisão antes da mudança. Amostra insuficiente ou fontes de tráfego incompatíveis produzem resultado inconclusivo, não vitória. Não comprar ferramentas ou executar chamadas pagas sem autorização.

No YouTube, conferir elegibilidade antes de sugerir A/B nativo. Alternância manual de texto antes/depois não é teste simultâneo e não isola causalidade. Separar métricas de lives e arquivos/replays. Para GEO, não atribuir oscilação de respostas a uma edição sem desenho experimental.

## Referências e limites

- [Plataformas e bots revisados](references/platform-ranking-factors.md): referência operacional desta revisão.
- `references/content-patterns.md` e `references/content-types.md`: materiais legados fora desta revisão. Não usar seus percentuais, preferências de motor ou exemplos factuais como evidência; templates só após validar fatos e pertinência. Em conflito, esta revisão prevalece.
- `evals/evals.json`: cenários de avaliação editorial. Validar JSON não comprova execução comportamental por um modelo.

## Entrega esperada

Por ativo: identificação confirmada; intenção específica; evidência e lacunas; FATO/OBSERVAÇÃO/HIPÓTESE; texto atual versus proposto; resultado do teste de troca; CTAs preservados; thumbnail; plano de medição; estado de autorização/readback. Sem evidência, entregar rascunho pendente, nunca afirmar publicação ou resultado.

## Skills relacionadas

- **seo-optimizer**: diagnóstico técnico/on-page tradicional; não substituir auditoria ampla por GEO.
- **schema**: marcação em site controlado, dentro do escopo.
- **content-strategy** e **copywriting**: intenção e texto útil.
- **youtube-seo**: títulos, descrições, tags, thumbnails e métricas da plataforma.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
