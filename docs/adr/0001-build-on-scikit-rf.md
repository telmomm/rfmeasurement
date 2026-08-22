# ADR 0001: Build on top of scikit-rf rather than replacing it

- Status: accepted
- Date: 2026-08-22

## Context

RF measurement analysis requires S-parameter algebra, network connection,
Touchstone I/O, calibration, and de-embedding. `scikit-rf` already
provides mature, widely used implementations of these.
`rfmeasurement`'s stated purpose is measurement provenance,
measurement-quality assessment, uncertainty modelling and propagation,
and reproducible reporting — a layer that is largely missing from the
existing ecosystem.

## Problem

Should `rfmeasurement` implement its own RF network mathematics, or
depend on and extend an existing package?

## Alternatives

1. Implement network mathematics from scratch for full control over the
   internal representation.
2. Fork `scikit-rf` and add the new functionality inside the fork.
3. Depend on `scikit-rf` as a library and add a higher-level layer on
   top (`skrf.Network` as the underlying data representation inside
   `Measurement`).

## Decision

Option 3. `rfmeasurement` depends on `scikit-rf` and does not
reimplement core RF network mathematics. See [scope.md](../scope.md) for
the full in-scope/out-of-scope boundary.

## Consequences

- Faster path to a useful tool; avoids duplicating well-tested numerics.
- `rfmeasurement`'s domain objects (`Measurement`, etc.) wrap or
  reference `skrf.Network` rather than reimplementing it.
- `rfmeasurement` takes on a dependency on `scikit-rf`'s release cadence
  and API stability.
- The scientific core (validation, uncertainty) must not depend on
  instrument-specific code, per [architecture.md](../architecture.md).
