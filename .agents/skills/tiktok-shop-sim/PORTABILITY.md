# Portability and dependency contract

Status: `adapted_private_config`. Original entry SHA-256: `bbacd8105537fddbf8a7de7d05bff21eee14f959b47bd60323defab626b53a9a`.

This is source transport, not proof of working credentials, live services, current APIs or installed MCPs. Set USER_WORKSPACE_ROOT, USER_TOOLS_ROOT, USER_PROFILE_ROOT and USER_SERVICE_ROOT privately when referenced. Reserved example domains, zero IDs, user assets and secret placeholders are non-operational. Do not execute sample commands until the actual dependency, input/output contract and consent are verified. No author environment or secret store is supplied or authorized.

Changed executable resources are templates pending user configuration and functional testing, even when syntax passes. AST comparison ignores literal values and does not prove runtime equivalence. No imported script was executed.

Placeholders require explicit template rendering or a local adapter; merely setting environment variables does not interpolate Python/JSON literals. Changed executable templates carry a requires_user_config fail-closed guard. Remove it only after rendering, reviewing distinct resource bindings and validating the configured copy locally.

## Rights

Original authors/notices retained where present. Root project license does not relicense imported works. Unknown is not a fabricated permissive license and is not itself a reason to omit the skill.

Detected license: unknown; no independent license audit.

## Missing resources and configuration

- `<USER_DEPENDENCY:GUIA_TIKTOK_3_PASSOS.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:capi_assiny.py>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:importador_bling.py>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:importador_tiktok_shop.py>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:prep_ga4.py>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:resposta.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:tiktok_auth.py>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:tiktok_daily.ps1>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.

## File transformations

- `./SKILL.md`: database-config-parameterized, installation-ids-parameterized, private-hosts-parameterized, private-names-parameterized, private-paths-parameterized, production-ids-parameterized, secret-source-configurable, small-resource-ids-parameterized, url-review
- `./evals/evals.json`: structured-json-sanitized
