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
-   assumptions;
-   degrees of freedom, when the standard uncertainty is itself an
    estimate (see [Degrees of freedom](#degrees-of-freedom)).

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

### Degrees of freedom

A Type A standard uncertainty estimated from `n` repeated readings is
itself uncertain. Expanding it with the Gaussian factor (k = 1.96 at
95 %) gives intervals that are too narrow: with five readings, a nominal
95 % interval contains the true value about 88 % of the time.

`UncertaintySource.degrees_of_freedom` records how well a standard
uncertainty is known: `n - 1` for the standard deviation of the mean of
`n` readings. `None` (the default) means it is treated as exactly known,
the usual convention for Type B sources.

Linear propagation (JCGM 100:2008, Annex G):

-   `propagate_linear` reports `effective_degrees_of_freedom`, from the
    Welch--Satterthwaite formula
    `ν_eff = u_c⁴ / Σ [(c_i·u_i)⁴ / ν_i]`, where exactly known sources
    add nothing to the sum. It is `None` when no source declares finite
    degrees of freedom.
-   `coverage_factor` and `expand` take the degrees of freedom and return
    the Student-t factor instead of the Gaussian one. The quantile is
    evaluated at the non-integer `ν_eff`; truncate it first to reproduce
    a table lookup (GUM G.6.4).
-   The formula assumes uncorrelated inputs. A source with finite degrees
    of freedom that is correlated with another source raises
    `NotImplementedError` rather than returning a number the formula does
    not justify.

Monte Carlo (JCGM 101:2008, 6.4.9.2):

-   A `NORMAL` source with finite degrees of freedom is sampled from a
    scaled and shifted t-distribution, `nominal + u·t_ν`, so
    `coverage_interval_from_samples` accounts for it without further
    input.
-   The standard deviation of that distribution is `u·sqrt(ν / (ν − 2))`,
    so the Monte Carlo standard uncertainty is larger than the linear one
    for the same model, and does not converge for `ν ≤ 2`
    (`propagate_monte_carlo` warns). This is the known difference between
    the GUM and its Supplement 1, not a defect of either method; the
    coverage intervals of the two agree.
-   Finite degrees of freedom on a non-normal or correlated source raise
    `NotImplementedError`.

`AnalysisResult.coverage_factor` and
`AnalysisResult.effective_degrees_of_freedom` carry the factor actually
used into the metadata package and the report, so a k = 1.96 interval can
be told apart from a k = 2.78 one.

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
