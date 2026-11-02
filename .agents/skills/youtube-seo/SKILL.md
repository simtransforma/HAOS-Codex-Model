---
name: youtube-seo
description: "When the user wants to optimize YouTube videos for search, create video descriptions, or improve channel visibility. Also use when the user mentions \"YouTube SEO,\" \"YouTube description,\" \"YouTube tags,\" \"YouTube thumbnail,\" \"YouTube title,\" \"YouTube channel,\" or \"video SEO.\" For YouTube ads, use youtube-ads."
---

## Contrato publico de execucao

Material de dominio portado da fonte real, nao uma instalacao de infraestrutura.
As regras do usuario e do AGENTS.md prevalecem sobre comandos e exemplos abaixo.
Publicar, enviar, gastar, alterar servidores, reiniciar, apagar, push e merge
exigem consentimento explicito para o destino e a acao. Nao executar comandos
com placeholders. Nao buscar o cofre ou ambientes do autor. Ferramentas/MCPs
citados precisam existir na instalacao do usuario; nomes nao provam acesso.
Consulte [PORTABILITY.md](PORTABILITY.md) para dependencias, recursos omitidos,
licencas e adaptacoes. Exemplos preservados nao sao prova de estado vivo.

# Platforms: YouTube SEO

Guia editorial para titulos, descricoes, tags e thumbnails de videos e lives YouTube, incluindo lives continuas 24h SIM. Nao promete ranking, crescimento ou citacoes em IA. Responder em PT-BR.

## Origem e adaptacao HAOS

Adaptacao local de kostja94/marketing-skills, upstream 1.1.1, caminho `skills/platforms/youtube/SKILL.md`, consultado em 2026-10-01. Referencia auditada: commit `26cef3434274129040dcfc64e9c7be85ba1ada15`. Licenca MIT preservada em `LICENSE`.

Removidas estatisticas sem evidencia vinculada, promessas algoritmicas e regras editoriais absolutas. Acrescentados cuidados para lives 24h e GEO/IA. O `skills-lock.json` registra a origem instalada, nao igualdade com esta curadoria local. Revisar diff antes de atualizar ou reinstalar: essas operacoes podem sobrescrever a adaptacao.

HAOS, marca e consentimento prevalecem. Esta skill produz propostas editoriais; nao autoriza publicacao, upload, chamadas de escrita, alteracao de monetizacao ou leitura de credenciais. Nao instalar skills relacionadas nem criar memoria/contexto paralelo automaticamente.

**When invoking**: On **first use**, if helpful, open with 1–2 sentences on what this skill covers and why it matters, then provide the main output. On **subsequent use** or when the user asks to skip, go directly to the main output.

## Initial Assessment

**Project context:** Read root `contextus.md` when present and load only the modules relevant to this task. Without Contextus, use available project material or user-provided facts and ask for missing information; do not create a parallel context system.

Identify:
1. **Video type**: Tutorial, review, vlog, Shorts, live agendada ou live continua 24h
2. **Target keyword**: Primary and secondary
3. **Audience**: Subscribers vs casual viewers

Confirmar canal, video/evento, idioma e conteudo real. Tratar EU SOU, RIQUEZA e EU RECEBO separadamente; nao presumir IDs ou estado ao vivo. Para copy SIM/usuario, aplicar a skill da marca quando disponivel. Preferir termos reais de busca do Analytics quando autorizados; sem dados, classificar escolhas como HIPOTESE.

## Metodo editorial por ativo

