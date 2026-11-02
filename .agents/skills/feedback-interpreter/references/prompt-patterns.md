# Padrões de Prompt por Tipo de Mudança — Lovable

## Visual

### Cores
```
Alterar a cor [do elemento X] de [cor atual ou "desconhecida"] para [nova cor em hex ou classe Tailwind].
Manter consistência com a paleta existente do projeto.
```

### Espaçamento / Layout
```
Aumentar/reduzir o espaçamento [interno/externo] do [componente X].
Usar [py-6 px-8 / gap-4 / mt-8] — ajustar conforme a densidade visual atual.
```

### Tipografia
```
Alterar [título/body/label] da seção [X] para:
- Tamanho: [text-xl / text-sm]
- Peso: [font-semibold / font-normal]
- Cor: [text-gray-900 / text-muted-foreground]
```

### Responsividade
```
Corrigir layout da [seção X] em mobile (< 768px):
- [Empilhar elementos que estão lado a lado]
- [Reduzir tamanho de fonte de text-4xl para text-2xl]
- [Ocultar [elemento Y] em telas pequenas]
```

---

## Funcional

### Botão / Ação
```
Ao clicar em [botão X]:
1. [Validar campos obrigatórios]
2. [Executar ação: salvar / navegar / abrir modal]
3. [Feedback visual: toast "Salvo com sucesso" / spinner durante loading]
```

### Formulário
```
No formulário [X]:
- Adicionar validação em [campo Y]: [obrigatório / formato email / mínimo N caracteres]
- Mensagem de erro: "[texto da mensagem]"
- Desabilitar botão Enviar enquanto há erros
```

### Navegação
```
Ao [trigger], navegar para [rota/página].
Preservar [estado / scroll position] se necessário.
```

### Estado Vazio / Loading / Erro
```
Adicionar estado [vazio / loading / erro] para [componente X]:
- Vazio: [ícone + mensagem "Nenhum item encontrado"]
- Loading: [skeleton / spinner]
- Erro: [mensagem + botão "Tentar novamente"]
```

---

## Conteúdo

### Textos e Labels
```
Atualizar textos:
- [Elemento A]: "[texto atual]" → "[novo texto]"
- [Elemento B]: "[texto atual]" → "[novo texto]"
```

### Hierarquia de Informação
```
Reorganizar a ordem de exibição dos campos/itens em [seção X]:
Nova ordem: [1. campo A, 2. campo B, 3. campo C]
```

---

## Feature Nova

### Componente Simples
```
Adicionar [componente] na [posição: topo da página / abaixo de X / sidebar]:
- Conteúdo: [o que exibe]
- Comportamento: [o que faz ao interagir]
- Estilo: [consistente com o design atual]
```

### Seção Nova
```
Criar nova seção "[nome]" entre [seção A] e [seção B]:
- Propósito: [o que comunica / faz]
- Elementos: [lista dos componentes internos]
- Dados: [estático / dinâmico — fonte dos dados]
```

---

## Combinado (Visual + Funcional)

Quando o feedback mistura visual e funcional, use este formato:

```
## Contexto
[Descrição do estado atual]

## Mudanças

### Visual
- [mudança 1]
- [mudança 2]

### Funcional
- [mudança 1]
- [mudança 2]

## Resultado esperado
O usuário deve [ver/conseguir fazer X] após as mudanças.
```
