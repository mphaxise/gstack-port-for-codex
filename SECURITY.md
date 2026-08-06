# Security

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting for this repository when
available. Do not open a public issue containing credentials, private prompts,
local memory, personal data, or an exploitable proof of concept.

If private reporting is unavailable, open a minimal public issue that asks for
a private contact path and contains no sensitive details.

## Scope and privacy

This package contains workflow instructions and local validation helpers. It is
not a sandbox, credential manager, or production security boundary. Review a
skill before installing it, especially when it refers to browser sessions,
automations, external tools, or local files.

The generated GBrain corpus is ignored by Git. Do not commit it or any other
private source material. The public-boundary check rejects known private
operating paths and common credential formats.

The upstream drift checker contacts GitHub when explicitly run. Review the
network and token behavior in `src/gstack_port_for_codex/upstream_drift.py`
before running it in a restricted environment.
