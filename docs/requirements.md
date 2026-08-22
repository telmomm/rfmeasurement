# Requirements

## Functional requirements

### R1 --- Load measurement data

The library shall import common RF measurement formats through adapters,
initially prioritising Touchstone and native scikit-rf `Network`
objects.

### R2 --- Preserve provenance

Every analysis result shall be traceable to its input measurement and
processing operations.

### R3 --- Validate measurements

Validation shall produce structured results rather than only raising
exceptions.

A validation result should distinguish:

-   pass;
-   warning;
-   failure;
-   not applicable;
-   not evaluated.

### R4 --- Model uncertainty

The library shall represent uncertainty sources independently from the
final result.

### R5 --- Propagate uncertainty

The library shall support propagation through derived quantities and
analysis pipelines.

### R6 --- Support correlated quantities

The design shall not assume that all RF quantities are independent.

### R7 --- Generate uncertainty budgets

Users shall be able to inspect which uncertainty sources dominate a
result.

### R8 --- Produce reproducible reports

A report shall identify:

-   data;
-   software;
-   configuration;
-   validation;
-   uncertainty;
-   result.

### R9 --- Remain composable

Users shall be able to use individual components without adopting the
complete framework.

### R10 --- Interoperate with existing RF Python

The project shall accept and return scikit-rf objects where practical.

## Non-functional requirements

### NFR1 --- Python-first

The project shall follow modern Python packaging conventions.

### NFR2 --- Type-aware

Public APIs should use type hints and be checked where practical.

### NFR3 --- Testable

Scientific functionality shall have automated tests with deterministic
reference cases.

### NFR4 --- Documented

Public APIs and scientific assumptions shall be documented.

### NFR5 --- Reproducible

Examples shall be executable and datasets shall be versioned or
permanently archived.

### NFR6 --- Lightweight core

The core package should avoid unnecessary dependencies.

### NFR7 --- Optional integrations

Instrument control, plotting, notebooks and advanced statistical
backends should be optional where possible.

### NFR8 --- Stable public API

Internal implementation details must be separable from the public domain
model.

### NFR9 --- Cross-platform

The analysis core should work on Linux, macOS and Windows.

### NFR10 --- Open development

Development should occur publicly from the beginning, including issues,
discussions, pull requests, releases and design decisions.