1. Registrar identificacao, texto atual, conteudo conferido e campos autorizados. Separar FATO (fonte/data), OBSERVACAO (amostra/estado verificado) e HIPOTESE (proposta ainda nao medida).
2. Preencher a intencao especifica: quem procura, o que quer ouvir/ver/encontrar, situacao de uso e o que esta live realmente entrega. Nome de keyword nao substitui essa ficha.
3. Redigir abertura e corpo com detalhes comprovados da midia. Se faltarem letra, genero ou tema, marcar lacuna; nao inventar diferencas ou beneficios.
4. Fazer o **teste de troca de paragrafos** no rascunho: trocar as aberturas e trechos especificos entre lives, desconsiderando nomes e o bloco comum de CTA. Se continuarem igualmente adequados, revisar a copy generica. Se o conteudo for realmente equivalente, registrar essa limitacao. O teste avalia especificidade, nao ranking.
5. Preservar integralmente texto, URLs, parametros e ordem dos links/CTAs aprovados. Entregar diff por campo; alteracao de CTA precisa estar no escopo autorizado.
6. Apos escrita externa pelo executor autorizado, fazer **readback** dos campos efetivamente salvos no ID correto e comparar com a proposta e CTAs originais. Clique em Salvar ou mensagem de sucesso sem releitura nao prova persistencia. Sem acesso, registrar PENDENTE; nao repetir escrita as cegas.

Exemplo de teste: tres aberturas com "musica poderosa para transformar sua vida" continuam intercambiaveis ao trocar EU SOU, RIQUEZA e EU RECEBO, portanto falham por genericidade. Uma abertura que identifica a faixa, seu formato real e a repeticao pode passar, desde que esses fatos tenham sido conferidos. Nao acrescentar promessa financeira para diferenciar RIQUEZA.

## Video Titles

| Rule | Guideline |
|------|-----------|
| **Length** | Conciso e legivel; 60 caracteres nao e limite obrigatorio. Conferir limites tecnicos atuais antes de integrar |
| **Keyword** | Assunto principal cedo quando natural, sem posicao magica |
| **Structure** | Mensagem fiel ao conteudo; nao inventar autoridade, prova social ou resultados |
| **Style** | Conversational; avoid keyword stuffing |
| **Avoid** | ALL CAPS except emphasis |

## Video Descriptions

| Rule | Guideline |
|------|-----------|
| **Opening** | Assunto e proposta reais nas primeiras linhas; keywords naturais. Nao impor 160 caracteres como limite da descricao |
| **Links** | Preservar bloco de CTAs/links aprovado; nao substituir destinos ou parametros por conveniencia editorial |
| **Readability** | Natural flow; help search understand topic |

## Tags

- Tags tem papel minimo na descoberta, principalmente uteis para grafias alternativas; titulo, thumbnail e descricao merecem prioridade
- Use relevant tags; avoid over-optimization
- Nao colocar excesso de tags na descricao

## Thumbnails

Usar thumbnail especifica, fiel ao conteudo, legivel em tamanho pequeno e coerente com a identidade SIM. Nao prometer cura, riqueza ou transformacao garantidas. Desempenho depende de contexto; nao deduzir causalidade de exemplos de sucesso. Recomendacao editorial de miniatura nao equivale a obrigatoriedade tecnica de upload; verificar requisito real da plataforma antes de afirma-lo.

| Rule | Guideline |
|------|-----------|
| **Contrast** | High contrast; readable fonts; bold colors |
| **Composition** | Rule of thirds; simple, uncluttered |
| **Audience** | Consider subscribers vs casual viewers |
| **Test** | Verificar elegibilidade do A/B nativo no ativo antes de propor; alternancia manual nao e teste simultaneo |

O YouTube documenta restricoes para lives agendadas e videos privados, entre outros, e permite testes em arquivos de lives elegiveis. Nao presumir disponibilidade nas lives continuas nem encerra-las para testar. O teste nativo considera tempo de exibicao, nao somente CTR; pode ser inconclusivo. Conferir documentacao e UI atuais.

## Title + Description + Thumbnail

Reforcar a mesma mensagem real nos tres elementos; nao prometer efeito algoritmico.

## Lives continuas 24h

- Informar conteudo continuo/repetido quando aplicavel; nao insinuar apresentador presente ou interacao em tempo real inexistentes.
- Usar "24h" somente se corresponder a proposta e operacao verificadas; nao garantir disponibilidade sem evidencia.
- Produzir proposta por live com identificacao confirmada, sem copiar mecanicamente publico ou promessas entre canais.
- SEO editorial nao exige reiniciar encoder, recriar evento ou mudar stream key, privacidade, monetizacao, anuncios, direitos, latencia ou chat. Preservar essas configuracoes; escrita externa cabe ao executor autorizado.
- Nao inventar capitulos/timestamps para loop continuo. Em replay finito, conferir conteudo e disponibilidade do recurso antes de propor marcacoes.

