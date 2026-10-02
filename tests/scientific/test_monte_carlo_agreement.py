"""Monte Carlo propagation checked against analytical references and an independent
implementation (linear/GUM propagation).

Reference: JCGM 101:2008 (GUM Supplement 1), the Monte Carlo method for
uncertainty propagation (6.4.9.2 for Type A sources with finite degrees of
freedom).
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from _sources import source

from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.coverage import coverage_interval_from_samples, expand
from rfmeasurement.uncertainty.linear import propagate_linear
from rfmeasurement.uncertainty.monte_carlo import propagate_monte_carlo

_MEASURAND = Measurand(name="y", definition="test output", unit="linear")
_N_SAMPLES = 50_000


def test_independent_sum_matches_analytical_root_sum_of_squares():
    """GUM 5.1.2 reference case, verified via sampling instead of the Taylor expansion."""
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
    """Cross-checks the correlated-normal Monte Carlo sampler against linear propagation."""
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


def test_finite_degrees_of_freedom_source_is_sampled_from_scaled_t_distribution():
    """JCGM 101 6.4.9.2: X = x + u * t_nu, so the 95 % interval is x +/- t_0.975(nu) * u
    (the GUM G.3 interval) and the standard deviation is u * sqrt(nu / (nu - 2))."""
    nominal, u, nu = 1.0, 0.1, 4
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x"],
        sources=(
            source("x", nominal_value=nominal, standard_uncertainty=u, degrees_of_freedom=nu),
        ),
        assumptions="y = x, x the mean of 5 repeated readings.",
    )
    mc_result = propagate_monte_carlo(model, n_samples=200_000, rng=np.random.default_rng(3))
    lower, upper = coverage_interval_from_samples(mc_result.samples, 0.95)
    _, (expected_lower, expected_upper) = expand(nominal, u, 0.95, degrees_of_freedom=nu)
    assert lower == pytest.approx(expected_lower, abs=0.005)
    assert upper == pytest.approx(expected_upper, abs=0.005)
    assert mc_result.standard_uncertainty == pytest.approx(u * math.sqrt(nu / (nu - 2)), rel=0.03)
