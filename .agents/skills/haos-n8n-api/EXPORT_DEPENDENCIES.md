# Portability, dependencies and provenance

This is a sanitized source port, not proof that integrations work in your environment.
No credentials, production resources, infrastructure configuration or historical cases are supplied.
Imported material is not relicensed by the public repository license. Preserve original author and license notices.

Files ending in .example are NONRUNNABLE SOURCE EXAMPLES: sanitization may change syntax and semantics. Do not rename and run blindly. Commands copied from the procedure that refer to missing helpers are not ready to execute.

## Required Setup

Configure endpoints, credentials and resource identifiers locally. Confirm tool availability and obtain authorization before external effects. Do not execute an unresolved command. Missing files are dependencies, not installed features.

- Dependency ../../../playbooks/n8n-voice-runtime-validation.md -> missing. Not bundled. Supply and review this dependency locally before dependent commands; source presence does not count as delivery.
- Dependency references/api.md -> bundled. File present in the exported package; static presence is not execution verification.
- Dependency scripts/RESTORE-RUNBOOK.md -> missing. Not bundled. Supply and review this dependency locally before dependent commands; source presence does not count as delivery.
- Dependency scripts/n8n-backup.sh -> missing. Not bundled. Supply and review this dependency locally before dependent commands; source presence does not count as delivery.
- Dependency scripts/wf_edit.py -> missing. Not bundled. Supply and review this dependency locally before dependent commands; source presence does not count as delivery.
- Dependency HAOS_PRIVATE_ROOT -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency RESOURCE_ID -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency USER_BRAND -> user-config-required. Set locally outside the public repository; never put secrets or production identifiers in examples.
- Dependency scripts/wf_edit.py -> nonrunnable-example. Only a sanitized .example is delivered. Review configuration and semantics, restore valid syntax, test in isolation and obtain authorization before use. Not a working helper.

## Omitted Artifacts

- scripts/__pycache__: generated-or-dependency-cache
