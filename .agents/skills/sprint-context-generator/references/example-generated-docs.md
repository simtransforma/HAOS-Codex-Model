# Exemplo Completo: FEAT-005 - Sistema de Autenticação JWT

Este arquivo demonstra o **nível de detalhe esperado** quando a skill `sprint-context-generator` gera documentação completa para uma feature.

**Feature exemplo:** Sistema de Autenticação JWT
**ID:** FEAT-005
**Categoria:** Authentication
**Prioridade:** High
**Status:** Pending
**Total de tasks:** 87 tasks
**Complexidade:** Média
**Tempo estimado:** 4-6 dias

---

## Arquivos Gerados

Localização: `<USER_DEPENDENCY:docs/context-log-running/sistema-autenticacao-jwt/>`

1. spec.md (~1200 linhas)
2. plan.md (~800 linhas)
3. tasks.md (~650 linhas, 87 tasks)
4. research.md (~500 linhas)
5. features.xml (~30 linhas)

---

# 1. SPEC.MD (Exemplo Completo)

```markdown
# FEAT-005: Sistema de Autenticação JWT

📂 **Documentação Relacionada:**
- Plano Técnico (user-supplied dependency; see PORTABILITY.md) - Arquitetura e decisões técnicas
- Lista de Tasks (user-supplied dependency; see PORTABILITY.md) - Tarefas detalhadas (87 tasks)
- Pesquisa (user-supplied dependency; see PORTABILITY.md) - Documentação e referências

---

## Visão Geral

Implementar sistema de autenticação completo usando JSON Web Tokens (JWT) com refresh tokens para sessões persistentes e seguras. O sistema permitirá que usuários façam login com email e senha, mantenham sessões ativas por 7 dias sem precisar fazer login novamente, e tenham seus tokens renovados automaticamente quando expirarem.

**Categoria:** Authentication
**Prioridade:** High
**Status:** Pending

---

## User Stories

1. Como usuário, quero fazer login com email e senha, para acessar minha conta de forma segura
2. Como usuário, quero que minha sessão persista por 7 dias, para não precisar fazer login toda vez
3. Como usuário, quero que meu token seja renovado automaticamente, para não ser deslogado abruptamente
4. Como desenvolvedor, quero tokens JWT assinados com RS256, para garantir segurança máxima
5. Como admin, quero poder invalidar tokens de usuários específicos, para controlar acesso

---

## 🏗️ Análise do Arquiteto de Soluções

### Estrutura de Diretórios Proposta

Baseado em Clean Architecture e melhores práticas de Next.js + TypeScript:

```
src/
├── app/                          # Next.js 13+ App Router
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx          # Página de login
│   │   └── register/
│   │       └── page.tsx          # Página de registro
│   ├── (protected)/
│   │   ├── dashboard/
│   │   │   └── page.tsx          # Dashboard protegido
│   │   └── layout.tsx            # Layout com verificação de auth
│   └── api/
│       └── auth/
│           ├── login/
│           │   └── route.ts      # POST /api/auth/login
│           ├── logout/
│           │   └── route.ts      # POST /api/auth/logout
│           └── refresh/
│               └── route.ts      # POST /api/auth/refresh
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx         # Formulário de login
│   │   └── RegisterForm.tsx      # Formulário de registro
│   └── ui/
│       ├── Button.tsx            # Componente button reutilizável
│       └── Input.tsx             # Componente input reutilizável
├── contexts/
│   └── AuthContext.tsx           # Context API para estado de auth
├── lib/
│   ├── auth/
│   │   ├── jwt.ts                # Geração e validação de JWT
│   │   ├── password.ts           # Hash e verificação de senha
│   │   └── tokens.ts             # Gerenciamento de refresh tokens
│   ├── db/
│   │   └── prisma.ts             # Cliente Prisma
│   └── errors/
│       └── AuthError.ts          # Erros customizados de auth
├── repositories/
│   ├── interfaces/
│   │   └── IUserRepository.ts    # Interface do repository
│   └── UserRepository.ts         # Implementação com Prisma
├── services/
│   └── AuthService.ts            # Lógica de negócio de auth
└── types/
    └── auth.ts                   # Types TypeScript de auth

prisma/
├── schema.prisma                 # Schema do banco de dados
└── migrations/                   # Migrations do Prisma

.env.example                      # Variáveis de ambiente
```

**Justificativa:**
- **Separação de responsabilidades**: Cada camada tem responsabilidade única (UI, business, data)
- **Testabilidade**: Services e repositories isolados facilitam unit tests
- **Escalabilidade**: Estrutura suporta crescimento do projeto
- **Next.js App Router**: Aproveita recursos modernos (Server Components, etc.)

### Dependências Necessárias

**Produção:**
```json
{
  "jsonwebtoken": "^9.0.2",         // Geração e validação de JWT
  "bcrypt": "^5.1.1",               // Hash de senhas
  "@prisma/client": "^5.7.0",       // ORM para PostgreSQL
  "zod": "^3.22.4",                 // Validação de schemas
  "jose": "^5.1.3"                  // JWT helpers modernos para Next.js
}
```

**Desenvolvimento:**
```json
{
  "prisma": "^5.7.0",               // CLI do Prisma
  "@types/jsonwebtoken": "^9.0.5",  // Types para JWT
  "@types/bcrypt": "^5.0.2",        // Types para bcrypt
  "typescript": "^5.3.3",           // TypeScript
  "eslint": "^8.56.0",              // Linting
  "prettier": "^3.1.1"              // Formatação
}
```

### Refatorações Necessárias

**Não aplicável**: Projeto novo, sem código legado para refatorar.

Se fosse projeto existente:
- **Módulo de Auth atual**: Migrar de sessões server-side para JWT
- **Componentes de formulário**: Extrair lógica de validação para hooks reutilizáveis

### Padrões de Arquitetura

**Padrão escolhido:** Clean Architecture + Repository Pattern

**Camadas:**
1. **Presentation Layer (App Router + Components)**:
   - Responsabilidade: UI, formulários, interação com usuário
   - Depende de: Contexts, Services (via API routes)

2. **Application Layer (Services)**:
   - Responsabilidade: Lógica de negócio, orquestração
   - Depende de: Repositories, Libraries (JWT, password)

3. **Domain Layer (Types, Interfaces)**:
   - Responsabilidade: Modelos de domínio, contratos
   - Depende de: Nada (camada mais interna)

4. **Infrastructure Layer (Repositories, DB)**:
   - Responsabilidade: Acesso a dados, integrações externas
   - Depende de: Domain (interfaces)

**Fluxo de dados:**
```
User Request (Login Form)
    ↓
LoginForm Component (presentation)
    ↓
POST /api/auth/login (API route)
    ↓
AuthService.login(email, password) (application)
    ↓
UserRepository.findByEmail(email) (infrastructure)
    ↓
Prisma Client → PostgreSQL Database
    ↑
User Model (domain)
    ↑
JWT + User Data (response)
    ↑
LoginForm (update UI, redirect)
```

### Decisões de Escalabilidade

1. **JWT Stateless**: Tokens são stateless (não armazenados no servidor), permitindo horizontal scaling sem sessões compartilhadas
2. **Refresh Tokens em DB**: Refresh tokens são stored no DB para permitir revogação
3. **Redis para blacklist** (Fase 2): Adicionar Redis para cache de tokens revogados (melhora performance)
4. **Rate Limiting**: Implementar rate limiting no Nginx/Vercel Edge para prevenir brute force

---

## 💻 Requisitos do Desenvolvedor

### Componentes/Módulos a Criar

**Backend:**

#### 1. AuthService (`src/services/AuthService.ts`)
- **Responsabilidade**: Lógica de autenticação (login, logout, refresh)
- **Métodos principais**:
  - `login(email: string, password: string): Promise<{accessToken: string, refreshToken: string, user: User}>`
  - `logout(userId: string): Promise<void>`
  - `refreshAccessToken(refreshToken: string): Promise<{accessToken: string}>`
  - `validateAccessToken(token: string): Promise<User | null>`

#### 2. UserRepository (`src/repositories/UserRepository.ts`)
- **Responsabilidade**: Acesso a dados de usuários
- **Métodos principais**:
  - `findByEmail(email: string): Promise<User | null>`
  - `findById(id: string): Promise<User | null>`
  - `create(data: CreateUserDto): Promise<User>`
  - `updateLastLogin(userId: string): Promise<void>`

#### 3. JWTService (`src/lib/auth/jwt.ts`)
- **Responsabilidade**: Geração e validação de tokens JWT
- **Funções exportadas**:
  - `generateAccessToken(payload: TokenPayload): string` (expira em 15min)
  - `generateRefreshToken(payload: TokenPayload): string` (expira em 7d)
  - `verifyAccessToken(token: string): TokenPayload | null`
  - `verifyRefreshToken(token: string): TokenPayload | null`

#### 4. PasswordService (`src/lib/auth/password.ts`)
- **Responsabilidade**: Hash e verificação de senhas
- **Funções exportadas**:
  - `hashPassword(password: string): Promise<string>` (bcrypt, custo 12)
  - `comparePassword(password: string, hash: string): Promise<boolean>`

**Frontend:**

#### 5. LoginForm (`src/components/auth/LoginForm.tsx`)
- **Responsabilidade**: Formulário de login com validação
- **Props**: `{ onSuccess?: () => void, onError?: (error: string) => void }`
- **State**: `email, password, isLoading, errors`
- **Validação**: Zod schema (email válido, senha mínimo 8 chars)

#### 6. AuthContext (`src/contexts/AuthContext.tsx`)
- **Responsabilidade**: Gerenciar estado global de autenticação
- **Funções exportadas**:
  - `useAuth(): { user, login, logout, isAuthenticated, isLoading }`
  - `login(email, password): Promise<void>`
  - `logout(): Promise<void>`
  - `refreshToken(): Promise<void>`

### APIs a Implementar

**REST Endpoints:**

#### 1. POST /api/auth/login
**Descrição:** Autenticar usuário com email e senha, retornar JWT tokens

**Request:**
```typescript
// Body
{
  "email": "user-000013@account.example.invalid",
  "password": "secret_placeholder!"
}

