# Portability and dependency contract

Status: `adapted_private_config`. Original entry SHA-256: `a07c77cc0f6598c2982280bf6604f86f581167cbd7ba7e29c3f5e0cd342a2f5f`.

This is source transport, not proof of working credentials, live services, current APIs or installed MCPs. Set USER_WORKSPACE_ROOT, USER_TOOLS_ROOT, USER_PROFILE_ROOT and USER_SERVICE_ROOT privately when referenced. Reserved example domains, zero IDs, user assets and secret placeholders are non-operational. Do not execute sample commands until the actual dependency, input/output contract and consent are verified. No author environment or secret store is supplied or authorized.

Changed executable resources are templates pending user configuration and functional testing, even when syntax passes. AST comparison ignores literal values and does not prove runtime equivalence. No imported script was executed.

Placeholders require explicit template rendering or a local adapter; merely setting environment variables does not interpolate Python/JSON literals. Changed executable templates carry a requires_user_config fail-closed guard. Remove it only after rendering, reviewing distinct resource bindings and validating the configured copy locally.

## Rights

Original authors/notices retained where present. Root project license does not relicense imported works. Unknown is not a fabricated permissive license and is not itself a reason to omit the skill.

Detected license: unknown; no independent license audit.

## Missing resources and configuration

- `<USER_DEPENDENCY:YOUTUBE_CHANNEL_INVENTORY>`: User-owned channel inventory, OAuth identity, allowed source media, and consent must be provided privately.
- `<USER_DEPENDENCY:deploy/youtube-live-sim/README.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:docs/YOUTUBE_LIVE_SIM_PILOTO_2026-09-28.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:references/canais.md>`: Missing or intentionally withheld local reference; do not claim this resource is installed.
- `<USER_DEPENDENCY:references/canais.md>`: Not bundled: personal-channel-and-live-inventory; configure owned channels using channels.list(mine=true)
- `<USER_DEPENDENCY:references/canais.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.

## File transformations

- `./SKILL.md`: private-names-parameterized, private-paths-parameterized, url-review
- `./references/live-api.md`: channel-ids-parameterized, private-names-parameterized, url-review
