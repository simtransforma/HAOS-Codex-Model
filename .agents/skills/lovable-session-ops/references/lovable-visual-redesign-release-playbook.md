# Playbook — redesign visual e release comprovado no Lovable

## Objetivo

Impedir três falhas recorrentes em redesigns: entregar um artefato de apresentação no lugar do site, confundir preview/local com produção e aprovar responsividade apenas por ausência de overflow.

Este playbook complementa `lovable-session-ops`. Publicação continua exigindo autorização explícita do usuario.

## 1. Preflight e fonte de verdade

1. Confirme projeto, workspace, rota pública e mecanismo de edição conforme o roteamento da skill.
2. Dê um nome inequívoco ao conceito solicitado e aos conceitos existentes. Não use apenas “V2” ou “redesign”.
3. Crie a matriz de estado:

| Estado | Prova mínima |
| --- | --- |
| `SOLICITADO` | referência do usuário + critérios semânticos visíveis |
| `LOCAL` | arquivos/assets reais e preview renderizado |
| `PREVIEW` | código do projeto atualizado + build + URL/preview observado |
| `LIVE` | URL pública com cache-buster + bundle/assets + screenshots novas |

4. Se `LOCAL != PREVIEW` ou `PREVIEW != LIVE`, o release está bloqueado. Uma apresentação, PDF, wireframe ou mensagem do agente nunca preenche essas provas nem fecha o caminho crítico.
5. Separe dois gates: `ACEITE_VISUAL` e `AUTORIZACAO_PUBLICAR`. Ambos devem estar aprovados para deploy, mas um não substitui o outro.
6. Registre o candidato com a tupla `concept_id + reference_sha256 + candidate_sha + screenshot_set`.
7. Registre um mapa literal de copy, uma allowlist de mudança e um contrato de preservação antes de editar.

### Manifesto de release por SHA

O manifesto mínimo deve conter:

```yaml
concept_id: nome-inequivoco-do-conceito
reference_sha256: hash-da-referencia-aprovada
candidate_sha: sha-do-codigo-candidato
screenshot_set:
  - viewport: 390x844
    file: caminho-da-captura
  - viewport: 1366x768
    file: caminho-da-captura
allowlist:
  files: []
  literals: []
  behaviors: []
visual_acceptance: pending
publish_authorization: pending
```

Após o deploy, acrescente somente o readback da mesma `candidate_sha`. Se a SHA mudou, é outro candidato e o aceite visual anterior não vale automaticamente.

Template reutilizável: [lovable-visual-release-manifest.example.yaml](lovable-visual-release-manifest.example.yaml).

## 2. Contrato de preservação

Congele e compare antes/depois:

- copy, opções, rotas e destinos;
- API, schema e comportamento de submit;
- UTMs e parâmetros allowlisted;
- tracking existente e atributos necessários;
- consentimento, acessibilidade e estados de erro;
- tags, etapas e códigos de rota, quando fizerem parte do contrato;
- componentes fora do escopo.

Regras:

- A allowlist é criada antes do primeiro patch; não deve ser expandida retroativamente para justificar drift.
- Redesign visual não autoriza GTM, footer, claims, links, tags, eventos ou integrações novas.
- Se o diff contiver item não solicitado, remova-o ou peça decisão explícita antes de publicar.
- Prefira diff por arquivo e por literal protegido. “Build passou” não substitui revisão semântica.

## 3. Implementação do conceito real

1. Gere ou selecione os assets finais para desktop e mobile; não deixe o asset aprovado apenas no pacote local.
2. Integre os arquivos no código real do projeto e confirme que o componente/rota os referencia.
3. Compare screenshot do preview com a referência usando marcos concretos, não apenas paleta ou “sensação”.
4. Para arte com elementos essenciais, defina a zona segura de cada elemento. Não dependa de `cover` sem medir o corte.
5. Preserve DOM semântico e funcionalidade; mudança visual não deve reescrever a jornada.

## 4. Matriz responsiva por largura e altura

O conjunto exato depende do produto, mas a matriz mínima para uma landing com formulário deve cobrir:

| Classe | Viewports mínimas | Assertivas |
| --- | --- | --- |
| telefone compacto | 320×568 | sem overflow; ação inicial alcançável |
| telefone comum | 375×667 e 390×844 | primeiro campo/CTA esperado na primeira dobra |
| telefone amplo | 430×932 | composição e leitura sem vazios artificiais |
| tablet | 768×1024 | transição de layout sem sobreposição |
| notebook baixo | 1024×768 e 1366×768 | elemento visual essencial inteiro; formulário utilizável |
| desktop | 1440×900 | equilíbrio do layout e margens seguras |
| full HD | 1920×1080 | escala sem afastar conteúdo nem cortar arte |

Para cada viewport, registre:

- `scrollWidth == clientWidth`;
- bounding boxes do primeiro campo/CTA e dos elementos visuais essenciais;
- distância do elemento à direita e à base da viewport;
- console, recursos quebrados e estado de carregamento;
- screenshot identificada por viewport e estado (`preview` ou `live`).

O `bbox` focal deve ser comparado com a zona segura definida no manifesto. Para elemento essencial inteiro, exija `left >= 0`, `top >= 0`, `right <= viewportWidth` e `bottom <= viewportHeight`, além das margens mínimas do design.

## 5. Imagens e arte dirigida

