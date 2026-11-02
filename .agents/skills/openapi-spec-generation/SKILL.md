---
name: openapi-spec-generation
description: "Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns. Use when creating API documentation, generating SDKs, or ensuring API contract compliance."
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

## Adaptacao local HAOS - ler antes dos exemplos upstream

Esta skill e referencia tecnica, nao autorizacao operacional. Preservar os gates HAOS e o escopo aprovado; nao instalar bibliotecas, mudar infraestrutura ou executar exemplos automaticamente. Conferir versoes reais e documentacao oficial via Context7 antes de implementar. Nunca usar dados ou credenciais reais nos exemplos. A origem e os hashes upstream/locais constam em SOURCE.json.

Aplicacao Dash: especificar contratos reais Next.js 14/NextAuth 4/Prisma 6, autenticacao por metodo, erros, idempotencia, paginacao e versionamento. Express/FastAPI/tsoa sao exemplos, nao migracao aprovada. Ferramentas CLI exemplificadas nao serao instaladas globalmente por esta skill; avaliar a versao e o gate do projeto.

# OpenAPI Spec Generation

Comprehensive patterns for creating, maintaining, and validating OpenAPI 3.1 specifications for RESTful APIs.

## When to Use This Skill

- Creating API documentation from scratch
- Generating OpenAPI specs from existing code
- Designing API contracts (design-first approach)
- Validating API implementations against specs
- Generating client SDKs from specs
- Setting up API documentation portals

## Core Concepts

### 1. OpenAPI 3.1 Structure

```yaml
openapi: 3.1.0
info:
  title: API Title
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /resources:
    get: ...
components:
  schemas: ...
  securitySchemes: ...
```

### 2. Design Approaches

| Approach         | Description                  | Best For            |
| ---------------- | ---------------------------- | ------------------- |
| **Design-First** | Write spec before code       | New APIs, contracts |
| **Code-First**   | Generate spec from code      | Existing APIs       |
| **Hybrid**       | Annotate code, generate spec | Evolving APIs       |

## Templates and detailed worked examples

Full template library and detailed worked examples live in `./references/details.md`. Read that file when you need the concrete templates.

## Best Practices

### Do's

- **Use $ref** - Reuse schemas, parameters, responses
- **Add examples** - Real-world values help consumers
- **Document errors** - All possible error codes
- **Version your API** - In URL or header
- **Use semantic versioning** - For spec changes

### Don'ts

- **Don't use generic descriptions** - Be specific
- **Don't skip security** - Define all schemes
- **Don't forget nullable** - Be explicit about null
- **Don't mix styles** - Consistent naming throughout
- **Don't hardcode URLs** - Use server variables
