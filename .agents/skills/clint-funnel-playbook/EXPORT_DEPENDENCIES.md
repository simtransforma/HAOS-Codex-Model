# Portability, dependencies and provenance

This is a sanitized source port, not proof that integrations work in your environment.
No credentials, production resources, infrastructure configuration or historical cases are supplied.
Imported material is not relicensed by the public repository license. Preserve original author and license notices.

Files ending in .example are NONRUNNABLE SOURCE EXAMPLES: sanitization may change syntax and semantics. Do not rename and run blindly. Commands copied from the procedure that refer to missing helpers are not ready to execute.

## Required Setup

Configure endpoints, credentials and resource identifiers locally. Confirm tool availability and obtain authorization before external effects. Do not execute an unresolved command. Missing files are dependencies, not installed features.

- Dependency ../clint-global/references/jornada-card-pagamento.md -> public-present. File present in the exported package; static presence is not execution verification.
- Dependency references/decide-node.js -> bundled. File present in the exported package; static presence is not execution verification.
- Dependency references/example-ids.md -> bundled. File present in the exported package; static presence is not execution verification.
- Dependency references/jornada-card-pagamento.md -> missing. Not bundled. Supply and review this dependency locally before dependent commands; source presence does not count as delivery.
- Dependency references/workflow-recipe.md -> bundled. File present in the exported package; static presence is not execution verification.
- Dependency RESOURCE_ID -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency ASSINY_UTM_PREFIX -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency CLINT_GROUP_NAME -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency LIA_STAGE_APPROVED -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency LIA_STAGE_PENDING -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency LIA_STAGE_REFUSED -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency LIA_UTM_PREFIX -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency ORIGIN_ABANDONED -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency ORIGIN_APPROVED -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency ORIGIN_PAYMENT_CREATED -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency ORIGIN_REFUSED -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency PAID_TAG_ID -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency TARGET_PRODUCT_ID -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency scripts/wf_edit.py -> missing. Not bundled. Supply and review this dependency locally before dependent commands; source presence does not count as delivery.

## Omitted Artifacts

None.
