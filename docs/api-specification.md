# Technical API Specification — `rfmeasurement` v0.1

## 1. Purpose

This document defines the initial public API of `rfmeasurement`.

The purpose of the API is to provide a stable scientific abstraction for:

* representing RF measurements;
* preserving measurement context and provenance;
* validating measurement quality;
* defining measurands;
* representing uncertainty sources;
* propagating uncertainty;
* producing reproducible analysis results.

The API intentionally does **not** attempt to replace RF network-analysis libraries.

The initial implementation should integrate with `scikit-rf` wherever appropriate.

---

# 2. Core design principles

## 2.1 Measurement is more than data

A measurement is not merely an S-parameter matrix.

Conceptually:

```text
Measurement
├── data
├── context
├── provenance
└── metadata
```

The data may be an `skrf.Network`, but the scientific object also contains information about how the data was obtained and processed.

---

## 2.2 Results must be traceable

Every `AnalysisResult` should be traceable to:

```text
input data
    ↓
processing operations
    ↓
validation
    ↓
measurement model
    ↓
uncertainty model
    ↓
reported result
```

---

## 2.3 Uncertainty is a first-class object

Uncertainty must not be represented as an optional number attached to a result.

Instead:

```text
UncertaintySource
        ↓
UncertaintyModel
        ↓
Propagation
        ↓
UncertaintyBudget
        ↓
AnalysisResult
```

---

## 2.4 Validation is not a boolean

Validation must provide structured evidence.

The result of a validation rule is therefore:

```text
PASS
WARNING
FAIL
NOT_APPLICABLE
NOT_EVALUATED
```

with an explanation and diagnostic information.

---

## 2.5 Explicit assumptions

The library must distinguish between:

* measured information;
* specified information;
* estimated information;
* assumed information.

An assumption must never silently become a measured fact.

---

# 3. Public API surface

The initial public API should expose the following concepts:

```text
Measurement
MeasurementContext

Measurand
AnalysisResult

ValidationRule
ValidationResult
ValidationReport

UncertaintySource
UncertaintyModel
UncertaintyBudget

ProvenanceRecord
AnalysisStep
```

Optional convenience APIs may be added later.

---

# 4. `Measurement`

## 4.1 Purpose

`Measurement` represents an RF measurement together with the context required to interpret it.

## 4.2 Proposed interface

```python
from rfmeasurement import Measurement

measurement = Measurement(
    data=network,
    context=context,
    metadata=metadata,
)
```

### Constructor

```python
Measurement(
    data,
    *,
    context=None,
    metadata=None,
    provenance=None,
    identifier=None,
)
```

### Parameters

#### `data`

The measurement data.

Initially supported:

```python
skrf.Network
```

Future adapters may support:

* arrays;
* pandas structures;
* Touchstone-backed lazy objects;
* other RF network representations.

The core should not require the data to be a particular concrete implementation.

#### `context`

Optional `MeasurementContext`.

#### `metadata`

User-defined metadata.

#### `provenance`

Optional provenance graph/history.

#### `identifier`

Stable user-provided measurement identifier.

---

# 5. Measurement immutability

The preferred design is **functional/immutable analysis**.

Operations should not silently mutate the original measurement.

For example:

```python
calibrated = measurement.apply_calibration(calibration)
```

should conceptually produce:

```text
measurement
     │
     └── calibrated
```

rather than modifying `measurement`.

Likewise:

```python
deembedded = calibrated.deembed(fixture)
```

creates a new analysis state.

This is essential for reproducibility.

---

# 6. `MeasurementContext`

## 6.1 Purpose

`MeasurementContext` contains information describing how the measurement was acquired.

```python
from rfmeasurement import MeasurementContext

context = MeasurementContext(
    instrument="VNA-01",
    calibration="SOLT-2026-001",
    temperature=23.4,
    humidity=42.0,
    power=-10.0,
)
```

## 6.2 Initial fields

The initial model should support:

```python
MeasurementContext(
    instrument=None,
    calibration=None,
    fixture=None,
    operator=None,
    timestamp=None,
    temperature=None,
    humidity=None,
    pressure=None,
    power=None,
    if_bandwidth=None,
    averaging=None,
    sweep=None,
    environment=None,
)
```

