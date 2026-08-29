"""End-to-end flow across domain, validation, and uncertainty modules.

Formalizes the narrative in examples/01_validate_measurement.py and
examples/02_propagate_uncertainty.py with concrete assertions: a synthetic
attenuator measurement passes QA, its insertion loss (a nonlinear dB
conversion) is propagated both ways, and the two independent methods agree.
Unlike tests/unit/, this exercises several modules together (domain,
validation, uncertainty) rather than one function or class in isolation.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
import skrf as rf

from rfmeasurement.domain import (
    AnalysisResult,
    Distribution,
    Measurand,
    Measurement,
    MeasurementContext,
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
from rfmeasurement.validation import validate

_NOMINAL_MAGNITUDE = 0.316  # |S21| of a ~10 dB attenuator


def _attenuator_measurement() -> Measurement:
    frequency = rf.Frequency(1, 3, 101, unit="GHz")
    n = frequency.npoints
    s = np.zeros((n, 2, 2), dtype=complex)
    s[:, 0, 0] = 0.05
    s[:, 1, 1] = 0.05
    s[:, 0, 1] = _NOMINAL_MAGNITUDE
    s[:, 1, 0] = _NOMINAL_MAGNITUDE
    network = rf.Network(frequency=frequency, s=s)
    context = MeasurementContext(dut="10 dB fixed attenuator", instrument="Simulated VNA")
    return Measurement(data=network, context=context)


def _insertion_loss_db(values: dict) -> float:
    measured = _NOMINAL_MAGNITUDE + values["vna_noise"] + values["calibration"]
    return -20 * math.log10(measured)


def _build_uncertainty_model() -> UncertaintyModel:
    vna_noise = UncertaintySource(
        name="vna_noise",
        description="Receiver noise / repeatability",
        uncertainty_type=UncertaintyType.TYPE_A,
        distribution=Distribution.NORMAL,
        standard_uncertainty=0.002,
        unit="linear magnitude",
        nominal_value=0.0,
    )
    calibration = UncertaintySource(
        name="calibration",
        description="Residual calibration-standard uncertainty",
        uncertainty_type=UncertaintyType.TYPE_B,
        distribution=Distribution.UNIFORM,
        standard_uncertainty=standard_uncertainty_from_half_width(Distribution.UNIFORM, 0.02),
        unit="linear magnitude",
        nominal_value=0.0,
    )
    measurand = Measurand(name="IL", definition="Insertion loss, -20*log10(|S21|)", unit="dB")
    return UncertaintyModel(
        measurand=measurand,
        function=_insertion_loss_db,
        sources=(vna_noise, calibration),
        assumptions="vna_noise and calibration are independent additive perturbations to |S21|.",
    )


def test_clean_measurement_passes_qa_before_any_analysis_is_attempted():
    report = validate(_attenuator_measurement())
    assert report.has_failures is False
    assert report.has_warnings is False


def test_linear_and_monte_carlo_propagation_agree_on_a_nonlinear_model():
    model = _build_uncertainty_model()

    linear = propagate_linear(model)
    monte_carlo = propagate_monte_carlo(model, n_samples=100_000, rng=np.random.default_rng(42))

    assert monte_carlo.standard_uncertainty == pytest.approx(
        linear.standard_uncertainty, rel=0.02
    )
    assert monte_carlo.value == pytest.approx(linear.value, abs=0.05)


def test_uncertainty_budget_identifies_the_dominant_source():
    model = _build_uncertainty_model()
    linear = propagate_linear(model)

    budget = build_budget(
        model.measurand, model.sources, linear.sensitivity_coefficients, linear.standard_uncertainty
    )

    assert budget.combined_standard_uncertainty == linear.standard_uncertainty
    assert budget.ranked[0].source.name == "calibration"
    assert sum(c.percentage_of_variance for c in budget.contributions) == pytest.approx(100.0)


def test_full_pipeline_assembles_a_coherent_analysis_result():
    model = _build_uncertainty_model()
    linear = propagate_linear(model)
    monte_carlo = propagate_monte_carlo(model, n_samples=100_000, rng=np.random.default_rng(7))

    expanded, gaussian_interval = expand(linear.value, linear.standard_uncertainty, 0.95)
    mc_interval = coverage_interval_from_samples(monte_carlo.samples, 0.95)

    result = AnalysisResult(
        measurand=model.measurand,
        value=linear.value,
        unit=model.measurand.unit,
        standard_uncertainty=linear.standard_uncertainty,
        expanded_uncertainty=expanded,
        coverage_probability=0.95,
        coverage_interval=gaussian_interval,
        contributing_sources=tuple(model.sources),
    )

    assert result.value == pytest.approx(10.0, abs=0.1)  # ~10 dB attenuator
    assert result.coverage_interval is not None
    assert result.coverage_interval[0] < result.value < result.coverage_interval[1]
    assert len(result.contributing_sources) == 2
    # The Gaussian and empirical (Monte Carlo) intervals should roughly agree,
    # since one input is close enough to Gaussian for this to hold.
    assert mc_interval[0] == pytest.approx(gaussian_interval[0], abs=0.2)
    assert mc_interval[1] == pytest.approx(gaussian_interval[1], abs=0.2)