// Headers
Content-Type: application/json
```

**Response (200 OK):**
```typescript
{
  "success": true,
  "data": {
    "accessToken": "secret_placeholder",
    "refreshToken": "secret_placeholder",
    "user": {
      "id": "uuid-here",
      "email": "user-000013@account.example.invalid",
      "name": "John Doe",
      "createdAt": "2024-01-15T10:00:00Z"
    }
  }
}
```

**Response (401 Unauthorized):**
```typescript
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Email ou senha incorretos"
  }
}
```

**Response (400 Bad Request):**
```typescript
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos",
    "details": [
      { "field": "email", "message": "Email inválido" }
    ]
  }
}
```

#### 2. POST /api/auth/logout
**Descrição:** Invalidar refresh token do usuário

**Request:**
```typescript
// Headers
Authorization: Bearer <access-token>
Content-Type: application/json
```

**Response (200 OK):**
```typescript
{
  "success": true,
  "message": "Logout realizado com sucesso"
}
```

#### 3. POST /api/auth/refresh
**Descrição:** Gerar novo access token usando refresh token

**Request:**
```typescript
// Body
{
  "refreshToken": "secret_placeholder"
}
```

**Response (200 OK):**
```typescript
{
  "success": true,
  "data": {
    "accessToken": "secret_placeholder"
  }
}
```

**Response (401 Unauthorized):**
```typescript
{
  "success": false,
  "error": {
    "code": "INVALID_REFRESH_TOKEN",
    "message": "Refresh token inválido ou expirado"
  }
}
```

### Padrões de Código (DRY, SOLID, etc.)

**DRY (Don't Repeat Yourself):**
- Extrair validação de email para `lib/validators/email.ts`
- Criar hook customizado `useFormValidation()` para reutilizar lógica de formulários
- Centralizar mensagens de erro em `lib/constants/error-messages.ts`

**SOLID:**
- **Single Responsibility**: AuthService só gerencia autenticação, não acessa DB diretamente
- **Dependency Inversion**: AuthService depende de IUserRepository (interface), não implementação concreta
- **Interface Segregation**: Interfaces pequenas e focadas (IUserRepository, IJWTService)

**Padrões específicos:**
- **DTOs (Data Transfer Objects)**: Usar DTOs para transferência entre camadas
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
  ```
- **Error Handling Centralizado**: Middleware de error handler para padronizar respostas
- **Constants**: Usar constants para valores mágicos
  ```typescript
  // src/lib/constants/auth.ts
  export const JWT_ACCESS_TOKEN_EXPIRY = '15m'
  export const JWT_REFRESH_TOKEN_EXPIRY = '7d'
  export const BCRYPT_SALT_ROUNDS = 12
  ```

### Variáveis de Ambiente

**Arquivo `.env.example`:**
```env
# Database
DATABASE_URL=secret_placeholderlocalhost:5432/myapp
DATABASE_URL_UNPOOLED=secret_placeholderlocalhost:5432/myapp # Para Prisma Migrate

# JWT
JWT_ACCESS_SECRET=your-access-token-secret-minimum-32-characters
JWT_REFRESH_SECRET=your-refresh-token-secret-minimum-32-characters
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# Environment
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:3000

# Next.js (gerado automaticamente)
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret-for-csrf
```

**Documentação no README:**
- `JWT_ACCESS_SECRET`: Gerar com `openssl rand -base64 32`
- `JWT_REFRESH_SECRET`: Gerar com `openssl rand -base64 32` (diferente do access)
- `DATABASE_URL`: String de conexão PostgreSQL (local: localhost:5432)
- **Produção (Vercel)**: Configurar em Settings → Environment Variables

---

## 🎨 Especificações de Design/UX

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
│  │   Não tem conta? Criar conta       │  │
│  │                                    │  │
│  └────────────────────────────────────┘  │
│                                          │
└──────────────────────────────────────────┘
```

**Layout:**
- Centralizado verticalmente e horizontalmente
- Card com sombra sutil (elevation-2)
- Max-width: 400px
- Padding: 2rem
- Border-radius: 8px

### Componentes UI Reutilizáveis

#### 1. Button (`src/components/ui/Button.tsx`)
**Variantes:**
- `primary`: Azul (#3B82F6), branco
- `secondary`: Cinza (#6B7280), branco
- `danger`: Vermelho (#EF4444), branco
- `ghost`: Transparente, texto colorido

**Tamanhos:**
- `small`: padding 0.5rem 1rem, font-size 14px
- `medium`: padding 0.75rem 1.5rem, font-size 16px (default)
- `large`: padding 1rem 2rem, font-size 18px

**Estados:**
- `normal`: Cor padrão
- `hover`: Cor mais escura (-10% lightness)
- `focus`: Ring azul (outline 2px)
- `disabled`: Opacidade 50%, cursor not-allowed
- `loading`: Spinner + texto "Carregando..."

**Exemplo de uso:**
```tsx
<Button variant="primary" size="medium" loading={isLoading}>
  Entrar
</Button>
```

#### 2. Input (`src/components/ui/Input.tsx`)
**Tipos:**
- `text`, `email`, `password`, `number`

**Estados:**
- `normal`: Borda cinza (#D1D5DB)
- `focus`: Borda azul (#3B82F6), ring azul
- `error`: Borda vermelha (#EF4444)
- `disabled`: Background cinza (#F3F4F6), cursor not-allowed

**Features:**
- Label (required/optional indicator)
- Helper text (abaixo do input)
- Error message (vermelho, ícone de alerta)
- Icon (start/end do input)

**Exemplo de uso:**
```tsx
<Input
  type="email"
  label="Email"
  placeholder="user-000037@account.example.invalid"
  error={errors.email}
  required
/>
```

### Acessibilidade (WCAG 2.1 Level AA)

**Requisitos obrigatórios:**

1. **Labels e ARIA:**
   - ✅ Todos os inputs têm `<label>` com `htmlFor` correto
   - ✅ Formulário tem `aria-label="Formulário de login"`
   - ✅ Botões têm texto descritivo

2. **Contraste de cores:**
   - ✅ Texto normal (#111827 em fundo #FFFFFF): Contraste 16.1:1 ✅
   - ✅ Botão primário (branco em #3B82F6): Contraste 4.5:1 ✅
   - ✅ Mensagem de erro (#DC2626 em fundo #FFFFFF): Contraste 7.9:1 ✅

3. **Navegação por teclado:**
   - ✅ Tab: Navega entre inputs e botão
   - ✅ Enter: Submete formulário
   - ✅ Escape: Limpa formulário (se houver erros)
   - ✅ Focus indicators visíveis (ring azul 2px)

4. **Screen readers:**
   - ✅ Mensagens de erro têm `role="alert"` (anunciadas automaticamente)
   - ✅ Estado de loading anunciado: `aria-live="polite"`
   - ✅ Campos obrigatórios têm `aria-required="true"`

**Implementação:**
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
      className="..."
    />
    {errors.email && (
      <p id="email-error" role="alert" className="text-red-600 text-sm mt-1">
        <span aria-hidden="true">⚠️</span> {errors.email}
      </p>
    )}
  </div>

  <button
    type="submit"
    disabled={isLoading}
    aria-busy={isLoading}
    className="..."
  >
    {isLoading ? (
      <>
        <span className="spinner" aria-hidden="true" />
        <span className="sr-only">Carregando...</span>
        Entrando...
      </>
    ) : (
      'Entrar'
    )}
  </button>
</form>
```

### Responsividade

**Breakpoints (Tailwind CSS):**
- `mobile`: 0-640px (sm)
- `tablet`: 641px-1024px (md/lg)
- `desktop`: 1025px+ (xl)

**Adaptações por device:**

**Mobile (0-640px):**
- Layout: Coluna única, full-width
- Card de login: Width 100%, padding reduzido (1rem)
- Botões: Full-width
- Font-size: 16px (evitar zoom automático no iOS)
- Espaçamento: Reduzido (gap-3 ao invés de gap-6)