## Output Format

- **Identificacao** confirmada da live e canal
- **Title** options (concisos, sem limite editorial arbitrario)
- **Description** (abertura e corpo completos)
- **Tags** (relevant set)
- **Thumbnail** guidance (elements, text, composition)
- **Metodo**: ficha de intencao, teste de troca de paragrafos, diff, CTAs preservados e readback ou pendencia explicita
- **Evidencias**: justificativa, fontes, lacunas, FATO/OBSERVACAO/HIPOTESE e checklist do que NAO deve mudar. Sem dados reais, entregar rascunho pendente de validacao, nao publicar
- **Medicao**: baseline, mudanca e janela de observacao; comparar lives com lives e fontes de trafego equivalentes usando impressoes, CTR, duracao media e termos de busca. Antes/depois nao prova causalidade

Antes de alterar, definir hipotese, variavel, janela e criterio de decisao. Considerar tambem tempo assistido e tamanho da amostra; nao impor meta universal de CTR. Evitar mudancas simultaneas sem registrar o pacote e seus confundidores. Dados insuficientes ou trafego incompativel significam INCONCLUSIVO. Separar live de replay e nao confundir saude do encoder com desempenho editorial.

## YouTube in Google Search & GEO

GEO e hipotese de descoberta complementar, nao garantia de indexacao, citacao ou favorecimento pelo Google. Nao extrapolar estudos de citacoes em IA para crescimento de lives SIM.

- Identificar temas e entidades com clareza; informacao util, verificavel e consistente com o conteudo. Legendas/transcricoes devem corresponder ao video.
- Distinguir YouTube, busca Google e citacoes em IA na medicao.
- Em amostras GEO, fixar consultas e registrar plataforma/modelo quando visivel, modo de busca, idioma/localidade e data. Separar mencao, URL citada e clique referido; ganho para estas lives permanece HIPOTESE ate evidencia adequada.
- Nao recomendar bots/robots do canal: o criador nao controla o robots.txt do YouTube. Site proprio/embeds exigem escopo e revisao separados.
- Nao fabricar estatisticas, fontes, FAQs, transcricoes ou prova social para IA.

## Fontes oficiais consultadas em 2026-10-01

- [Titulos e thumbnails](https://support.google.com/youtube/answer/12340300?hl=pt-BR)
- [Papel das tags](https://support.google.com/youtube/answer/146402?hl=pt-BR)
- [Configuracoes de live](https://support.google.com/youtube/answer/9854503?hl=pt-BR)
- [Analytics de lives](https://support.google.com/youtube/answer/12942217?co=YOUTUBE._YTVideoType%3Dlivestream&hl=pt-BR)
- [Descricoes](https://support.google.com/youtube/answer/12948449?hl=pt-BR)
- [A/B de titulos e thumbnails](https://support.google.com/youtube/answer/16391400?hl=en)
- [Interpretacao de CTR](https://support.google.com/youtube/answer/7628154?hl=pt-BR)
- [Como a busca encontra videos](https://support.google.com/youtube/answer/58097?hl=pt-BR)
- [Politica de thumbnails](https://support.google.com/youtube/answer/9229980?hl=pt-BR)
- [Upstream auditado](https://github.com/kostja94/marketing-skills/blob/26cef3434274129040dcfc64e9c7be85ba1ada15/skills/platforms/youtube/SKILL.md)

Rever fontes quando houver mudanca de plataforma; fontes nao garantem resultado da SIM.

## Related Skills

- **video-marketing**: Video script, hook, structure
- **video-optimization**: Website video SEO; VideoObject; video sitemap; embed optimization
- **youtube-ads**: YouTube paid ads (TrueView, Bumper)
- **content-marketing**: Video as content format
- **parasite-seo**: YouTube as high-authority platform
- **generative-engine-optimization**: GEO strategy; YouTube as distribution for AI citation
