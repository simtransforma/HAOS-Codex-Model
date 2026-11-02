# Playbook de prospecção ativa

## ICP e fontes

Priorize fontes que já façam uma curadoria setorial: associações, sindicatos, film commissions, entidades de ensino e diretórios institucionais. Confirme o candidato no site oficial antes de qualificá-lo.

Hierarquia de fonte:

1. Site oficial da conta.
2. Diretório ou associação setorial oficial.
3. Governo, universidade ou entidade profissional.
4. Perfil institucional público.
5. Diretório comercial, somente como pista.

## Score de 100 pontos

| Sinal | Pontos |
|---|---:|
| Categoria e oferta compatíveis | 30 |
| Região prioritária | 20 |
| Associação ou site oficial confirma a conta | 20 |
| Canal institucional público (e-mail, telefone ou formulário) | 15 |
| Site acessível e coerente | 10 |
| Sinal de interesse no ecossistema/eventos | 5 |

`A` começa em 75; `B`, 50; `C`, 30. Sem URL oficial ou fonte setorial, aplicar teto `C`.

## Campos mínimos para inclusão

- nome;
- categoria;
- cidade e UF quando a fonte permitir;
- site ou fonte pública;
- data de verificação;
- origem e próxima ação.

## Modelo de lote

| Campo | Valor esperado |
|---|---|
| Origem | `Prospecção ativa — [fonte] — AAAA-MM-DD` |
| Validação do registro | `Validado por diretório setorial público` ou `Validado por site oficial` |
| Status de trabalho | `Não iniciado` |
| Próxima ação | `Personalizar abordagem e contatar` ou `Localizar canal público` |

## Referências abertas consultadas

- Sales Skills — sequência prospect list → enrich → deliverability → cadence: https://github.com/sales-skills/sales
- Goose Skills — pipeline de prospecção de eventos e qualificação de leads: https://github.com/gooseworks-ai/goose-skills
- Ironclaw — etapas de CRM, enriquecimento e gestão de pipeline: https://github.com/contains-studio/ironclaw

## Guardrail para eventos setoriais

Quando a prospecção for para um evento local ou setorial:

- confirme cidade-sede, região operacional e ICP antes de expandir a busca;
- não assuma capital ou polo amplo como prioridade se o evento estiver em cidade específica;
- trate cursos, portais, marketplaces e diretórios como fontes de garimpo, não como leads finais, salvo se o objetivo for parceria institucional;
- redes sociais públicas como Instagram e LinkedIn servem como pista institucional e personalização humana; não automatize convite, DM, scraping agressivo ou disparo;
- não suba lista de contatos públicos garimpados como Customer List/público personalizado sem consentimento ou base legal adequada; prefira públicos salvos, engajamento próprio, visitantes do site e bases opt-in;
- em cada lote, marque a fila com status claro: promovido, duplicado, descartar, revisar, pendente de validação.
