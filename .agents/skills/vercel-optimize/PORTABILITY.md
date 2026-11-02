# Portability and dependency contract

Status: `adapted_private_config`. Original entry SHA-256: `538de17bbaf4d86d12f08bdd166721e31c964e79d1583f5b785f9c5163d75c27`.

This is source transport, not proof of working credentials, live services, current APIs or installed MCPs. Set USER_WORKSPACE_ROOT, USER_TOOLS_ROOT, USER_PROFILE_ROOT and USER_SERVICE_ROOT privately when referenced. Reserved example domains, zero IDs, user assets and secret placeholders are non-operational. Do not execute sample commands until the actual dependency, input/output contract and consent are verified. No author environment or secret store is supplied or authorized.

Changed executable resources are templates pending user configuration and functional testing, even when syntax passes. AST comparison ignores literal values and does not prove runtime equivalence. No imported script was executed.

Placeholders require explicit template rendering or a local adapter; merely setting environment variables does not interpolate Python/JSON literals. Changed executable templates carry a requires_user_config fail-closed guard. Remove it only after rendering, reviewing distinct resource bindings and validating the configured copy locally.

## Rights

Original authors/notices retained where present. Root project license does not relicense imported works. Unknown is not a fabricated permissive license and is not itself a reason to omit the skill.

Detected license: unknown; no independent license audit.

## Bundled resources (presence only)

- `.agents/skills/vercel-optimize/CONTRIBUTING.md`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/SKILL.md`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/bot-protection-certainty.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/build-minutes-fanout.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/cache-components-suspense-dedupe.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/cache-tag-invalidation-certainty.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/citations.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/cold-start.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/cost-coverage.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/count-correct.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/cwv-poor.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/display-labels.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/edge-heavy-import.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/external-api-slow.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/force-dynamic.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/function-duration-invocations.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/index.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/scanner-driven.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/headers-in-page.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/impact-label.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/impact-magnitude.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/isr-overrevalidation.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/large-static-asset.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/max-age-without-s-maxage.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/middleware-broad-matcher.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/middleware-conflict.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/middleware-heavy.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/missing-cache-headers.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/missing-citation.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/observability-events-attribution.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/platform-bot-protection.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/platform-fluid-compute.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/pre-release.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/prisma-include-tree.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/project-facts.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/queries.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/rate-limit.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/references/doctrine.md`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/region-misconfig.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/region-pin-in-config.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/rendering-mode-mislabel.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/route-errors.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/route-normalize.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/scanner-driven.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/slow-route.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/source-maps-production.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/support-topics.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/sveltekit-prerender-missing.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/throttle.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/turbo-force-bypass.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/uncached-route.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/undeclared-dep.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/unoptimized-image.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/gates/usage-spike-triage.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/scanners/use-cache-date-stamp.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/vercel-directive-strip.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/vercel.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/references/voice.md`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/lib/sanitizers/window-units.mjs`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.
- `.agents/skills/vercel-optimize/SKILL.md`: Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.

## Missing resources and configuration

- `<USER_DEPENDENCY:.test.mjs>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:.vercel/project.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:.vercel/repo.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:Next.js>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:Node.js>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/briefs-manifest.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/budget-summary.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/codebase.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/debug.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/final-message.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/gate.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/investigation-evidence.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/recommendations.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/reconciled-investigation.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/report.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/signals.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/vercel-signals.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:RUN_DIR/verify.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:briefs-manifest.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:briefs/manifest.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:codebase.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:final-message.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:gate.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:index.js>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:investigation-evidence.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:investigation.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:lerna.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:merged.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:next.config.js>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:next.config.mjs>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:next.js>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:package.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:packages/vercel-optimize-tests/test/investigation-brief.test.mjs>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:packages/vercel-optimize-tests/test/support-topics.test.mjs>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:plans/wild-splashing-flamingo.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:pnpm-workspace.yaml>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:project.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:recommendations.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:reconciled-investigation.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:repo.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:report.md>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:signals.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:skills.sh>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:skills/vercel-optimize/scripts/build-docs.mjs>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:skills/vercel-optimize/scripts/check-citations.mjs>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:skills/vercel-optimize/scripts/check-docs-fresh.mjs>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:test/time-window.test.mjs>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:tsconfig.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:turbo.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:vercel-signals.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:vercel.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:verifiedFindings.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:verify.json>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-07fe16a2e935>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-0c0b6c67e84d>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-0e075742498a>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-12d92c73b001>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-1690b9c9c448>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-3219e65a60f5>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-3a5682480fc0>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-3ce7a1b79a73>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-3eb80be33902>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-4b5a05de78cb>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-5285122cb33e>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-5328ffae774b>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-55bb4f0eb8a6>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-5960524de96d>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-5a95023aec96>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-5ed6be86c2fc>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-61e3f53ceb0a>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-67645fafbb97>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-6effd485d37f>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-742d73412c37>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-775dad1c8733>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-7cba1b2254a7>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-80c263a7df25>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-814cc3740b83>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-965c87dc4849>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-a33091ec36c6>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-a3b1f0bdd3fc>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-abe2db695b5c>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-bf2de0f134ae>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-bff2a0837ca0>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-c4bfe7be2ac1>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-cb086b7a47d0>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-d65a33080763>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-e72c0f0c23bb>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-ef792a02ff53>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.
- `<USER_DEPENDENCY:withheld-artifact-f723925de7ad>`: Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.

## File transformations

- `./metadata.json`: structured-json-sanitized
- `./README.md`: service-urls-parameterized, url-review
- `./SKILL.md`: private-memory-pointers-removed
- `./scripts/collect-signals.mjs`: production-ids-parameterized
- `./scripts/deep-dive.mjs`: production-ids-parameterized
- `./references/data-collection.md`: private-memory-pointers-removed, production-ids-parameterized
- `./references/docs-library.json`: structured-json-sanitized
- `./references/observability-plus.md`: private-memory-pointers-removed, url-review
- `./references/verification.md`: private-memory-pointers-removed
- `./references/support-topics/not-found-catchall-request-waste.md`: private-paths-parameterized, url-review
- `./references/support-topics/route-error-durable-offload.md`: service-urls-parameterized, url-review
- `./references/support-topics/workflow-resumable-stream-routes.md`: service-urls-parameterized, url-review
- `./references/playbooks/sveltekit.md`: service-urls-parameterized, url-review
- `./lib/budget-summary.mjs`: private-paths-parameterized
- `./lib/vercel.mjs`: production-ids-parameterized
