# Framework de Análise Comparativa — Incorporador

## Dimensões de Avaliação

Para cada capacidade dos dois sistemas, avalie em 5 dimensões:

### 1. Completude
- Essa capacidade cobre o caso de uso completamente?
- Há edge cases não tratados?
- Score: 1 (fragmentada) → 5 (completa)

### 2. Qualidade do Output
- O resultado entregue é acionável? Rico? Específico?
- É genérico/hipotético ou baseado em dados reais?
- Score: 1 (vago) → 5 (preciso e acionável)

### 3. Integração
- Conecta bem com outros módulos do sistema?
- Tem inputs/outputs padronizados?
- Score: 1 (ilha isolada) → 5 (totalmente integrado)

### 4. Reusabilidade
- Pode ser reutilizado para diferentes contextos/clientes?
- É parametrizável?
- Score: 1 (hardcoded) → 5 (genérico)

### 5. Unicidade
- É difícil de replicar? Dá vantagem competitiva?
- Score: 1 (commodity) → 5 (exclusivo)

---

## Tabela de Decisão

| Sistema Alvo | Sistema Base | Decisão Recomendada |
|---|---|---|
| Score alto | Score baixo | SUBSTITUIR |
| Score alto | Não existe | INCORPORAR |
| Score alto | Score alto diferente | FUNDIR |
| Score alto | Score alto igual | MANTER BASE + DESCARTAR |
| Score baixo | Não existe | Avaliar se CRIAR algo melhor |
| Score baixo | Qualquer | DESCARTAR |

---

## Categorias de Análise

### Camada de Dados (Intelligence Layer)
Capacidades que produzem ou transformam dados reais do mercado:
- Coleta de dados (scraping, APIs, uploads)
- Processamento (transcrição, parsing, scoring)
- Análise (IA, relatórios, insights)
- Armazenamento (formatos, persistência, índices)

### Camada de Estratégia (Strategy Layer)
Capacidades que transformam dados em decisões:
- Posicionamento
- Análise competitiva
- Identificação de oportunidades
- Definição de avatar/persona

### Camada de Produção (Production Layer)
Capacidades que criam entregáveis:
- Copywriting
- Roteiros
- Calendário editorial
- Design briefing
- Campanha completa

### Camada de Operações (Ops Layer)
Capacidades que gerenciam o processo:
- Pipelines e workflows
- Memória e estado
- Gestão de cliente
- Automações e hooks

### Camada de Interface (Interface Layer)
Como o usuário acessa tudo:
- Slash commands
- Skills
- Agentes
- Documentação

---

## Regras de Priorização

**Prioridade ALTA** — item que trava outras capacidades ou tem alto impacto no output final
**Prioridade MÉDIA** — melhora a qualidade mas o sistema funciona sem
**Prioridade BAIXA** — nice-to-have, qualidade de vida

**Esforço PEQUENO** — copiar arquivo + pequenas adaptações (< 1h)
**Esforço MÉDIO** — criar novo arquivo + integrar com existentes (1-4h)
**Esforço GRANDE** — redesenhar arquitetura ou criar múltiplos artefatos (> 4h)

**Quick Win** = Prioridade ALTA + Esforço PEQUENO → fazer imediatamente
**High Value** = Prioridade ALTA + Esforço MÉDIO → próximo sprint
**Backlog** = Prioridade BAIXA + qualquer esforço → registrar, não comprometer

---

## Padrão de Análise de Agente HAOS

Ao analisar um agente HAOS, extraia estas dimensões:

```
IDENTIDADE: Quem é, especialidade, personalidade
NORTE: Objetivo final, métrica de sucesso
BRIEF OBRIGATÓRIO: O que precisa receber para funcionar
FRAMEWORK FIXO: Como pensa, método, referências
RETORNO ESTRUTURADO: Formato exato do output
NUNCA: Restrições absolutas
```

Compare com o equivalente em HAOS Master (se existir) e avalie qual versão
produz output mais rico e acionável.

---

## Padrão de Análise de Script Python

Ao analisar scripts do pipeline AE, capture:

```
INPUT: Parâmetros, arquivos necessários, dependências
PROCESSO: O que faz, modelos usados, tempo estimado
OUTPUT: Arquivos gerados, formato, tamanho típico
RESUME: Tem suporte a retomada?
ERROS CONHECIDOS: Falhas documentadas e workarounds
```
