# Domain Model

## Measurement

A `Measurement` represents an observation plus its acquisition context.

Conceptually:

``` text
Measurement
├── data
├── context
├── provenance
├── validation
└── analysis history
```

A measurement is not necessarily raw data. It can represent imported,
calibrated, de-embedded or derived data, provided the processing history
is preserved.

## Measurement context

The context should be able to describe:

-   DUT;
-   operator;
-   instrument;
-   calibration;
-   cables;
-   fixture;
-   temperature;
-   humidity;
-   pressure where relevant;
-   RF power;
-   IF bandwidth;
-   averaging;
-   sweep settings;
-   frequency range;
-   date/time.

Metadata should distinguish:

-   measured;
-   specified;
-   estimated;
-   assumed;
-   unknown.

## Measurand

The `Measurand` is the quantity being reported.

Examples:

-   `S11` at a frequency;
-   insertion loss at a frequency;
-   group delay;
-   resonance frequency;
-   loaded Q;
-   bandwidth;
-   effective permittivity.

A measurand should carry its definition and units.

## Uncertainty source

An uncertainty source represents a contributor such as:

-   instrument noise;
-   calibration;
-   connector repeatability;
-   temperature;
-   dimensional uncertainty;
-   reference-standard uncertainty.

Each source should be independently identifiable.

## Validation result

A validation result should contain:

-   rule identifier;
-   status;
-   measured evidence;
-   threshold or criterion;
-   explanation;
-   timestamp/version;
-   optional remediation suggestion.

## Analysis result

An analysis result should include:

-   measurand;
-   value;
-   units;
-   uncertainty;
-   coverage statement;
-   provenance;
-   validation status.

## Provenance

Provenance is a directed history of transformations:

``` text
raw measurement
    ↓
calibration
    ↓
de-embedding
    ↓
filtering
    ↓
derived quantity
    ↓
uncertainty propagation
    ↓
reported result
```

The exact serialization format should remain implementation-independent.
