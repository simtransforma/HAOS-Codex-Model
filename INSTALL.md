# Instalacao

Este modelo e intencionalmente manual: nao sobrescreve `config.toml`, hooks,
credenciais ou politicas existentes.

1. Copie `AGENTS.md`, `.agents/skills/` e `memory/` para o projeto desejado.
2. Revise o texto e os arquivos auxiliares de cada skill antes de executar.
3. Para usar os agentes, copie os TOML de `.codex/agents/` para um diretorio
   privado de configuracao e registre cada papel no `config.toml` existente.
   Exemplo, substituindo o caminho absoluto pelo seu:

```toml
[agents.qa-reviewer]
description = "Revisao independente de qualidade e testes"
config_file = "/caminho/absoluto/qa-reviewer.toml"
```

4. Faca merge cuidadoso: preserve provider, MCPs, politicas, memoria e hooks
   ja existentes. Nao copie uma configuracao inteira por cima da sua.
5. Confirme no prompt/diagnostico do seu Codex que skills e agentes foram
   carregados; depois execute uma tarefa de teste sem efeitos externos.

Este modelo nao configura memoria remota, LLM, broker, RAG, rede ou automacao.
Essas conexoes exigem projeto e identidade proprios.
