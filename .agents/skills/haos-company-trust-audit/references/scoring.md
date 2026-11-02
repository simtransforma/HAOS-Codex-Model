# Trust Scoring

Pontuar a confiabilidade da empresa em 0-100. O score nao substitui julgamento; ele organiza evidencias.

## Dimensoes

| Dimensao | Peso | O que observar |
|---|---:|---|
| Identidade e existencia legal | 20 | Registro ativo, entidade correta, dominio consistente, dados comerciais claros |
| Regulacao e conformidade | 15 | Licencas setoriais, politicas, termos, privacidade, ausencia de sancoes relevantes |
| Reputacao e reclamacoes | 20 | Volume, severidade, recencia, resolucao, padroes recorrentes |
| Transparencia comercial | 15 | Preco, cobranca, recorrencia, reembolso, suporte, contratos e promessas |
| Operacao e entrega | 10 | Evidencia de produto/servico real, clientes, tempo de mercado, suporte |
| Website, dominio e seguranca basica | 10 | HTTPS, dominio coerente, canais oficiais, antifraude, sem impersonacao |
| Contraevidencia e red flags | 10 | Fraude, processos graves, sancoes, ocultacao, promessas impossiveis |

## Vereditos

| Score | Veredito padrao |
|---:|---|
| 85-100 | Confiavel |
| 70-84 | Confiavel com ressalvas |
| 50-69 | Inconclusivo / risco moderado |
| 30-49 | Nao recomendado |
| 0-29 | Alto risco |

## Gates bloqueantes

Aplicar independentemente do score:

- Sancao oficial relevante e atual: no minimo `nao recomendado`.
- Registro inexistente ou incompatibilidade grave entre marca, dominio e cobranca: no minimo `alto risco` ate explicar.
- Promessa financeira/saude/legal impossivel ou proibida: no minimo `nao recomendado`.
- Padrao forte de reclamacoes recentes sem resposta/resolucao: limitar a `confiavel com ressalvas` ou pior.
- Evidencia oficial de fraude, estelionato, piramide, empresa fantasma ou ordem de parada: `alto risco`.

## Red flags

- Nao informa razao social, CNPJ/registro, endereco comercial ou canal de suporte.
- Usa dominio recem-criado para marca que diz ter anos de mercado, sem explicacao.
- Depoimentos sem identificacao verificavel, logos de clientes sem permissao aparente ou claims exagerados.
- Pressao de urgencia, desconto extremo, garantia confusa, assinatura escondida.
- Reclamos repetidos sobre nao entrega, cancelamento impossivel, cobranca indevida ou suporte inexistente.
- Cobranca por entidade sem relacao clara com a marca.
- Regulador exige autorizacao e a empresa nao aparece no cadastro oficial.

## Green flags

- Registro ativo e coerente com site/cobranca.
- Regulacao ou certificacao verificavel quando exigida.
- Politicas claras de privacidade, termos, reembolso e cancelamento.
- Historico de resposta a reclamacoes com resolucao consistente.
- Clientes/cases verificaveis e claims moderados.
- Dominio antigo/coerente, HTTPS, canais oficiais consistentes.

## Nivel de confianca

- Alta: fontes oficiais + multiplas fontes independentes + dados recentes.
- Media: fontes suficientes, mas algum ponto central depende de inferencia ou dado social.
- Baixa: entidade pouco conhecida, poucas fontes, dados antigos ou homonimos nao resolvidos.

Nunca compensar uma red flag grave com muitas green flags cosmeticas.
