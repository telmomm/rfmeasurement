# Measurement Quality and Validation

## Goal

Provide a structured way to answer:

> Is this RF measurement sufficiently trustworthy for the analysis I am
> about to perform?

This is broader than checking whether a file can be parsed.

## Validation levels

### Level 1 --- Data integrity

Checks:

-   file readability;
-   finite values;
-   valid dimensions;
-   frequency ordering;
-   duplicate frequency points;
-   consistent port count;
-   valid units.

### Level 2 --- Physical consistency

Where applicable:

-   passivity;
-   reciprocity;
-   causality;
-   continuity;
-   physically plausible magnitude.

These checks must explicitly state when they are not applicable.

### Level 3 --- Instrument/measurement quality

Potential indicators:

-   noise floor;
-   dynamic range;
-   trace discontinuities;
-   compression indicators;
-   suspicious phase behaviour;
-   repeatability;
-   drift.

### Level 4 --- Calibration/fixture quality

Potential checks:

-   calibration age;
-   calibration metadata completeness;
-   standard consistency;
-   fixture validity;
-   de-embedding residuals.

### Level 5 --- Application-specific validity

The framework should allow a user to define requirements such as:

``` text
Insertion loss uncertainty < 0.1 dB
Frequency uncertainty < 1 MHz
S11 repeatability < 0.02
```

## Result model

Validation should never be represented only by a boolean.

Recommended statuses:

``` text
PASS
WARNING
FAIL
NOT_APPLICABLE
NOT_EVALUATED
```

Each rule should return structured evidence.

## Quality score

A global quality score may be introduced later, but it must not hide the
underlying evidence.

The preferred first release is therefore:

-   transparent individual rules;
-   weighted aggregation only as an optional layer;
-   no arbitrary score presented as metrological truth.

## Rule interface

Conceptually:

``` text
ValidationRule
├── identifier
├── description
├── applicability
├── evaluate(measurement)
└── result
```

Rules should be composable.

## Important distinction

A validation failure does not automatically mean the measurement is
scientifically useless.

For example, non-reciprocity may be physically expected for an active or
non-reciprocal DUT.

The framework should therefore distinguish:

-   failed universal integrity checks;
-   failed assumptions;
-   failed user-defined acceptance criteria.