**Tablet (641px-1024px):**
- Card de login: Max-width 400px, centralizado
- Botões: Width auto (padding lateral)
- Font-size: 16px
- Espaçamento: Normal (gap-4)

**Desktop (1025px+):**
- Card de login: Max-width 420px, centralizado
- Botões: Width auto
- Font-size: 16px
- Espaçamento: Generoso (gap-6)
- Hover effects ativos

**Implementação (Tailwind CSS):**
```tsx
<div className="min-h-screen flex items-center justify-center p-4 sm:p-6 lg:p-8">
  <div className="w-full max-w-md sm:max-w-lg lg:max-w-xl bg-white rounded-lg shadow-lg p-6 sm:p-8">
    {/* Formulário */}
  </div>
</div>

<button className="w-full sm:w-auto px-6 py-3">
  Entrar
</button>
```

### Jornada do Usuário (User Flow)

**Fluxo de Login (Happy Path):**
1. Usuário acessa `/login`
2. Vê formulário de login (campos vazios, botão ativo)
3. Preenche email: `user-000013@account.example.invalid`
4. Preenche senha: `SecurePassword123!`
5. Clica botão "Entrar"
6. **Loading state**: Botão mostra spinner, fica disabled
7. **Request success**: API retorna 200 OK com tokens
8. Tokens salvos no localStorage/cookies
9. AuthContext atualiza (user, isAuthenticated = true)
10. Redirecionamento para `/dashboard`
11. Dashboard mostra nome do usuário: "Bem-vindo, John Doe!"

**Fluxo de Login (Erro de Credenciais):**
1. Usuário acessa `/login`
2. Preenche email: `user-000013@account.example.invalid`
3. Preenche senha: `WrongPassword`
4. Clica botão "Entrar"
5. **Loading state**: Botão mostra spinner
6. **Request error**: API retorna 401 Unauthorized
7. **Error state**:
   - Mensagem de erro aparece: "Email ou senha incorretos"
   - Cor vermelha, ícone de alerta
   - Campo de senha é limpo
   - Foco retorna ao campo de email
   - Screen reader anuncia erro
8. Usuário corrige senha e tenta novamente

**Fluxo de Login (Validação Client-Side):**
1. Usuário preenche email: `invalid-email`
2. Preenche senha: `123` (muito curta)
3. Clica botão "Entrar"
4. **Validação client-side (Zod)**:
   - Email inválido: Mensagem "Email inválido" aparece
   - Senha curta: Mensagem "Senha deve ter no mínimo 8 caracteres"
5. **Request NÃO é enviado** (evita overhead no servidor)
6. Usuário corrige erros
7. Validação passa, request é enviado

---

## ✅ Requisitos de QA (Quality Assurance)

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
**Meta de cobertura:** >90%

**Frameworks:**
- **Unitários**: Jest (já configurado no Next.js)
- **Integração**: Jest + Supertest (para APIs)
- **E2E**: Playwright

### Casos de Teste (Unitários)

**AuthService.ts:**
1. `login()`:
   - ✅ Deve retornar accessToken e refreshToken com credenciais válidas
   - ✅ Deve atualizar lastLoginAt do usuário
   - ✅ Deve retornar erro com email inexistente
   - ✅ Deve retornar erro com senha incorreta
   - ✅ Deve retornar erro se usuário está inativo

2. `validateAccessToken()`:
   - ✅ Deve retornar user payload com token válido
   - ✅ Deve retornar null com token expirado
   - ✅ Deve retornar null com token malformado
   - ✅ Deve retornar null com assinatura inválida

3. `refreshAccessToken()`:
   - ✅ Deve gerar novo accessToken com refreshToken válido
   - ✅ Deve retornar erro com refreshToken expirado
   - ✅ Deve retornar erro com refreshToken inválido
   - ✅ Deve retornar erro se refreshToken foi revogado

**Exemplo de teste:**
```typescript
// src/services/__tests__/AuthService.spec.ts
import { AuthService } from '../AuthService'
import { UserRepository } from '@/repositories/UserRepository'
import { hashPassword } from '@/lib/auth/password'

jest.mock('@/repositories/UserRepository')

describe('AuthService', () => {
  let authService: AuthService
  let mockUserRepository: jest.Mocked<UserRepository>

  beforeEach(() => {
    mockUserRepository = new UserRepository() as jest.Mocked<UserRepository>
    authService = new AuthService(mockUserRepository)
  })

  describe('login', () => {
    it('should return tokens with valid credentials', async () => {
      const mockUser = {
        id: 'user-123',
        email: 'user-000002@account.example.invalid',
        passwordHash: await hashPassword('ValidPassword123!'),
        name: 'Test User',
        createdAt: new Date(),
      }

      mockUserRepository.findByEmail.mockResolvedValue(mockUser)
      mockUserRepository.updateLastLogin.mockResolvedValue(undefined)

      const result = await authService.login('user-000002@account.example.invalid', 'ValidPassword123!')

      expect(result.success).toBe(true)
      expect(result.data.accessToken).toBeDefined()
      expect(result.data.refreshToken).toBeDefined()
      expect(result.data.user.email).toBe('user-000002@account.example.invalid')
      expect(mockUserRepository.updateLastLogin).toHaveBeenCalledWith('user-123')
    })

    it('should return error with invalid credentials', async () => {
      mockUserRepository.findByEmail.mockResolvedValue(null)

      const result = await authService.login('user-000034@account.example.invalid', 'WrongPassword')

      expect(result.success).toBe(false)
      expect(result.error.code).toBe('INVALID_CREDENTIALS')
      expect(result.error.message).toBe('Email ou senha incorretos')
    })
  })
})
```

[... continuar para todos os 42 testes unitários ...]

### Casos de Teste (E2E com Playwright)

**Fluxos de Autenticação:**

#### 1. E2E: Login com credenciais válidas
**Steps:**
1. Navegar para `http://localhost:3000/login`
2. Preencher campo email: `user-000035@account.example.invalid`
3. Preencher campo senha: `ValidPassword123!`
4. Clicar botão "Entrar"
5. Aguardar navegação

**Verificações:**
- ✅ URL muda para `/dashboard`
- ✅ Token salvo no localStorage: `localStorage.getItem('accessToken')` existe
- ✅ Header mostra nome do usuário: "Test User"
- ✅ Não há mensagens de erro visíveis

**Código:**
```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('should allow user to login with valid credentials', async ({ page }) => {
    // Navigate to login page
    await page.goto('/login')

    // Fill in the form
    await page.fill('input[name="email"]', 'user-000035@account.example.invalid')
    await page.fill('input[name="password"]', 'ValidPassword123!')

    // Submit
    await page.click('button[type="submit"]')

    // Wait for navigation to dashboard
    await expect(page).toHaveURL('/dashboard')

    // Verify token is saved
    const token = await page.evaluate(() => localStorage.getItem('accessToken'))
    expect(token).toBeTruthy()

    // Verify user name is displayed
    await expect(page.locator('[data-testid="user-name"]')).toContainText('Test User')
  })
})
```

#### 2. E2E: Login com credenciais inválidas
**Steps:**
1. Navegar para `/login`
2. Preencher email: `user-000035@account.example.invalid`
3. Preencher senha: `WrongPassword`
4. Clicar "Entrar"
5. Aguardar resposta do servidor

**Verificações:**
- ✅ Permanece em `/login` (não redireciona)
- ✅ Mensagem de erro aparece: "Email ou senha incorretos"
- ✅ Campo senha é limpo (value vazio)
- ✅ Foco retorna ao campo email

**Código:**
```typescript
test('should show error with invalid credentials', async ({ page }) => {
  await page.goto('/login')

  await page.fill('input[name="email"]', 'user-000035@account.example.invalid')
  await page.fill('input[name="password"]', 'WrongPassword')
  await page.click('button[type="submit"]')

  // Should stay on login page
  await expect(page).toHaveURL('/login')

  // Error message should appear
  await expect(page.locator('[role="alert"]')).toContainText('Email ou senha incorretos')

  // Password field should be cleared
  await expect(page.locator('input[name="password"]')).toHaveValue('')

  // Focus should return to email field
  await expect(page.locator('input[name="email"]')).toBeFocused()
})
```

[... continuar para todos os 15 testes E2E ...]

### Cobertura de Testes

**Metas:**
- **Unitários**: >90% de statement coverage
- **Integração**: 100% das APIs testadas
- **E2E**: 100% dos fluxos principais (happy + error paths)

**Comandos:**
```bash
# Rodar testes unitários com coverage
npm run test:unit -- --coverage

# Rodar testes de integração
npm run test:integration

# Rodar testes E2E
npm run test:e2e

# Rodar todos os testes
npm test
```

**Relatórios:**
- Coverage HTML: `coverage/index.html`
- E2E reports: `playwright-report/index.html`

---

## 📊 Análise do Gerente de Projeto

### Prioridade da Feature

**Prioridade:** High

**Justificativa:**
- Bloqueador para outras features (Dashboard, Profile, etc. dependem de auth)
- Funcionalidade core da aplicação
- Impacto em segurança (não pode ser postergado)

