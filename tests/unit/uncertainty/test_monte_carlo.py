import math

import numpy as np
import pytest
from _helpers import source

from rfmeasurement.domain.enums import Distribution
from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.linear import propagate_linear
from rfmeasurement.uncertainty.monte_carlo import propagate_monte_carlo

_MEASURAND = Measurand(name="y", definition="test output", unit="linear")
_N_SAMPLES = 50_000


def test_independent_sum_matches_analytical_root_sum_of_squares():
    sources = (
        source("x1", nominal_value=1.0, standard_uncertainty=0.1),
        source("x2", nominal_value=2.0, standard_uncertainty=0.2),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x1"] + v["x2"],
        sources=sources,
        assumptions="Independent additive contributions.",
    )
    result = propagate_monte_carlo(model, n_samples=_N_SAMPLES, rng=np.random.default_rng(0))
    assert result.value == pytest.approx(3.0, abs=0.01)
    assert result.standard_uncertainty == pytest.approx(math.hypot(0.1, 0.2), rel=0.02)


def test_fully_correlated_sum_matches_linear_propagation():
    sources = (
        source("x1", nominal_value=1.0, standard_uncertainty=0.1, correlation={"x2": 1.0}),
        source("x2", nominal_value=2.0, standard_uncertainty=0.2),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x1"] + v["x2"],
        sources=sources,
        assumptions="Fully correlated additive contributions.",
    )
    mc_result = propagate_monte_carlo(model, n_samples=_N_SAMPLES, rng=np.random.default_rng(1))
    linear_result = propagate_linear(model)
    assert mc_result.standard_uncertainty == pytest.approx(
        linear_result.standard_uncertainty, rel=0.02
    )


def test_nonlinear_model_agrees_with_linear_propagation_for_small_uncertainty():
    """Cross-check two independent implementations on a genuinely nonlinear RF model."""
    sources = (source("x", nominal_value=0.5, standard_uncertainty=0.002),)
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: 20 * math.log10(v["x"]),
        sources=sources,
        assumptions="dB conversion; uncertainty small enough for the linear approximation to hold.",
    )
    mc_result = propagate_monte_carlo(model, n_samples=_N_SAMPLES, rng=np.random.default_rng(2))
    linear_result = propagate_linear(model)
    assert mc_result.standard_uncertainty == pytest.approx(
        linear_result.standard_uncertainty, rel=0.05
    )


def test_reproducible_with_explicit_seed():
    sources = (source("x", nominal_value=1.0, standard_uncertainty=0.1),)
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x"] ** 2,
        sources=sources,
        assumptions="n/a",
    )
    result_a = propagate_monte_carlo(model, n_samples=1000, rng=np.random.default_rng(42))
    result_b = propagate_monte_carlo(model, n_samples=1000, rng=np.random.default_rng(42))
    assert result_a.value == result_b.value
    assert result_a.standard_uncertainty == result_b.standard_uncertainty
    np.testing.assert_array_equal(result_a.samples, result_b.samples)


def test_unsupported_distribution_raises():
    sources = (
        source(
            "x", nominal_value=0.0, standard_uncertainty=1.0, distribution=Distribution.EMPIRICAL
        ),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND, function=lambda v: v["x"], sources=sources, assumptions="n/a"
    )
    with pytest.raises(NotImplementedError):
        propagate_monte_carlo(model, n_samples=10)


def test_correlation_between_non_normal_sources_raises():
    sources = (
        source(
            "x1",
            nominal_value=0.0,
            standard_uncertainty=1.0,
            distribution=Distribution.UNIFORM,
            correlation={"x2": 0.5},
        ),
        source(
            "x2", nominal_value=0.0, standard_uncertainty=1.0, distribution=Distribution.UNIFORM
        ),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x1"] + v["x2"],
        sources=sources,
        assumptions="n/a",
    )
    with pytest.raises(NotImplementedError):
        propagate_monte_carlo(model, n_samples=10)
