# SIM-Dash: especificacao de build (Fase 3)

Referencia da identidade visual, layout, tema e estrutura de dados do HTML SIM-Dash.
O HTML e unico e self-contained: Chart.js via CDN, dados embutidos no objeto `DATA`,
logos em base64. SEM travessao. SEM GTM (dash interna).

## Template reutilizavel

Arquivo: `workspace\dev-frontend\out\dash-vendas\sim-dash-template.html`

Para uma nova dash de um novo periodo: **editar somente o objeto `DATA`** (e o
periodo/rodape). Nao reescrever a estrutura HTML/CSS/JS. As logos base64 ja ficam
embutidas no template.

## Paleta / identidade

| Token | Valor | Uso |
|---|---|---|
| Azul SIM | `#1E9BF0` | acento, barras de chart, links, destaque do total |
| Navy | `#1B2A3A` | texto no tema claro, fundo no tema escuro |
| (tema claro) fundo | branco / cinza muito claro | superficie |
| (tema escuro) fundo | navy `#1B2A3A` (e variacoes) | superficie |

- Tema **claro**: fundo claro, texto navy, logo variante **clara** (texto navy).
- Tema **escuro**: fundo navy, texto branco, logo variante **escura** (texto branco).

## Logos

- Pasta: `${USER_WORKSPACE_ROOT}`
  - variante **clara** -> usar no tema CLARO (texto navy).
  - variante **escura** -> usar no tema ESCURO (texto branco).
- Otimizar com **Pillow** (reduzir dimensao/peso) antes de embutir.
- Embutir as DUAS variantes em **base64** no HTML (data URI). O JS troca o `src`
  conforme o tema.
- As logos precisam estar em **ARQUIVO no disco**. Anexo de chat nao serve para
  embutir.

## Toggle de tema

- Botao de toggle claro/escuro.
- **Default: dark** (escuro).
- Persistir a escolha em `localStorage` (ex.: chave `sim-dash-theme`).
- Ao trocar de tema: trocar a logo (clara/escura) e **re-renderizar os charts** com
  as cores de eixo/grid/legenda do tema (Chart.js: atualizar `options.scales` e
  `options.plugins.legend.labels.color`, depois `chart.update()` ou recriar).

## Responsividade

Breakpoints:

- `920px`: layout de cards/colunas colapsa para grid mais estreito.
- `560px`: layout de coluna unica, tabelas com scroll horizontal se preciso, charts
  reduzem altura.

## Estrutura do objeto `DATA`

O `DATA` carrega tudo que a UI renderiza. Forma sugerida:

```js
const DATA = {
  periodo: { label: "09/06/2026", inicio_brt: "2026-06-09 00:00", fim_brt: "2026-06-09 23:59", fuso: "America/Sao_Paulo (UTC-3)" },
  total_geral: { qtd: 0, valor: 0 },          // so vendas pagas
  plataformas: [
    {
      nome: "Bling",
      qtd: 0, valor: 0,                         // subtotal plataforma
      base_valor: "pago pelo cliente",         // para a nota de bases mistas
      ofertas: [
        {
          nome: "Oferta X",
          qtd: 0, valor: 0,                     // subtotal oferta
          utms: [
            { source: "", medium: "", campaign: "", qtd: 0, valor: 0 }  // folha
          ]
        }
      ]
    }
    // ... demais plataformas
  ],
  a_parte: {                                    // NUNCA somar no total_geral
    pendentes: { qtd: 0, valor: 0 },
    reembolsos: { qtd: 0, valor: 0 }
  },
  notas: [
    "Bases de valor mistas: Assiny/Asaas liquido, Bling pago pelo cliente, LIA caixa.",
    "Periodo no fuso America/Sao_Paulo (UTC-3); APIs convertidas de UTC."
  ]
};
```

## Componentes da UI (minimo)

1. **Header**: logo (troca por tema) + titulo "SIM-Dash" + label do periodo + toggle tema.
2. **Cards de KPI**: Total geral (qtd + R$ <USER_AMOUNT>em destaque azul), e cards por plataforma.
3. **Chart por plataforma**: barras (R$ por plataforma) via Chart.js.
4. **Chart por oferta** (top ofertas) ou por UTM source, opcional.
5. **Tabela hierarquica**: PLATAFORMA > OFERTA > UTM com qtd e R$ <USER_AMOUNT>subtotais e TOTAL GERAL.
6. **Bloco "a parte"**: pendentes e reembolsos (separados, nao somam no total).
7. **Rodape**: notas de bases mistas + fuso usado no corte. SEM travessao.

## Regras finais do build

- Zero travessao (`—`), zero `–`, `…`, aspas/apostrofo curvos.
- Sem GTM, sem pixel, sem tracking (dash interna).
- Tudo embutido (Chart.js via CDN e a unica dependencia externa).
- Validar visualmente nos dois temas e nos dois breakpoints antes do deploy.

