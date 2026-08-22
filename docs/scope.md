# Scope

## In scope

### 1. Measurement representation

The framework should represent an RF measurement together with:

-   measured data;
-   frequency grid;
-   network representation;
-   instrument metadata;
-   calibration metadata;
-   DUT identity;
-   fixture information;
-   environmental conditions;
-   acquisition settings;
-   processing history;
-   software versions.

### 2. Measurement quality

The framework should provide composable checks for:

-   malformed data;
-   frequency-grid consistency;
-   missing or non-finite values;
-   dynamic-range limitations;
-   suspicious discontinuities;
-   outliers;
-   repeatability;
-   passivity;
-   reciprocity where applicable;
-   causality where applicable;
-   calibration consistency;
-   noise-floor indicators.

### 3. Uncertainty

The framework should support:

-   standard uncertainty;
-   probability distributions;
-   covariance and correlation;
-   sensitivity analysis;
-   uncertainty budgets;
-   Monte Carlo propagation;
-   multivariate outputs;
-   coverage intervals or regions;
-   uncertainty contributions.

The scientific design should be compatible with the GUM family of
approaches and the NIST guidance on uncertainty evaluation.

### 4. Reproducibility

The framework should capture enough provenance to reproduce an analysis:

-   input data identifiers;
-   processing operations;
-   parameters;
-   calibration identifiers;
-   software versions;
-   environment metadata;
-   random seeds where relevant;
-   result identifiers.

### 5. Reporting

The framework should generate:

-   human-readable reports;
-   machine-readable result records;
-   uncertainty budgets;
-   validation summaries;
-   provenance summaries.

## Explicitly out of scope for the initial project

### Instrument-driver ecosystem

Instrument communication should be supported through existing projects
such as PyVISA rather than duplicated.

### Core RF network mathematics

S-parameter algebra, network connection, Touchstone handling,
calibration and de-embedding should preferentially rely on mature
upstream packages such as scikit-rf.

### Proprietary instrument features

Vendor-specific functionality should not be required for the core
package.

### GUI

A GUI may be developed later by third parties or as an optional project,
but the core library must remain usable headlessly.

### Cloud infrastructure

The core package must not require a server, account or internet
connection.

### Machine learning as a dependency

ML may be used experimentally for future anomaly-detection modules, but
the core framework must not depend on ML.

## Boundary with scikit-rf

The project should follow a **build-on-top rather than
fork-and-replace** strategy.

scikit-rf already provides extensive RF network, calibration,
de-embedding, NetworkSet, plotting and virtual-instrument functionality.
The new project should use those capabilities where appropriate and
focus on the missing higher-level scientific workflow.
