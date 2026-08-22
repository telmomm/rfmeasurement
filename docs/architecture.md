# Architecture

## Architectural principle

The architecture should separate:

1.  **domain objects** --- what an RF measurement is;
2.  **scientific algorithms** --- how uncertainty and validation are
    calculated;
3.  **adapters** --- how external data enters and leaves the framework;
4.  **reporting** --- how results are presented;
5.  **integration** --- optional connections to instruments and external
    tools.

## Proposed layers

``` text
+-------------------------------------------------------+
|                  Reporting / Export                   |
|       Markdown | HTML | JSON | notebooks             |
+-------------------------------------------------------+
|               Workflow / Experiment                  |
|        Measurement | Analysis | Provenance           |
+-------------------------------------------------------+
|          Quality + Uncertainty Engine                |
|      Validation | UQ | budgets | propagation         |
+-------------------------------------------------------+
|                 RF Domain Layer                      |
|       Network | Frequency | Measurand | Context      |
+-------------------------------------------------------+
|                  Adapter Layer                       |
|     Touchstone | scikit-rf | PyVISA | future         |
+-------------------------------------------------------+
```

## Dependency philosophy

The preferred dependency direction is:

``` text
external tools → adapters → domain → scientific engines → reports
```

The scientific core must not depend on instrument-specific code.

## Core modules

A possible package layout is:

``` text
src/rfmeasurement/
    domain/
    io/
    validation/
    uncertainty/
    provenance/
    analysis/
    reporting/
    integrations/
```

The exact names may change after prototyping.

## Domain objects

The first stable objects should likely include:

-   `Measurement`;
-   `MeasurementContext`;
-   `ValidationReport`;
-   `ValidationResult`;
-   `UncertaintySource`;
-   `UncertaintyModel`;
-   `UncertaintyBudget`;
-   `Measurand`;
-   `AnalysisResult`;
-   `ProvenanceRecord`;
-   `Experiment`.

## Plugin architecture

Optional functionality should be extensible through explicit interfaces.

Examples:

``` text
ValidationRule
UncertaintyModel
DataReader
ReportRenderer
InstrumentAdapter
AnalysisMethod
```

The core package should not need to know every future implementation.

## Design trade-off

Avoid both extremes:

-   a monolithic framework that does everything;
-   a collection of unrelated one-function packages.

The preferred design is a small stable domain model with pluggable
scientific components.
