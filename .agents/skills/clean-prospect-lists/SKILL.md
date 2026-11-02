---
name: clean-prospect-lists
description: "Audita, higieniza, deduplica, valida, enriquece e prioriza listas de prospecção em Google Sheets, Excel, CSV ou CRM. Use quando uma base comercial estiver desatualizada, incompleta, duplicada, com contatos duvidosos, dados inventados, baixa entregabilidade ou sem segmentação e próxima ação."
---

# Limpar listas de prospecção

Transformar uma base bruta em uma fila comercial confiável, auditável e pronta para execução.

## Fluxo obrigatório

1. Definir objetivo, público ideal, região, oferta e canal de abordagem.
2. Criar backup imutável antes da primeira alteração.
3. Ler todas as abas, cabeçalhos, fórmulas, validações e formatos.
4. Preservar a origem: não apagar histórico; arquivar registros ruins em aba separada.
5. Normalizar antes de enriquecer:
   - remover espaços e caracteres invisíveis;
   - padronizar capitalização, e-mail, telefone, cidade, UF, categoria e status;
   - separar títulos, subtítulos e linhas vazias dos registros reais.
6. Deduplicar antes de gastar créditos ou pesquisar:
   - mesclar automaticamente somente por chave forte: e-mail exato, telefone exato ou identificador oficial;
   - usar nome normalizado + empresa/local como candidato;
   - enviar correspondência fuzzy para revisão, nunca para mescla cega;
   - preservar origem, histórico, opt-out e o valor mais completo de cada campo.
7. Validar em camadas:
   - sintaxe do e-mail;
   - existência do domínio e resposta pública do site;
   - compatibilidade entre nome, setor, localização e site oficial;
   - formato do telefone e sequências com aparência de placeholder;
   - existência do perfil social somente quando houver evidência pública.
8. Enriquecer apenas registros que cabem no público ideal:
   - preferir site oficial, diretórios públicos confiáveis e perfis institucionais;
   - adicionar URL da fonte e data de verificação;
   - não inventar e-mail, telefone, cargo, empresa ou pessoa;
   - marcar lacunas como ausentes ou pendentes.
9. Pontuar fit, evidência e acionabilidade. Separar:
   - prioridade A: alto fit e evidência suficiente;
   - prioridade B: bom fit, exige confirmação leve;
   - prioridade C: baixo fit ou contato incompleto;
   - revisar/arquivar: evidência conflitante, domínio inativo, duplicidade ou sem canal utilizável.
10. Entregar abas claras:
   - LEIA PRIMEIRO;
   - BASE ATIVA;
   - REVISAR E ARQUIVAR;
   - DUPLICIDADES;
   - LOG E METODOLOGIA;
   - listas auxiliares para validações.
11. Verificar contagens, fórmulas, filtros, datas, telefones, links, clipping e formatação.
12. Relatar o antes/depois com totais exatos e limitações.

## Semântica de validação

- Domínio ativo prova somente que o domínio existe tecnicamente.
- Caixa verificada exige um verificador de e-mail próprio; não inferir por DNS ou site.
- Telefone com formato válido não prova que a linha está ativa.
- Validado por domínio público significa que a fonte pública é compatível com a organização; confirmar o contato antes do envio.
- Não encontrado significa ausência de evidência, não inexistência definitiva.

## Segurança e conformidade

- Respeitar opt-out, listas de não contato e minimização de dados.
- Não reativar quem pediu remoção.
- Não coletar dados pessoais privados ou contornar autenticação.
- Não automatizar disparos durante a limpeza.
- Manter fonte e data para todo dado enriquecido.

## Recursos

- Ler [references/methodology.md](references/methodology.md) para critérios de fonte, pontuação e metas de qualidade.
- Executar scripts/audit_prospect_list.py para um diagnóstico reprodutível de CSV/XLSX antes da limpeza manual.

## Exemplos

- “Limpe esta planilha de patrocinadores, retire duplicados e diga quem vale abordar.”
- “Valide os contatos desta lista sem inventar dados e separe os que precisam de pesquisa.”
- “Enriqueça somente os leads com alto fit e deixe fonte e data de verificação.”

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
