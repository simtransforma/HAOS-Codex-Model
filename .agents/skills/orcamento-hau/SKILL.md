---
name: orcamento-hau
description: "Criar, revisar, corrigir, publicar e validar or\u00e7amentos, propostas comerciais, propostas t\u00e9cnicas e contratos da HAU Solu\u00e7\u00f5es Digitais. Usar sempre que usuario mencionar or\u00e7amento HAU, proposta HAU, p\u00e1gina de proposta no Lovable, formul\u00e1rio de aceite, contrato de cliente, pre\u00e7o, escopo, cronograma, SLA ou condi\u00e7\u00f5es comerciais."
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

# Orçamento HAU

Produzir propostas HAU consistentes, técnicas, comerciais e verificáveis sem misturar clientes, inventar termos ou romper o padrão visual e funcional existente.

## Preflight obrigatório

1. Identificar cliente, projeto, decisor, objetivo, escopo, preço e estado atual.
2. Consultar as memórias pertinentes, incluindo o domínio Mnemoverse `project:HAU-Orçamentos`, e separar confirmado, pendente e `A CONFIRMAR`.
3. Ler a proposta atual e os entrypoints das propostas HAU existentes na fonte real. Usar a proposta de Ronei/GrowthSpace como referência forte de padrão quando aplicável, nunca como fonte de conteúdo de outro cliente.
4. Resolver o projeto Lovable e o commit atual pela API/MCP Master. Quando a API estiver disponível, não operar pela UI.
5. Capturar baseline, allowlist de arquivos e contrato de preservação antes de editar.
6. Para texto jurídico ou minuta, acionar o Brabo e manter aviso de revisão por advogado habilitado antes da assinatura.

## Padrão da página

Aplicar o checklist detalhado em [references/padrao-propostas-hau.md](references/padrao-propostas-hau.md).

Toda proposta publicada deve conter, salvo decisão expressa em contrário:

- logo HAU destacado no topo/hero e novamente no rodapé;
- identidade visual HAU vigente, com ícones Lucide semânticos e sem emoji como ícone;
- hero com contexto institucional, título, síntese, badges de decisão e CTA primário de aceite;
- escopo, entregáveis, cronograma, investimento, condições, SLA/suporte, critérios de aceite, responsabilidades, fora de escopo, FAQ e próximos passos quando pertinentes;
- link para contrato/minuta quando existir;
- formulário de aceite funcional no fim da proposta;
- `noindex` e indicação de proposta privada;
- rodapé com HAU e CNPJ vigente confirmado no projeto.

## Formulário de aceite

Reutilizar o `ApprovalForm` compartilhado sempre que possível. Preservar webhook e comportamento existentes, mas permitir copy específica por cliente sem alterar os defaults das propostas antigas.

Exigir:

- nome completo, e-mail e telefone com labels, `required` e `autocomplete` apropriado;
- consentimento comercial e consentimento LGPD separados;
- loading, erro com recuperação e sucesso sem apagar dados em falha;
- prevenção de duplo envio no cliente;
- `proposal`/slug exclusivo e identificável;
- texto de sucesso e próximos passos compatíveis com o cronograma e contrato reais.

Nunca copiar mensagens genéricas como “24 horas”, “início imediato” ou “7 dias úteis” quando não forem verdadeiras para o cliente. Aceite da proposta não substitui contrato quando a proposta disser o contrário.

No QA público, não submeter o formulário nem criar lead, e-mail, card ou webhook real sem autorização específica. Validar estrutura, foco, consentimentos, botão, estados e endpoint por inspeção, mock ou interceptação segura.

## Conteúdo e condições comerciais

- Ser direto, técnico e orientado a decisão.
- Não expor o valor total na primeira dobra por padrão. Conduzir o leitor por diagnóstico, solução e escopo antes da seção de investimento, salvo decisão expressa do usuario.
- Distinguir escopo incluído, dependências do cliente, custos de terceiros e fora de escopo.
- Definir marcos, buffers já embutidos, SLA de primeira resposta, critérios objetivos de aceite e gatilhos de pagamento. Buffers e dias de gordura são planejamento interno: nunca rotular ou expor ao cliente como reserva, folga ou margem operacional.
- Não prometer resultado comercial, tempo real, disponibilidade de terceiro ou efeito jurídico não comprovado.
- Preservar a proposta aprovada como fonte do conteúdo; redesign não autoriza reescrever preço, prazo, escopo, tracking, rotas ou integrações.
- Usar `A CONFIRMAR` em dados jurídicos, contas, responsáveis ou integrações ainda não verificados.

## Edição Lovable

1. Confirmar projeto, workspace, rota, commit e domínio canônico pela API Master.
2. Ler todos os arquivos da rota alvo e os entrypoints das propostas de referência.
3. Definir allowlist antes da primeira mutação.
4. Editar somente arquivos do cliente e componentes compartilhados estritamente necessários, mantendo defaults retrocompatíveis.
5. Revisar o diff contra o baseline; remover qualquer mudança fora da allowlist.
6. Validar preview/build antes do deploy.
7. Publicar somente com OK explícito aplicável ao escopo atual.
8. Fazer readback da URL pública e dos arquivos baixáveis.

## QA mínimo

- desktop e mobile em 320, 375/390, 430, 768, 1024, 1440 e 1920 px quando viável;
- em 320, 375/390 e 430 px, revisar manualmente formulário, consentimentos longos, tabelas, CTAs e títulos; não considerar apenas ausência de overflow global como aprovação mobile;
- logo, hero, ícones, CTA, formulário, contrato e rodapé visíveis;
- sem overflow horizontal, sobreposição ou alvo de toque menor que 44 px;
- foco visível, labels, contraste e ordem semântica adequados;
- botão de aceite rola/foca o formulário correto;
- copy, preço, prazo, pagamentos, escopo e contrato conferidos contra a fonte aprovada;
- outras propostas preservadas por diff e smoke test;
- PDF remoto com status, tipo, tamanho e hash comparados ao local quando aplicável;
- URL pública validada com cache-buster e sem selo Lovable;
- nenhuma submissão real durante QA sem autorização específica.

## Saída

Reportar separadamente:

- `CONFIRMADO`: fonte, build, preview, deploy e readback;
- `CORRIGIDO`: arquivos e comportamentos alterados;
- `PRESERVADO`: rotas, propostas, tracking e integrações fora do escopo;
- `PENDENTE` ou `A CONFIRMAR`: dados ou validações não comprovados.

Nunca declarar concluído apenas porque o agente Lovable respondeu. Exigir diff, build, preview e readback público.
