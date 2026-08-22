# ADR 0004: Support Python 3.10-3.13

- Status: accepted
- Date: 2026-08-22

## Context

The roadmap requires defining supported Python versions as part of
Phase 0 (see [roadmap.md](../roadmap.md)). CI must run against every
supported version (see [testing-validation.md](../testing-validation.md)).

## Problem

Which Python versions should `rfmeasurement` officially support at
initial development?

## Alternatives

1. Support back to Python 3.9 for maximum compatibility. Python 3.9
   reached end-of-life in October 2025, so this trades reach for
   maintaining an already-unsupported interpreter.
2. Support only the newest Python version, allowing use of the latest
   syntax and typing features but excluding most current users.
3. Support the range of actively maintained CPython versions at project
   start (3.10-3.13), balancing modern language features (e.g.
   structural pattern matching, improved typing syntax) with realistic
   adoption in research/lab environments.

## Decision

Option 3: support Python 3.10, 3.11, 3.12, and 3.13, encoded as
`requires-python = ">=3.10"` in `pyproject.toml` and as the CI test
matrix.

## Consequences

- The project can use typing and standard-library features introduced
  in 3.10+ without compatibility shims.
- The supported range must be revisited periodically as CPython versions
  reach end-of-life and new versions are released; update this ADR (or
  supersede it) when the range changes, and reflect the change in
  `CHANGELOG.md` since it is a compatibility-relevant change.