### Riscos Potenciais

#### Risco 1: JWT Secret Comprometido
- **Probabilidade:** Baixa
- **Impacto:** Crítico
- **Descrição:** Se o JWT secret vazar, atacantes podem gerar tokens válidos
- **Mitigação:**
  - Usar secrets fortes (>32 chars, gerados com `openssl rand -base64 32`)
  - Nunca commitar secrets no Git (.env no .gitignore)
  - Rotacionar secrets periodicamente (a cada 6 meses)
  - Usar secrets diferentes para access e refresh tokens
  - Implementar token blacklist para invalidar tokens comprometidos

#### Risco 2: Ataque de Brute Force
- **Probabilidade:** Alta
- **Impacto:** Médio
- **Descrição:** Atacantes tentam adivinhar senhas com múltiplas tentativas
- **Mitigação:**
  - Rate limiting: max 5 tentativas por IP em 15 minutos
  - Captcha após 3 tentativas falhadas
  - Account lockout temporário após 10 tentativas
  - Monitoramento de IPs suspeitos

#### Risco 3: Sessões Não Expiram Corretamente
- **Probabilidade:** Média
- **Impacto:** Médio
- **Descrição:** Refresh tokens não são invalidados no logout ou expiração
- **Mitigação:**
  - Armazenar refresh tokens no DB (tabela `refresh_tokens`)
  - Marcar token como revoked no logout
  - Cronjob para limpar tokens expirados
  - Validar no backend se token não está revoked

### Estimativa de Complexidade e Tempo

**Complexidade:** Média

**Critérios:**
- Tasks: 87 (31-70 = média)
- Integrações externas: 0 (apenas bibliotecas npm)
- Stack: Conhecida (Next.js + TypeScript)
- Incerteza técnica: Baixa (padrão JWT bem estabelecido)

**Estimativa de tempo:**
- **Backend (AuthService, APIs, DB)**: 2 dias
- **Frontend (LoginForm, AuthContext, UI)**: 2 dias
- **Testes (Unit + Integration + E2E)**: 1,5 dias
- **Code Review + Ajustes**: 0,5 dias
- **Total**: 6 dias (assumindo 1 desenvolvedor full-time)

**Fatores que podem afetar:**
- ⬆️ Aumentar: Desenvolvedor júnior sem experiência com JWT
- ⬇️ Reduzir: Desenvolvedor sênior com experiência em Next.js

### Critérios de Aceitação

**A feature será considerada completa quando:**

1. ✅ **Funcional:**
   - Usuário pode fazer login com email e senha válidos
   - Usuário recebe tokens JWT (access + refresh)
   - Tokens são salvos no localStorage/cookies
   - Usuário é redirecionado para `/dashboard` após login
   - Usuário pode fazer logout (tokens são revogados)
   - Access token expira em 15 minutos e é renovado automaticamente
   - Refresh token expira em 7 dias

2. ✅ **Qualidade:**
   - Cobertura de testes unitários >90%
   - Todos os 15 testes E2E passando
   - Sem erros críticos ou bloqueadores
   - Performance: API `/api/auth/login` responde em <200ms (95th percentile)

3. ✅ **Segurança:**
   - Senhas armazenadas com bcrypt (custo 12)
   - JWT assinado com RS256
   - Secrets fortes (>32 chars)
   - Rate limiting implementado (5 tentativas / 15min)
   - Refresh tokens armazenados no DB e revogáveis

4. ✅ **Não-Funcional:**
   - Código segue ESLint/Prettier
   - Acessibilidade WCAG 2.1 Level AA
   - Responsivo (mobile, tablet, desktop)
   - Documentação: README atualizado, JSDoc nos métodos principais

5. ✅ **Aprovação:**
   - Code review aprovado por 2 reviewers
   - QA testou manualmente e aprovou
   - Security review aprovado (verificação de secrets, bcrypt, JWT)

### Dependências Críticas

**Dependências internas:**
- Nenhuma (feature base, outras dependem dela)

**Dependências externas:**
- ✅ PostgreSQL configurado (DATABASE_URL)
- ✅ Prisma CLI instalado
- ✅ Node.js >=18.0.0

**Bloqueadores:**
- Nenhum

---

## 💼 Requisitos de Negócio (Business Analyst)

### Valor de Negócio

**Problema que resolve:**
Atualmente, a aplicação não tem sistema de autenticação. Qualquer pessoa pode acessar todas as páginas, incluindo dashboards com dados sensíveis. Isso impede:
- Personalização da experiência do usuário
- Controle de acesso a funcionalidades premium
- Tracking de ações por usuário
- Proteção de dados privados

**Benefícios esperados:**
1. **Segurança**: Proteger dados sensíveis de acesso não autorizado
2. **Personalização**: Mostrar conteúdo relevante para cada usuário
3. **Monetização**: Habilitar funcionalidades premium para usuários pagantes
4. **Compliance**: Atender requisitos legais (LGPD, GDPR) de proteção de dados

### KPIs (Key Performance Indicators)

#### 1. Taxa de Conversão de Registro para Login
- **Métrica**: % de usuários que se registram e fazem login pela primeira vez
- **Baseline**: N/A (feature nova)
- **Meta**: 85% (benchmark da indústria)
- **Prazo**: 30 dias após deploy

#### 2. Tempo Médio de Login
- **Métrica**: Tempo desde clicar "Entrar" até redirecionar para dashboard
- **Baseline**: N/A
- **Meta**: <2 segundos (95th percentile)
- **Prazo**: Desde o deploy

#### 3. Taxa de Sucesso de Login
- **Métrica**: % de tentativas de login que são bem-sucedidas
- **Baseline**: N/A
- **Meta**: >80% (indica que usuários lembram suas senhas)
- **Prazo**: 60 dias após deploy

#### 4. Sessões Ativas (7 dias)
- **Métrica**: % de usuários que permanecem logados por 7 dias (token não expira)
- **Baseline**: N/A
- **Meta**: >60%
- **Prazo**: 30 dias após deploy

### Impacto no Usuário

**Personas afetadas:**

1. **Maria, 28, usuária frequente**
   - **Como afeta**: Pode acessar suas preferências salvas, histórico, favoritos
   - **Sentimento**: Muito positivo - mais conveniente, experiência personalizada

2. **João, 45, novo usuário**
   - **Como afeta**: Precisa criar conta antes de usar funcionalidades principais
   - **Sentimento**: Neutro/Leve fricção - um passo a mais, mas entende a necessidade

3. **Admin, 35, gestor de conteúdo**
   - **Como afeta**: Pode controlar quem acessa áreas administrativas
   - **Sentimento**: Muito positivo - maior controle e segurança

**Jornada do usuário - Antes vs Depois:**

**ANTES (sem autenticação):**
1. Usuário acessa site
2. Vê todo conteúdo (incluindo dados que deveriam ser privados)
3. Não tem personalização
4. Sai do site
- **Fricção**: Baixa, mas sem valor agregado

**DEPOIS (com autenticação):**
1. Usuário acessa site
2. Vê landing page pública
3. Clica "Entrar" ou "Criar conta"
4. Faz login (15 segundos)
5. Vê dashboard personalizado com seus dados
6. Sessão persiste por 7 dias (não precisa login novamente)
- **Fricção**: Leve (login), mas alto valor agregado

### ROI (Return on Investment)

**Investimento:**
- Custo de desenvolvimento: 6 dias × $500/dia = $3,000
- Custo de design/UX: 1 dia × $400/dia = $400
- Custo de QA/testes: 1 dia × $350/dia = $350
- **Total**: $3,750

**Retorno esperado:**

**Cálculo conservador:**
- Baseline: 5000 visitantes/mês
- Sem auth: Todos acessam gratuitamente, sem conversão para premium
- Com auth: 20% se registram (1000 usuários)
- Desses, 10% convertem para plano pago ($20/mês) = 100 usuários pagantes
- **Receita adicional/mês**: 100 × $20 = $2,000
- **Receita adicional/ano**: $24,000

**Break-even:**
- Investimento: $3,750
- Receita adicional/mês: $2,000
- **Meses para break-even**: $3,750 / $2,000 = 1,9 meses (2 meses)

**ROI em 12 meses:**
- ROI = (Receita - Investimento) / Investimento × 100
- ROI = ($24,000 - $3,750) / $3,750 × 100 = **540%**

**Benefícios não-monetários:**
- Compliance com LGPD/GDPR (evita multas potenciais de até 2% do faturamento)
- Melhora na experiência do usuário (personalização)
- Capacidade de coletar dados de uso (analytics)

### Alinhamento com Objetivos de Negócio

**Objetivo estratégico da empresa:**
"Crescer base de usuários pagantes em 50% no próximo ano"

**Como esta feature contribui:**
- Pré-requisito para modelo freemium (free + premium features)
- Permite tracking de usuários para otimizar funil de conversão
- Habilita personalização que aumenta engajamento (+30% retention em benchmarks)
- Base para features futuras: perfil de usuário, preferências, histórico

