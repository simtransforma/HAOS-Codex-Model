# Portability and dependency contract

Status: `adapted_private_config`. Original entry SHA-256: `acf401e6858232b87b3fa79f67ea2d2a2fc9766e11bda38b2fac63dcc893cfa4`.

This is source transport, not proof of working credentials, live services, current APIs or installed MCPs. Set USER_WORKSPACE_ROOT, USER_TOOLS_ROOT, USER_PROFILE_ROOT and USER_SERVICE_ROOT privately when referenced. Reserved example domains, zero IDs, user assets and secret placeholders are non-operational. Do not execute sample commands until the actual dependency, input/output contract and consent are verified. No author environment or secret store is supplied or authorized.

Changed executable resources are templates pending user configuration and functional testing, even when syntax passes. AST comparison ignores literal values and does not prove runtime equivalence. No imported script was executed.

Placeholders require explicit template rendering or a local adapter; merely setting environment variables does not interpolate Python/JSON literals. Changed executable templates carry a requires_user_config fail-closed guard. Remove it only after rendering, reviewing distinct resource bindings and validating the configured copy locally.

## Rights

Original authors/notices retained where present. Root project license does not relicense imported works. Unknown is not a fabricated permissive license and is not itself a reason to omit the skill.

Detected license: unknown; no independent license audit.

## Missing resources and configuration

- `<USER_DEPENDENCY:./scripts/last30days.py>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:./setup.sh>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:assets/aging-portrait.jpeg>`: Not bundled: binary-or-large-artifact-not-audited
- `<USER_DEPENDENCY:assets/claude-code-rap.mp3>`: Missing or intentionally withheld local reference; do not claim this resource is installed.
- `<USER_DEPENDENCY:assets/claude-code-rap.mp3>`: Not bundled: binary-or-large-artifact-not-audited
- `<USER_DEPENDENCY:assets/dog-as-human.png>`: Not bundled: binary-or-large-artifact-not-audited
- `<USER_DEPENDENCY:assets/dog-as-human.png>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:assets/dog-original.jpeg>`: Not bundled: binary-or-large-artifact-not-audited
- `<USER_DEPENDENCY:assets/swimmom-mockup.jpeg>`: Not bundled: binary-or-large-artifact-not-audited
- `<USER_DEPENDENCY:last30days.context.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:local/share/last30days/out/last30days.context.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:model_selection.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:raw_openai.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:raw_reddit_threads_enriched.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:raw_xai.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:report.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:report.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:research.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:tests/test_websearch_weighting.py>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.

## File transformations

- `./README.md`: profile-paths-parameterized, url-review
- `./SKILL.md`: skill-paths-localized
- `./SPEC.md`: skill-paths-localized
- `./plans/feat-add-websearch-source.md`: service-urls-parameterized, url-review
- `./fixtures/models_openai_sample.json`: structured-json-sanitized
- `./fixtures/models_xai_sample.json`: structured-json-sanitized
- `./fixtures/openai_sample.json`: structured-json-sanitized
- `./fixtures/reddit_thread_sample.json`: structured-json-sanitized
- `./fixtures/xai_sample.json`: structured-json-sanitized
