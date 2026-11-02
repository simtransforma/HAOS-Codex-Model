# Guia de Personas - Sprint Context Generator

Este guia detalha o que cada uma das **6 personas** deve analisar e fornecer ao gerar a especificação de uma feature.

Cada persona representa uma perspectiva diferente (técnica, negócio, UX, qualidade) e garante cobertura holística de todos os aspectos da feature.

---

## Índice

1. [🏗️ Arquiteto de Soluções](#arquiteto-de-soluções)
2. [💻 Desenvolvedor](#desenvolvedor)
3. [🎨 Designer/UX](#designerux)
4. [✅ QA (Quality Assurance)](#qa-quality-assurance)
5. [📊 Gerente de Projeto](#gerente-de-projeto)
6. [💼 Business Analyst](#business-analyst)

---

## 🏗️ Arquiteto de Soluções

### Foco
Estrutura técnica, arquitetura, dependências, escalabilidade, manutenibilidade

### Responsabilidade
Definir a arquitetura técnica que suportará a feature de forma escalável, segura e manutenível.

### Perguntas que o Arquiteto responde

1. **Como organizar o código?**
   - Qual estrutura de diretórios usar?
   - Como separar responsabilidades (layers)?
   - Onde cada arquivo deve ficar?

2. **Quais dependências instalar?**
   - Que packages npm/pip/etc são necessários?
   - Quais versões usar?
   - Por que escolher cada dependência?

3. **Há necessidade de refatoração?**
   - Código existente precisa ser modificado?
   - Há componentes a serem extraídos/reutilizados?
   - Há duplicação a ser eliminada?

4. **Qual padrão de arquitetura aplicar?**
   - Clean Architecture?
   - MVC? MVVM?
   - Hexagonal?
   - Microservices?

5. **Como garantir escalabilidade?**
   - Como a feature escala com mais usuários?
   - Há pontos de bottleneck?
   - Como otimizar performance?

---

### Análise a Gerar

#### 1. Estrutura de Diretórios Proposta

**O que incluir:**
- Árvore de diretórios completa (formato ASCII ou markdown)
- Justificativa da estrutura (por que organizar assim?)
- Separação de camadas (presentation, business, data)
- Convenções de nomenclatura

**Exemplo:**
```markdown
### Estrutura de Diretórios Proposta

Baseado em Clean Architecture e melhores práticas de [framework detectado]:

```
src/
├── app/                    # Presentation layer (Next.js App Router)
│   ├── (auth)/
│   │   └── login/
│   │       └── page.tsx    # Página de login
│   └── api/
│       └── auth/
│           └── route.ts    # API endpoints
├── services/               # Application layer (business logic)
│   └── AuthService.ts
├── repositories/           # Infrastructure layer (data access)
│   └── UserRepository.ts
├── lib/                    # Utilities and helpers
│   └── auth/
│       ├── jwt.ts          # JWT utilities
│       └── password.ts     # Password hashing
└── types/                  # Domain models and interfaces
    └── auth.ts
```

**Justificativa:**
- **Separação de responsabilidades**: Cada camada tem responsabilidade única
- **Testabilidade**: Services isolados facilitam mocking e unit tests
- **Escalabilidade**: Estrutura suporta crescimento sem refatoração massiva
- **Manutenibilidade**: Fácil encontrar e modificar código (princípio do menor conhecimento)
```

---

#### 2. Dependências Necessárias

**O que incluir:**
- Lista de packages de produção (com versões)
- Lista de packages de desenvolvimento (com versões)
- Justificativa para cada dependência (por que escolher?)
- Alternativas consideradas (se relevante)

**Exemplo:**
```markdown
### Dependências Necessárias

**Produção:**
```json
{
  "jsonwebtoken": "^9.0.2",    // Geração e validação de JWT (padrão da indústria)
  "bcrypt": "^5.1.1",          // Hash seguro de senhas (resistente a rainbow tables)
  "zod": "^3.22.4"             // Validação de schemas com types automáticos
}
```

**Desenvolvimento:**
```json
{
  "@types/jsonwebtoken": "^9.0.5",  // Types TypeScript para JWT
  "@types/bcrypt": "^5.0.2",        // Types TypeScript para bcrypt
  "jest": "^29.7.0"                 // Framework de testes unitários
}
```

**Por que estas escolhas:**
- **jsonwebtoken** vs jose: jsonwebtoken é mais maduro e amplamente usado
- **bcrypt** vs argon2: bcrypt é padrão da indústria, mais documentado
- **zod** vs yup: zod tem melhor integração com TypeScript (type inference)
```

---

#### 3. Refatorações Necessárias

**O que incluir:**
- Código existente que precisa ser modificado
- Componentes a serem extraídos para reutilização
- Duplicações a serem eliminadas
- Impacto das refatorações (breaking changes?)

**Exemplo:**
```markdown
### Refatorações Necessárias

**1. Módulo de Auth Atual**
- **Problema**: Atualmente usa sessões server-side (stateful, dificulta scaling)
- **Refatoração**: Migrar para JWT (stateless)
- **Impacto**: Breaking change - usuários serão deslogados na migração
- **Mitigação**: Comunicar mudança, oferecer "Lembrar-me" opcional

**2. Componente de Formulário**
- **Problema**: Lógica de validação duplicada em LoginForm e RegisterForm
- **Refatoração**: Extrair hook customizado `useFormValidation(schema)`
- **Benefício**: DRY, reutilizável em outros formulários

**Não aplicável (projeto novo):**
Se projeto novo, escrever: "Não aplicável - projeto novo sem código legado."
```

---

#### 4. Padrões de Arquitetura

**O que incluir:**
- Padrão escolhido (Clean, MVC, Hexagonal, etc.)
- Descrição das camadas
- Fluxo de dados (diagrama)
- Por que este padrão? (justificativa)

**Exemplo:**
```markdown
### Padrões de Arquitetura

**Padrão escolhido:** Clean Architecture + Repository Pattern

**Camadas:**
1. **Presentation (app/, components/)**: UI, formulários, interação com usuário
   - Depende de: Application Layer (via API routes)
2. **Application (services/)**: Lógica de negócio, use cases, orquestração
   - Depende de: Domain (interfaces), Infrastructure (repositories via DI)
3. **Domain (types/, interfaces/)**: Modelos, contratos, regras de negócio puras
   - Depende de: Nada (camada mais interna)
4. **Infrastructure (repositories/, lib/)**: Acesso a dados, integrações externas
   - Depende de: Domain (implementa interfaces)

**Fluxo de dados:**
```
User clicks "Login"
    ↓
LoginForm (presentation)
    ↓
POST /api/auth/login (API route)
    ↓
AuthService.login() (application)
    ↓
UserRepository.findByEmail() (infrastructure)
    ↓
Prisma → PostgreSQL (database)
    ↑
User entity (domain)
    ↑
JWT token + user data (response)
```

**Justificativa:**
- Clean Architecture garante baixo acoplamento e alta coesão
- Repository Pattern isola lógica de acesso a dados (fácil trocar Prisma por TypeORM se necessário)
- Testabilidade: Services podem ser testados sem DB (mocking repositories)
```

---

#### 5. Decisões de Escalabilidade

**O que incluir:**
- Como a feature escala com mais usuários?
- Pontos de bottleneck identificados
- Estratégias de otimização
- Considerações de performance

**Exemplo:**
```markdown
### Decisões de Escalabilidade

1. **JWT Stateless**: Tokens não são armazenados no servidor, permitindo horizontal scaling sem sessões compartilhadas
   - **Vantagem**: Adicionar servidores não requer sincronização de sessões
   - **Limitação**: Impossível invalidar access tokens (mitigado com expiração curta de 15min)

2. **Refresh Tokens em DB**: Armazenar apenas refresh tokens no DB para permitir revogação
   - **Performance**: Lookup de refresh token é raro (apenas a cada 7 dias ou logout)
   - **Escalabilidade**: DB index em `refresh_tokens.token` garante O(log n) lookup

3. **Rate Limiting no Edge**: Implementar rate limiting no Nginx/Vercel Edge (antes de atingir aplicação)
   - **Previne**: Brute force, DDoS
   - **Escalabilidade**: Proteção no edge não consome recursos da aplicação

4. **Fase 2 (futuro)**: Redis para token blacklist
   - **Quando**: Se precisar invalidar access tokens em tempo real
   - **Como**: Armazenar tokens revogados em Redis com TTL = tempo até expiração
```

---

### Checklist do Arquiteto

Antes de finalizar, verificar:

- [ ] Estrutura de diretórios clara e justificada
- [ ] Todas as dependências listadas com versões
- [ ] Refatorações identificadas (ou "N/A" se projeto novo)
- [ ] Padrão de arquitetura escolhido e documentado
- [ ] Fluxo de dados visualizado (diagrama ASCII)
- [ ] Decisões de escalabilidade documentadas
- [ ] Alternativas consideradas e descartadas explicadas

---

## 💻 Desenvolvedor

### Foco
Implementação prática, componentes/módulos, APIs, padrões de código, variáveis de ambiente

### Responsabilidade
Definir **O QUE** implementar: quais classes, funções, componentes, endpoints criar.

### Perguntas que o Desenvolvedor responde

1. **Que componentes/módulos criar?**
   - Quais classes/serviços implementar?
   - Quais componentes React/Vue criar?
   - Que funções utilitárias são necessárias?

2. **Quais APIs implementar?**
   - Endpoints REST/GraphQL necessários?
   - Request/response de cada endpoint?
   - Validações de entrada?

3. **Que padrões de código seguir?**
   - DRY, SOLID aplicados como?
   - DTOs, interfaces, abstrações?
   - Error handling centralizado?

4. **Quais variáveis de ambiente?**
   - Que configurações vêm de `.env`?
   - Secrets, URLs, flags de feature?
   - Documentação de cada variável?

---

### Análise a Gerar

#### 1. Componentes/Módulos a Criar

**O que incluir:**
- Lista completa de componentes backend
- Lista completa de componentes frontend
- Responsabilidade de cada componente
- Métodos/funções principais
- Assinaturas de métodos (tipos de entrada/saída)

**Formato:**
```markdown
### Componentes/Módulos a Criar

**Backend:**

#### 1. [NomeDoServico] (`caminho/para/Service.ts`)
- **Responsabilidade**: [Descrição clara em 1 frase]
- **Métodos principais**:
  - `metodo1(param1: Type1, param2: Type2): Promise<ReturnType>` - [O que faz]
  - `metodo2(param: Type): Promise<ReturnType>` - [O que faz]
- **Dependências**: [Lista de dependências injetadas]

**Frontend:**

#### 1. [NomeDoComponente] (`caminho/para/Component.tsx`)
- **Responsabilidade**: [Descrição]
- **Props**:
  ```typescript
  interface ComponentProps {
    prop1: string
    prop2?: number
    onAction: () => void
  }
  ```
- **State**: [Descrição do estado interno]
- **Hooks usados**: useState, useEffect, useAuth (custom)
```

**Exemplo:**
```markdown
**Backend:**

#### 1. AuthService (`src/services/AuthService.ts`)
- **Responsabilidade**: Gerenciar autenticação de usuários (login, logout, refresh)
- **Métodos principais**:
  - `login(email: string, password: string): Promise<AuthResponse>` - Autentica usuário e retorna tokens JWT
  - `logout(userId: string): Promise<void>` - Invalida refresh tokens do usuário
  - `refreshAccessToken(refreshToken: string): Promise<{accessToken: string}>` - Gera novo access token
- **Dependências**: IUserRepository (injetado via DI)

**Frontend:**

#### 1. LoginForm (`src/components/auth/LoginForm.tsx`)
- **Responsabilidade**: Formulário de login com validação client-side
- **Props**:
  ```typescript
  interface LoginFormProps {
    onSuccess?: () => void
    onError?: (error: string) => void
  }
  ```
- **State**: email, password, isLoading, errors
- **Hooks usados**: useForm (React Hook Form), useAuth (custom context)
```

---

#### 2. APIs a Implementar

**O que incluir:**
- Lista completa de endpoints
- Método HTTP (GET, POST, PUT, DELETE)
- Request (headers, body, query params)
- Response (sucesso + erro)
- Validações de entrada
- Status codes retornados

**Formato:**
```markdown
### APIs a Implementar

**REST Endpoints:**

#### 1. [METHOD] /api/[endpoint]
**Descrição:** [O que faz em 1 frase]

**Request:**
- **Headers**: [Lista headers necessários]
- **Body** (application/json):
  ```typescript
  {
    "campo1": "tipo",
    "campo2": "tipo"
  }
  ```
- **Validações**:
  - campo1: [Regras de validação]
  - campo2: [Regras de validação]

**Response (200 OK):**
```typescript
{
  "success": true,
  "data": {
    [conteúdo da resposta]
  }
}
```

**Response (4XX/5XX Error):**
```typescript
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Mensagem amigável"
  }
}
```

**Status codes:**
- 200: Sucesso
- 400: Dados inválidos
- 401: Não autenticado
- 500: Erro interno
```

**Exemplo:**
```markdown
#### 1. POST /api/auth/login
**Descrição:** Autenticar usuário com email e senha, retornar tokens JWT

**Request:**
- **Headers**: Content-Type: application/json
- **Body**:
  ```json
  {
    "email": "user-000013@account.example.invalid",
    "password": "secret_placeholder!"
  }
  ```
- **Validações**:
  - email: Formato de email válido, obrigatório
  - password: String, mínimo 8 caracteres, obrigatório

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "accessToken": "secret_placeholder",
    "refreshToken": "secret_placeholder",
    "user": {
      "id": "uuid",
      "email": "user-000013@account.example.invalid",
      "name": "John Doe"
    }
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Email ou senha incorretos"
  }
}
```

**Status codes:**
- 200: Login bem-sucedido
- 400: Validação falhou (email inválido, senha vazia, etc.)
- 401: Credenciais incorretas
- 500: Erro interno do servidor
```

---

#### 3. Padrões de Código (DRY, SOLID, etc.)

**O que incluir:**
- Aplicação de DRY (Don't Repeat Yourself)
- Aplicação de SOLID (principalmente SRP e DIP)
- Padrões específicos (DTOs, Constants, Error handling)
- Exemplos de código aplicando os padrões

**Exemplo:**
```markdown
### Padrões de Código (DRY, SOLID, etc.)

**DRY (Don't Repeat Yourself):**
- Extrair validação de email para `lib/validators/email.ts`
  ```typescript
  export const isValidEmail = (email: string): boolean => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }
  ```
- Criar hook customizado `useFormValidation(schema)` para reutilizar lógica de formulários
- Centralizar mensagens de erro em `lib/constants/error-messages.ts`

**SOLID:**
- **Single Responsibility**: AuthService só gerencia autenticação, não acessa DB diretamente
- **Dependency Inversion**: AuthService depende de IUserRepository (interface), não UserRepository (implementação)
  ```typescript
  class AuthService {
    constructor(private userRepository: IUserRepository) {}
    // Não depende de implementação concreta, apenas da interface
  }
  ```

**Padrões específicos:**

**DTOs (Data Transfer Objects):**
```typescript
// src/types/auth.ts
export interface LoginDto {
  email: string
  password: string
}

export interface CreateUserDto {
  email: string
  password: string
  name: string
}

export interface AuthResponse {
  accessToken: string
  refreshToken: string
  user: User
}
```

**Constants para valores mágicos:**
```typescript
// src/lib/constants/auth.ts
export const JWT_ACCESS_TOKEN_EXPIRY = '15m'
export const JWT_REFRESH_TOKEN_EXPIRY = '7d'
export const BCRYPT_SALT_ROUNDS = 12
export const MAX_LOGIN_ATTEMPTS = 5
```

**Error Handling Centralizado:**
```typescript
// src/lib/errors/AuthError.ts
export class AuthError extends Error {
  constructor(
    public code: string,
    message: string
  ) {
    super(message)
    this.name = 'AuthError'
  }
}

// Uso em AuthService
throw new AuthError('INVALID_CREDENTIALS', 'Email ou senha incorretos')
```
```

---

#### 4. Variáveis de Ambiente

**O que incluir:**
- Arquivo `.env.example` completo
- Documentação de cada variável
- Como obter valores (para APIs externas)
- Valores padrão para desenvolvimento
- Diferenças entre dev/prod

**Formato:**
```markdown
### Variáveis de Ambiente

**Arquivo `.env.example`:**
```env
# Database
DATABASE_URL=secret_placeholderlocalhost:5432/dbname
DATABASE_URL_UNPOOLED=... # (se aplicável, ex: Prisma)

# JWT
JWT_ACCESS_SECRET=your-secret-here
JWT_REFRESH_SECRET=your-refresh-secret-here

# API Keys (se aplicável)
STRIPE_API_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Environment
NODE_ENV=development
PORT=3000
```

**Documentação:**

| Variável | Descrição | Como obter | Valor padrão (dev) |
|----------|-----------|------------|---------------------|
| `DATABASE_URL` | String de conexão PostgreSQL | Local: `secret_placeholderlocalhost:5432/myapp` | - |
| `JWT_ACCESS_SECRET` | Secret para assinar access tokens | Gerar com `openssl rand -base64 32` | (gerar) |
| `JWT_REFRESH_SECRET` | Secret para assinar refresh tokens | Gerar com `openssl rand -base64 32` (diferente do access) | (gerar) |
| `STRIPE_API_KEY` | Chave da API Stripe | Dashboard Stripe → API Keys | sk_test_... |

**Produção:**
- Configurar em Vercel/Heroku/AWS: Settings → Environment Variables
- **NUNCA** commitar valores reais no Git
- Usar secrets managers (AWS Secrets Manager, Vercel Secrets) para produção
```

---

### Checklist do Desenvolvedor

- [ ] Todos os componentes backend listados com métodos e assinaturas
- [ ] Todos os componentes frontend listados com props e state
- [ ] Todas as APIs documentadas com request/response
- [ ] Validações de entrada especificadas
- [ ] Padrões de código (DRY, SOLID) aplicados com exemplos
- [ ] `.env.example` completo
- [ ] Documentação de variáveis de ambiente clara

---

## 🎨 Designer/UX

### Foco
Interface do usuário, acessibilidade, responsividade, experiência do usuário

### Responsabilidade
Definir COMO a interface deve ser (layout, cores, interações, acessibilidade).

### Perguntas que o Designer responde

1. **Como a UI deve se parecer?**
   - Layout e estrutura visual?
   - Cores, tipografia, espaçamento?
   - Componentes visuais necessários?

2. **Quais componentes UI criar?**
   - Button, Input, Card, Modal?
   - Variantes de cada componente?
   - Estados (hover, focus, disabled)?

3. **Como garantir acessibilidade?**
   - WCAG 2.1 Level AA?
   - Navegação por teclado?
   - Screen readers?
   - Contraste de cores?

4. **Como garantir responsividade?**
   - Breakpoints?
   - Adaptações mobile vs desktop?
   - Touch targets adequados?

5. **Qual a jornada do usuário?**
   - User flow completo?
   - Happy path vs error paths?
   - Estados de carregamento?

---

### Análise a Gerar

#### 1. Wireframes/Mockups

**O que incluir:**
- Wireframe em ASCII art ou descrição textual
- Layout da página/tela principal
- Posicionamento de elementos
- Hierarquia visual

**Exemplo:**
```markdown
### Wireframes/Mockups

**Tela de Login:**

```
┌──────────────────────────────────────────┐
│                                          │
│            [Logo da Aplicação]           │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │                                    │  │
│  │   Bem-vindo de volta!              │  │
│  │                                    │  │
│  │   [Email]                          │  │
│  │   ┌──────────────────────────────┐ │  │
│  │   │ user-000037@account.example.invalid        │ │  │
│  │   └──────────────────────────────┘ │  │
│  │                                    │  │
│  │   [Senha]                          │  │
│  │   ┌──────────────────────────────┐ │  │
│  │   │ ••••••••                     │ │  │
│  │   └──────────────────────────────┘ │  │
│  │                                    │  │
│  │   ┌──────────────────────────────┐ │  │
│  │   │        Entrar                │ │  │
│  │   └──────────────────────────────┘ │  │
│  │                                    │  │
│  │   Esqueceu sua senha?              │  │
│  │                                    │  │
│  └────────────────────────────────────┘  │
│                                          │
└──────────────────────────────────────────┘
```

**Layout:**
- Centralizado verticalmente e horizontalmente
- Card com elevação (sombra sutil)
- Max-width: 400px
- Padding interno: 2rem
- Border-radius: 8px
```

---

#### 2. Componentes UI Reutilizáveis

**O que incluir:**
- Lista de componentes UI a criar
- Variantes de cada componente
- Tamanhos disponíveis
- Estados (normal, hover, focus, disabled, loading)
- Props e API do componente
- Exemplo de uso

**Formato:**
```markdown
### Componentes UI Reutilizáveis

#### 1. Button (`components/ui/Button.tsx`)

**Variantes:**
- `primary`: Azul (#3B82F6), texto branco
- `secondary`: Cinza (#6B7280), texto branco
- `danger`: Vermelho (#EF4444), texto branco
- `ghost`: Transparente, texto colorido

**Tamanhos:**
- `small`: padding 0.5rem 1rem, font-size 14px
- `medium`: padding 0.75rem 1.5rem, font-size 16px (default)
- `large`: padding 1rem 2rem, font-size 18px

**Estados:**
- `normal`: Cor padrão da variante
- `hover`: Cor 10% mais escura
- `focus`: Ring azul 2px (outline)
- `disabled`: Opacidade 50%, cursor not-allowed
- `loading`: Spinner + texto "Carregando..."

**API:**
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'small' | 'medium' | 'large'
  loading?: boolean
  disabled?: boolean
  onClick?: () => void
  children: React.ReactNode
}
```

**Exemplo de uso:**
```tsx
<Button variant="primary" size="medium" loading={isLoading}>
  Entrar
</Button>
```
```

---

#### 3. Acessibilidade (WCAG 2.1 Level AA)

**O que incluir:**
- Requisitos de acessibilidade obrigatórios
- Labels e ARIA
- Contraste de cores (com valores calculados)
- Navegação por teclado
- Screen readers
- Exemplos de código acessível

**Formato:**
```markdown
### Acessibilidade (WCAG 2.1 Level AA)

**Requisitos obrigatórios:**

1. **Labels e ARIA:**
   - ✅ Todos os inputs têm `<label>` com `htmlFor`
   - ✅ Formulário tem `aria-label="Formulário de login"`
   - ✅ Botões têm texto descritivo (não apenas ícones)

2. **Contraste de cores:**
   - ✅ Texto normal (#111827 em #FFFFFF): **16.1:1** (mínimo 4.5:1) ✅
   - ✅ Botão primário (branco em #3B82F6): **4.5:1** (mínimo 4.5:1) ✅
   - ✅ Erro (#DC2626 em #FFFFFF): **7.9:1** (mínimo 4.5:1) ✅

3. **Navegação por teclado:**
   - ✅ Tab: Navega entre inputs e botão
   - ✅ Enter: Submete formulário
   - ✅ Escape: Limpa formulário (se houver erros)
   - ✅ Focus indicators visíveis (ring azul 2px)

4. **Screen readers:**
   - ✅ Mensagens de erro têm `role="alert"` (anunciadas automaticamente)
   - ✅ Estado de loading: `aria-live="polite"`
   - ✅ Campos obrigatórios: `aria-required="true"`

**Exemplo de implementação:**
```tsx
<form aria-label="Formulário de login" onSubmit={handleSubmit}>
  <div>
    <label htmlFor="email" className="block text-sm font-medium">
      Email <span aria-label="obrigatório">*</span>
    </label>
    <input
      id="email"
      type="email"
      required
      aria-required="true"
      aria-invalid={!!errors.email}
      aria-describedby={errors.email ? "email-error" : undefined}
    />
    {errors.email && (
      <p id="email-error" role="alert" className="text-red-600">
        <span aria-hidden="true">⚠️</span> {errors.email}
      </p>
    )}
  </div>
</form>
```
```

---

#### 4. Responsividade

**O que incluir:**
- Breakpoints definidos
- Adaptações por device (mobile, tablet, desktop)
- Exemplos de implementação (Tailwind, CSS)
- Touch targets adequados (mínimo 44x44px)

**Exemplo:**
```markdown
### Responsividade

**Breakpoints (Tailwind CSS):**
- `mobile`: 0-640px (sm)
- `tablet`: 641px-1024px (md/lg)
- `desktop`: 1025px+ (xl)

**Adaptações por device:**

**Mobile (0-640px):**
- Layout em coluna única, full-width
- Card de login: width 100%, padding reduzido (1rem)
- Botões: Full-width
- Font-size base: 16px (evitar zoom no iOS)
- Espaçamento: Reduzido (gap-3)

**Tablet (641px-1024px):**
- Card de login: Max-width 400px, centralizado
- Botões: Width auto
- Font-size: 16px
- Espaçamento: Normal (gap-4)

**Desktop (1025px+):**
- Card de login: Max-width 420px
- Botões: Width auto, hover effects ativos
- Font-size: 16px
- Espaçamento: Generoso (gap-6)

**Implementação (Tailwind CSS):**
```tsx
<div className="min-h-screen flex items-center justify-center p-4 sm:p-6 lg:p-8">
  <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-6 sm:p-8">
    {/* Formulário */}
  </div>
</div>

<button className="w-full sm:w-auto px-6 py-3">
  Entrar
</button>
```

**Touch targets:**
- Mínimo 44x44px em mobile (WCAG 2.1)
- Botões: min-height 44px, padding vertical 0.75rem
- Links e inputs: min-height 44px
```

---

#### 5. Jornada do Usuário (User Flow)

**O que incluir:**
- Fluxo happy path (sucesso)
- Fluxos de erro
- Estados de carregamento
- Feedback visual em cada etapa

**Formato:**
```markdown
### Jornada do Usuário (User Flow)

**Fluxo de Login (Happy Path):**
1. Usuário acessa `/login`
2. Vê formulário de login (campos vazios, botão ativo)
3. Preenche email: `user-000013@account.example.invalid`
4. Preenche senha: `SecurePassword123!`
5. Clica botão "Entrar"
6. **Loading state**: Botão mostra spinner, fica disabled, cursor muda para `wait`
7. **Request success**: API retorna 200 OK
8. Tokens salvos no localStorage
9. **Feedback visual**: Toast verde "Login realizado!" (2 segundos)
10. Redirecionamento para `/dashboard` (fade transition)
11. Dashboard mostra: "Bem-vindo, John Doe!"

**Fluxo de Login (Erro de Credenciais):**
1-5. [Mesmo que happy path]
6. **Loading state**: Botão mostra spinner
7. **Request error**: API retorna 401 Unauthorized
8. **Error state**:
   - Mensagem de erro aparece: "Email ou senha incorretos"
   - Cor vermelha (#DC2626), ícone de alerta
   - Borda dos campos fica vermelha
   - Campo de senha é limpo (value vazio)
   - Foco retorna ao campo de email
   - Screen reader anuncia: "Erro: Email ou senha incorretos"
   - Botão volta ao estado normal
9. Usuário corrige senha e tenta novamente

**Fluxo de Login (Validação Client-Side):**
1-3. [Usuário preenche email: `invalid-email`]
4. Clica botão "Entrar"
5. **Validação client-side (Zod)**:
   - Email inválido: Mensagem "Email inválido" aparece inline
   - Borda do campo email fica vermelha
   - **Request NÃO é enviado** (evita overhead no servidor)
6. Usuário corrige email
7. Mensagem de erro desaparece, borda volta ao normal
8. Clica "Entrar" novamente
9. [Continua fluxo normal]
```

---

### Checklist do Designer

- [ ] Wireframes/mockups descritos ou desenhados
- [ ] Todos os componentes UI listados com variantes e estados
- [ ] Acessibilidade WCAG 2.1 AA garantida (labels, contraste, keyboard, SR)
- [ ] Responsividade especificada (breakpoints e adaptações)
- [ ] Jornada do usuário documentada (happy + error paths)
- [ ] Feedback visual em cada estado (loading, sucesso, erro)

---

## ✅ QA (Quality Assurance)

### Foco
Estratégia de testes, cobertura, casos extremos, performance, qualidade

### Responsabilidade
Garantir que a feature funciona corretamente em todos os cenários (normais e extremos).

### Perguntas que o QA responde

1. **Que casos de teste são necessários?**
   - Unitários, integração, E2E?
   - Quantos testes por tipo?
   - Que cenários cobrir?

2. **Qual cobertura de testes atingir?**
   - Meta de cobertura (%, linhas)?
   - Quais módulos são críticos?
   - Como medir cobertura?

3. **Quais edge cases testar?**
   - Entradas inválidas?
   - Limites de valores?
   - Condições de corrida?

4. **Como testar performance?**
   - Requisitos de tempo de resposta?
   - Load testing?
   - Métricas a medir?

5. **Que cenários de erro cobrir?**
   - Falhas de rede?
   - Erros de servidor?
   - Timeouts?

---

### Análise a Gerar

#### 1. Estratégia de Testes

**O que incluir:**
- Pirâmide de testes (unitários > integração > E2E)
- Quantidade de testes por tipo
- Frameworks usados
- Meta de cobertura

**Exemplo:**
```markdown
### Estratégia de Testes

**Pirâmide de testes:**
```
        /\
       / 15\       ← E2E: 15 testes (fluxos principais)
      / E2E \
     /________\
    /    30    \   ← Integração: 30 testes (APIs + DB)
   / Integration\
  /______________\
 /      42        \ ← Unitários: 42 testes (lógica de negócio)
/      Unit        \
/____________________\
```

**Total de testes:** 87
**Meta de cobertura:** >90% (statement coverage)

**Frameworks:**
- **Unitários**: Jest (já configurado no Next.js)
- **Integração**: Jest + Supertest (para testar APIs)
- **E2E**: Playwright (cross-browser)

**Priorização:**
- **Crítico** (100% cobertura): AuthService, PasswordService, JWT generation
- **Alto** (>90% cobertura): API routes, UserRepository
- **Médio** (>80% cobertura): UI components
```

---

#### 2. Casos de Teste (Unitários)

**O que incluir:**
- Lista de testes por módulo/componente
- Descrição de cada teste (formato "should ... when ...")
- Exemplos de código de teste
- Estratégia de mocking

**Exemplo:**
```markdown
### Casos de Teste (Unitários)

**AuthService.ts:**

1. `login()`:
   - ✅ Should return access and refresh tokens when credentials are valid
   - ✅ Should update user's lastLoginAt timestamp
   - ✅ Should return error when user does not exist
   - ✅ Should return error when password is incorrect
   - ✅ Should return error when user account is disabled

2. `validateAccessToken()`:
   - ✅ Should return user payload when token is valid
   - ✅ Should return null when token is expired
   - ✅ Should return null when token is malformed
   - ✅ Should return null when signature is invalid

[... continuar para todos os módulos ...]

**Exemplo de teste:**
```typescript
// src/services/__tests__/AuthService.spec.ts
describe('AuthService', () => {
  let authService: AuthService
  let mockUserRepository: jest.Mocked<IUserRepository>

  beforeEach(() => {
    mockUserRepository = {
      findByEmail: jest.fn(),
      updateLastLogin: jest.fn(),
    } as any
    authService = new AuthService(mockUserRepository)
  })

  describe('login', () => {
    it('should return tokens when credentials are valid', async () => {
      const mockUser = {
        id: 'user-123',
        email: 'user-000002@account.example.invalid',
        passwordHash: await hashPassword('ValidPassword123!'),
      }
      mockUserRepository.findByEmail.mockResolvedValue(mockUser)

      const result = await authService.login('user-000002@account.example.invalid', 'ValidPassword123!')

      expect(result.success).toBe(true)
      expect(result.data.accessToken).toBeDefined()
      expect(mockUserRepository.updateLastLogin).toHaveBeenCalledWith('user-123')
    })
  })
})
```
```

---

#### 3. Casos de Teste (E2E)

**O que incluir:**
- Lista de testes E2E (fluxos principais)
- Steps de cada teste
- Verificações (assertions)
- Exemplos de código Playwright

**Exemplo:**
```markdown
### Casos de Teste (E2E com Playwright)

#### 1. E2E: User logs in with valid credentials
**Steps:**
1. Navigate to `/login`
2. Fill email field: `user-000035@account.example.invalid`
3. Fill password field: `ValidPassword123!`
4. Click "Entrar" button
5. Wait for navigation to `/dashboard`

**Verifications:**
- ✅ URL changes to `/dashboard`
- ✅ Token saved in localStorage: `localStorage.getItem('accessToken')` exists
- ✅ User name displayed in header: "Test User"
- ✅ No error messages visible

**Code:**
```typescript
test('should allow user to login with valid credentials', async ({ page }) => {
  await page.goto('/login')
  await page.fill('input[name="email"]', 'user-000035@account.example.invalid')
  await page.fill('input[name="password"]', 'ValidPassword123!')
  await page.click('button[type="submit"]')

  await expect(page).toHaveURL('/dashboard')

  const token = await page.evaluate(() => localStorage.getItem('accessToken'))
  expect(token).toBeTruthy()

  await expect(page.locator('[data-testid="user-name"]')).toContainText('Test User')
})
```
```

---

#### 4. Edge Cases e Cenários de Erro

**O que incluir:**
- Lista de edge cases a testar
- Lista de cenários de erro
- Como testar cada cenário

**Exemplo:**
```markdown
### Edge Cases e Cenários de Erro

**Lista de edge cases:**
1. ✅ Email com caracteres especiais válidos (ex: `user-000036@account.example.invalid`)
2. ✅ Senha com todos os tipos de caracteres especiais permitidos
3. ✅ Email com domínio internacional (IDN): `test@münchen.de`
4. ✅ Múltiplas tentativas de login falhadas (rate limiting ativa)
5. ✅ Login simultâneo de múltiplos dispositivos (tokens únicos)
6. ✅ Token expira durante navegação (refresh automático)
7. ✅ Conexão de rede perdida durante login
8. ✅ Request timeout (servidor lento >30s)
9. ✅ Browser sem suporte a localStorage (graceful degradation)
10. ✅ JavaScript desabilitado (mensagem de aviso)

**Lista de cenários de erro:**
1. ✅ Servidor retorna 500 (Internal Server Error)
2. ✅ Servidor retorna 503 (Service Unavailable)
3. ✅ Request timeout (>30s sem resposta)
4. ✅ Network error (sem conexão à internet)
5. ✅ CORS error (configuração incorreta no servidor)
6. ✅ JSON malformado na resposta do servidor
7. ✅ Token expirado no meio da sessão ativa
8. ✅ Banco de dados indisponível (fallback ou mensagem de erro)

**Como testar:**
- Edge cases: Testes E2E com dados reais
- Cenários de erro: Mock de responses (Playwright `page.route()`)

**Exemplo de mock de erro:**
```typescript
test('should show error when server returns 500', async ({ page }) => {
  // Mock API to return 500
  await page.route('**/api/auth/login', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Internal Server Error' })
    })
  })

  await page.goto('/login')
  await page.fill('input[name="email"]', 'user-000002@account.example.invalid')
  await page.fill('input[name="password"]', 'password')
  await page.click('button[type="submit"]')

  await expect(page.locator('[role="alert"]')).toContainText('Erro no servidor')
})
```
```

---

#### 5. Testes de Performance

**O que incluir:**
- Requisitos de performance
- Ferramentas de teste de performance
- Métricas a medir
- Cenários de load testing

**Exemplo:**
```markdown
### Testes de Performance

**Requisitos:**
- Tempo de resposta API `/api/auth/login`: <200ms (95th percentile)
- Tempo de carregamento inicial `/login`: <1s (LCP)
- Time to Interactive (TTI): <2s

**Ferramentas:**
- **Frontend**: Lighthouse CI (métricas Core Web Vitals)
- **Backend**: Artillery ou k6 (load testing de API)

**Métricas a medir:**
- **LCP (Largest Contentful Paint)**: <1s
- **FID (First Input Delay)**: <100ms
- **CLS (Cumulative Layout Shift)**: <0.1
- **API Response Time**: p50 <100ms, p95 <200ms, p99 <500ms
- **Throughput**: Suportar 100 requests/segundo

**Cenários de load testing:**
1. **Baseline**: 10 usuários simultâneos por 1 minuto
2. **Normal load**: 100 usuários simultâneos por 5 minutos
3. **Peak load**: 500 usuários simultâneos por 1 minuto
4. **Stress test**: Aumentar gradualmente até encontrar ponto de falha

**Exemplo de config Artillery:**
```yaml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10  # 10 users/sec
      name: "Warm up"
    - duration: 300
      arrivalRate: 100 # 100 users/sec
      name: "Normal load"

scenarios:
  - name: "Login flow"
    flow:
      - post:
          url: "/api/auth/login"
          json:
            email: "user-000002@account.example.invalid"
            password: "password123"
```
```

---

### Checklist do QA

- [ ] Estratégia de testes definida (pirâmide, frameworks, meta de cobertura)
- [ ] Casos de teste unitários listados por módulo
- [ ] Casos de teste E2E listados com steps e verificações
- [ ] Edge cases identificados (mínimo 5)
- [ ] Cenários de erro identificados (mínimo 5)
- [ ] Testes de performance especificados (requisitos + ferramentas)
- [ ] Exemplos de código de teste fornecidos

---

## 📊 Gerente de Projeto

### Foco
Priorização, riscos, estimativas, critérios de aceitação, dependências

### Responsabilidade
Gerenciar aspectos de planejamento e execução da feature (prioridade, riscos, estimativas).

### Perguntas que o PM responde

1. **Qual a prioridade desta feature?**
   - High, Medium ou Low?
   - Por quê?
   - Bloqueia outras features?

2. **Quais são os riscos potenciais?**
   - Riscos técnicos, de negócio, de prazo?
   - Probabilidade e impacto?
   - Como mitigar?

3. **Qual a estimativa de complexidade e tempo?**
   - Complexidade (Baixa, Média, Alta)?
   - Estimativa de tempo (dias, semanas)?
   - Fatores que afetam estimativa?

4. **Quais são os critérios de aceitação?**
   - Quando a feature está completa?
   - O que deve ser testado?
   - Quem aprova?

5. **Há dependências críticas?**
   - Dependências internas (outras features)?
   - Dependências externas (serviços, APIs)?
   - Bloqueadores?

---

### Análise a Gerar

#### 1. Prioridade da Feature

**O que incluir:**
- Prioridade (High/Medium/Low)
- Justificativa clara
- Contexto de por que esta prioridade

**Exemplo:**
```markdown
### Prioridade da Feature

**Prioridade:** High

**Justificativa:**
- **Bloqueador para outras features**: Dashboard, Profile, Settings dependem de autenticação
- **Funcionalidade core**: Aplicação não pode funcionar sem login
- **Impacto em segurança**: Proteção de dados sensíveis é crítica
- **Expectativa do usuário**: Autenticação é esperada em qualquer aplicação moderna

**Contexto:**
Sem autenticação, todas as outras features planejadas para a fase 2 (Dashboard, Perfil de Usuário, Configurações) não podem ser implementadas. Esta é a feature fundamental que desbloqueia o roadmap.
```

---

#### 2. Riscos Potenciais

**O que incluir:**
- Lista de riscos (mínimo 3)
- Probabilidade (Alta, Média, Baixa)
- Impacto (Alto, Médio, Baixo)
- Descrição do risco
- Estratégias de mitigação

**Formato:**
```markdown
### Riscos Potenciais

#### Risco 1: [Nome do Risco]
- **Probabilidade:** [Alta / Média / Baixa]
- **Impacto:** [Alto / Médio / Baixo]
- **Descrição:** [Descrição detalhada do risco]
- **Mitigação:**
  - [Estratégia 1]
  - [Estratégia 2]
  - [Estratégia 3]
```

**Exemplo:**
```markdown
#### Risco 1: JWT Secret Comprometido
- **Probabilidade:** Baixa
- **Impacto:** Crítico
- **Descrição:** Se o JWT secret vazar (commit acidental no Git, log de erro, etc.), atacantes podem gerar tokens válidos e se passar por qualquer usuário
- **Mitigação:**
  - Usar secrets fortes (>32 chars, gerados com `openssl rand -base64 32`)
  - Nunca commitar secrets no Git (`.env` no `.gitignore`)
  - Rotacionar secrets periodicamente (a cada 6 meses)
  - Usar secrets diferentes para access e refresh tokens
  - Implementar token blacklist para invalidar tokens comprometidos
  - Monitoramento de tentativas de acesso suspeitas

#### Risco 2: Ataque de Brute Force
- **Probabilidade:** Alta
- **Impacto:** Médio
- **Descrição:** Atacantes tentam adivinhar senhas de usuários através de múltiplas tentativas automatizadas
- **Mitigação:**
  - Rate limiting: max 5 tentativas por IP em 15 minutos
  - Captcha após 3 tentativas falhadas
  - Account lockout temporário após 10 tentativas (desbloqueia após 1 hora)
  - Monitoramento de IPs suspeitos (múltiplos logins falhados)
  - Alertar usuário via email após múltiplas tentativas falhadas

#### Risco 3: Sessões Não Expiram Corretamente
- **Probabilidade:** Média
- **Impacto:** Médio
- **Descrição:** Refresh tokens não são invalidados no logout ou quando expiram, permitindo acesso não autorizado
- **Mitigação:**
  - Armazenar refresh tokens no DB (tabela `refresh_tokens`)
  - Marcar token como `revoked=true` no logout
  - Cronjob diário para limpar tokens expirados
  - Validar no backend se token não está revoked
  - Implementar refresh token rotation (novo token a cada refresh)
```

---

#### 3. Estimativa de Complexidade e Tempo

**O que incluir:**
- Complexidade (Baixa, Média, Alta) com justificativa
- Estimativa de tempo por etapa
- Total de tempo
- Fatores que afetam estimativa

**Exemplo:**
```markdown
### Estimativa de Complexidade e Tempo

**Complexidade:** Média

**Critérios:**
- Tasks: 87 (31-70 = Média complexidade)
- Integrações externas: 0 (apenas bibliotecas npm, sem APIs externas)
- Stack: Conhecida (Next.js + TypeScript)
- Incerteza técnica: Baixa (JWT é padrão bem estabelecido)

**Breakdown de tempo:**
- **Backend (AuthService, APIs, DB)**: 2 dias
  - Setup (Prisma, migrations): 0,5 dia
  - Services e Repositories: 1 dia
  - API routes: 0,5 dia
- **Frontend (LoginForm, AuthContext, UI)**: 2 dias
  - UI components (Button, Input, Card): 0,5 dia
  - LoginForm + validação: 0,5 dia
  - AuthContext e integração: 0,5 dia
  - Páginas e routing: 0,5 dia
- **Testes (Unit + Integration + E2E)**: 1,5 dias
  - Unit tests: 0,5 dia
  - Integration tests: 0,5 dia
  - E2E tests: 0,5 dia
- **Code Review + Ajustes**: 0,5 dias
- **Total**: **6 dias** (assumindo 1 desenvolvedor full-time)

**Fatores que podem afetar:**
- ⬆️ **Aumentar estimativa**:
  - Desenvolvedor júnior sem experiência com JWT: +1-2 dias
  - Problemas inesperados com Prisma/DB: +0,5-1 dia
  - Requisitos de segurança adicionais descobertos: +0,5 dia
- ⬇️ **Reduzir estimativa**:
  - Desenvolvedor sênior com experiência em Next.js + Auth: -1 dia
  - Reutilização de componentes UI existentes: -0,5 dia
  - Sem necessidade de E2E (apenas unit tests): -0,5 dia

**Notas:**
- Estimativas baseadas em tasks granulares geradas (87 tasks)
- Assume trabalho focado sem interrupções
- Inclui tempo para testes e code review
- NÃO inclui tempo para design/UX (assumido como já definido)
```

---

#### 4. Critérios de Aceitação

**O que incluir:**
- Critérios funcionais
- Critérios de qualidade
- Critérios não-funcionais
- Aprovações necessárias

**Formato:**
```markdown
### Critérios de Aceitação

**A feature será considerada completa quando:**

**1. ✅ Funcional:**
- [ ] Usuário pode fazer login com email e senha válidos
- [ ] Usuário recebe tokens JWT (access + refresh)
- [ ] Usuário é redirecionado para `/dashboard` após login
- [ ] Usuário pode fazer logout e tokens são invalidados
- [ ] [... todos os requisitos funcionais ...]

**2. ✅ Qualidade:**
- [ ] Cobertura de testes unitários >90%
- [ ] Todos os 15 testes E2E passando
- [ ] Sem erros críticos ou bloqueadores
- [ ] Performance: API `/api/auth/login` <200ms (95th percentile)

**3. ✅ Segurança:**
- [ ] Senhas armazenadas com bcrypt (custo 12)
- [ ] JWT assinado com RS256
- [ ] Secrets fortes (>32 chars)
- [ ] Rate limiting implementado (5 tentativas / 15min)

**4. ✅ Não-Funcional:**
- [ ] Código segue ESLint/Prettier
- [ ] Acessibilidade WCAG 2.1 Level AA
- [ ] Responsivo (mobile, tablet, desktop)
- [ ] Documentação: README atualizado, JSDoc nos métodos principais

**5. ✅ Aprovação:**
- [ ] Code review aprovado por 2 reviewers
- [ ] QA testou manualmente e aprovou
- [ ] Security review aprovado (verificação de secrets, bcrypt, JWT)
- [ ] Product Owner aprovou UI/UX (se aplicável)
```

---

#### 5. Dependências Críticas

**O que incluir:**
- Dependências internas (features)
- Dependências externas (serviços, APIs)
- Bloqueadores
- Status de cada dependência

**Exemplo:**
```markdown
### Dependências Críticas

**Dependências internas:**
- Nenhuma (feature base, outras dependem dela)

**Dependências externas:**
- ✅ PostgreSQL configurado (DATABASE_URL disponível)
- ✅ Prisma CLI instalado (npx prisma)
- ✅ Node.js >=18.0.0

**Bloqueadores:**
- Nenhum

**Notas:**
- Esta feature é um pré-requisito para FEAT-006 (Dashboard), FEAT-007 (Profile)
- Não bloqueia features de landing page ou marketing (públicas)
```

---

### Checklist do Gerente de Projeto

- [ ] Prioridade definida (High/Medium/Low) com justificativa
- [ ] Pelo menos 3 riscos identificados com mitigações
- [ ] Estimativa de complexidade e tempo detalhada
- [ ] Critérios de aceitação claros e testáveis
- [ ] Dependências mapeadas (internas e externas)
- [ ] Bloqueadores identificados (ou "Nenhum")

---

## 💼 Business Analyst

### Foco
Valor de negócio, KPIs, impacto no usuário, ROI

### Responsabilidade
Conectar a feature técnica aos objetivos de negócio, garantindo que entrega valor mensurável.

### Perguntas que o BA responde

1. **Qual o valor de negócio desta feature?**
   - Que problema de negócio resolve?
   - Quais benefícios traz?
   - Como alinha com estratégia da empresa?

2. **Que KPIs medir para avaliar sucesso?**
   - Quais métricas acompanhar?
   - Baseline atual vs meta pós-feature?
   - Como coletar dados?

3. **Qual o impacto nos usuários?**
   - Quais personas afetadas?
   - Impacto positivo, neutro ou negativo?
   - Mudanças na jornada do usuário?

4. **Qual o ROI esperado?**
   - Investimento (custo de desenvolvimento)?
   - Retorno esperado (receita, economia)?
   - Break-even point?

---

### Análise a Gerar

#### 1. Valor de Negócio

**O que incluir:**
- Problema de negócio que resolve
- Benefícios esperados (mínimo 3)
- Quantificação quando possível

**Exemplo:**
```markdown
### Valor de Negócio

**Problema que resolve:**
Atualmente, a aplicação não tem sistema de autenticação. Qualquer pessoa pode acessar todas as páginas, incluindo dashboards com dados sensíveis. Isso impede:
- Personalização da experiência do usuário
- Controle de acesso a funcionalidades premium
- Tracking de ações por usuário
- Proteção de dados privados
- Compliance com LGPD/GDPR

**Benefícios esperados:**

1. **Segurança e Compliance (+valor legal)**:
   - Proteger dados sensíveis de usuários (LGPD Art. 46)
   - Evitar multas (até 2% do faturamento ou R$ <USER_AMOUNT>ilhões)
   - Garantir controle de acesso a funcionalidades administrativas

2. **Personalização e Engajamento (+30% retention)**:
   - Mostrar conteúdo relevante para cada usuário
   - Salvar preferências e histórico
   - Aumentar tempo de sessão (benchmark: +25% com personalização)

3. **Monetização (+receita recorrente)**:
   - Habilitar modelo freemium (free + premium features)
   - Controlar acesso a funcionalidades pagas
   - Tracking de conversão free → paid

4. **Insights e Analytics (+dados)**:
   - Rastrear comportamento de usuários específicos
   - Medir funil de conversão
   - A/B testing personalizado

**Quantificação:**
- Baseline: Taxa de conversão para premium ~5% (sem dados individuais, difícil otimizar)
- Pós-feature: Taxa de conversão estimada ~12% (com tracking e personalização)
- **Ganho estimado**: +7% conversão = +140 usuários premium/mês (assumindo 2000 usuários free)
```

---

#### 2. KPIs (Key Performance Indicators)

**O que incluir:**
- 3-5 KPIs principais
- Métrica exata
- Baseline atual
- Meta pós-feature
- Prazo para medir
- Ferramentas de tracking

**Formato:**
```markdown
### KPIs (Key Performance Indicators)

#### 1. [Nome do KPI]
- **Métrica**: [O que medir exatamente]
- **Baseline atual**: [Valor antes da feature]
- **Meta pós-feature**: [Valor esperado após feature]
- **Prazo**: [Quando medir - ex: 30 dias após deploy]
- **Ferramenta**: [Como coletar dados]
```

**Exemplo:**
```markdown
#### 1. Taxa de Conversão de Registro para Login
- **Métrica**: % de usuários que se registram e fazem login pela primeira vez
- **Baseline**: N/A (feature nova)
- **Meta**: 85% (benchmark da indústria)
- **Prazo**: 30 dias após deploy
- **Ferramenta**: Google Analytics (evento "registration_complete" → "first_login")

#### 2. Tempo Médio de Login
- **Métrica**: Tempo desde clicar "Entrar" até redirecionar para dashboard
- **Baseline**: N/A
- **Meta**: <2 segundos (95th percentile)
- **Prazo**: Desde o deploy (monitoramento contínuo)
- **Ferramenta**: Datadog RUM (Real User Monitoring)

#### 3. Taxa de Sucesso de Login
- **Métrica**: % de tentativas de login que são bem-sucedidas (não retornam 401)
- **Baseline**: N/A
- **Meta**: >80% (indica que usuários lembram suas senhas)
- **Prazo**: 60 dias após deploy
- **Ferramenta**: Backend logs + Mixpanel (evento "login_attempt" → "login_success/failure")

#### 4. Sessões Ativas (7 dias)
- **Métrica**: % de usuários que permanecem logados por 7 dias (token não expira)
- **Baseline**: N/A
- **Meta**: >60%
- **Prazo**: 30 dias após deploy
- **Ferramenta**: Backend analytics (JWT refresh rate)

#### 5. Conversão Free → Premium (pós-auth)
- **Métrica**: % de usuários free que convertem para premium após 30 dias
- **Baseline**: ~5% (sem personalização)
- **Meta**: 12%
- **Prazo**: 90 dias após deploy
- **Ferramenta**: Stripe + Mixpanel (cohorte de usuários registrados)
```

---

#### 3. Impacto no Usuário

**O que incluir:**
- Personas afetadas (mínimo 2)
- Como afeta cada persona
- Sentimento esperado (positivo/neutro/negativo)
- Jornada do usuário - Antes vs Depois

**Exemplo:**
```markdown
### Impacto no Usuário

**Personas afetadas:**

#### 1. Maria, 28, usuária frequente
- **Como afeta**: Pode salvar preferências, acessar histórico de compras, receber recomendações personalizadas
- **Sentimento**: **Muito positivo**
  - Mais conveniente (não precisa re-preencher dados)
  - Experiência personalizada aumenta satisfação
  - Sensação de segurança (dados protegidos por login)

#### 2. João, 45, novo usuário
- **Como afeta**: Precisa criar conta e fazer login antes de acessar funcionalidades principais
- **Sentimento**: **Neutro/Leve fricção**
  - Um passo a mais no onboarding
  - Compreende a necessidade (expectativa padrão em apps)
  - Compensado por benefícios de personalização

#### 3. Admin, 35, gestor de conteúdo
- **Como afeta**: Pode controlar quem acessa áreas administrativas, auditar ações de usuários
- **Sentimento**: **Muito positivo**
  - Maior controle e segurança
  - Auditabilidade de ações
  - Conformidade com políticas de segurança

**Jornada do usuário - Antes vs Depois:**

**ANTES (sem autenticação):**
1. Usuário acessa site
2. Vê todo conteúdo (incluindo dados que deveriam ser privados)
3. Não tem personalização
4. Não há tracking de ações
5. Sai do site
- **Fricção**: Baixa
- **Valor agregado**: Baixo (sem personalização, sem segurança)

**DEPOIS (com autenticação):**
1. Usuário acessa site
2. Vê landing page pública
3. Clica "Entrar" ou "Criar conta"
4. Faz login em ~15 segundos (processo rápido)
5. Vê dashboard personalizado com seus dados
6. Sessão persiste por 7 dias (não precisa login novamente)
7. Ações são rastreadas para melhorias
- **Fricção**: Leve (login inicial de 15s)
- **Valor agregado**: Alto (personalização, segurança, conveniência)

**Resumo:** +15s de fricção inicial compensados por experiência significativamente melhor.
```

---

#### 4. ROI (Return on Investment)

**O que incluir:**
- Investimento (custo de desenvolvimento)
- Retorno esperado (receita ou economia)
- Cálculo de break-even
- ROI em 12 meses
- Benefícios não-monetários

**Exemplo:**
```markdown
### ROI (Return on Investment)

**Investimento:**
- Custo de desenvolvimento: 6 dias × $500/dia (desenvolvedor) = $3,000
- Custo de design/UX: 1 dia × $400/dia (designer) = $400
- Custo de QA/testes: 1 dia × $350/dia (QA) = $350
- **Total de investimento**: **$3,750**

**Retorno esperado:**

**Cálculo conservador:**
- Baseline: 2000 usuários free/mês
- Sem auth: Conversão para premium ~5% = 100 usuários pagantes
- Com auth + personalização: Conversão ~12% = 240 usuários pagantes
- **Ganho**: +140 usuários pagantes/mês
- Ticket médio: $20/mês
- **Receita adicional/mês**: 140 × $20 = **$2,800**
- **Receita adicional/ano**: $2,800 × 12 = **$33,600**

**Break-even:**
- Investimento: $3,750
- Receita adicional/mês: $2,800
- **Meses para break-even**: $3,750 / $2,800 = **1,34 meses** (~40 dias)

**ROI em 12 meses:**
- ROI = (Receita adicional - Investimento) / Investimento × 100
- ROI = ($33,600 - $3,750) / $3,750 × 100
- **ROI = 796%**

**Benefícios não-monetários:**
- **Compliance**: Evita multas LGPD (até R$ <USER_AMOUNT> ou 2% do faturamento)
- **Segurança**: Reduz risco de breach de dados (custo médio de $4.35M segundo IBM)
- **Brand**: Melhora percepção de profissionalismo e segurança
- **Analytics**: Dados de usuários individuais permitem otimização contínua (+10-15% lifetime value)

**Cenário pessimista (se conversão aumentar apenas 2%):**
- Ganho: +40 usuários pagantes/mês
- Receita adicional/mês: $800
- Break-even: 4,7 meses
- ROI em 12 meses: 156%
- **Ainda assim positivo e justificável**
```

---

#### 5. Alinhamento com Objetivos de Negócio

**O que incluir:**
- Objetivo estratégico da empresa
- Como a feature contribui
- Prioridade estratégica
- Alternativas consideradas

**Exemplo:**
```markdown
### Alinhamento com Objetivos de Negócio

**Objetivo estratégico da empresa (2024):**
"Crescer base de usuários pagantes em 50% e atingir $1M ARR"

**Como esta feature contribui:**
- **Direto**: Aumenta conversão free → premium de 5% para 12% (+7% = +140 usuários pagantes/mês)
- **Indireto**: Habilita tracking para otimizar funil de conversão (+10-15% adicional em 6 meses)
- **Habilitador**: Pré-requisito para features premium planejadas (Dashboard, Analytics, Exports)
- **Personalização**: Aumenta retention em +30% (benchmark), reduzindo churn

**Impacto projetado no objetivo:**
- Baseline: 1200 usuários pagantes
- Meta: 1800 usuários pagantes (+50%)
- Contribuição desta feature: +140/mês × 12 = +1680/ano
- **Contribuição para meta**: ~93% do crescimento necessário

**Prioridade estratégica:** **Máxima (P0)**

Esta é a feature mais importante do roadmap Q1 pois:
1. Desbloqueia 80% das features planejadas para Q2-Q3
2. Contribui diretamente para KPI principal da empresa
3. Reduz riscos legais (compliance LGPD)

**Alternativas consideradas:**

1. **OAuth-only (Google, GitHub login)**:
   - Prós: Implementação mais rápida (3 dias vs 6 dias)
   - Contras: Dependência de terceiros, não funciona para usuários corporativos com SSO restrito
   - Decisão: Descartado - queremos controle total de identidades

2. **Session-based auth (cookies)**:
   - Prós: Mais simples, padrão antigo conhecido
   - Contras: Dificulta scaling horizontal, não funciona bem com API para mobile
   - Decisão: Descartado - preferimos stateless JWT para escalar

**Decisão final:**
Implementar autenticação JWT com email/senha é a melhor opção porque:
- Alinha perfeitamente com objetivo de crescimento
- Oferece controle total e segurança
- Escalável para futuro (API mobile)
- ROI altíssimo (796% em 12 meses)
```

---

### Checklist do Business Analyst

- [ ] Valor de negócio claramente articulado
- [ ] 3-5 KPIs definidos com baseline e metas
- [ ] Impacto em pelo menos 2 personas descrito
- [ ] Jornada do usuário (Antes vs Depois) documentada
- [ ] ROI calculado com break-even e projeção 12 meses
- [ ] Alinhamento com objetivos estratégicos demonstrado
- [ ] Alternativas consideradas e descartadas explicadas

---

## Resumo

Cada persona contribui com uma perspectiva única:

| Persona | Foco Principal | Output Principal |
|---------|----------------|-------------------|
| 🏗️ Arquiteto | Estrutura técnica, arquitetura | Estrutura de diretórios, dependências, padrões |
| 💻 Desenvolvedor | Implementação prática | Componentes, APIs, código, variáveis de ambiente |
| 🎨 Designer/UX | Interface e experiência | Wireframes, componentes UI, acessibilidade, responsividade |
| ✅ QA | Qualidade e testes | Estratégia de testes, casos de teste, edge cases |
| 📊 PM | Planejamento e execução | Prioridade, riscos, estimativas, critérios de aceitação |
| 💼 BA | Valor de negócio | KPIs, ROI, impacto no usuário, alinhamento estratégico |

**Juntas**, as 6 personas garantem que a feature seja:
- Tecnicamente sólida (Arquiteto + Desenvolvedor)
- Usável e acessível (Designer/UX)
- Bem testada e de qualidade (QA)
- Entregue no prazo e sem riscos (PM)
- Alinhada com objetivos de negócio (BA)

---

**Criado por:** sprint-context-generator skill
**Versão:** 1.0.0
**Última atualização:** 2026-01-13
