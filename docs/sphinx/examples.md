# Examples

Runnable scripts under
[`examples/`](https://github.com/telmomm/rfmeasurement/tree/main/examples)
in the repository. Each answers a specific question rather than merely
demonstrating syntax (see
[the project's repository organization](training/repository-organization.md#examples)).
Run any of them locally with:

```bash
python examples/01_validate_measurement.py
```

## 01 -- Is this measurement trustworthy enough to analyze?

Builds a clean and a corrupted synthetic attenuator measurement and runs
the validation engine on both, to see how the structured QA report tells
them apart.

```{literalinclude} ../../examples/01_validate_measurement.py
:language: python
```

## 02 -- What is the uncertainty in this attenuator's insertion loss?

Continues example 01: propagates uncertainty through a genuinely nonlinear
measurement model (dB conversion) via both linear (GUM) and Monte Carlo
propagation, builds a ranked uncertainty budget, and computes coverage
intervals.

```{literalinclude} ../../examples/02_propagate_uncertainty.py
:language: python
```

## 03 -- Does a real, lab-measured antenna pass the same checks?

Validates real Touchstone data (scikit-rf's own bundled "ring slot" antenna
measurement) instead of synthetic networks -- whatever the validation
engine reports here is a genuine property of a real measurement, not a
constructed demonstration.

```{literalinclude} ../../examples/03_real_measurement.py
:language: python
```

## 04 -- How was this number produced?

Continues examples 01/02: attaches a `ProvenanceRecord` to each processing
step (import, calibration, validation, both uncertainty-propagation
methods, final report) and links them into a `ProvenanceGraph` to audit the
reported result back to its raw input, per {doc}`training/reproducibility`.

```{literalinclude} ../../examples/04_provenance_graph.py
:language: python
```

## 05 -- Can an external user reproduce this result from a clean environment?

Completes examples 01/02/04: assembles the full machine-readable metadata
package and human-readable Markdown report for the attenuator result --
software/Python versions, analysis configuration (validation rules,
uncertainty model, propagation method and RNG state), input identifiers,
validation summary, uncertainty summary, and an explicit 1-4
reproducibility level, per {doc}`training/reproducibility`.

```{literalinclude} ../../examples/05_reproducible_report.py
:language: python
```
