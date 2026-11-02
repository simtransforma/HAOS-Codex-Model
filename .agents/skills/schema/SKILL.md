---
name: schema
description: "Use quando o usu\u00e1rio quiser adicionar, corrigir ou otimizar schema markup e dados estruturados no site. Use tamb\u00e9m quando ele mencionar 'schema markup', 'dados estruturados', 'JSON-LD', 'rich snippets', 'schema.org', 'FAQ schema', 'product schema', 'review schema', 'breadcrumb schema', 'rich results do Google', 'painel de conhecimento', 'estrelas na busca' ou 'adicionar dados estruturados'. Use sempre que algu\u00e9m quiser que as p\u00e1ginas apare\u00e7am com resultados aprimorados no Google. Para SEO mais amplo, veja seo-optimizer. Para otimiza\u00e7\u00e3o para busca por IA, veja ai-seo."
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

# Schema Markup (HAOS)

Você é especialista em dados estruturados e schema markup. Seu objetivo é implementar marcação schema.org que ajuda buscadores a entender o conteúdo e habilita rich results na busca.

## Avaliação Inicial

**Verifique o contexto de marketing de produto primeiro:**
Se `<USER_DEPENDENCY:.agents/product-marketing.md>` existir (ou `.claude/product-marketing.md`, ou o legado `product-marketing-context.md`), leia antes de perguntar. Use esse contexto e só pergunte o que faltar ou for específico desta tarefa.

Antes de implementar schema, entenda:

1. **Tipo de Página** — que tipo de página? Qual é o conteúdo principal? Quais rich results são possíveis?
2. **Estado Atual** — já existe schema? Erros na implementação? Quais rich results já aparecem?
3. **Metas** — quais rich results você quer? Qual o valor de negócio?

---

## Princípios Centrais

### 1. Precisão Primeiro
- O schema deve representar com precisão o conteúdo da página
- Não marque conteúdo que não existe
- Mantenha atualizado quando o conteúdo mudar

### 2. Use JSON-LD
- O Google recomenda o formato JSON-LD
- Mais fácil de implementar e manter
- Coloque no `<head>` ou no fim do `<body>`

### 3. Siga as Diretrizes do Google
- Use só a marcação que o Google suporta
- Evite táticas de spam
- Revise os requisitos de elegibilidade

### 4. Valide Tudo
- Teste antes de publicar
- Monitore o Search Console
- Corrija erros rapidamente

---

## Tipos Comuns de Schema

| Tipo | Usar para | Propriedades obrigatórias |
|------|-----------|---------------------------|
| Organization | Homepage/sobre da empresa | name, url |
| WebSite | Homepage (caixa de busca) | name, url |
| Article | Posts de blog, notícias | headline, image, datePublished, author |
| Product | Páginas de produto | name, image, offers |
| SoftwareApplication | Páginas de app/SaaS | name, offers |
| FAQPage | Conteúdo de FAQ | mainEntity (array de Q&A) |
| HowTo | Tutoriais | name, step |
| BreadcrumbList | Qualquer página com breadcrumb | itemListElement |
| LocalBusiness | Páginas de negócio local | name, address |
| Event | Eventos, webinars | name, startDate, location |

**Para exemplos completos de JSON-LD**: veja [references/schema-examples.md](references/schema-examples.md)

---

## Referência Rápida

### Organization (Página da Empresa)
Obrigatório: name, url
Recomendado: logo, sameAs (perfis sociais), contactPoint

### Article/BlogPosting
Obrigatório: headline, image, datePublished, author
Recomendado: dateModified, publisher, description

### Product
Obrigatório: name, image, offers (price + availability)
Recomendado: sku, brand, aggregateRating, review

### FAQPage
Obrigatório: mainEntity (array de pares Question/Answer)

### BreadcrumbList
Obrigatório: itemListElement (array com position, name, item)

---

## Múltiplos Tipos de Schema

Você pode combinar vários tipos numa página usando `@graph`:

```json
{
  "@context": "https://service.example.invalid",
  "@graph": [
    { "@type": "Organization", ... },
    { "@type": "WebSite", ... },
    { "@type": "BreadcrumbList", ... }
  ]
}
```

---

## Validação e Teste

### Ferramentas
- **Teste de Rich Results do Google**: https://search.google.com/test/rich-results
- **Validador Schema.org**: https://service.example.invalid
- **Search Console**: relatórios de Melhorias

### Erros Comuns

**Propriedades obrigatórias faltando** — confira a documentação do Google para campos obrigatórios

**Valores inválidos** — datas em ISO 8601, URLs totalmente qualificadas, enumerações exatas

**Divergência com o conteúdo** — o schema não bate com o conteúdo visível

---

## Implementação

### Sites Estáticos
- Adicione JSON-LD direto no template HTML
- Use includes/partials para schema reaproveitável

### Sites Dinâmicos (React, Next.js)
- Componente que renderiza o schema
- Renderizado no servidor para SEO
- Serialize os dados para JSON-LD

### CMS / WordPress
- Plugins (Yoast, Rank Math, Schema Pro)
- Modificações no tema
- Campos personalizados para dados estruturados

---

## Formato de Saída

### Implementação do Schema
```json
// Bloco JSON-LD completo
{
  "@context": "https://service.example.invalid",
  "@type": "...",
  // Marcação completa
}
```

### Checklist de Teste
- [ ] Valida no Teste de Rich Results
- [ ] Sem erros ou avisos
- [ ] Bate com o conteúdo da página
- [ ] Todas as propriedades obrigatórias incluídas

---

## Perguntas Específicas da Tarefa

1. Que tipo de página é esta?
2. Quais rich results você quer alcançar?
3. Que dados estão disponíveis para popular o schema?
4. Já existe schema na página?
5. Qual é sua stack?

---

## Skills Relacionadas

- **seo-optimizer**: para SEO geral, incluindo revisão de schema
- **ai-seo**: para otimização de busca por IA (schema ajuda a IA a entender o conteúdo)
