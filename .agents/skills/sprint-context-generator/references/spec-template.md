# FEAT-XXX: [Nome da Feature]

📂 **Documentação Relacionada:**
- Plano Técnico (user-supplied dependency; see PORTABILITY.md) - Arquitetura e decisões técnicas
- Lista de Tasks (user-supplied dependency; see PORTABILITY.md) - Tarefas detalhadas (XX tasks)
- Pesquisa (user-supplied dependency; see PORTABILITY.md) - Documentação e referências

---

## Visão Geral

[Descrição clara e concisa da feature. O que ela faz? Qual problema resolve?]

**Contexto:**
[Por que esta feature é necessária? Qual é o contexto de negócio/técnico?]

**Escopo:**
[O que está INCLUÍDO nesta feature]
[O que está EXCLUÍDO (out of scope)]

---

## User Stories

### História Principal
> Como [tipo de usuário], quero [ação/funcionalidade], para [benefício/objetivo]

**Critérios de Aceitação:**
- [ ] [Critério específico e mensurável 1]
- [ ] [Critério específico e mensurável 2]
- [ ] [Critério específico e mensurável 3]

### Histórias Secundárias

#### História 2
> Como [tipo de usuário], quero [ação], para [benefício]

**Critérios de Aceitação:**
- [ ] [Critério 1]
- [ ] [Critério 2]

#### História 3
> Como [tipo de usuário], quero [ação], para [benefício]

**Critérios de Aceitação:**
- [ ] [Critério 1]
- [ ] [Critério 2]

---

## 🏗️ Análise do Arquiteto de Soluções

### Estrutura de Arquitetura

**Padrão de Arquitetura Escolhido:**
[Ex: Clean Architecture, MVC, MVVM, Hexagonal, etc.]

**Justificativa:**
[Por que este padrão é adequado para esta feature]

### Estrutura de Diretórios Proposta

```
[Mostrar árvore de diretórios completa com todos os arquivos a serem criados]

Exemplo:
src/
├── features/
│   └── auth/
│       ├── components/
│       │   ├── LoginForm.tsx
│       │   └── LogoutButton.tsx
│       ├── services/
│       │   └── auth.service.ts
│       ├── types/
│       │   └── auth.types.ts
│       └── utils/
│           └── validators.ts
├── lib/
│   └── auth/
│       ├── jwt.ts
│       └── password.ts
└── api/
    └── routes/
        └── auth.routes.ts
```

### Dependências Necessárias

**Novas Dependências (a instalar):**
```json
{
  "dependencies": {
    "[package-name]": "[versão]",  // [Propósito]
  },
  "devDependencies": {
    "[package-name]": "[versão]",  // [Propósito]
  }
}
```

**Dependências Existentes (a usar):**
- `[package-name]` - [Como será usado]

### Refatorações Necessárias

**Código Existente a Refatorar:**
1. **[Arquivo/Módulo 1]**: [O que precisa ser refatorado e por quê]
2. **[Arquivo/Módulo 2]**: [O que precisa ser refatorado e por quê]

**Motivação:**
[Por que essas refatorações são necessárias]

### Decisões de Arquitetura

#### Decisão 1: [Título da Decisão]
**Contexto:**
[Qual é o problema/questão a ser resolvido]

**Opções Consideradas:**
1. **Opção A**: [Descrição]
   - **Prós**: [Vantagens]
   - **Contras**: [Desvantagens]

2. **Opção B**: [Descrição]
   - **Prós**: [Vantagens]
   - **Contras**: [Desvantagens]

**Decisão Escolhida:**
[Opção X] foi escolhida

**Justificativa:**
[Por que esta opção é melhor para este contexto específico]

#### Decisão 2: [Título da Decisão]
[Repetir estrutura acima]

### Considerações de Escalabilidade

**Capacidade Esperada:**
- [Número de usuários simultâneos]
- [Volume de dados]
- [Transações por segundo]

