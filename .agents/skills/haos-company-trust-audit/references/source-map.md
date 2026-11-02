# Source Map

Use fontes publicas e legais. Priorize fonte primaria quando existir.

## Brasil

### Identidade juridica

- Receita Federal / Gov.br: CNPJ, razao social, situacao cadastral, CNAE, abertura, quadro societario quando disponivel.
- Junta Comercial estadual: atos societarios, alteracoes e registro mercantil quando publico.
- Diario Oficial: publicacoes societarias, sancoes, licitacoes e atos publicos.
- Portal da Transparencia: CEIS, CNEP, acordos e sancoes contra empresas quando aplicavel.

### Reguladores por setor

- Banco Central: instituicoes financeiras, autorizacoes e consorcios.
- CVM: companhias abertas, intermediarios, ofertas e processos administrativos.
- SUSEP: seguros, previdencia aberta, capitalizacao e corretores.
- ANS: planos de saude.
- ANATEL: telecom.
- ANVISA: saude, alimentos, cosmeticos, medicamentos.
- e-MEC / MEC: instituicoes e cursos de educacao superior.
- MAPA, ANTT, ANAC, ANP ou agencia setorial quando a categoria exigir.

### Reclamacoes e consumidor

- Consumidor.gov.br: empresas participantes, volume, resposta e satisfacao.
- Procon estadual/municipal quando houver consulta publica.
- Reclame Aqui: reputacao, volume, tipo de reclamacao, resposta e recorrencia. Tratar como fonte social/privada-publica, nao oficial.
- Google Maps, lojas de app, marketplaces e redes sociais: usar como observacao agregada.

### Processos e risco juridico

- Tribunais oficiais: TJ, TRF, TRT/TST, STJ, STF, PJe, e-SAJ ou portal local.
- JusBrasil e agregadores: usar apenas como ponte de descoberta; confirmar em fonte oficial quando possivel.

## Internacional

- SEC EDGAR: empresas listadas nos EUA.
- Companies House: empresas do Reino Unido.
- Registros estaduais/mercantis do pais de origem.
- OFAC, UN Security Council Consolidated List e EU Sanctions Map: sancoes.
- Better Business Bureau, Trustpilot, G2, Capterra, app stores e marketplaces: reputacao e padroes de review.
- ICANN Lookup/RDAP: dominio, registrador, idade, nameservers e sinais de ocultacao normal vs suspeita.

## Website e seguranca basica

- Dominio: idade, mudancas recentes, registrador, HTTPS, correspondencia entre dominio e marca.
- Site: razao social, CNPJ/registro, endereco comercial, politica de privacidade, termos, canais de suporte, politica de reembolso.
- Pagamento: gateway conhecido, antifraude, transparencia de cobranca, recorrencia e cancelamento.
- Comunicacao: promessas, garantias, depoimentos, logos de clientes e certificacoes; verificar claims centrais.

## Query plan base

Adaptar por pais e setor:

- `"[empresa]" CNPJ`
- `"[empresa]" reclame aqui`
- `"[empresa]" consumidor.gov`
- `"[empresa]" procon`
- `"[empresa]" processo`
- `"[empresa]" golpe OR fraude OR reclamação`
- `"[empresa]" reviews OR complaints OR scam`
- `site:gov.br "[empresa]"`
- `site:jus.br "[empresa]"`
- `"[dominio]" whois OR rdap`
- `"[empresa]" terms privacy refund`

## Qualidade das fontes

- Oficial/regulatoria: alta.
- Documento legal/processual oficial: alta, mas interpretar com cautela.
- Review agregado com volume: medio-alto.
- Post isolado: baixo a medio.
- Blog afiliado, lista de "melhores" e SEO spam: baixo, usar com vies declarado.
- Conteudo sem data/autoria: fraco.
