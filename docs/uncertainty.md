# Uncertainty Quantification

## Scientific objective

The framework should treat uncertainty as part of the measurement result
rather than as a plotting feature.

NIST guidance describes measurement uncertainty in terms of the
dispersion associated with the values attributed to a measurand and
recommends approaches based on measurement models, probability
distributions, covariance/correlation and Monte Carlo methods where
appropriate.

## Initial uncertainty model

The first implementation should distinguish:

### Type A

Uncertainty estimated from repeated observations.

Examples:

-   repeatability;
-   short-term noise;
-   repeated connector mating.

### Type B

Uncertainty based on other information.

Examples:

-   calibration certificate;
-   manufacturer specification;
-   dimensional tolerance;
-   temperature coefficient;
-   known instrument accuracy.

The distinction should be metadata rather than an architectural
restriction.

## Representation

Each uncertainty source should contain at least:

-   name;
-   description;
-   nominal value;
-   distribution;
-   standard uncertainty;
-   unit;
-   correlation information;
-   source/reference;
-   assumptions.

Possible distributions:

-   normal;
-   uniform;
-   triangular;
-   empirical;
-   discrete;
-   custom.

## Complex quantities

RF data are inherently complex. The implementation must not reduce
complex uncertainty to independent magnitude and phase uncertainties
without documenting the transformation.

The design should allow:

``` text
real/imaginary covariance
```

and, where appropriate:

``` text
magnitude/phase covariance
```

## Correlation

Correlation is essential for RF measurements.

Examples include:

-   frequency-correlated VNA noise;
-   common calibration errors;
-   shared environmental effects;
-   correlated S-parameter components.

The API must therefore avoid an implicit assumption of independence.

## Propagation methods

### Linear propagation

Useful for:

-   approximately linear models;
-   fast uncertainty estimates;
-   sensitivity analysis.

### Monte Carlo

The preferred general-purpose method for nonlinear transformations and
non-Gaussian distributions.

The Monte Carlo implementation should support:

-   reproducible random seeds;
-   vectorised sampling;
-   convergence diagnostics;
-   configurable sample counts;
-   multivariate outputs.

## Uncertainty budget

A budget should expose:

``` text
measurand
├── source A
├── source B
├── source C
└── combined uncertainty
```

It should be possible to rank contributors.

## Coverage

The API should explicitly distinguish:

-   standard uncertainty;
-   expanded uncertainty;
-   confidence/coverage probability;
-   coverage interval;
-   coverage region for multivariate outputs.

The implementation must avoid presenting a numerical interval as a
generic "confidence interval" unless its statistical interpretation is
actually justified.

## Validation of the UQ engine

The uncertainty engine should be tested against:

-   analytical solutions;
-   synthetic Monte Carlo cases;
-   published metrology examples;
-   known limiting cases.

## Important scientific constraint

The project must not claim that an uncertainty estimate is meaningful
merely because a Monte Carlo calculation produced a number.

A valid uncertainty result requires a defensible measurement model and
documented assumptions.