**Estratégias de Escalabilidade:**
1. [Estratégia 1: Ex: Caching com Redis]
2. [Estratégia 2: Ex: Load balancing]

### Considerações de Manutenibilidade

**Facilidade de Manutenção:**
- [Como o código será organizado para facilitar manutenção]
- [Padrões de código a seguir]
- [Documentação necessária]

---

## 💻 Requisitos do Desenvolvedor

### Componentes/Módulos a Criar

#### Backend

##### 1. [Nome do Módulo/Serviço]
**Localização:** `[caminho/do/arquivo]`

**Responsabilidade:**
[O que este módulo faz]

**Métodos/Funções Principais:**
```typescript
// Exemplo de assinatura de método
async function methodName(param1: Type1, param2: Type2): Promise<ReturnType> {
  // [Descrição do que o método faz]
}
```

**Dependências:**
- [Depende de qual outro módulo/serviço]

##### 2. [Nome do Controller]
**Localização:** `[caminho/do/arquivo]`

**Endpoints:**
- `POST /api/[endpoint]` - [Descrição]
- `GET /api/[endpoint]` - [Descrição]

#### Frontend

##### 1. [Nome do Componente]
**Localização:** `[caminho/do/arquivo]`

**Responsabilidade:**
[O que este componente faz]

**Props:**
```typescript
interface ComponentProps {
  prop1: Type1;  // [Descrição]
  prop2: Type2;  // [Descrição]
}
```

**Estado:**
- [Estados que o componente gerencia]

**Eventos:**
- [Eventos que o componente emite/escuta]

### APIs a Implementar

#### API 1: [Nome da API]

**Endpoint:** `[METHOD] /api/[path]`

**Autenticação:** [Requerida/Não requerida] [Tipo: JWT, API Key, etc.]

**Request:**
```typescript
interface RequestBody {
  field1: Type1;  // [Descrição, validações]
  field2: Type2;  // [Descrição, validações]
}
```

**Response (Success - 200):**
```typescript
interface ResponseBody {
  field1: Type1;  // [Descrição]
  field2: Type2;  // [Descrição]
}
```

**Response (Error - 4xx/5xx):**
```typescript
interface ErrorResponse {
  error: string;
  message: string;
  statusCode: number;
}
```

**Validações:**
- [ ] [Validação 1: Ex: Email deve ser válido]
- [ ] [Validação 2: Ex: Senha mínimo 8 caracteres]

**Tratamento de Erros:**
- `400 Bad Request`: [Quando ocorre]
- `401 Unauthorized`: [Quando ocorre]
- `500 Internal Server Error`: [Quando ocorre]

### Padrões de Código

