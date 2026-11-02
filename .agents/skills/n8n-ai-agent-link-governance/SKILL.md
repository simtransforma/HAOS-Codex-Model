---
name: n8n-ai-agent-link-governance
description: "Use para impedir que agentes de atendimento em n8n enviem URLs antigas ou inventadas, reconciliando links publicados, aplicando UTMs determin\u00edsticas e validando tudo sem mensagens reais."
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

# Governança de links para agentes de IA no n8n

Use esta skill quando um agente conversacional baseado em LLM precisar recomendar páginas, produtos ou checkouts sem depender da memória do modelo para construir URLs.

## Princípio

O modelo decide a intenção e ajuda na resposta. A aplicação decide o link.

Nunca trate a resposta livre do LLM como fonte de verdade para URL comercial. Mantenha um manifesto determinístico com `offer_id`, destino oficial e política de atribuição.

## Fluxo obrigatório

1. Identifique a página oficial publicada.
2. Extraia os links do DOM renderizado.
3. Se o site for SPA e parte das ofertas aparecer somente em modal, seletor ou lazy load, inspecione também o bundle publicado.
4. Normalize e deduplique os destinos.
5. Associe cada URL a uma chave semântica estável, como `pass_pro` ou `day_pro_27`.
6. Compare o manifesto extraído com o manifesto ativo do agente: quantidade, ausências e excedentes.
7. No pós-processamento da resposta, substitua URLs antigas conhecidas e acrescente o destino oficial escolhido pelo código.
8. Aplique UTMs de forma determinística, sem pedir ao LLM que as escreva.
9. Valide em `test_mode` ou sandbox, sem chamar o canal real.
10. Publique ou altere o workflow remoto somente com autorização explícita.

## Política de UTM

Defina a convenção por canal. Para WhatsApp, um padrão possível é:

```text
utm_source=whatsapp
utm_medium=atendimento_ia
utm_campaign=<campanha_estavel>
utm_content=<offer_id>
```

O `utm_content` deve identificar a oferta exata. Não use texto livre gerado pelo modelo.

## Pós-processador determinístico

O código deve:

- reconhecer pedidos explícitos de link, compra ou checkout;
- escolher a oferta pela chave do produto, categoria e data;
- usar o site oficial quando a oferta estiver ambígua;
- substituir domínios e rotas legadas conhecidos;
- preservar somente parâmetros autorizados;
- impedir que o LLM introduza um checkout não presente no manifesto;
- acrescentar a URL oficial depois que a resposta textual estiver pronta.

### Compatibilidade com Code node do n8n

Não presuma que todos os globais de navegador ou Node estejam disponíveis. Em alguns runtimes do Code node, `URL` pode não existir.

Para UTMs simples, prefira montagem controlada:

```javascript
const withUtm = (base, content) => {
  const joiner = String(base).includes('?') ? '&' : '?';
  return `${base}${joiner}utm_source=whatsapp&utm_medium=atendimento_ia&utm_campaign=${encodeURIComponent(CAMPAIGN)}&utm_content=${encodeURIComponent(content)}`;
};
```

Se precisar manipular parâmetros existentes com maior complexidade, valide primeiro a API disponível no runtime ou implemente um parser explícito e testado.

## QA mínimo

Execute testes sem mensagem real para:

1. site oficial;
2. uma oferta completa;
3. um ingresso por dia com categoria e data;
4. pergunta ambígua de compra;
5. resposta simulada contendo URL antiga;
6. todas as ofertas do manifesto presentes no workflow ativo;
7. nenhuma oferta extra;
8. todas as URLs com `utm_source`, `utm_medium`, `utm_campaign` e `utm_content`;
9. workflow ativo depois da alteração;
10. ausência de erro no nó pós-processador.

Critério de aprovação:

```text
site_manifest_count == agent_manifest_count
missing_in_agent == 0
extra_in_agent == 0
all_required_utm_fields == true
real_channel_calls == 0 durante o QA
```

## Segurança

- Não imprimir credenciais, payloads pessoais ou números de telefone.
- Não registrar identificadores de cliente nesta skill distribuível.
- Fazer backup do workflow antes de alterar.
- Preservar o estado ativo/inativo original e prever rollback.
- Não clicar em checkout nem gerar pedido durante a auditoria de links.