- `object-fit: cover` é aceitável somente quando o corte não remove informação essencial.
- Se o elemento essencial precisa ficar inteiro, use uma destas estratégias: asset alternativo por breakpoint, `object-position` comprovado por medição, `contain`, camada DOM separada ou composição com zona segura.
- Em desktop de baixa altura, considere `100svh`/`100dvh` para a camada visual quando o documento for mais alto que a viewport. Valide navegadores suportados e não aplique a regra ao mobile sem necessidade.
- Não declare correção com base apenas em “sem overflow”. O objeto pode estar cortado dentro de um container perfeitamente sem overflow.

## 6. QA sem efeito externo

Para formulários integrados:

1. No live, use somente `GET`/`HEAD` para layout, assets e readback.
2. Valide campos, foco, consentimento, progressão visual e rotas sem submeter dados reais.
3. Use mocks locais, interceptação de rede ou validação estrutural quando disponíveis.
4. Depois de todo reload, navegação, troca de viewport, nova aba/página ou reinício do navegador, reinstale ou reafirme a guarda e faça um teste inofensivo que prove que ela está ativa. Não presuma persistência de interceptor/proxy.
5. Se surgir POST inesperado, pare, registre quantidade/rota sem PII, contenha o efeito, verifique a guarda e só retome após causa definida.
6. Se um POST real for indispensável, trate-o como ação externa e obtenha autorização específica, identidade sintética, limpeza e readback.
7. Nunca use contato real ou gere e-mail/card para provar um ajuste de layout.

### Perfil de navegador

- Use diretório temporário dedicado fora do repositório para `--user-data-dir`.
- Trate o perfil como efêmero e potencialmente sensível; ele não é evidência nem artefato de entrega.
- Garanta ignore preventivo para qualquer fallback sob `runtime/artifacts/**/chrome-profile-*/`.
- Limpeza só pode atingir caminho absoluto previamente verificado e requer o gate aplicável; na dúvida, deixe pendência explícita.

## 7. Gate de publicação

Antes do clique final:

- [ ] conceito solicitado chegou ao código real do projeto;
- [ ] tupla `concept_id + reference_sha256 + candidate_sha + screenshot_set` fechada;
- [ ] aceite visual aprovado para essa tupla;
- [ ] autorização de publicação aprovada separadamente;
- [ ] allowlist prévia comparada ao diff;
- [ ] candidato e live foram nomeados sem ambiguidade;
- [ ] contrato de preservação comparado contra o diff final;
- [ ] nenhum código, claim, tracking ou footer inventado permaneceu;
- [ ] testes, lint/typecheck e build aplicáveis passaram;
- [ ] preview passou na matriz de largura e altura;
- [ ] copy e comportamento protegidos permanecem iguais;
- [ ] autorização explícita cobre esta publicação.

Após publicar:

- [ ] abrir URL pública com cache-buster;
- [ ] identificar bundle/assets live novos;
- [ ] confirmar que o release manifest e o live correspondem à `candidate_sha` aceita;
- [ ] repetir em lote as capturas desktop e mobile;
- [ ] medir novamente primeira dobra e elementos essenciais;
- [ ] validar console/rede sem envio real;
- [ ] confirmar novamente a guarda `GET/HEAD-only` após cada reload usado no QA;
- [ ] registrar versão/deployment no relatório privado, sem expor identificadores em artefatos distribuíveis.

## 8. Hotfix e regressão

1. Faça o menor diff possível e nomeie a causa do defeito.
2. Reexecute a matriz completa em uma rodada batched, mesmo que o patch pareça restrito a uma largura.
3. Corrija todos os defeitos reproduzidos em um único lote.
4. Faça no máximo uma segunda rodada de confirmação, salvo novo bloqueio objetivo.
5. Só encerre com prova live, `P0=0`, `P1=0` no escopo e preservação do contrato.

## 9. Evidência de fechamento

O relatório final deve separar:

- fato observado no live;
- fato documental de build/diff;
- inferência;
- pendência não verificada.

Entrega visual concluída exige simultaneamente: conceito certo, código certo, produção certa e composição funcional nas viewports críticas.

## 10. Promoção de integração autenticada e limites do player

Procedimento observado em 24/09/2026: `runtime/state/box-milhao-publicacao-2026-09-24.md`. Não contém credenciais.

1. Após o deploy autorizado, confirmar publicação, SHA e a cadeia de redirecionamento da URL informada pelo conector. Um domínio próprio já vinculado pode ser o destino canônico; não alterar DNS por causa desse redirecionamento.
2. Verificadores autenticados sem redirects devem apontar diretamente para o destino canônico. Testar credencial válida e inválida sem expor valores; não habilitar redirects como atalho para transportar cabeçalhos entre hosts.
3. Promover somente o campo da URL, comparar o restante do candidato e reler o estado ativo. Confirmar o formulário público com dados sintéticos, consentimento, rota final e UTMs; sucesso em preview não substitui esse teste.
4. Em testes de navegação, aguardar a mudança de URL. Um elemento de status do formulário pode sair do DOM após sucesso; sua ausência não significa que o envio falhou.
5. Para vídeo, separar falha de licença/domínio, carregamento da mídia e compatibilidade de codec. Registrar estados antes/depois da interação identificada. HTTP 200/206 e licença válida não demonstram avanço do tempo; `manifestIncompatibleCodecsError` no ambiente automatizado exige relatar o limite, sem prometer playback não observado.