**DRY (Don't Repeat Yourself):**
- [Como evitar duplicação de código nesta feature]
- [Código/lógica que deve ser extraída para utils/helpers]

**SOLID Principles:**
- **Single Responsibility**: [Como cada módulo/classe tem uma única responsabilidade]
- **Dependency Inversion**: [Como dependências são injetadas]

**Nomenclatura:**
- **Arquivos**: [Padrão: kebab-case, PascalCase, camelCase]
- **Variáveis/Funções**: [Padrão]
- **Constantes**: [Padrão]
- **Componentes**: [Padrão]

### Variáveis de Ambiente

**Novas Variáveis:**
```env
# [Categoria: Ex: Authentication]
VAR_NAME=valor_exemplo  # [Descrição do que a variável controla]
ANOTHER_VAR=valor       # [Descrição]

# [Categoria: Ex: Database]
DB_VAR=valor            # [Descrição]
```

**Validação de Variáveis:**
- [Quais variáveis são obrigatórias]
- [Quais têm valores padrão]
- [Como validar na inicialização da aplicação]

### Tratamento de Erros

**Estratégia Geral:**
[Como erros devem ser tratados nesta feature]

**Tipos de Erro:**
1. **Erros de Validação**: [Como tratar]
2. **Erros de Autenticação/Autorização**: [Como tratar]
3. **Erros de Negócio**: [Como tratar]
4. **Erros de Infraestrutura** (DB, rede): [Como tratar]

**Logging:**
- [Que informações logar]
- [Níveis de log: error, warn, info, debug]

---

## 🎨 Especificações de Design/UX

### Wireframes/Mockups

**Tela 1: [Nome da Tela]**
[Descrição ou link para mockup]

**Layout:**
```
┌─────────────────────────────────┐
│  [Cabeçalho]                    │
├─────────────────────────────────┤
│                                 │
│  [Conteúdo principal]           │
│                                 │
├─────────────────────────────────┤
│  [Rodapé]                       │
└─────────────────────────────────┘
```

**Elementos principais:**
- [Elemento 1: Ex: Formulário de login]
- [Elemento 2: Ex: Botão de submit]

### Componentes UI Reutilizáveis

#### Componente 1: [Nome do Componente]
**Descrição:**
[O que é e para que serve]

**Variantes:**
- **Variante 1**: [Quando usar]
- **Variante 2**: [Quando usar]

**Estados:**
- **Default**: [Aparência]
- **Hover**: [Aparência]
- **Active/Pressed**: [Aparência]
- **Disabled**: [Aparência]
- **Loading**: [Aparência]
- **Error**: [Aparência]

### Acessibilidade (WCAG 2.1 Level AA)

**Requisitos Obrigatórios:**
- [ ] **Navegação por teclado**: Todos os elementos interativos acessíveis via Tab
- [ ] **Labels ARIA**: Todos os inputs têm `aria-label` ou `<label>` associado
- [ ] **Contraste de cores**: Mínimo 4.5:1 para texto normal
- [ ] **Focus visível**: Indicador claro de foco em elementos interativos
- [ ] **Mensagens de erro**: Anunciadas por screen readers (`role="alert"`)
- [ ] **Headings semânticos**: Uso correto de h1, h2, h3, etc.

**Testagem:**
- [Como testar acessibilidade: ferramentas, screen readers]

### Responsividade

**Breakpoints:**
```
Mobile:     320px - 767px
Tablet:     768px - 1023px
Desktop:    1024px - 1439px
Wide:       1440px+
```

**Comportamento em cada breakpoint:**

**Mobile (320px - 767px):**
- [Como layout se adapta]
- [Elementos que são escondidos/reorganizados]

**Tablet (768px - 1023px):**
- [Adaptações de layout]

**Desktop (1024px+):**
- [Layout completo]

### Jornada do Usuário

**Fluxo Principal:**
```
[Passo 1] → [Passo 2] → [Passo 3] → [Sucesso]
             ↓
          [Erro]
```

**Descrição de cada passo:**
1. **[Passo 1]**: [O que acontece, interações, validações]
2. **[Passo 2]**: [O que acontece, interações, validações]
3. **[Passo 3]**: [O que acontece, interações, validações]
4. **[Sucesso]**: [Tela/mensagem de sucesso]

**Fluxos de Erro:**
- **Erro 1**: [Cenário, como usuário é informado, ações possíveis]
- **Erro 2**: [Cenário, como usuário é informado, ações possíveis]

### Feedback Visual

**Loading States:**
- [Quando mostrar loading]
- [Tipo de indicador: spinner, skeleton, progress bar]

**Success States:**
- [Mensagens de sucesso]
- [Animações/transições]

**Error States:**
- [Como exibir erros: toast, inline, modal]
- [Cores/ícones]

---

## ✅ Requisitos de QA

### Estratégia de Testes

**Pirâmide de Testes:**
```
        /\
       /E2E\        10% - Testes End-to-End (Playwright)
      /______\
     /        \
    /Integração\    20% - Testes de Integração
   /____________\
  /              \
 /   Unitários    \ 70% - Testes Unitários
/__________________\
```

### Cobertura de Testes

**Meta de Cobertura:** >90%

**Cobertura por Tipo:**
- **Unitários**: 95% (funções, métodos, componentes isolados)
- **Integração**: 85% (APIs, serviços, fluxos)
- **E2E**: 80% (jornadas críticas do usuário)

### Casos de Teste Unitários

#### Backend

##### Teste 1: [Nome da Função/Método]
**Arquivo de teste:** `[caminho].test.ts`

**Cenários:**
1. **Happy path**: [Entrada válida → Saída esperada]
2. **Erro de validação**: [Entrada inválida → Erro esperado]
3. **Edge case**: [Caso extremo → Comportamento esperado]

**Exemplo:**
```typescript
describe('[FunctionName]', () => {
  it('deve retornar [X] quando [condição]', () => {
    // Arrange
    const input = [...]

    // Act
    const result = functionName(input)

    // Assert
    expect(result).toBe([expected])
  })

  it('deve lançar erro quando [condição inválida]', () => {
    // ...
  })
})
```

#### Frontend

##### Teste 1: [Nome do Componente]
**Arquivo de teste:** `[caminho].test.tsx`

**Cenários:**
1. **Renderização**: Componente renderiza corretamente
2. **Interação**: Eventos (click, change) funcionam
3. **Estados**: Estados (loading, error) renderizam corretamente
4. **Props**: Diferentes props produzem diferentes outputs

### Casos de Teste de Integração

#### API 1: [Endpoint]
**Arquivo de teste:** `[caminho].integration.test.ts`

**Cenários:**
1. **Success (200)**: Request válido → Response esperada
2. **Bad Request (400)**: Request inválido → Erro de validação
3. **Unauthorized (401)**: Sem autenticação → Erro 401
4. **Server Error (500)**: Falha no servidor → Erro 500

### Casos de Teste E2E (Playwright)

#### Fluxo 1: [Nome do Fluxo]
**Arquivo de teste:** `[caminho].e2e.spec.ts`

**Cenário:**
1. [Passo 1: Ação do usuário]
2. [Passo 2: Verificação de resultado]
3. [Passo 3: Próxima ação]
4. [Passo 4: Verificação final]

**Exemplo:**
```typescript
test('[Descrição do teste]', async ({ page }) => {
  // 1. Navegar para página
  await page.goto('/[caminho]')

  // 2. Preencher formulário
  await page.fill('[selector]', '[valor]')

  // 3. Clicar em botão
  await page.click('[selector]')

  // 4. Verificar resultado
  await expect(page.locator('[selector]')).toHaveText('[texto esperado]')
})
```

### Edge Cases e Cenários Extremos

**Edge Case 1: [Descrição]**
- **Cenário**: [Condição extrema]
- **Comportamento esperado**: [Como o sistema deve reagir]
- **Teste**: [Como testar]

**Edge Case 2: [Descrição]**
- [Repetir estrutura acima]

**Exemplos comuns:**
- Strings vazias
- Números muito grandes/pequenos
- Caracteres especiais
- Dados nulos/undefined
- Arrays vazios
- Timeout de rede

### Testes de Performance

**Requisito 1: [Métrica]**
- **Métrica**: [Ex: Tempo de resposta da API]
- **Threshold**: [Ex: <200ms para 95% das requests]
- **Como medir**: [Ferramenta, método]

**Requisito 2: [Métrica]**
- [Repetir estrutura acima]

### Testes de Segurança

**Teste 1: [Vulnerabilidade]**
- **Vulnerabilidade**: [Ex: SQL Injection]
- **Como testar**: [Método, ferramenta]
- **Mitigação**: [Como prevenir]

**Teste 2: [Vulnerabilidade]**
- [Repetir estrutura acima]

**Checklist OWASP Top 10:**
- [ ] Injection (SQL, NoSQL, Command)
- [ ] Broken Authentication
- [ ] Sensitive Data Exposure
- [ ] XML External Entities (XXE)
- [ ] Broken Access Control
- [ ] Security Misconfiguration
- [ ] Cross-Site Scripting (XSS)
- [ ] Insecure Deserialization
- [ ] Using Components with Known Vulnerabilities
- [ ] Insufficient Logging & Monitoring

---

## 📊 Análise do Gerente de Projeto

### Prioridade da Feature

**Nível de Prioridade:** [High / Medium / Low]

**Justificativa:**
[Por que esta prioridade? Impacto no negócio, dependências, urgência]

**Impacto se NÃO implementado:**
[O que acontece se esta feature não for entregue]

### Riscos Potenciais

#### Risco 1: [Título do Risco]
**Probabilidade:** [Alta / Média / Baixa]
**Impacto:** [Alto / Médio / Baixo]

**Descrição:**
[O que pode dar errado]

**Mitigação:**
[Como reduzir probabilidade ou impacto]

**Plano de Contingência:**
[O que fazer se o risco se concretizar]

#### Risco 2: [Título do Risco]
[Repetir estrutura acima]

**Exemplo de riscos comuns:**
- Dependência de API externa instável
- Falta de conhecimento da equipe em tecnologia X
- Requisitos não claros
- Integração com sistema legado complexo
- Prazo apertado

### Estimativa de Complexidade

**Complexidade Técnica:** [Baixa / Média / Alta]

**Fatores de Complexidade:**
- [Fator 1: Ex: Integração com múltiplas APIs externas]
- [Fator 2: Ex: Lógica de negócio complexa]
- [Fator 3: Ex: Requisitos de performance rigorosos]

**Tempo Estimado:** [X-Y dias]

**Distribuição:**
- Setup e configuração: [X%]
- Desenvolvimento backend: [X%]
- Desenvolvimento frontend: [X%]
- Testes (unitários, integração, E2E): [X%]
- Code review e refinamento: [X%]
- Documentação: [X%]

### Critérios de Aceitação

**Critério 1:**
- [ ] [Critério específico, mensurável e testável]

**Critério 2:**
- [ ] [Critério específico, mensurável e testável]

**Critério 3:**
- [ ] [Critério específico, mensurável e testável]

**Definição de "Done":**
- [ ] Código implementado e funcionando
- [ ] Testes passando (>90% cobertura)
- [ ] Code review aprovado
- [ ] Documentação atualizada
- [ ] Deploy em ambiente de staging bem-sucedido
- [ ] QA manual realizado e aprovado
- [ ] Acessibilidade validada (WCAG 2.1 AA)
- [ ] Performance validada (métricas atingidas)

### Dependências Críticas

**Dependência 1: [Título]**
- **Tipo**: [Feature / Infraestrutura / Recurso]
- **Descrição**: [O que é necessário]
- **Status**: [Pending / In Progress / Complete / Blocked]
- **Impacto se bloqueado**: [O que acontece]

**Dependência 2: [Título]**
[Repetir estrutura acima]

### Stakeholders

**Stakeholder 1: [Nome/Cargo]**
- **Interesse**: [Por que esta feature importa para este stakeholder]
- **Nível de envolvimento**: [Alto / Médio / Baixo]
- **Comunicação necessária**: [O que precisa ser comunicado, quando]

---

## 💼 Requisitos de Negócio

### Valor de Negócio

**Problema que Resolve:**
[Qual dor do cliente/usuário esta feature alivia]

**Benefícios Quantificáveis:**
1. [Benefício 1: Ex: Redução de 30% no tempo de onboarding]
2. [Benefício 2: Ex: Aumento de 20% na conversão]
3. [Benefício 3: Ex: Redução de 50% em tickets de suporte]

**Benefícios Qualitativos:**
1. [Benefício 1: Ex: Melhora experiência do usuário]
2. [Benefício 2: Ex: Aumenta confiança na marca]

### KPIs (Key Performance Indicators)

**KPI 1: [Nome da Métrica]**
- **Definição**: [Como é medido]
- **Baseline atual**: [Valor antes da feature]
- **Meta**: [Valor esperado após feature]
- **Quando medir**: [Frequência, momento]

**KPI 2: [Nome da Métrica]**
[Repetir estrutura acima]

**Exemplos de KPIs:**
- Taxa de conversão
- Tempo médio de sessão
- NPS (Net Promoter Score)
- Churn rate
- Tickets de suporte
- Tempo de resposta

### Impacto no Usuário

**Persona 1: [Nome da Persona]**
**Impacto:**
- [Como a vida deste usuário melhora]
- [Que tarefas ficam mais fáceis/rápidas]
- [Frustrações que são eliminadas]

**Persona 2: [Nome da Persona]**
[Repetir estrutura acima]

### ROI (Return on Investment)

**Custos Estimados:**
- **Desenvolvimento**: [X horas × $Y/hora = $Z]
- **Infraestrutura**: [$X/mês]
- **Manutenção**: [$X/mês]
- **Total (primeiro ano)**: [$X]

**Retorno Estimado (primeiro ano):**
- **Aumento de receita**: [$X]
- **Redução de custos**: [$X]
- **Total**: [$X]

**ROI:** [(Retorno - Custo) / Custo × 100%] = [X%]

**Break-even:** [X meses]

### Alinhamento com Objetivos de Negócio

**Objetivo de Negócio 1: [Título]**
- **Como esta feature contribui**: [Explicação]

**Objetivo de Negócio 2: [Título]**
[Repetir estrutura acima]

**Exemplos de objetivos:**
- Aumentar market share em X%
- Expandir para novo mercado/região
- Melhorar retenção de clientes
- Reduzir custos operacionais
- Diferenciar-se da concorrência

---

## Requisitos de Performance/Segurança

### Performance

**Requisito 1: [Métrica]**
- **Métrica**: [Ex: Tempo de resposta da API]
- **Threshold**: [Ex: <200ms para 95% das requests]
- **Como medir**: [Ferramenta, método]
- **Como garantir**: [Estratégia: caching, otimização, etc.]

**Requisito 2: [Métrica]**
[Repetir estrutura acima]

**Métricas comuns:**
- Tempo de resposta (P50, P95, P99)
- Throughput (requests/segundo)
- Tempo de carregamento da página (FCP, LCP)
- Uso de memória
- Uso de CPU

### Segurança

**Requisito 1: [Categoria]**
- **Descrição**: [O que deve ser protegido, como]
- **Padrão/Compliance**: [Ex: OWASP, GDPR, LGPD]
- **Como implementar**: [Técnica, biblioteca, configuração]

**Requisito 2: [Categoria]**
[Repetir estrutura acima]

**Exemplos de requisitos de segurança:**
- Autenticação deve usar JWT com RS256
- Senhas devem ser hasheadas com bcrypt (custo 12)
- Dados sensíveis criptografados em repouso (AES-256)
- HTTPS obrigatório
- Rate limiting: max 100 requests/min por IP
- Logs não devem conter dados sensíveis
- Validação de input em todas as entradas

---

## Dependências e Bloqueadores

### Dependências

**Dependência 1: [ID ou Descrição]**
- **Tipo**: [Feature / Infraestrutura / Recurso]
- **Descrição**: [O que é necessário]
- **Status**: [Pending / In Progress / Complete / Blocked]
- **Impacto**: [O que acontece se não estiver pronto]

**Dependência 2: [ID ou Descrição]**
[Repetir estrutura acima]

### Bloqueadores

**Bloqueador 1: [Descrição]**
- **Descrição**: [O que está bloqueando]
- **Responsável**: [Quem pode resolver]
- **Ação necessária**: [O que precisa ser feito]
- **ETA**: [Quando será resolvido]

---

## Notas Adicionais

[Quaisquer informações que não se encaixam nas seções acima mas são relevantes para a implementação]

**Links Úteis:**
- [Documentação técnica relacionada]
- [Issues do GitHub relacionadas]
- [Discussões de design]
- [Protótipos/Mockups]

---

**Documento criado em:** [Data]
**Última atualização:** [Data]
**Versão:** 1.0
