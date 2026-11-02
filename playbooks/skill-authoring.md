# Autoria original de skills

## Plano de autoria

Nomear a lacuna, publico, gatilho, owner, arquivos e aceite. Consultar o catalogo
por metadados antes de abrir fontes selecionadas. Catalogo privado nao concede
licenca nem autorizacao de distribuicao. Preferir melhorar um recurso existente.

Para cada fonte registrar origem acessivel ao revisor autorizado, tipo de uso,
direitos conhecidos, limite e decisao. No publico usar apenas localizadores
publicos ou referencias internas seguras; nenhum caminho/dado privado.
Se direitos nao estiverem claros, nao copiar texto, exemplos, personas ou assets.
Sintetizar apenas ideias gerais e requisitos autorizados em formulacao propria.

## Contrato do arquivo

- Pasta e frontmatter name identicos; nome em minusculas, numeros e hifens.
- Description descreve quando usar, nao substitui leitura do corpo.
- Corpo define entradas, procedimento, saida, aceite, limites e falhas.
- Paths locais relativos; ferramentas opcionais nunca presumidas instaladas.
- Um exemplo seguro, com dados ficticios e sem segredos.
- Referencias complementares somente quando pertinentes e realmente existentes.

O adaptador haos-superpowers precede metodos auxiliares. A orientacao de
writing-skills foi usada por sintese, sem redistribuir o upstream. Ela nao
autoriza commit, instalacao, descarte de trabalho, worktree obrigatorio ou
publicacao. Pedido/HAOS subordinam-se a instrucoes superiores da plataforma.

## Verificacao antes e depois

Antes da escrita, verificar lacunas do arquivo e escolher cenarios de pressao.
Depois, validar frontmatter, caminhos, dependencias, limites e saidas observaveis.
Verificar cada skill alterada; nao chamar presenca de palavras de teste
comportamental. So afirmar RED/GREEN de agente quando houver execucao real dos
mesmos cenarios sem/com a skill e leitura dos resultados.

Para regras condicionais, testar ambos os ramos: destino enabled/disabled,
AUDIT/APPLY, dado confiavel/nao confiavel, tarefa financeira/nao financeira.
Para instrucoes de disciplina, combinar pressao de prazo com historico hostil e
resultado parcial. Ausencia de falha na baseline nao demonstra ganho causal.
Um teste manual de cenarios nao e benchmark nem garante aderencia futura.

## Aceite de distribuicao

Revisor distinto le o pacote inteiro, incluindo arquivos novos e sem commit,
e confere escopo/direitos/privacidade. Autor corrige; revisor repete checks
afetados. Registrar testes nao executados e cobertura residual. Nao distribuir
conteudo sem licenca verificada nem usar sucesso estatico como prova de runtime.
