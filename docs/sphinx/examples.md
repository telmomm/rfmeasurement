# Examples

Runnable scripts under
[`examples/`](https://github.com/telmomm/rfmeasurement/tree/main/examples)
in the repository. Each answers a specific question rather than merely
demonstrating syntax (see
[docs/repository-organization.md](https://github.com/telmomm/rfmeasurement/blob/main/docs/repository-organization.md#examples)).
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
