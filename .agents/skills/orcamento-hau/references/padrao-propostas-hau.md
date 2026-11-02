# Padrão das propostas HAU

## Estrutura visual e funcional

1. Hero imersivo em `bg-gradient-hero` com logo HAU central e destacado.
2. Identificação institucional em pill discreta.
3. Um único H1, benefício/resultado real e subtítulo técnico curto.
4. Três ou quatro badges com ícones Lucide para prazo, escopo, suporte ou condição.
5. CTA primário `Aprovar proposta`; CTA secundário para contrato/PDF; impressão como ação terciária.
6. Seções com ritmo HAU, títulos fortes, ícones semânticos e cards somente quando o conteúdo justificar agrupamento.
7. Investimento e pagamentos com valores, percentuais, marcos e custos de terceiros explícitos somente na seção de investimento; não antecipar o valor total no hero por padrão.
8. Critérios de aceite objetivos separados de linguagem comercial.
9. Formulário de aceite antes do rodapé.
10. Rodapé com logo, proposta privada e CNPJ confirmado.

## Matriz de conteúdo

| Bloco | Conteúdo mínimo |
| --- | --- |
| Diagnóstico/objetivo | problema, resultado esperado e limites |
| Escopo | entregas verificáveis e quantidades |
| Jornada | fases, dependências e responsáveis |
| Cronograma | Gate 0, marcos, buffers embutidos e aceite |
| Investimento | total, parcelas, gatilhos e terceiros |
| SLA/suporte | canal, horário, primeira resposta, franquia e exclusões |
| Governança | acessos, dados, segurança, mudanças e handoff |
| Fora de escopo | itens excluídos e mecanismo de aditivo |
| Contrato | status da minuta, download e próximos passos |
| Aceite | identidade, consentimentos, slug e confirmação específica |

## Contrato de preservação

Antes de editar, congelar:

- rota e slug;
- copy comercial aprovada;
- preço, parcelas e datas;
- contrato/PDF e nome do arquivo;
- webhook e schema de aceite;
- pixels, GTM, Clarity e atributos de tracking;
- demais propostas e componentes compartilhados fora da allowlist.

## Aceite visual

- logo HAU reconhecível na primeira dobra;
- CTA primário visível e ligado ao formulário;
- ícones consistentes com Lucide;
- leitura clara em 390×844 e 1440×900;
- formulário revisado também em 320, 375 e 430 px, com consentimentos em grade de checkbox fixo + texto flexível, alvos de toque de 44 px e nenhuma quebra ou alinhamento torto;
- formulário com estados inicial, inválido, processando, erro e sucesso;
- sem mensagens herdadas de outro cliente;
- nenhum conteúdo de uma proposta inserido em outra.

## Gate de publicação

Publicar somente quando o mesmo candidato tiver:

- diff restrito à allowlist;
- build/preview aprovado;
- QA desktop/mobile sem P0/P1;
- autorização externa vigente;
- readback do domínio canônico após deploy.
