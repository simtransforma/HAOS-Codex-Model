---
name: limpar-lista-contatos
description: "Limpa e normaliza listas de contatos de planilhas (Excel/CSV) gerando CSV pronto com nome, email e numero. Use quando o usuario pedir para \"limpar lista\", \"tratar planilha de contatos\", \"normalizar telefone/numero\", \"tirar formatacao dos numeros\" (espaco, parenteses, hifen), \"padronizar telefone com 55 / DDI\", \"gerar CSV de disparo ou importacao\" (WhatsApp, CRM, email marketing) ou \"converter aba de Excel em CSV de contatos\". Normaliza o telefone para o padrao E.164 brasileiro sem o sinal de mais (ex: 5511914103783)."
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

# Limpar Lista de Contatos

Transforma uma planilha baguncada (Excel ou CSV) em um CSV limpo de `nome,email,numero`, com o telefone normalizado para `55 + DDD + numero` (padrao E.164 sem o "+").

## Quando usar
- "Limpa essa lista pra mim", "trata essa planilha de contatos"
- "Poe os numeros no padrao 5511914103783"
- "Tira o parenteses e o espaco dos telefones e bota 55 na frente"
- "Gera um CSV pra importar no WhatsApp / CRM / email marketing"

## Regra de normalizacao do telefone (mecanica, NAO inventa nada)
1. Remove tudo que nao e digito: espaco, `( )`, `-`, `.`, `+`, etc.
2. Remove prefixo de discagem internacional `00` no inicio, se houver.
3. Remove o `0` de troncal do DDD no inicio, se houver (ex: `011` vira `11`).
4. Se ja comeca com o codigo do pais e tem 12+ digitos, mantem como esta.
5. Senao, prefixa o codigo do pais (default Brasil `55`).

Importante: e limpeza de FORMATO, nao auditoria. Nao valida se o DDD existe, nao adiciona nem remove o nono digito, nao corrige numero torto. O que entra sujo de formatacao sai limpo; o que entra com digito errado na origem continua com o digito errado (isso se resolve na fonte do dado, nao aqui).

## Como rodar
Script: `./scripts/limpar_lista.py` (Python 3 + pandas + openpyxl).

```
python scripts/limpar_lista.py ENTRADA [opcoes]

  --sheet ABA         processa uma aba especifica (Excel)
  --all-sheets        processa todas as abas, gera um CSV por aba
  --out SAIDA.csv     arquivo de saida (default: <entrada>_<aba>.csv)
  --nome COL          forca o nome da coluna de nome  (senao auto-detecta)
  --email COL         forca o nome da coluna de email (senao auto-detecta)
  --fone COL          forca o nome da coluna de telefone (senao auto-detecta)
  --country 55        codigo do pais (default 55 Brasil)
  --dedup             remove telefones duplicados
  --keep-cols         mantem so nome,email,numero (default ja faz isso)
```

### Exemplos
```
# uma aba especifica para um arquivo nomeado
python scripts/limpar_lista.py base.xlsx --sheet Master --out Master_PNL.csv

# todas as abas de uma vez (um CSV por aba)
python scripts/limpar_lista.py base.xlsx --all-sheets

# CSV de entrada, forcando a coluna de telefone
python scripts/limpar_lista.py contatos.csv --fone Celular --out limpo.csv --dedup
```

## Saida
CSV em UTF-8 com BOM (abre com acento certo no Excel PT-BR), colunas `nome,email,numero`. O script imprime no fim: quantas linhas saiu, quais colunas usou e quantos ficaram sem numero.

## Auto-deteccao de colunas
Reconhece headers comuns sem precisar configurar:
- nome: nome, name, cliente, contato, nome completo
- email: email, e-mail, mail
- telefone: numero, telefone, celular, whatsapp, fone, tel, mobile, phone
Se nao achar a coluna de telefone, ele para e pede `--fone NOME_DA_COLUNA`.

## Boas praticas aprendidas (referencia)
- Guardar sempre em E.164 (`55...`) e exibir em formato local so quando precisar.
- Deduplicar pelo telefone normalizado evita disparar pro mesmo contato duas vezes.
- Para validacao forte (DDD real existe, linha movel x fixa, portabilidade), usar a lib `phonenumbers` (Google libphonenumber). Esta skill faz limpeza de formato, nao validacao de existencia.
- Numero so vira discavel/WhatsApp com pais + DDD + assinante completos. Se a planilha de origem perdeu o DDD, nenhuma limpeza recupera; tem que voltar na fonte e exportar a coluna como TEXTO (nao numero), senao a planilha come zeros e desloca digitos.