These fields should remain extensible.

---

# 7. Metadata provenance

Every metadata item should ideally carry a source classification.

Conceptually:

```python
MetadataValue(
    value=23.4,
    source="measured",
)
```

Allowed source categories:

```text
measured
specified
estimated
assumed
unknown
```

This distinction is scientifically important.

For example:

```text
temperature = 23.4 °C
source = measured
```

is fundamentally different from:

```text
temperature = 23.4 °C
source = assumed
```

---

# 8. `Measurand`

## 8.1 Purpose

A `Measurand` defines what quantity is actually being reported.

Examples:

```python
Measurand(
    name="insertion_loss",
    quantity="S21",
    frequency=2.45e9,
    unit="dB",
)
```

or:

```python
Measurand(
    name="resonance_frequency",
    unit="Hz",
)
```

## 8.2 Proposed interface

```python
Measurand(
    name,
    *,
    definition=None,
    unit=None,
    coordinates=None,
    model=None,
)
```

### `name`

Human-readable identifier.

Examples:

```text
S11
S21
insertion_loss
group_delay
resonance_frequency
Q_loaded
```

### `definition`

Mathematical/scientific definition.

Example:

```text
Insertion loss = -20 log10(|S21|)
```

### `unit`

Physical unit.

### `coordinates`

Coordinates required to define the quantity.

For example:

```python
coordinates={
    "frequency": 2.45e9,
}
```

### `model`

Optional measurement/analysis model.

---

# 9. `AnalysisResult`

## 9.1 Purpose

`AnalysisResult` is the principal scientific output of the framework.

```python
result = AnalysisResult(
    measurand=measurand,
    value=-2.31,
    unit="dB",
)
```

## 9.2 Required properties

A result should contain:

```text
measurand
value
unit
uncertainty
validation
provenance
```

## 9.3 Example

```python
result.value
# -2.31

result.standard_uncertainty
# 0.031

result.expanded_uncertainty
# 0.06

result.coverage_probability
# 0.95
```

The exact statistical terminology must be explicit.

---

# 10. Uncertainty representation

## 10.1 `UncertaintySource`

Represents one contributor.

```python
from rfmeasurement import UncertaintySource

source = UncertaintySource(
    name="connector_repeatability",
    distribution="normal",
    standard_uncertainty=0.02,
    unit="dB",
)
```

## 10.2 Required fields

```python
UncertaintySource(
    name,
    *,
    value=None,
    distribution,
    standard_uncertainty=None,
    unit=None,
    degrees_of_freedom=None,
    source=None,
    correlation_group=None,
    metadata=None,
)
```

---

# 11. Distributions

The initial API should support:

```text
normal
uniform
triangular
empirical
```

The architecture should allow future custom distributions.

Example:

```python
source = UncertaintySource(
    name="connector_repeatability",
    distribution="normal",
    standard_uncertainty=0.02,
    unit="dB",
)
```

For a uniform specification:

```python
source = UncertaintySource(
    name="frequency_accuracy",
    distribution="uniform",
    bounds=(-1e6, 1e6),
    unit="Hz",
)
```

---

# 12. Correlation

Correlation must be explicitly supported.

A source may belong to a correlation group:

```python
UncertaintySource(
    name="calibration_error",
    correlation_group="calibration_2026_01",
)
```

The implementation must not assume:

```text
covariance = 0
```

unless independence has actually been specified.

---

# 13. `UncertaintyModel`

## 13.1 Purpose

Defines how uncertainty sources affect a measurand.

```python
model = UncertaintyModel(
    measurand=measurand,
    sources=[
        vna_noise,
        calibration,
        connector,
    ],
)
```

## 13.2 Measurement equation

The model should support a conceptual function:

```python
y = f(x_1, x_2, ..., x_n)
```

where:

```text
x_i = input quantities
y   = measurand
```

Example:

```python
model = UncertaintyModel(
    function=insertion_loss,
    inputs={
        "s21": s21,
    },
    sources=[...],
)
```

---

# 14. Propagation methods

