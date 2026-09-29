---
name: haos-evidence
description: Verificar entregas, separar fato de inferencia e reportar riscos residuais.
---

# Evidencia antes de conclusao

1. Liste as afirmacoes de conclusao que pretende fazer.
2. Para cada uma, escolha um teste observavel: leitura de diff, teste,
   resposta da API, estado vivo ou readback no destino.
3. Execute o teste no escopo autorizado e leia o resultado.
4. Corrija falhas ou declare a pendencia. Nao invente evidencia.
5. Informe o que passou, o que nao foi testado e o risco residual.

Documentacao e memoria representam contexto, nao substituem verificacao do
estado atual. Um arquivo presente nao prova que um recurso foi carregado.
