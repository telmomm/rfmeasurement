"""GUM first-order propagation checked against textbook analytical reference cases.

Reference: JCGM 100:2008 (GUM), the law of propagation of uncertainty,
clause 5 (in particular 5.1.2 for uncorrelated inputs and 5.2.2 for
correlated inputs).
"""

from __future__ import annotations

import math

import pytest
from _sources import source

from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.linear import propagate_linear

_MEASURAND = Measurand(name="y", definition="test output", unit="linear")


def test_independent_sum_matches_root_sum_of_squares():
    """GUM 5.1.2: y = x1 + x2, independent -> u_c(y) = sqrt(u(x1)^2 + u(x2)^2)."""
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
    result = propagate_linear(model)
    assert result.value == pytest.approx(3.0)
    assert result.standard_uncertainty == pytest.approx(math.hypot(0.1, 0.2))
    assert result.sensitivity_coefficients["x1"] == pytest.approx(1.0)
    assert result.sensitivity_coefficients["x2"] == pytest.approx(1.0)


def test_perfectly_correlated_sum_adds_linearly():
    """GUM 5.2.2: fully correlated (r=1) sum -> u_c(y) = u(x1) + u(x2), not root-sum-of-squares."""
    sources = (
        source("x1", nominal_value=1.0, standard_uncertainty=0.1, correlation={"x2": 1.0}),
        source("x2", nominal_value=2.0, standard_uncertainty=0.2),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x1"] + v["x2"],
        sources=sources,
        assumptions="Fully correlated additive contributions (e.g. a shared calibration error).",
    )
    result = propagate_linear(model)
    assert result.standard_uncertainty == pytest.approx(0.1 + 0.2)


def test_analytic_sensitivity_matches_finite_difference_for_nonlinear_model():
    """y = 20*log10(x): compare the closed-form dB/dx sensitivity to the numerical fallback.

    A genuinely nonlinear RF measurement model (magnitude-to-dB conversion),
    not the toy linear sums above.
    """
    x0 = 0.5
    ux = 0.01
    sources_with_analytic = (source("x", nominal_value=x0, standard_uncertainty=ux),)
    dB = lambda v: 20 * math.log10(v["x"])  # noqa: E731
    analytic_sensitivity = 20 / (x0 * math.log(10))

    with_analytic = propagate_linear(
        UncertaintyModel(
            measurand=_MEASURAND,
            function=dB,
            sources=sources_with_analytic,
            assumptions="dB conversion of a linear-magnitude measurement.",
            sensitivity={"x": analytic_sensitivity},
        )
    )
    with_numeric = propagate_linear(
        UncertaintyModel(
            measurand=_MEASURAND,
            function=dB,
            sources=sources_with_analytic,
            assumptions="dB conversion of a linear-magnitude measurement.",
        )
    )
    assert with_numeric.sensitivity_coefficients["x"] == pytest.approx(
        analytic_sensitivity, rel=1e-4
    )
    assert with_analytic.standard_uncertainty == pytest.approx(
        with_numeric.standard_uncertainty, rel=1e-4
    )
    assert with_analytic.standard_uncertainty == pytest.approx(
        abs(analytic_sensitivity) * ux, rel=1e-6
    )
