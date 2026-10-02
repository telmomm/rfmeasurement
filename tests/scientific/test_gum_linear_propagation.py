"""GUM first-order propagation checked against textbook analytical reference cases.

Reference: JCGM 100:2008 (GUM), the law of propagation of uncertainty,
clause 5 (in particular 5.1.2 for uncorrelated inputs and 5.2.2 for
correlated inputs), and Annex G.4 (Welch-Satterthwaite formula) with the
worked example H.1 for effective degrees of freedom.
"""

from __future__ import annotations

import math

import pytest
from _sources import source

from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.coverage import expand
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


def test_effective_degrees_of_freedom_of_two_equal_contributions():
    """GUM G.2b: two equal contributions with nu each -> nu_eff = 2 * nu."""
    sources = (
        source("x1", nominal_value=1.0, standard_uncertainty=0.1, degrees_of_freedom=4),
        source("x2", nominal_value=2.0, standard_uncertainty=0.1, degrees_of_freedom=4),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x1"] + v["x2"],
        sources=sources,
        assumptions="Independent additive contributions.",
    )
    assert propagate_linear(model).effective_degrees_of_freedom == pytest.approx(8.0)


def test_exactly_known_source_raises_effective_degrees_of_freedom():
    """GUM G.2b with nu_2 -> infinity: nu_eff = nu_1 * (u_c / u_1)^4."""
    sources = (
        source("x1", nominal_value=1.0, standard_uncertainty=0.1, degrees_of_freedom=4),
        source("x2", nominal_value=2.0, standard_uncertainty=0.1),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x1"] + v["x2"],
        sources=sources,
        assumptions="Independent additive contributions.",
    )
    assert propagate_linear(model).effective_degrees_of_freedom == pytest.approx(16.0)


def test_effective_degrees_of_freedom_is_none_when_no_source_declares_any():
    sources = (
        source("x1", nominal_value=1.0, standard_uncertainty=0.1),
        source("x2", nominal_value=2.0, standard_uncertainty=0.2, degrees_of_freedom=math.inf),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x1"] + v["x2"],
        sources=sources,
        assumptions="Independent additive contributions.",
    )
    assert propagate_linear(model).effective_degrees_of_freedom is None


def test_gum_h1_end_gauge_calibration():
    """GUM H.1 (Table H.1, H.1.6): u_c(l) = 32 nm, nu_eff = 16.7, U_99 = 93 nm.

    l = l_s + d - l_s * (delta_alpha * theta + alpha_s * delta_theta), lengths in nm.
    """
    sources = (
        source("l_s", nominal_value=50_000_623.0, standard_uncertainty=25.0, degrees_of_freedom=18),
        source("d", nominal_value=215.0, standard_uncertainty=9.7, degrees_of_freedom=25.6),
        source("alpha_s", nominal_value=11.5e-6, standard_uncertainty=1.2e-6),
        source("theta", nominal_value=-0.1, standard_uncertainty=0.41),
        source(
            "delta_alpha", nominal_value=0.0, standard_uncertainty=0.58e-6, degrees_of_freedom=50
        ),
        source("delta_theta", nominal_value=0.0, standard_uncertainty=0.029, degrees_of_freedom=2),
    )
    model = UncertaintyModel(
        measurand=Measurand(name="l", definition="end gauge length at 20 degC", unit="nm"),
        function=lambda v: v["l_s"]
        + v["d"]
        - v["l_s"] * (v["delta_alpha"] * v["theta"] + v["alpha_s"] * v["delta_theta"]),
        sources=sources,
        assumptions="GUM H.1: uncorrelated inputs, first-order terms only.",
    )
    result = propagate_linear(model)
    assert result.value == pytest.approx(50_000_838.0)
    assert result.standard_uncertainty == pytest.approx(32.0, abs=0.5)
    assert result.effective_degrees_of_freedom == pytest.approx(16.7, abs=0.1)

    # GUM G.6.4: truncate nu_eff to the next lower integer for the table lookup.
    expanded, _ = expand(
        result.value,
        result.standard_uncertainty,
        0.99,
        math.floor(result.effective_degrees_of_freedom),
    )
    assert expanded == pytest.approx(93.0, abs=1.0)
