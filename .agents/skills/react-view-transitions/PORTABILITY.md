# Portability and dependency contract

Status: `adapted_private_config`. Original entry SHA-256: `2cf9ce07c43be50ff5d43d5bedd73054969a98cedcf0f297623b1b4a8ef0d6ae`.

This is source transport, not proof of working credentials, live services, current APIs or installed MCPs. Set USER_WORKSPACE_ROOT, USER_TOOLS_ROOT, USER_PROFILE_ROOT and USER_SERVICE_ROOT privately when referenced. Reserved example domains, zero IDs, user assets and secret placeholders are non-operational. Do not execute sample commands until the actual dependency, input/output contract and consent are verified. No author environment or secret store is supplied or authorized.

Changed executable resources are templates pending user configuration and functional testing, even when syntax passes. AST comparison ignores literal values and does not prove runtime equivalence. No imported script was executed.

Placeholders require explicit template rendering or a local adapter; merely setting environment variables does not interpolate Python/JSON literals. Changed executable templates carry a requires_user_config fail-closed guard. Remove it only after rendering, reviewing distinct resource bindings and validating the configured copy locally.

## Rights

Original authors/notices retained where present. Root project license does not relicense imported works. Unknown is not a fabricated permissive license and is not itself a reason to omit the skill.

Detected license: unknown; no independent license audit.

## Missing resources and configuration

- `<USER_DEPENDENCY:Next.js>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:next.config.js>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:skills.sh>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.

## File transformations

- `./metadata.json`: structured-json-sanitized
- `./README.md`: service-urls-parameterized, url-review
