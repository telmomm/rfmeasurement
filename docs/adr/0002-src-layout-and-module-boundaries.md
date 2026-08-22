# ADR 0002: Use a `src/` layout with domain-first module boundaries

- Status: accepted
- Date: 2026-08-22

## Context

The project needs a package layout that (a) avoids accidental imports
from an unbuilt repository root during development, and (b) keeps
scientific domain code decoupled from I/O and instrument-specific code,
per the layered architecture in [architecture.md](../architecture.md).

## Problem

How should the package be laid out on disk, and how should modules be
divided?

## Alternatives

1. Flat layout (`rfmeasurement/` at repository root).
2. `src/` layout with a single flat module.
3. `src/` layout with modules split by architectural layer
   (`domain`, `io`, `validation`, `uncertainty`, `provenance`,
   `analysis`, `reporting`, `integrations`).

## Decision

Option 3, as proposed in
[repository-organization.md](../repository-organization.md). The
dependency direction is `external tools -> adapters -> domain ->
scientific engines -> reports`; the scientific core (`domain`,
`validation`, `uncertainty`) must not import from `io` or
`integrations`.

## Consequences

- `pip install -e .` cannot accidentally pick up an unbuilt package from
  the repository root.
- Module boundaries make the "core must not depend on instrument code"
  rule enforceable (e.g. via import-linter in CI, to be added later).
- Exact submodule names may still change after prototyping, as noted in
  architecture.md; this ADR fixes the layering principle, not every
  final name.
