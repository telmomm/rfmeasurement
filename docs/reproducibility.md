# Reproducibility and Provenance

## Objective

A researcher should be able to answer:

> How was this number produced?

without relying on memory, undocumented notebooks or local scripts.

## Provenance requirements

Every final analysis result should be traceable to:

-   input dataset;
-   acquisition context;
-   calibration;
-   fixture/de-embedding;
-   analysis methods;
-   parameters;
-   validation rules;
-   uncertainty models;
-   software version.

## Provenance graph

The conceptual model is:

``` text
Dataset
   |
   v
Measurement
   |
   +--> Calibration
   |
   +--> Validation
   |
   v
Transformation
   |
   v
Derived Measurement
   |
   +--> Uncertainty Model
   |
   v
Measurand
   |
   v
Report
```

## Determinism

Algorithms should be deterministic by default.

If stochastic computation is used:

-   the random generator should be explicit;
-   the seed should be recordable;
-   the algorithm/version should be recorded.

## Serialization

The project should provide a machine-readable representation of analysis
metadata.

JSON is a likely first interchange format.

Binary scientific data should not be forced into JSON if this creates
inefficient or lossy representations. Large numerical data may remain in
established formats while metadata references them.

## Reproducible reports

Reports should contain:

-   software version;
-   Python version;
-   dependency versions where useful;
-   analysis configuration;
-   input identifiers;
-   validation summary;
-   uncertainty summary.

## Environment capture

The project should support optional environment manifests rather than
making exact environment capture mandatory for every use case.

Potential formats include:

-   `pyproject.toml`;
-   lock files;
-   Conda environment exports;
-   package version metadata.

## Reproducibility levels

### Level 0

Result only.

### Level 1

Result + input data.

### Level 2

Result + data + analysis configuration.

### Level 3

Result + data + configuration + software environment.

### Level 4

Level 3 plus complete instrument/calibration/environment provenance.

The framework should make these levels visible rather than claiming
every result is equally reproducible.