The public API should initially support:

```python
result = model.propagate(
    method="linear"
)
```

and:

```python
result = model.propagate(
    method="monte_carlo",
    samples=100_000,
    seed=1234,
)
```

## 14.1 Linear propagation

Appropriate for models where linearisation is justified.

The result must document that linear propagation was used.

## 14.2 Monte Carlo

Required for nonlinear/non-Gaussian cases where appropriate.

The execution metadata should record:

```text
method
sample count
random seed
distribution definitions
software version
```

---

# 15. `UncertaintyBudget`

## 15.1 Purpose

Represents the contribution of each source to the final uncertainty.

Example:

```python
budget = result.uncertainty_budget
```

Conceptual output:

```text
Source                  Contribution
-------------------------------------
Calibration             51 %
Connector repeatability 27 %
VNA noise               14 %
Temperature               8 %
```

## 15.2 API

```python
budget.sources
budget.total
budget.rank()
```

Potential convenience:

```python
budget.to_dataframe()
budget.plot()
```

Plotting should remain optional.

---

# 16. Validation framework

## 16.1 `ValidationRule`

A validation rule is an independent scientific/software test.

Example:

```python
from rfmeasurement.validation import PassivityRule

rule = PassivityRule()
```

Conceptual interface:

```python
class ValidationRule:
    identifier: str
    description: str

    def applies(self, measurement) -> bool:
        ...

    def evaluate(self, measurement) -> ValidationResult:
        ...
```

The actual implementation should use an abstract base class or protocol depending on the final architecture.

---

# 17. `ValidationResult`

```python
ValidationResult(
    rule="passivity",
    status="PASS",
    message="Network satisfies passivity criterion.",
    evidence={...},
)
```

Allowed statuses:

```text
PASS
WARNING
FAIL
NOT_APPLICABLE
NOT_EVALUATED
```

## Required fields

```text
rule
status
message
evidence
```

Optional:

```text
threshold
observed
unit
recommendation
```

---

# 18. `ValidationReport`

A collection of validation results.

```python
report = measurement.validate()
```

Example:

```python
report.status
# "WARNING"

report.results
# [...]

report.failed
# [...]

report.warnings
# [...]
```

A report must retain individual evidence.

It must not reduce everything to:

```python
True / False
```

---

# 19. Validation execution

The measurement API should support:

```python
report = measurement.validate()
```

and:

```python
report = measurement.validate(
    rules=[
        FrequencyGridRule(),
        PassivityRule(),
        ReciprocityRule(),
    ]
)
```

Future versions may provide rule registries:

```python
report = measurement.validate(profile="default")
```

But named profiles should be introduced only after the underlying rules are mature.

---

# 20. Validation profiles

Potential future profiles:

```text
basic
network
metrology
fixture
application
```

A profile must be explicit.

For example:

```python
measurement.validate(profile="network")
```

must document exactly which rules are included.

---

# 21. Provenance

## 21.1 `ProvenanceRecord`

Every transformation should produce a provenance record.

```python
ProvenanceRecord(
    operation="calibration",
    parameters={...},
    software="rfmeasurement",
    version="0.1.0",
)
```

## 21.2 `AnalysisStep`

Conceptually:

```python
AnalysisStep(
    operation="deembed",
    inputs=["measurement-001"],
    outputs=["measurement-002"],
    parameters={...},
)
```

The exact provenance graph implementation may evolve.

---

# 22. Immutable processing pipeline

The preferred API is:

```python
raw = Measurement.from_touchstone("dut.s2p")

calibrated = raw.apply_calibration(calibration)

validated = calibrated.validate()

deembedded = calibrated.deembed(fixture)

result = deembedded.analyze(measurand)
```

Every operation should preserve the previous state.

This enables:

```text
raw
 ├── calibrated
 │      ├── deembedded
 │      └── alternate_analysis
 └── independent_analysis
```

rather than forcing one mutable history.

---

# 23. Analysis API

The framework should provide a generic analysis interface:

```python
result = measurement.analyze(measurand)
```

Example:

```python
measurand = Measurand(
    name="insertion_loss",
    frequency=2.45e9,
    unit="dB",
)

result = measurement.analyze(measurand)
```

