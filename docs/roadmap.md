# Roadmap

The roadmap is deliberately staged around scientific credibility rather
than feature count.

## Phase 0 --- Project definition

**Goal:** establish the scientific and software foundation.

-   [x] Choose final project name.
-   [x] Create public repository.
-   [x] Select OSI-approved license.
-   [x] Add README and documentation skeleton.
-   [x] Add Code of Conduct.
-   [x] Add CONTRIBUTING guide.
-   [x] Add issue templates.
-   [x] Add CI.
-   [x] Define supported Python versions.
-   [x] Create initial architecture decision records.
-   [x] Establish citation policy.

**Exit criterion:** a public repository with transparent design
decisions and runnable development environment.

## Phase 1 --- Domain model

**Goal:** define the stable concepts.

-   [ ] `Measurement`
-   [ ] `MeasurementContext`
-   [ ] `Measurand`
-   [ ] `ProvenanceRecord`
-   [ ] `AnalysisResult`
-   [ ] validation result model
-   [ ] uncertainty source model

**Exit criterion:** domain objects can represent a realistic VNA
measurement without instrument-specific assumptions.

## Phase 2 --- Measurement quality MVP

**Goal:** make validation useful.

Initial rules:

-   [ ] data integrity;
-   [ ] frequency-grid checks;
-   [ ] finite-value checks;
-   [ ] passivity;
-   [ ] reciprocity;
-   [ ] basic continuity;
-   [ ] noise/dynamic-range indicators.

**Exit criterion:** a real measurement can generate a useful structured
QA report.

## Phase 3 --- Uncertainty MVP

**Goal:** produce defensible uncertainty estimates.

-   [ ] uncertainty distributions;
-   [ ] uncertainty sources;
-   [ ] covariance;
-   [ ] linear propagation;
-   [ ] Monte Carlo;
-   [ ] uncertainty budgets;
-   [ ] coverage intervals.

**Exit criterion:** results agree with analytical reference cases and
published metrology examples.

## Phase 4 --- Reproducibility

**Goal:** make analysis auditable.

-   [ ] provenance graph;
-   [ ] machine-readable metadata;
-   [ ] reproducible configuration;
-   [ ] deterministic execution;
-   [ ] report generation.

**Exit criterion:** an external user can reproduce a published example
from a clean environment.

## Phase 5 --- Research benchmark

**Goal:** demonstrate scholarly significance.

-   [ ] collect representative RF datasets;
-   [ ] document measurement conditions;
-   [ ] define reference results;
-   [ ] compare methods;
-   [ ] measure computational performance;
-   [ ] quantify limitations;
-   [ ] publish benchmark artifacts.

**Exit criterion:** evidence of research utility beyond a toy example.

## Phase 6 --- Community and maturity

-   [ ] external users;
-   [ ] external issues;
-   [ ] external pull requests;
-   [ ] multiple releases;
-   [ ] stable public API;
-   [ ] long-term maintenance policy.

## Phase 7 --- JOSS readiness

-   [ ] at least six months of public development;
-   [ ] sustained commit history;
-   [ ] tests and CI;
-   [ ] complete documentation;
-   [ ] examples;
-   [ ] research usage;
-   [ ] citations/adoption where available;
-   [ ] paper draft;
-   [ ] Zenodo integration;
-   [ ] JOSS metadata;
-   [ ] AI usage disclosure;
-   [ ] final release.

The JOSS strategy must be treated as a maturity target, not as a reason
to submit prematurely.
