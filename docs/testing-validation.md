# Testing and Scientific Validation

## Principle

Scientific software requires two different forms of correctness:

1.  **software correctness** --- the implementation behaves as intended;
2.  **scientific correctness** --- the implementation represents the
    intended physical/statistical model.

Both must be tested.

## Test pyramid

``` text
             End-to-end research examples
                      /                     /                Integration tests
                   /                    Scientific tests
                 /                       Unit tests
```

## Unit tests

Use for:

-   data structures;
-   transformations;
-   distributions;
-   serialization;
-   validation rules;
-   numerical utilities.

## Scientific reference tests

Every core scientific algorithm should have at least one independently
verifiable reference.

Preferred references:

1.  analytical solution;
2.  independently implemented calculation;
3.  authoritative published example;
4.  trusted external package comparison.

Tests should document the reference source.

## Property-based testing

Where useful, use property-based tests for invariants such as:

-   round-trip transformations;
-   passivity preservation where mathematically expected;
-   identity operations;
-   serialization round trips.

## Numerical tolerances

Numerical comparisons must use explicit tolerances.

Tests should distinguish:

-   absolute tolerance;
-   relative tolerance;
-   expected numerical precision.

Avoid exact floating-point equality for scientific results.

## Synthetic datasets

Synthetic measurements are essential for controlled tests.

They should include:

-   known uncertainty;
-   known noise;
-   known calibration error;
-   known physical properties.

Synthetic data must never be the only validation evidence.

## Real-world datasets

At least one complete workflow should use a real RF measurement.

The dataset should include enough context to understand:

-   instrument;
-   calibration;
-   DUT;
-   frequency range;
-   environment;
-   analysis objective.

## Continuous integration

CI should run:

-   supported Python versions;
-   unit tests;
-   scientific tests;
-   linting;
-   type checks where enabled;
-   documentation checks.

## Reproducibility checks

A scheduled or manual workflow should periodically execute key examples
from a clean environment.

## Performance

Performance should only be advertised when benchmark methodology is
documented.

The benchmark suite should distinguish:

-   input size;
-   number of ports;
-   number of frequency points;
-   Monte Carlo sample count;
-   hardware;
-   Python/dependency versions.
