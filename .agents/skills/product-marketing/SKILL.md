---
name: product-marketing
description: "Use quando o usu\u00e1rio quiser criar ou atualizar o documento de contexto de marketing de produto. Use tamb\u00e9m quando ele mencionar 'contexto de produto', 'contexto de marketing', 'configurar contexto', 'posicionamento', 'quem \u00e9 meu p\u00fablico-alvo', 'descrever meu produto', 'ICP', 'perfil de cliente ideal', ou quando quiser evitar repetir informa\u00e7\u00f5es fundamentais em v\u00e1rias tarefas de marketing. Use no in\u00edcio de qualquer projeto novo, antes das outras skills de marketing \u2014 ela cria `<USER_DEPENDENCY:.agents/product-marketing.md>`, que todas as outras skills consultam para contexto de produto, p\u00fablico e posicionamento."
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

# Contexto de Marketing de Produto (HAOS)

Você ajuda o usuário a criar e manter um documento de contexto de marketing de produto. Ele captura o posicionamento e as mensagens fundamentais que as demais skills de marketing consultam, para o usuário não precisar se repetir.

O documento fica em `<USER_DEPENDENCY:.agents/product-marketing.md>`.

> **Fundação das 4 marcas HAOS.** No nosso contexto, "produto" pode ser qualquer uma das marcas. Capture a voz correta de cada uma:
> - **HAU Soluções Digitais** — técnico, direto, B2B (agência/operações).
> - **EdsonBurger** — provocador, energético, masculino.
> - **SIM (Sociedade Internacional do Mindset)** — acolhedor, feminino, público 55+, transformação pessoal.
> - **Editora Mindset** — educacional, autoral, livros/conteúdo.
>
> Quando o projeto envolver uma marca específica, gere a seção **Voz da Marca** com base na voz dela. Se for um projeto multimarca, crie um bloco por marca.

## Fluxo de Trabalho

### Passo 1: Verificar Contexto Existente

Primeiro, verifique se `<USER_DEPENDENCY:.agents/product-marketing.md>` já existe. Verifique também `.claude/product-marketing.md` e o nome legado `product-marketing-context.md` (em `.agents/` ou `.claude/`) para setups antigos — se encontrar em qualquer lugar diferente de `<USER_DEPENDENCY:.agents/product-marketing.md>`, ofereça mover para o local canônico.

**Se existir:**
- Leia e resuma o que está capturado
- Pergunte quais seções o usuário quer atualizar
- Colete informação apenas dessas seções

**Se não existir, ofereça duas opções:**

1. **Rascunho automático a partir do repo/material** (recomendado): você estuda o que existe — README, landing pages, copy de marketing, dossiês de marca (HAU/SIM/usuario/Editora), etc. — e rascunha uma V1 do documento. O usuário então revisa, corrige e preenche lacunas. É mais rápido que começar do zero.

2. **Começar do zero**: percorrer cada seção em conversa, coletando informação uma seção por vez.

A maioria prefere a opção 1. Depois de apresentar o rascunho, pergunte: "O que precisa de correção? O que está faltando?"

### Passo 2: Coletar Informação

**Se estiver rascunhando automaticamente:**
1. Leia o material: README, landing pages, copy, páginas "sobre", meta descriptions, dossiês de marca, qualquer doc existente
2. Rascunhe todas as seções com base no que encontrar
3. Apresente o rascunho e pergunte o que precisa corrigir ou está faltando
4. Itere até o usuário ficar satisfeito

**Se estiver começando do zero:**
Percorra cada seção abaixo conversando, uma de cada vez. Não despeje todas as perguntas de uma vez.

Para cada seção:
1. Explique brevemente o que está capturando
2. Faça as perguntas relevantes
3. Confirme a precisão
4. Passe para a próxima

Insista na linguagem literal do cliente — frases exatas valem mais que descrições polidas, porque refletem como o cliente realmente pensa e fala, o que torna a copy mais ressonante.

---

## Seções a Capturar

### 1. Visão Geral do Produto
- Descrição em uma linha
- O que faz (2-3 frases)
- Categoria do produto (em qual "prateleira" você está — como o cliente busca por você)
- Tipo de produto (infoproduto, e-commerce, serviço, SaaS, comunidade, etc.)
- Modelo de negócio e precificação

### 2. Público-Alvo
- Tipo de cliente (segmento, faixa etária, estágio)
- Tomadores de decisão (papéis, quem decide a compra)
- Caso de uso principal (o principal problema que você resolve)
- Jobs to be done (2-3 coisas para as quais o cliente "contrata" você)
- Casos de uso ou cenários específicos

### 3. Personas (quando há mais de um decisor)
Se vários envolvidos participam da compra, capture para cada um:
- Usuário, Influenciador, Decisor, Comprador financeiro
- O que cada um valoriza, o desafio deles e o valor que você promete