The analysis method should be selected explicitly or through a registered implementation.

---

# 24. Uncertainty-aware analysis

The intended high-level workflow is:

```python
result = measurement.analyze(
    measurand,
    uncertainty=True,
)
```

or, preferably for explicitness:

```python
result = measurement.analyze(measurand)

result = result.propagate_uncertainty(
    model=uncertainty_model,
    method="monte_carlo",
    samples=100_000,
)
```

The second form should remain available because scientific workflows benefit from explicit steps.

---

# 25. Complete example

The target user experience is approximately:

```python
import skrf as rf

from rfmeasurement import (
    Measurement,
    MeasurementContext,
    Measurand,
    UncertaintyModel,
)

network = rf.Network("filter.s2p")

context = MeasurementContext(
    instrument="VNA-01",
    calibration="SOLT-2026-001",
    temperature=23.4,
    power=-10,
)

measurement = Measurement(
    data=network,
    context=context,
)

validation = measurement.validate()

measurand = Measurand(
    name="insertion_loss",
    definition="-20*log10(abs(S21))",
    frequency=2.45e9,
    unit="dB",
)

result = measurement.analyze(measurand)

uncertainty_model = UncertaintyModel(
    measurand=measurand,
    sources=[
        vna_noise,
        calibration_uncertainty,
        connector_uncertainty,
    ],
)

result = result.with_uncertainty(
    model=uncertainty_model,
    method="monte_carlo",
    samples=100_000,
    seed=42,
)

report = result.report()
```

The final report should be able to express:

```text
Measurand:
    Insertion loss @ 2.45 GHz

Value:
    -2.31 dB

Standard uncertainty:
    0.031 dB

Expanded uncertainty:
    0.060 dB

Coverage probability:
    95 %

Measurement validation:
    PASS

Dominant uncertainty contributors:
    calibration          51 %
    connector            27 %
    VNA noise            14 %
    temperature           8 %

Provenance:
    filter.s2p
    → calibration
    → insertion-loss analysis
    → Monte Carlo uncertainty propagation
```

---

# 26. Error handling

The API must distinguish:

## User/input errors

Examples:

```text
invalid frequency
missing data
incompatible dimensions
invalid units
```

These should raise appropriate exceptions.

## Scientific non-applicability

Example:

```text
Reciprocity cannot be evaluated because the network is not reciprocal by design.
```

This should produce:

```text
NOT_APPLICABLE
```

not an exception.

## Numerical failure

Examples:

* singular matrix;
* failed convergence;
* insufficient Monte Carlo samples.

These should produce explicit scientific/software errors.

---

# 27. Exception hierarchy

Initial proposal:

```text
RFMeasurementError
├── DataError
├── ValidationError
├── UncertaintyError
├── AnalysisError
├── ProvenanceError
└── ConfigurationError
```

Avoid creating dozens of specialised exceptions until actual use cases require them.

---

# 28. Units

The framework should use an established units ecosystem rather than implementing its own unit parser.

A likely dependency is `pint`.

Internal APIs should therefore conceptually support:

```python
2.45e9 * ureg.hertz
```

rather than silently assuming units.

However, adopting Pint should be evaluated during the Phase 1 prototype because RF-specific arrays and scikit-rf interoperability need careful handling.

---

# 29. Arrays and vector quantities

RF measurements commonly contain:

```text
frequency × port × port
```

and complex values.

The framework should avoid copying large arrays unnecessarily.

The domain model should therefore store references to numerical objects where possible.

Initial numerical backend:

```text
NumPy
```

Potential future support:

```text
Dask
JAX
CuPy
```

must not influence the initial architecture.

---

# 30. Serialization

The first machine-readable representation should be JSON-compatible metadata.

Example:

```json
{
  "measurement_id": "filter-001",
  "instrument": "VNA-01",
  "calibration": "SOLT-2026-001",
  "temperature": {
    "value": 23.4,
    "unit": "degC",
    "source": "measured"
  }
}
```

Numerical RF data should not necessarily be embedded directly into JSON.

