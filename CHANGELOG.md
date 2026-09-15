# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/)
once a stable API is released.

## [Unreleased]

### Added

- `ProvenanceGraph` (`rfmeasurement.provenance`, Phase 4): links a
  measurement's `ProvenanceRecord` history into an auditable, acyclic graph
  (topological order, ancestors/descendants, external-source detection, JSON
  export). `ProvenanceRecord` gained a `record_id` so records can reference
  each other.
- `examples/04_provenance_graph.py`: builds the provenance graph for the
  attenuator result from `examples/01`/`02` and audits it back to its raw
  input.
- Published documentation ("Training" section, `docs/sphinx/training/`):
  republishes every `docs/*.md` design/process document and ADR on Read the
  Docs via thin MyST `{include}` stub pages, so `docs/*.md` stays the only
  place that content is edited while readers of the published site no
  longer have to jump to GitHub for it. Sphinx pages that used to link out
  to `docs/*.md` on GitHub now cross-reference these pages directly.
- `nanovna-calibration` and `pydigger-data` listed on the publications page
  as, respectively, the first real downstream user of `rfmeasurement` and
  an automated PyPI index that has picked it up.
- `tests/scientific/`: analytical GUM/NIST reference-case tests moved out of
  `tests/unit/`, each citing the specific clause it verifies.
- `tests/regression/` and `tests/data/`: pinned validation outcomes for a
  real, lab-measured antenna (scikit-rf's "ring slot" data, frozen locally
  so the test does not depend on `scikit-rf`'s internal package layout).
- `tests/integration/`: the validate -> propagate -> budget ->
  `AnalysisResult` pipeline shown in `examples/01`/`02`, formalized with
  assertions instead of printed output.
- `examples/03_real_measurement.py`: validates real measured data instead
  of synthetic networks.
- Virtual environment setup documented in `CONTRIBUTING.md`/`README.md`.

### Fixed

- Silenced an expected `InvalidFrequencyWarning` in the frequency-grid
  validation test (the disordered grid is deliberate there).

## [0.1.0] - 2026-08-22

First tagged release. The public API is not yet stable (pre-1.0 semantic
versioning): expect breaking changes in `0.x` releases. See
[docs/roadmap.md](docs/roadmap.md) for what is and is not implemented yet --
notably, there is no dedicated I/O/adapter layer, provenance persistence, or
reporting output beyond the in-memory domain objects.

### Added

- **Project foundation** (Phase 0): BSD-3-Clause license, code of conduct,
  contributing guide, issue templates, CI (tests, lint, type checks, docs
  build), `src/` package layout, and initial Architecture Decision Records.
- **Domain model** (Phase 1): `Measurement`, `MeasurementContext`,
  `Measurand`, `ProvenanceRecord`, `AnalysisResult`, `ValidationResult` /
  `ValidationReport`, and `UncertaintySource`, wrapping `skrf.Network` rather
  than reimplementing RF network mathematics.
- **Measurement-quality validation engine** (Phase 2): a composable
  `ValidationRule` interface and seven rules (structural integrity, finite
  values, frequency-grid consistency, passivity, reciprocity, continuity,
  dynamic-range indicator), producing a structured `ValidationReport`.
- **Uncertainty quantification engine** (Phase 3): `UncertaintyModel` and
  `UncertaintyBudget` domain objects; Type A/B distribution sampling;
  covariance-aware linear (GUM) propagation; Monte Carlo propagation with
  correlated-normal sampling; ranked uncertainty budgets; and coverage
  intervals (Gaussian and empirical).
- Published documentation on Read the Docs
  (<https://rfmeasurement.readthedocs.io/en/latest/>), built with Sphinx +
  MyST from docstrings, alongside the project design specification in
  `docs/`.
- Two runnable examples: validating a synthetic measurement
  (`examples/01_validate_measurement.py`) and propagating uncertainty
  through a nonlinear dB conversion (`examples/02_propagate_uncertainty.py`).

[Unreleased]: https://github.com/telmomm/rfmeasurement/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/telmomm/rfmeasurement/releases/tag/v0.1.0
