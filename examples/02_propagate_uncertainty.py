"""What is the uncertainty in this attenuator's insertion loss, and what dominates it?

Continues the story from examples/01_validate_measurement.py: the QA report
passed on the "clean measurement" S21 trace, so it is safe to ask a
quantitative question of it. Insertion loss is reported in dB, but the raw
VNA reading and its two error sources (receiver noise, calibration residual)
live in linear magnitude -- a genuinely nonlinear measurement model, not a
toy linear one.

This exercises the whole Phase 3 uncertainty engine: Type A/B distributions,
linear (GUM) propagation, Monte Carlo propagation, a ranked uncertainty
budget, and coverage intervals -- then assembles the result into a Phase 1
`AnalysisResult`, showing how the domain model and the uncertainty engine fit
together.

Run with:
    python examples/02_propagate_uncertainty.py
"""

from __future__ import annotations

import math

import numpy as np

from rfmeasurement.domain import (
    AnalysisResult,
    Distribution,
    Measurand,
    UncertaintySource,
    UncertaintyType,
)
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty import (
    build_budget,
    coverage_interval_from_samples,
    expand,
    propagate_linear,
    propagate_monte_carlo,
    standard_uncertainty_from_half_width,
)

SEED = 42  # fixed for reproducibility, per docs/reproducibility.md
NOMINAL_MAGNITUDE = 0.316  # |S21| of the ~10 dB attenuator from example 01
COVERAGE_PROBABILITY = 0.95


def _insertion_loss_db(values: dict) -> float:
    """The nonlinear measurement model: dB = -20*log10(measured linear magnitude)."""
    measured_magnitude = NOMINAL_MAGNITUDE + values["vna_noise"] + values["calibration"]
    return -20 * math.log10(measured_magnitude)


def _build_model() -> UncertaintyModel:
    vna_noise = UncertaintySource(
        name="vna_noise",
        description="Receiver noise / trace repeatability, estimated from repeated sweeps",
        uncertainty_type=UncertaintyType.TYPE_A,
        distribution=Distribution.NORMAL,
        standard_uncertainty=0.002,
        unit="linear magnitude",
        nominal_value=0.0,
    )

    # A calibration-kit datasheet gives a +/- tolerance, not a standard deviation
    # directly: convert it via the Type B half-width relation for a uniform
    # distribution (docs/uncertainty.md).
    calibration_half_width = 0.02
    calibration = UncertaintySource(
        name="calibration",
        description="Residual calibration-standard uncertainty (datasheet +/- tolerance)",
        uncertainty_type=UncertaintyType.TYPE_B,
        distribution=Distribution.UNIFORM,
        standard_uncertainty=standard_uncertainty_from_half_width(
            Distribution.UNIFORM, calibration_half_width
        ),
        unit="linear magnitude",
        nominal_value=0.0,
        source_reference="Calibration kit datasheet",
    )

    measurand = Measurand(
        name="IL",
        definition="Insertion loss, -20*log10(|S21|)",
        unit="dB",
        frequency_hz=2e9,
    )
    return UncertaintyModel(
        measurand=measurand,
        function=_insertion_loss_db,
        sources=(vna_noise, calibration),
        assumptions=(
            "vna_noise and calibration are independent and additive perturbations to the "
            "linear-magnitude reading around its nominal value; no drift or temperature "
            "dependence is modelled."
        ),
    )


def main() -> None:
    model = _build_model()

    linear = propagate_linear(model)
    monte_carlo = propagate_monte_carlo(
        model, n_samples=100_000, rng=np.random.default_rng(SEED)
    )

    print("Linear (GUM) propagation")
    print("-------------------------")
    print(f"value               = {linear.value:.4f} dB")
    print(f"standard_uncertainty = {linear.standard_uncertainty:.4f} dB")

    print("\nMonte Carlo propagation (100,000 samples)")
    print("------------------------------------------")
    print(f"value               = {monte_carlo.value:.4f} dB")
    print(f"standard_uncertainty = {monte_carlo.standard_uncertainty:.4f} dB")
    print(f"MC standard_error    = {monte_carlo.standard_error:.5f} dB")
    agreement = abs(linear.standard_uncertainty - monte_carlo.standard_uncertainty)
    print(f"(linear vs Monte Carlo agree to within {agreement:.4f} dB)")

    budget = build_budget(
        model.measurand, model.sources, linear.sensitivity_coefficients, linear.standard_uncertainty
    )
    print("\nUncertainty budget (ranked by contribution)")
    print("--------------------------------------------")
    for contribution in budget.ranked:
        print(
            f"{contribution.source.name:12} {contribution.contribution:.4f} dB "
            f"({contribution.percentage_of_variance:5.1f}% of variance) "
            f"[{contribution.source.uncertainty_type.value}]"
        )

    expanded, gaussian_interval = expand(
        linear.value, linear.standard_uncertainty, COVERAGE_PROBABILITY
    )
    mc_interval = coverage_interval_from_samples(monte_carlo.samples, COVERAGE_PROBABILITY)
    print(f"\n{COVERAGE_PROBABILITY:.0%} coverage interval")
    print("--------------------------")
    print(f"Gaussian (linear)   : [{gaussian_interval[0]:.4f}, {gaussian_interval[1]:.4f}] dB")
    print(f"Empirical (Monte Carlo): [{mc_interval[0]:.4f}, {mc_interval[1]:.4f}] dB")

    result = AnalysisResult(
        measurand=model.measurand,
        value=linear.value,
        unit=model.measurand.unit,
        standard_uncertainty=linear.standard_uncertainty,
        expanded_uncertainty=expanded,
        coverage_probability=COVERAGE_PROBABILITY,
        coverage_interval=gaussian_interval,
        contributing_sources=tuple(model.sources),
    )
    print(f"\nReported result: {result.value:.3f} dB +/- {result.expanded_uncertainty:.3f} dB "
          f"(k=95% coverage)")


if __name__ == "__main__":
    main()
