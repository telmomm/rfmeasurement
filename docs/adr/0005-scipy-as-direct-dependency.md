# ADR 0005: Depend on SciPy directly for Student-t quantiles

- Status: accepted
- Date: 2026-10-02

## Context

Coverage factors for Type A sources estimated from few repeated readings
need the Student-t quantile (GUM Annex G; see
[uncertainty.md](../uncertainty.md) and issue #8). The Python standard
library provides the normal quantile (`statistics.NormalDist`) but has no
t-distribution counterpart, and numpy can sample a t-distribution but not
invert its CDF.

NFR6 in [requirements.md](../requirements.md) asks the core package to
avoid unnecessary dependencies. SciPy is already installed with every
`rfmeasurement` installation because scikit-rf requires it (see
[ADR 0001](0001-build-on-scikit-rf.md)), but it was not declared by
`rfmeasurement` itself.

## Problem

Where should the t-quantile come from?

## Alternatives

1. Implement the inverse of the regularized incomplete beta function in
   `rfmeasurement`. No new declared dependency, but it reimplements
   numerical special functions that the project would then have to
   validate and maintain.
2. Ship a lookup table (GUM Table G.2) and interpolate. Simple, but
   limited to tabulated coverage probabilities and degrees of freedom.
3. Import it from SciPy through scikit-rf's transitive dependency without
   declaring it. Works today, but breaks silently if scikit-rf ever drops
   or makes SciPy optional.
4. Declare SciPy as a direct dependency and use `scipy.special.stdtrit`.

## Decision

Option 4. SciPy is declared in `pyproject.toml` (`scipy>=1.10`) and used
only for the t-quantile in `rfmeasurement.uncertainty.coverage`. The
installed footprint does not change, since scikit-rf already requires
SciPy, and the numerical routine is one the scientific Python community
already maintains and tests.

## Consequences

- Coverage factors are available for any coverage probability and any
  (including non-integer) degrees of freedom.
- SciPy's version is recorded in the software environment of a report,
  alongside numpy and scikit-rf.
- New uses of SciPy in the core package are possible without another
  dependency decision, but should stay justified against NFR6.