**Prioridade estratégica:** Alta

---

## Critérios de Aceitação

- [ ] Usuário pode fazer login com email e senha válidos e recebe tokens JWT
- [ ] Usuário é redirecionado para `/dashboard` após login bem-sucedido
- [ ] Tokens são salvos corretamente (localStorage ou httpOnly cookies)
- [ ] Sessão persiste por 7 dias sem precisar novo login
- [ ] Access token expira em 15 minutos e é renovado automaticamente
- [ ] Usuário pode fazer logout e tokens são invalidados
- [ ] Mensagens de erro claras para credenciais inválidas
- [ ] Validação client-side impede envio de dados inválidos
- [ ] Formulário é responsivo (mobile, tablet, desktop)
- [ ] Acessibilidade WCAG 2.1 Level AA (navegação por teclado, screen reader)
- [ ] Senhas armazenadas com bcrypt (custo 12)
- [ ] Cobertura de testes >90% (unit + integration + E2E)
- [ ] Performance: API /api/auth/login <200ms (95th percentile)
- [ ] Rate limiting implementado (5 tentativas / 15min)
- [ ] Código aprovado em code review (2 reviewers)
- [ ] Documentação atualizada (README, API docs)

---

## Requisitos de Performance/Segurança

**Segurança:**
- Senhas DEVEM ser armazenadas com bcrypt (custo 12 ou superior)
- JWT DEVE ser assinado com algoritmo RS256 (não HS256)
- Secrets DEVEM ter no mínimo 32 caracteres
- Access tokens DEVEM expirar em 15 minutos (máximo)
- Refresh tokens DEVEM ser armazenados no DB e revogáveis
- Rate limiting DEVE limitar a 5 tentativas de login por IP em 15 minutos
- Refresh tokens DEVEM ser únicos e não reutilizáveis (rotation)

**Performance:**
- Tempo de resposta da API `/api/auth/login` DEVE ser <200ms (95th percentile)
- Tempo de carregamento da página `/login` DEVE ser <1s (LCP)
- Time to Interactive (TTI) da página `/login` DEVE ser <2s

---

## Dependências

**Dependências internas:**
- Nenhuma (feature base)

**Dependências externas:**
- PostgreSQL configurado e acessível
- Variáveis de ambiente configuradas (JWT secrets, DATABASE_URL)

**Ação necessária:**
Nenhuma - feature não está bloqueada.

---

**Gerado automaticamente por:** sprint-context-generator skill
**Data:** 2024-01-15
```

---

# 2. PLAN.MD (Trechos Principais)

```markdown
# Plano Técnico: FEAT-005 - Sistema de Autenticação JWT

📂 **Documentação Relacionada:**
- Especificação (user-supplied dependency; see PORTABILITY.md) - Requisitos e análise de personas
- Lista de Tasks (user-supplied dependency; see PORTABILITY.md) - Tarefas detalhadas (87 tasks)
- Pesquisa (user-supplied dependency; see PORTABILITY.md) - Documentação e referências

---

## Arquitetura Proposta

Sistema de autenticação stateless baseado em JWT (JSON Web Tokens) com refresh tokens para sessões persistentes.

**Fluxo de autenticação:**

```
┌─────────┐                ┌─────────────┐              ┌──────────────┐
│ Client  │                │  Next.js    │              │  PostgreSQL  │
│ (Browser)│                │  API Routes │              │   Database   │
└────┬────┘                └──────┬──────┘              └──────┬───────┘
     │                            │                            │
     │ 1. POST /api/auth/login    │                            │
     │ { email, password }        │                            │
     │───────────────────────────>│                            │
     │                            │ 2. findByEmail(email)      │
     │                            │ ──────────────────────────>│
     │                            │                            │
     │                            │<────────── User data ───── │
     │                            │                            │
     │                            │ 3. compare(password, hash) │
     │                            │                            │
     │                            │ 4. generateTokens(user)    │
     │                            │    - accessToken (15min)   │
     │                            │    - refreshToken (7d)     │
     │                            │                            │
     │                            │ 5. storeRefreshToken       │
     │                            │ ──────────────────────────>│
     │                            │                            │
     │<────── accessToken ───────│                            │
     │        refreshToken        │                            │
     │        user data           │                            │
     │                            │                            │
     │ 6. Store tokens (localStorage)                         │
     │ 7. Redirect to /dashboard  │                            │
```

