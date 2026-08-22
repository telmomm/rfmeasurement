# ADR 0003: License the project under BSD-3-Clause

- Status: accepted
- Date: 2026-08-22

## Context

JOSS requires an OSI-approved license (see
[joss-strategy.md](../joss-strategy.md)). The project builds on
`scikit-rf`, which is itself BSD-licensed, and more broadly on the
scientific Python ecosystem (numpy, scipy), which favors permissive
BSD-style licenses.

## Problem

Which OSI-approved license should govern the project?

## Alternatives

1. MIT — permissive, minimal text.
2. BSD-3-Clause — permissive, includes a non-endorsement clause,
   consistent with the license used by `scikit-rf` and most of the
   scientific Python stack.
3. Apache-2.0 — permissive, adds an explicit patent grant, more text.

## Decision

BSD-3-Clause, matching the convention of the scientific Python ecosystem
this project builds on.

## Consequences

- Full license text lives in [LICENSE](../../LICENSE) at the repository
  root, satisfying the JOSS "open source" requirement.
- Consistent with `scikit-rf`'s license, simplifying any future
  redistribution questions.
- No explicit patent grant (unlike Apache-2.0); considered acceptable
  given the scientific/academic nature of the project.
