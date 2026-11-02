# Operacao HAOS com Superpowers

1. Carregar o adaptador antes do workflow upstream.
2. Consultar a matriz de agente/fase no repo canonico.
3. Ler somente as skills pertinentes e incluir paths/motivos na delegacao.
4. Aplicar HAOS quando houver conflito com upstream; preservar instrucoes da plataforma.
5. Revisar pacote staged/unstaged/new contra baseline, sem exigir commit de subagente.
6. Achado real que viole aceite bloqueia conclusao, mesmo apos limite de tentativas.
7. Verificar resultado, fechar via Evoluir e obter readback por destino.

Contrato completo: `${HAOS_PRIVATE_ROOT}`.
Matriz: `${HAOS_PRIVATE_ROOT}`.
Testes: `${USER_PROJECT_ROOT}/scripts/tests/test_haos_superpowers_router.py` e
`${USER_PROJECT_ROOT}/.codex/hooks/tests/test_superpowers_integration.py`.
Upstream: Superpowers 6.3.0; nova versao exige revalidacao e paths existentes.