Large data should remain in established formats such as Touchstone, with provenance linking the data object.

---

# 31. Public vs internal API

Only explicitly documented objects should be considered public.

Initial public namespace:

```python
rfmeasurement.Measurement
rfmeasurement.MeasurementContext
rfmeasurement.Measurand
rfmeasurement.AnalysisResult

rfmeasurement.UncertaintySource
rfmeasurement.UncertaintyModel
rfmeasurement.UncertaintyBudget

rfmeasurement.ValidationRule
rfmeasurement.ValidationResult
rfmeasurement.ValidationReport
```

Internal implementation modules may change without backwards compatibility guarantees.

---

# 32. Versioning

The project should initially use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

Before 1.0:

```text
0.x
```

may contain breaking changes.

However, breaking scientific semantics must be explicitly documented even when the semantic-versioning rules technically permit the change.

Example:

```text
0.3.0

BREAKING SCIENTIFIC CHANGE

The uncertainty propagation method for complex S-parameters
now preserves real/imaginary covariance instead of independently
propagating magnitude and phase.
```

---

# 33. Scientific reproducibility requirements

Every uncertainty-aware result should record at minimum:

```text
measurement identifier
measurand definition
analysis method
uncertainty method
uncertainty sources
distribution assumptions
correlation assumptions
Monte Carlo sample count
random seed, if applicable
software version
```

A result without this information should be considered incomplete for reproducibility purposes.

---

# 34. First implementation boundary

The v0.1 implementation should **not** implement everything described above.

The first executable prototype should implement only:

```text
Measurement
MeasurementContext

Measurand
AnalysisResult

ValidationRule
ValidationResult
ValidationReport

UncertaintySource
UncertaintyModel
UncertaintyBudget

ProvenanceRecord
```

plus:

```text
Touchstone/scikit-rf adapter
basic validation
basic measurands
linear uncertainty propagation
Monte Carlo propagation
JSON metadata serialization
```

---

# 35. First supported scientific workflow

The first end-to-end workflow should be:

```text
Touchstone
    ↓
Measurement
    ↓
MeasurementContext
    ↓
Validation
    ↓
Measurand
    ↓
UncertaintyModel
    ↓
Monte Carlo propagation
    ↓
UncertaintyBudget
    ↓
AnalysisResult
    ↓
Reproducible report
```

The initial target example should be deliberately simple:

```text
Two-port passive filter
S21
Insertion loss at f0
```

This provides a manageable vertical slice.

---

# 36. First vertical slice

The first milestone should allow:

```python
measurement = Measurement.from_touchstone(
    "filter.s2p"
)

validation = measurement.validate()

measurand = Measurand(
    name="insertion_loss",
    frequency=2.45e9,
)

result = measurement.analyze(measurand)

result = result.with_uncertainty(
    model=model,
    method="monte_carlo",
    samples=10_000,
    seed=42,
)

result.save("result.json")
```

If this workflow is reliable, tested and scientifically documented, the project has its first meaningful MVP.

---

# 37. What must not enter the v0.1 API

The following should remain outside the first public API:

* GUI abstractions;
* cloud services;
* databases;
* automatic ML anomaly detection;
* vendor-specific VNA drivers;
* automatic calibration selection;
* automatic fixture discovery;
* complex plugin registries;
* distributed Monte Carlo;
* GPU support;
* arbitrary workflow engines.

These can be future extensions.

---

# 38. Definition of success for v0.1

The v0.1 API is successful if an external researcher can:

1. import an RF measurement;
2. describe its acquisition context;
3. run meaningful validation;
4. define a measurand;
5. define uncertainty sources;
6. propagate uncertainty;
7. inspect an uncertainty budget;
8. obtain a structured result;
9. reconstruct how the result was generated.

The API does **not** need to solve every RF measurement problem.

Its first responsibility is to establish a sound scientific foundation.

---

# 39. Architectural rule

The most important API rule is:

> **No scientific result without an explicit path from measurement to measurand.**

And for uncertainty-aware results:

> **No uncertainty number without an explicit uncertainty model.**

And for reproducible results:

> **No final result without provenance.**

These three rules should guide future API decisions.