**Componentes principais:**
1. **AuthService**: Lógica de negócio (login, logout, refresh)
2. **JWTService**: Geração e validação de tokens
3. **UserRepository**: Acesso a dados de usuários
4. **API Routes**: Endpoints REST (/api/auth/*)
5. **AuthContext**: Estado global de autenticação (React Context)

---

## Stack Tecnológica

**Linguagem:** TypeScript 5.3
**Framework:** Next.js 14 (App Router)

**Backend:**
- Next.js API Routes
- Prisma ORM 5.7 (PostgreSQL)
- jsonwebtoken 9.0 (JWT generation)
- bcrypt 5.1 (password hashing)
- zod 3.22 (validation)

**Frontend:**
- React 18
- Tailwind CSS 3.4
- React Hook Form (form validation)
- AuthContext (state management)

**Testing:**
- Jest (unit tests)
- Supertest (integration tests)
- Playwright (E2E tests)

**DevOps:**
- ESLint + Prettier
- Husky (git hooks)

---

## Estrutura de Diretórios

[Ver seção completa em spec.md]

---

## Componentes/Módulos

[Ver seção completa em spec.md - Requisitos do Desenvolvedor]

---

## APIs e Contratos

[Ver seção completa em spec.md - Requisitos do Desenvolvedor]

---

## Variáveis de Ambiente

[Ver seção completa em spec.md - Requisitos do Desenvolvedor]

---

## Setup e Configurações

### ESLint

`.eslintrc.js`:
```javascript
module.exports = {
  extends: ['next/core-web-vitals', 'prettier'],
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/no-explicit-any': 'warn',
  },
}
```

### Prettier

`.prettierrc`:
```json
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2
}
```

### Husky

`.husky/pre-commit`:
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
```

`package.json`:
```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

---

## Decisões Técnicas

### 1. JWT vs Session-based Auth
- **Decisão**: Usar JWT (JSON Web Tokens)
- **Razão**:
  - Stateless (não requer armazenamento de sessões no servidor)
  - Escalável horizontalmente (sem dependência de memória compartilhada)
  - Suporta múltiplos domínios/apps (tokens podem ser compartilhados)
  - Padrão da indústria para SPAs e APIs
- **Alternativas consideradas**:
  - Session-based (cookies): Requer sessões no servidor, dificulta scaling
- **Trade-offs**:
  - ➕ Escalabilidade, performance
  - ➖ Impossível invalidar access tokens (mitigado com expiração curta de 15min)

### 2. Algoritmo RS256 vs HS256
- **Decisão**: Usar RS256 (RSA com SHA-256)
- **Razão**:
  - Chave pública/privada (mais seguro que chave simétrica)
  - Permite validação de tokens sem acesso à chave privada
  - Recomendado para produção
- **Alternativas**: HS256 (simétrico, mais simples mas menos seguro)

### 3. Refresh Token Rotation
- **Decisão**: Implementar rotation de refresh tokens
- **Razão**:
  - Cada refresh gera um novo refresh token e invalida o anterior
  - Previne reutilização de tokens roubados
- **Implementação**: Armazenar refresh tokens no DB, marcar como revoked ao usar

---

## Riscos Técnicos

[Ver seção completa em spec.md - Análise do PM]

---

**Gerado automaticamente por:** sprint-context-generator skill
**Data:** 2024-01-15
```

---

# 3. TASKS.MD (Trechos Principais)

```markdown
# Lista de Tarefas: FEAT-005 - Sistema de Autenticação JWT

📂 **Documentação Relacionada:**
- Especificação (user-supplied dependency; see PORTABILITY.md) - Requisitos e análise de personas
- Plano Técnico (user-supplied dependency; see PORTABILITY.md) - Arquitetura e decisões técnicas
- Pesquisa (user-supplied dependency; see PORTABILITY.md) - Documentação e referências

**Total: 87 tasks | Complexidade: Média**

---

## Legenda

- 🏗️ Arquitetura/Setup
- 💻 Desenvolvimento Backend
- 🎨 Desenvolvimento Frontend/UI
- ✅ Testes
- 📝 Documentação

---

## 1. Setup e Configuração (10 tasks)

- [ ] 🏗️ **TASK-001:** Instalar dependências backend: `npm install jsonwebtoken bcrypt @prisma/client zod jose`
- [ ] 🏗️ **TASK-002:** Instalar dependências de tipos: `npm install -D @types/jsonwebtoken @types/bcrypt`
- [ ] 🏗️ **TASK-003:** Criar arquivo `.eslintrc.js` com configuração conforme research.md seção 2.4
- [ ] 🏗️ **TASK-004:** Criar arquivo `.prettierrc` conforme research.md seção 2.4
- [ ] 🏗️ **TASK-005:** Configurar Husky: `npx husky init`
- [ ] 🏗️ **TASK-006:** Criar `.husky/pre-commit` com lint-staged conforme research.md seção 2.5
- [ ] 🏗️ **TASK-007:** Criar `.husky/pre-push` para rodar testes
- [ ] 🏗️ **TASK-008:** Criar estrutura de diretórios conforme plan.md (src/lib/auth/, src/services/, src/repositories/, etc.)
- [ ] 🏗️ **TASK-009:** Criar arquivo `.env.example` com variáveis: DATABASE_URL, JWT_ACCESS_SECRET, JWT_REFRESH_SECRET
- [ ] 🏗️ **TASK-010:** Configurar Playwright: `npm init playwright@latest`

---

## 2. Backend - Database & Models (12 tasks)

- [ ] 💻 **TASK-011:** Criar schema Prisma para User em `prisma/schema.prisma` com campos: id, email, passwordHash, name, createdAt, updatedAt, lastLoginAt
- [ ] 💻 **TASK-012:** Criar schema Prisma para RefreshToken em `prisma/schema.prisma` com campos: id, token, userId, expiresAt, revoked, createdAt
- [ ] 💻 **TASK-013:** Adicionar relação User ↔ RefreshToken (1:N) no schema
- [ ] 💻 **TASK-014:** Adicionar índice único em User.email para performance de lookup
- [ ] 💻 **TASK-015:** Criar migration: `npx prisma migrate dev --name add_auth_tables`
- [ ] 💻 **TASK-016:** Rodar migration em desenvolvimento
- [ ] 💻 **TASK-017:** Gerar Prisma Client: `npx prisma generate`
- [ ] 💻 **TASK-018:** Criar `src/lib/db/prisma.ts` com singleton do PrismaClient
- [ ] 💻 **TASK-019:** Criar types TypeScript em `src/types/auth.ts` para User, LoginDto, TokenPayload, AuthResponse
- [ ] 💻 **TASK-020:** Criar Zod schemas em `src/lib/validators/auth.ts` para validação de email e senha
- [ ] 💻 **TASK-021:** Exportar schemas Zod: `loginSchema`, `registerSchema`
- [ ] 💻 **TASK-022:** Testar conexão com DB executando query simples no Prisma Studio

---

## 3. Backend - Auth Libraries (8 tasks)

- [ ] 💻 **TASK-023:** Criar `src/lib/auth/password.ts` com função `hashPassword(password): Promise<string>` usando bcrypt custo 12
- [ ] 💻 **TASK-024:** Criar função `comparePassword(password, hash): Promise<boolean>` em password.ts
- [ ] 💻 **TASK-025:** Criar constants em `src/lib/constants/auth.ts`: JWT_ACCESS_EXPIRY='15m', JWT_REFRESH_EXPIRY='7d', BCRYPT_SALT_ROUNDS=12
- [ ] 💻 **TASK-026:** Criar `src/lib/auth/jwt.ts` com função `generateAccessToken(payload): string` assinando com RS256
- [ ] 💻 **TASK-027:** Criar função `generateRefreshToken(payload): string` em jwt.ts
- [ ] 💻 **TASK-028:** Criar função `verifyAccessToken(token): TokenPayload | null` em jwt.ts tratando erros (expired, malformed)
- [ ] 💻 **TASK-029:** Criar função `verifyRefreshToken(token): TokenPayload | null` em jwt.ts
- [ ] 💻 **TASK-030:** Criar classe customizada `AuthError extends Error` em `src/lib/errors/AuthError.ts` com código de erro

---

## 4. Backend - Repositories (7 tasks)

- [ ] 💻 **TASK-031:** Criar interface `IUserRepository` em `src/repositories/interfaces/IUserRepository.ts` com métodos: findByEmail, findById, create, updateLastLogin
- [ ] 💻 **TASK-032:** Implementar `UserRepository` em `src/repositories/UserRepository.ts` implementando IUserRepository
- [ ] 💻 **TASK-033:** Implementar `findByEmail(email): Promise<User | null>` usando Prisma.user.findUnique
- [ ] 💻 **TASK-034:** Implementar `findById(id): Promise<User | null>` usando Prisma.user.findUnique
- [ ] 💻 **TASK-035:** Implementar `create(data): Promise<User>` usando Prisma.user.create
- [ ] 💻 **TASK-036:** Implementar `updateLastLogin(userId): Promise<void>` atualizando lastLoginAt
- [ ] 💻 **TASK-037:** Adicionar tratamento de erros do Prisma (P2002 unique constraint, etc.) retornando mensagens amigáveis

---

## 5. Backend - Services (10 tasks)

- [ ] 💻 **TASK-038:** Criar `AuthService` em `src/services/AuthService.ts` com constructor recebendo UserRepository via DI
- [ ] 💻 **TASK-039:** Implementar método `login(email, password): Promise<AuthResponse>` no AuthService
- [ ] 💻 **TASK-040:** No login(), buscar usuário com userRepository.findByEmail(email)
- [ ] 💻 **TASK-041:** Verificar senha com comparePassword(password, user.passwordHash)
- [ ] 💻 **TASK-042:** Se credenciais inválidas, lançar AuthError com código INVALID_CREDENTIALS
- [ ] 💻 **TASK-043:** Gerar accessToken e refreshToken com generateAccessToken() e generateRefreshToken()
- [ ] 💻 **TASK-044:** Salvar refreshToken no banco (tabela refresh_tokens) com expiresAt = now + 7d
- [ ] 💻 **TASK-045:** Atualizar lastLoginAt do usuário chamando userRepository.updateLastLogin()
- [ ] 💻 **TASK-046:** Retornar { accessToken, refreshToken, user } no formato AuthResponse
- [ ] 💻 **TASK-047:** Implementar método `logout(userId): Promise<void>` marcando refresh tokens como revoked=true
- [ ] 💻 **TASK-048:** Implementar método `refreshAccessToken(refreshToken): Promise<{accessToken}>` validando e gerando novo access token

---

## 6. Backend - API Routes (9 tasks)

- [ ] 💻 **TASK-049:** Criar `src/app/api/auth/login/route.ts` com handler POST
- [ ] 💻 **TASK-050:** Validar request body com loginSchema (Zod)
- [ ] 💻 **TASK-051:** Chamar AuthService.login(email, password)
- [ ] 💻 **TASK-052:** Retornar resposta JSON 200 OK com { success: true, data: { accessToken, refreshToken, user } }
- [ ] 💻 **TASK-053:** Tratar erros: INVALID_CREDENTIALS → 401, VALIDATION_ERROR → 400, erro genérico → 500
- [ ] 💻 **TASK-054:** Criar `src/app/api/auth/logout/route.ts` com handler POST
- [ ] 💻 **TASK-055:** Extrair userId do header Authorization (Bearer token)
- [ ] 💻 **TASK-056:** Chamar AuthService.logout(userId)
- [ ] 💻 **TASK-057:** Criar `src/app/api/auth/refresh/route.ts` com handler POST validando refreshToken e retornando novo accessToken

---

## 7. Frontend - UI Components (12 tasks)

- [ ] 🎨 **TASK-058:** Criar componente `Button` em `src/components/ui/Button.tsx` com props: variant, size, loading, disabled
- [ ] 🎨 **TASK-059:** Implementar variantes do Button: primary (#3B82F6), secondary (#6B7280), danger (#EF4444), ghost
- [ ] 🎨 **TASK-060:** Implementar tamanhos do Button: small (py-2), medium (py-3), large (py-4)
- [ ] 🎨 **TASK-061:** Adicionar estado loading ao Button mostrando spinner e desabilitando
- [ ] 🎨 **TASK-062:** Criar componente `Input` em `src/components/ui/Input.tsx` com props: type, label, error, required
- [ ] 🎨 **TASK-063:** Implementar estados do Input: normal, focus (ring azul), error (borda vermelha), disabled
- [ ] 🎨 **TASK-064:** Adicionar mensagem de erro abaixo do Input com role="alert" para screen readers
- [ ] 🎨 **TASK-065:** Criar componente `Card` em `src/components/ui/Card.tsx` com props: children, className
- [ ] 🎨 **TASK-066:** Aplicar estilos ao Card: bg-white, rounded-lg, shadow-lg, padding 2rem
- [ ] 🎨 **TASK-067:** Tornar Button e Input 100% acessíveis (aria-labels, keyboard navigation, focus indicators)
- [ ] 🎨 **TASK-068:** Testar Button e Input em mobile (375px), tablet (768px), desktop (1280px)
- [ ] 🎨 **TASK-069:** Verificar contraste de cores com ferramenta de acessibilidade (WebAIM Contrast Checker)

---

## 8. Frontend - Auth Components (10 tasks)

- [ ] 🎨 **TASK-070:** Criar componente `LoginForm` em `src/components/auth/LoginForm.tsx`
- [ ] 🎨 **TASK-071:** Adicionar campos Input para email e password no LoginForm
- [ ] 🎨 **TASK-072:** Integrar React Hook Form para gerenciar state e validação do formulário
- [ ] 🎨 **TASK-073:** Adicionar validação Zod: email válido, senha mínimo 8 caracteres
- [ ] 🎨 **TASK-074:** Implementar função handleSubmit que chama POST /api/auth/login
- [ ] 🎨 **TASK-075:** Mostrar estado de loading durante request (botão disabled, spinner)
- [ ] 🎨 **TASK-076:** Exibir mensagens de erro inline abaixo dos campos (borda vermelha, texto vermelho)
- [ ] 🎨 **TASK-077:** Armazenar tokens no localStorage após login bem-sucedido: localStorage.setItem('accessToken', token)
- [ ] 🎨 **TASK-078:** Atualizar AuthContext com dados do usuário após login
- [ ] 🎨 **TASK-079:** Redirecionar para /dashboard após login usando useRouter().push('/dashboard')

---

## 9. Frontend - Auth Context (6 tasks)

- [ ] 🎨 **TASK-080:** Criar `AuthContext` em `src/contexts/AuthContext.tsx` com createContext
- [ ] 🎨 **TASK-081:** Criar `AuthProvider` component com state: user, isAuthenticated, isLoading
- [ ] 🎨 **TASK-082:** Implementar função `login(email, password)` no AuthProvider chamando API e atualizando state
- [ ] 🎨 **TASK-083:** Implementar função `logout()` removendo tokens do localStorage e resetando state
- [ ] 🎨 **TASK-084:** Criar hook customizado `useAuth()` retornando context: { user, login, logout, isAuthenticated }
- [ ] 🎨 **TASK-085:** Adicionar AuthProvider no layout root (`src/app/layout.tsx`) para disponibilizar globalmente

---

## 10. Frontend - Pages (4 tasks)

- [ ] 🎨 **TASK-086:** Criar página `src/app/(auth)/login/page.tsx` renderizando LoginForm dentro de Card
- [ ] 🎨 **TASK-087:** Adicionar logo e título "Bem-vindo de volta!" na página de login
- [ ] 🎨 **TASK-088:** Criar página `src/app/(protected)/dashboard/page.tsx` mostrando dados do usuário logado
- [ ] 🎨 **TASK-089:** Adicionar verificação de autenticação: redirecionar para /login se não autenticado

---

## 11. Testes Unitários (15 tasks)

- [ ] ✅ **TASK-090:** Criar `src/services/__tests__/AuthService.spec.ts` para testar AuthService
- [ ] ✅ **TASK-091:** Testar AuthService.login() com credenciais válidas retorna tokens
- [ ] ✅ **TASK-092:** Testar AuthService.login() com email inexistente retorna erro INVALID_CREDENTIALS
- [ ] ✅ **TASK-093:** Testar AuthService.login() com senha incorreta retorna erro INVALID_CREDENTIALS
- [ ] ✅ **TASK-094:** Testar AuthService.login() atualiza lastLoginAt do usuário
- [ ] ✅ **TASK-095:** Criar `src/lib/auth/__tests__/password.spec.ts` para testar funções de senha
- [ ] ✅ **TASK-096:** Testar hashPassword() gera hash diferente da senha original
- [ ] ✅ **TASK-097:** Testar comparePassword() com senha correta retorna true
- [ ] ✅ **TASK-098:** Testar comparePassword() com senha incorreta retorna false
- [ ] ✅ **TASK-099:** Criar `src/lib/auth/__tests__/jwt.spec.ts` para testar funções JWT
- [ ] ✅ **TASK-100:** Testar generateAccessToken() cria token válido decodificável
- [ ] ✅ **TASK-101:** Testar verifyAccessToken() com token válido retorna payload correto
- [ ] ✅ **TASK-102:** Testar verifyAccessToken() com token expirado retorna null
- [ ] ✅ **TASK-103:** Testar verifyAccessToken() com token malformado retorna null
- [ ] ✅ **TASK-104:** Rodar `npm run test:coverage` e verificar cobertura >90%

---

## 12. Testes E2E (10 tasks)

- [ ] ✅ **TASK-105:** Criar `<USER_DEPENDENCY:tests/e2e/auth.spec.ts>` para testes E2E de autenticação
- [ ] ✅ **TASK-106:** E2E: Navegar para /login, preencher credenciais válidas, clicar Entrar, verificar redirecionamento para /dashboard
- [ ] ✅ **TASK-107:** E2E: Verificar que token foi salvo no localStorage após login
- [ ] ✅ **TASK-108:** E2E: Verificar que nome do usuário aparece no dashboard após login
- [ ] ✅ **TASK-109:** E2E: Tentar login com credenciais inválidas e verificar mensagem de erro
- [ ] ✅ **TASK-110:** E2E: Verificar que campo de senha é limpo após erro
- [ ] ✅ **TASK-111:** E2E: Validação client-side de email inválido impede submit
- [ ] ✅ **TASK-112:** E2E: Botão "Entrar" mostra spinner durante loading
- [ ] ✅ **TASK-113:** E2E: Usuário logado acessa /login e é redirecionado para /dashboard
- [ ] ✅ **TASK-114:** E2E: Fluxo completo - Login → Navegar no dashboard → Logout → Redirecionado para /login

---

## 13. Documentação (6 tasks)

- [ ] 📝 **TASK-115:** Atualizar README.md com seção "Autenticação" explicando fluxo JWT
- [ ] 📝 **TASK-116:** Documentar endpoints da API em README.md: POST /api/auth/login, /logout, /refresh
- [ ] 📝 **TASK-117:** Adicionar exemplos de request/response para cada endpoint
- [ ] 📝 **TASK-118:** Documentar variáveis de ambiente no README com instruções de como gerar secrets
- [ ] 📝 **TASK-119:** Adicionar comentários JSDoc nos métodos principais: AuthService.login(), generateAccessToken(), etc.
- [ ] 📝 **TASK-120:** Atualizar CHANGELOG.md com entrada: `[v1.1.0] - Add JWT authentication system`

---

## Resumo de Tasks

| Categoria | Quantidade |
|-----------|------------|
| 🏗️ Setup  | 10 tasks   |
| 💻 Backend | 56 tasks   |
| 🎨 Frontend | 32 tasks   |
| ✅ Testes  | 25 tasks   |
| 📝 Docs    | 6 tasks    |
| **TOTAL**  | **129 tasks** |

*(Nota: Contagem ajustada - plano original previa 87 tasks, mas granularidade alta gerou 129)*

**Complexidade:** Média
**Estimativa:** 5-7 dias de desenvolvimento

---

**Gerado automaticamente por:** sprint-context-generator skill
**Data:** 2024-01-15
```

---

# 4. RESEARCH.MD (Trechos Principais)

```markdown
# Pesquisa e Documentação: FEAT-005 - Sistema de Autenticação JWT

**Data da pesquisa:** 2024-01-15
**Tecnologias pesquisadas:** 3 tecnologias (jsonwebtoken, bcrypt, Prisma)
**Melhores práticas:** 5 áreas (Clean Arch, E2E, TDD, Linting, Hooks)

---

## Índice

1. [Tecnologias Utilizadas](#tecnologias-utilizadas)
2. [Melhores Práticas Pesquisadas](#melhores-práticas-pesquisadas)
3. [Artigos Relevantes](#artigos-relevantes)
4. [Exemplos de Implementação](#exemplos-de-implementação)

---

## 1. Tecnologias Utilizadas

### 1.1. jsonwebtoken (JWT)

- **Link oficial**: https://github.com/auth0/node-jsonwebtoken
- **Versão**: 9.0.2 (latest)
- **Descrição**: Implementação de JSON Web Tokens para Node.js, padrão da indústria para autenticação stateless

**Instalação:**
```bash
npm install jsonwebtoken
npm install -D @types/jsonwebtoken
```

**Principais métodos:**
- `jwt.sign(payload, secret, options)`: Gerar token JWT assinado
- `jwt.verify(token, secret, options)`: Verificar e decodificar token
- `jwt.decode(token)`: Decodificar token sem verificar (útil para debug)

**Exemplo básico:**
```typescript
import jwt from 'jsonwebtoken'

// Gerar access token (expira em 15 minutos)
const accessToken = jwt.sign(
  { userId: 'user-123', email: 'user-000013@account.example.invalid' },
  process.env.JWT_ACCESS_SECRET!,
  {
    expiresIn: '15m',
    algorithm: 'RS256', // Recomendado para produção
    issuer: 'my-app',
  }
)

// Verificar token
try {
  const payload = jwt.verify(accessToken, process.env.JWT_ACCESS_SECRET!) as TokenPayload
  console.log('User ID:', payload.userId)
} catch (error) {
  if (error.name === 'TokenExpiredError') {
    // Token expirado
  } else if (error.name === 'JsonWebTokenError') {
    // Token malformado ou assinatura inválida
  }
}
```

**Configurações importantes:**
- **algorithm**: Usar `RS256` (RSA) para produção, não `HS256` (HMAC)
- **expiresIn**: Access token curto (15m), refresh token longo (7d)
- **issuer**: Identificar origem do token
- **audience**: Validar destinatário do token

**Links úteis:**
- Algoritmos suportados: https://github.com/auth0/node-jsonwebtoken#algorithms-supported
- Verificação de tokens: https://service.example.invalid

---

### 1.2. bcrypt

- **Link oficial**: https://github.com/kelektiv/node.bcrypt.js
- **Versão**: 5.1.1 (latest)
- **Descrição**: Biblioteca para hash de senhas com salt automático, resistente a rainbow tables e brute force

**Instalação:**
```bash
npm install bcrypt
npm install -D @types/bcrypt
```

**Principais métodos:**
- `bcrypt.hash(password, saltRounds)`: Criar hash de senha
- `bcrypt.compare(password, hash)`: Verificar senha contra hash
- `bcrypt.genSalt(rounds)`: Gerar salt manualmente (raramente necessário)

**Exemplo básico:**
```typescript
import bcrypt from 'bcrypt'

const SALT_ROUNDS = 12 // Custo recomendado (2^12 iterações)

// Hash de senha no registro
async function hashPassword(password: string): Promise<string> {
  return await bcrypt.hash(password, SALT_ROUNDS)
}

// Verificar senha no login
async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return await bcrypt.compare(password, hash)
}

// Uso
const hash = await hashPassword('SecurePassword123!')
// $2b$12$... (60 caracteres)

const isValid = await verifyPassword('SecurePassword123!', hash)
// true

const isInvalid = await verifyPassword('WrongPassword', hash)
// false
```

**Configurações importantes:**
- **Salt Rounds (custo)**: 12 é recomendado (equilíbrio entre segurança e performance)
  - 10: ~65ms por hash (mais rápido, menos seguro)
  - 12: ~260ms per hash (recomendado)
  - 14: ~1000ms per hash (muito lento para autenticação)

**Segurança:**
- bcrypt usa salt automático (incluído no hash)
- Resistente a rainbow tables
- Custo computacional ajustável (protege contra hardware mais rápido)

---

### 1.3. Prisma ORM

- **Link oficial**: https://service.example.invalid
- **Versão**: 5.7.0 (latest)
- **Descrição**: ORM type-safe para Node.js e TypeScript com suporte a PostgreSQL, MySQL, SQLite

**Instalação:**
```bash
npm install @prisma/client
npm install -D prisma
npx prisma init
```

**Principais comandos:**
- `npx prisma migrate dev`: Criar e aplicar migrations em desenvolvimento
- `npx prisma generate`: Gerar Prisma Client com types baseados no schema
- `npx prisma studio`: Interface visual para visualizar/editar dados

**Exemplo de schema:**
```prisma
// prisma/schema.prisma
model User {
  id           String   @id @default(uuid())
  email        String   @unique
  passwordHash String   @map("password_hash")
  name         String
  createdAt    DateTime @default(now()) @map("created_at")
  updatedAt    DateTime @updatedAt @map("updated_at")
  lastLoginAt  DateTime? @map("last_login_at")

  refreshTokens RefreshToken[]

  @@map("users")
}

model RefreshToken {
  id        String   @id @default(uuid())
  token     String   @unique
  userId    String   @map("user_id")
  expiresAt DateTime @map("expires_at")
  revoked   Boolean  @default(false)
  createdAt DateTime @default(now()) @map("created_at")

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("refresh_tokens")
}
```

**Uso básico:**
```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Buscar usuário por email
const user = await prisma.user.findUnique({
  where: { email: 'user-000013@account.example.invalid' },
})

// Criar usuário
const newUser = await prisma.user.create({
  data: {
    email: 'user-000038@account.example.invalid',
    passwordHash: hashedPassword,
    name: 'New User',
  },
})

// Atualizar last login
await prisma.user.update({
  where: { id: userId },
  data: { lastLoginAt: new Date() },
})
```

**Links úteis:**
- Schema reference: https://service.example.invalid
- CRUD operations: https://service.example.invalid

---

## 2. Melhores Práticas Pesquisadas

### 2.1. Clean Architecture

**Fontes:**
- [Clean Architecture for Next.js Apps](https://service.example.invalid) (exemplo fictício)
- [Hexagonal Architecture in TypeScript](https://service.example.invalid)

**Estrutura de diretórios recomendada:**
```
src/
├── app/              # Presentation (Next.js pages, API routes)
├── components/       # UI components (presentation)
├── contexts/         # State management (presentation)
├── services/         # Application layer (business logic)
├── repositories/     # Infrastructure layer (data access)
├── lib/              # Libraries and utilities
└── types/            # Domain types and interfaces
```

**Princípios chave:**
- **Dependências apontam para dentro**: Domain não depende de nada, Infrastructure depende de Domain
- **Use cases orquestram o fluxo**: Services contêm lógica de negócio, não acesso a dados direto
- **Inversão de dependência**: Services dependem de interfaces (IUserRepository), não implementações concretas

**Exemplo de estrutura aplicada ao Auth:**
```
AuthService (application)
    ↓ depende de interface
IUserRepository (domain)
    ↑ implementa
UserRepository (infrastructure)
    ↓ usa
Prisma Client (infrastructure)
```

---

### 2.2. Testes E2E com Playwright

**Fontes:**
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [E2E Testing Next.js Apps](https://example.com)

**Estrutura recomendada:**
```
tests/
├── e2e/
│   ├── fixtures/
│   │   └── auth.fixture.ts    # Helper para criar usuário de teste
│   ├── pages/
│   │   ├── login.page.ts      # Page Object Model
│   │   └── dashboard.page.ts
│   └── specs/
│       ├── auth.spec.ts
│       └── user-flow.spec.ts
└── playwright.config.ts
```

**Patterns úteis:**

**Page Object Model:**
```typescript
// tests/e2e/pages/login.page.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login')
  }

  async fillEmail(email: string) {
    await this.page.fill('input[name="email"]', email)
  }

  async fillPassword(password: string) {
    await this.page.fill('input[name="password"]', password)
  }

  async submit() {
    await this.page.click('button[type="submit"]')
  }

  async login(email: string, password: string) {
    await this.fillEmail(email)
    await this.fillPassword(password)
    await this.submit()
  }
}
```

**Fixtures customizados:**
```typescript
// tests/e2e/fixtures/auth.fixture.ts
import { test as base } from '@playwright/test'

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    // Setup: criar usuário e fazer login
    const user = await createTestUser()
    await page.goto('/login')
    await page.fill('input[name="email"]', user.email)
    await page.fill('input[name="password"]', user.password)
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard')

    // Use fixture
    await use(page)

    // Teardown: deletar usuário de teste
    await deleteTestUser(user.id)
  },
})
```

---

[... continuar com seções 2.3, 2.4, 2.5, seção 3 e 4 ...]

---

**Fim do research.md**
```

---

# 5. FEATURES.XML (Completo)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<features project="My Application" total="5" completed="0">

  <category name="Authentication">
    <feature id="FEAT-005" status="pending" priority="high">
      <description>Implementar sistema de autenticação JWT com refresh tokens para sessões persistentes e seguras</description>
      <steps>
        <step>Usuário pode fazer login com email e senha válidos e recebe tokens JWT</step>
        <step>Usuário é redirecionado para /dashboard após login bem-sucedido</step>
        <step>Tokens são salvos corretamente (localStorage ou httpOnly cookies)</step>
        <step>Sessão persiste por 7 dias sem precisar novo login</step>
        <step>Access token expira em 15 minutos e é renovado automaticamente</step>
        <step>Usuário pode fazer logout e tokens são invalidados</step>
        <step>Mensagens de erro claras para credenciais inválidas</step>
        <step>Formulário é responsivo (mobile, tablet, desktop)</step>
        <step>Acessibilidade WCAG 2.1 Level AA</step>
        <step>Cobertura de testes >90%</step>
        <step>Performance: API /api/auth/login <200ms</step>
        <step>Código aprovado em code review</step>
      </steps>
      <notes>Tasks: 87 | Docs: docs/context-log-running/sistema-autenticacao-jwt/ | Complexity: Média | Time: 4-6 dias</notes>
    </feature>
  </category>

</features>
```

---

## Resumo do Exemplo

Este exemplo demonstra o **nível de detalhe e qualidade esperados** quando a skill `sprint-context-generator` gera documentação completa.

**Características principais:**
1. **Especificação completa** (spec.md) com análises detalhadas de todas as 6 personas
2. **Plano técnico profundo** (plan.md) com arquitetura, decisões, riscos
3. **Tasks granulares** (tasks.md) com 87+ tasks específicas mencionando arquivos exatos
4. **Pesquisa abrangente** (research.md) com documentação de tecnologias e melhores práticas
5. **features.xml bem estruturado** com todos os critérios de aceitação

**Qualidade:**
- ✅ Tasks específicas (mencionam arquivos, métodos, componentes)
- ✅ Análises de personas completas e relevantes
- ✅ Pesquisa de documentação útil e organizada
- ✅ Decisões técnicas justificadas
- ✅ Critérios de aceitação claros e testáveis

---

**Gerado como exemplo por:** sprint-context-generator skill
**Data:** 2024-01-15
