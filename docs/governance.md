# Governance

## Initial governance

During the initial phase, the project may operate under a maintainer-led
model.

Scientific and architectural decisions should nevertheless be documented
publicly.

## Decision process

Important decisions should be recorded as Architecture Decision Records
(ADRs).

Each ADR should contain:

-   context;
-   problem;
-   alternatives;
-   decision;
-   consequences;
-   status.

## Maintainer responsibilities

Maintainers are responsible for:

-   release management;
-   issue triage;
-   code review;
-   documentation quality;
-   dependency management;
-   security response;
-   scientific integrity.

## Community evolution

As external contributors become active, governance should evolve toward
shared maintainership.

Potential future mechanisms:

-   maintainer team;
-   scientific advisory group;
-   steering committee;
-   documented voting rules for major changes.

The project should avoid creating governance bureaucracy before there is
a community that needs it.

## Scientific integrity

The project should distinguish:

-   established scientific methods;
-   implementation assumptions;
-   experimental heuristics;
-   exploratory algorithms.

Experimental algorithms must not be presented as validated metrology
methods without evidence.

## Versioning and deprecation

Public APIs should follow a documented deprecation policy.

Scientific changes that alter numerical results should be highlighted
prominently in release notes.

## Citation policy

The project provides machine-readable citation metadata in
[`CITATION.cff`](../CITATION.cff) at the repository root.

-   Every tagged release should keep `CITATION.cff` in sync with the
    released version and, once available, the Zenodo-issued DOI for that
    release (see [JOSS strategy](joss-strategy.md)).
-   Contributors whose work is substantial to the scientific software
    should be added to the author list in `CITATION.cff`, subject to the
    attribution process described in
    [contributing.md](contributing.md#attribution).
-   Publications, benchmarks, or datasets produced using
    `rfmeasurement` should cite the specific version used, not just the
    project in general, so that results remain reproducible.
-   Once a JOSS paper exists, `CITATION.cff` should reference it as the
    preferred citation.