### 4. Problemas & Dores
- Desafio central que o cliente enfrenta antes de te encontrar
- Por que as soluções atuais falham
- Quanto isso custa (tempo, dinheiro, oportunidades)
- Tensão emocional (estresse, medo, dúvida)

### 5. Cenário Competitivo
- **Concorrentes diretos**: mesma solução, mesmo problema
- **Concorrentes secundários**: solução diferente, mesmo problema
- **Concorrentes indiretos**: abordagem conflitante (ex.: fazer nada, planilha, "deixar pra depois")
- Como cada um falha para o cliente

### 6. Diferenciação
- Diferenciais-chave (capacidades que as alternativas não têm)
- Como você resolve diferente
- Por que isso é melhor (benefícios)
- Por que o cliente escolhe você

### 7. Objeções & Anti-Personas
- Top 3 objeções ouvidas na venda e como respondê-las
- Quem NÃO é bom cliente (anti-persona)

### 8. Dinâmica de Mudança (4 Forças do JTBD)
- **Empurrão**: que frustrações afastam o cliente da solução atual
- **Atração**: o que atrai ele para você
- **Hábito**: o que o mantém preso à abordagem atual
- **Ansiedade**: o que o preocupa em mudar

### 9. Linguagem do Cliente
- Como o cliente descreve o problema (literal)
- Como descreve sua solução (literal)
- Palavras/frases para usar
- Palavras/frases para evitar
- Glossário de termos específicos do produto

### 10. Voz da Marca
- Marca (HAU / EdsonBurger / SIM / Editora Mindset ou outra)
- Tom (técnico, provocador, acolhedor, educacional)
- Estilo de comunicação (direto, conversacional, técnico)
- Personalidade da marca (3-5 adjetivos)

### 11. Provas
- Métricas ou resultados-chave para citar
- Clientes/marcas notáveis
- Trechos de depoimento
- Principais temas de valor e evidências de apoio

### 12. Metas
- Meta principal de negócio
- Ação de conversão-chave (o que você quer que a pessoa faça)
- Métricas atuais (se conhecidas)

---

## Passo 3: Criar o Documento

Depois de coletar a informação, crie `<USER_DEPENDENCY:.agents/product-marketing.md>` com esta estrutura:

```markdown
# Contexto de Marketing de Produto

*Última atualização: [data]*

## Visão Geral do Produto
**Frase de uma linha:**
**O que faz:**
**Categoria:**
**Tipo de produto:**
**Modelo de negócio:**

## Público-Alvo
**Clientes-alvo:**
**Tomadores de decisão:**
**Caso de uso principal:**
**Jobs to be done:**
-
**Casos de uso:**
-

## Personas
| Persona | Valoriza | Desafio | Valor que prometemos |
|---------|----------|---------|----------------------|
| | | | |

## Problemas & Dores
**Problema central:**
**Por que as alternativas falham:**
-
**Quanto custa:**
**Tensão emocional:**

## Cenário Competitivo
**Direto:** [Concorrente] — falha porque...
**Secundário:** [Abordagem] — falha porque...
**Indireto:** [Alternativa] — falha porque...

## Diferenciação
**Diferenciais-chave:**
-
**Como fazemos diferente:**
**Por que é melhor:**
**Por que escolhem a gente:**

## Objeções
| Objeção | Resposta |
|---------|----------|
| | |

**Anti-persona:**

## Dinâmica de Mudança
**Empurrão:**
**Atração:**
**Hábito:**
**Ansiedade:**

## Linguagem do Cliente
**Como descreve o problema:**
- "[literal]"
**Como nos descreve:**
- "[literal]"
**Palavras para usar:**
**Palavras para evitar:**
**Glossário:**
| Termo | Significado |
|-------|-------------|
| | |

## Voz da Marca
**Marca:**
**Tom:**
**Estilo:**
**Personalidade:**

## Provas
**Métricas:**
**Clientes:**
**Depoimentos:**
> "[citação]" — [quem]
**Temas de valor:**
| Tema | Prova |
|------|-------|
| | |

## Metas
**Meta de negócio:**
**Ação de conversão:**
**Métricas atuais:**
```

---

## Passo 4: Confirmar e Salvar

- Mostre o documento completo
- Pergunte se algo precisa de ajuste
- Salve em `<USER_DEPENDENCY:.agents/product-marketing.md>`
- Avise: "As outras skills de marketing do HAOS vão usar esse contexto automaticamente. Rode `/product-marketing` quando quiser atualizar."

---

## Dicas

- **Seja específico**: pergunte "Qual é a frustração nº 1 que traz o cliente até você?" e não "Que problema você resolve?"
- **Capture as palavras exatas**: a linguagem do cliente vence descrições polidas
- **Peça exemplos**: "Você me dá um exemplo?" destrava respostas melhores
- **Valide no caminho**: resuma cada seção e confirme antes de seguir
- **Pule o que não se aplica**: nem todo produto precisa de todas as seções (ex.: Personas em B2C)
