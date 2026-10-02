"""Coverage factors and intervals checked against known GUM/NIST reference values.

Reference: JCGM 100:2008 (GUM) clause 6, and NIST TN 1297, section 6, for
the standard k=1/k=2/k=1.96 coverage-factor conventions; GUM Annex G
(Table G.2) for Student-t factors with finite degrees of freedom.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from _sources import source

from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.coverage import (
    coverage_factor,
    coverage_interval_from_samples,
    expand,
)
from rfmeasurement.uncertainty.linear import propagate_linear


def test_coverage_factor_matches_known_gum_values():
    """k=1 at 68.27%, k=2 at 95.45%, k=1.959964 at 95% -- the standard GUM/NIST table."""
    assert coverage_factor(0.6826894921) == pytest.approx(1.0, abs=1e-6)
    assert coverage_factor(0.9544997361) == pytest.approx(2.0, abs=1e-6)
    assert coverage_factor(0.95) == pytest.approx(1.959963985, abs=1e-6)


def test_expand_returns_symmetric_interval_around_value():
    expanded, (lower, upper) = expand(
        value=10.0, standard_uncertainty=0.5, coverage_probability=0.95
    )
    assert expanded == pytest.approx(0.5 * 1.959963985, abs=1e-6)
    assert lower == pytest.approx(10.0 - expanded)
    assert upper == pytest.approx(10.0 + expanded)


def test_coverage_interval_from_samples_matches_expand_for_normal_data():
    """The empirical (percentile-based) interval should agree with the Gaussian one when the
    underlying data really is Gaussian -- cross-checking two independent implementations."""
    rng = np.random.default_rng(0)
    samples = rng.normal(loc=10.0, scale=0.5, size=500_000)
    lower, upper = coverage_interval_from_samples(samples, 0.95)
    _, (expected_lower, expected_upper) = expand(10.0, 0.5, 0.95)
    assert lower == pytest.approx(expected_lower, abs=0.01)
    assert upper == pytest.approx(expected_upper, abs=0.01)


@pytest.mark.parametrize(
    ("coverage_probability", "degrees_of_freedom", "expected"),
    [
        (0.95, 1, 12.71),
        (0.95, 2, 4.30),
        (0.95, 4, 2.78),
        (0.95, 10, 2.23),
        (0.95, 30, 2.04),
        (0.95, 100, 1.984),
        (0.6827, 5, 1.11),
        (0.99, 16, 2.92),
        (0.9973, 3, 9.22),
    ],
)
def test_coverage_factor_matches_gum_table_g2(coverage_probability, degrees_of_freedom, expected):
    """GUM Table G.2: t_p(nu) for a given coverage probability and degrees of freedom."""
    assert coverage_factor(coverage_probability, degrees_of_freedom) == pytest.approx(
        expected, abs=0.006
    )


def test_coverage_factor_tends_to_gaussian_for_large_degrees_of_freedom():
    """GUM G.3.2: the t-distribution approaches the normal as nu -> infinity."""
    gaussian = coverage_factor(0.95)
    assert coverage_factor(0.95, 1e7) == pytest.approx(gaussian, abs=1e-6)
    assert coverage_factor(0.95, math.inf) == gaussian


def test_expand_uses_student_t_factor_when_degrees_of_freedom_given():
    expanded, (lower, upper) = expand(10.0, 0.5, 0.95, degrees_of_freedom=4)
    assert expanded == pytest.approx(0.5 * 2.776445, abs=1e-6)
    assert lower == pytest.approx(10.0 - expanded)
    assert upper == pytest.approx(10.0 + expanded)


@pytest.mark.parametrize("n_readings", [3, 5, 10])
def test_expanded_interval_reaches_nominal_coverage_for_few_readings(n_readings):
    """y = x, with x the mean of n normal readings and u(x) its experimental standard deviation.

    With the effective degrees of freedom (nu = n - 1) the 95 % interval must
    contain the true value 95 % of the time; the Gaussian factor does not
    (81 %, 88 % and 92 % for n = 3, 5, 10).
    """
    true_value, sigma, trials, probability = 1.0, 0.1, 20_000, 0.95
    rng = np.random.default_rng(n_readings)
    measurand = Measurand(name="y", definition="y = x", unit="linear")
    hits = gaussian_hits = 0
    for _ in range(trials):
        readings = rng.normal(true_value, sigma, n_readings)
        model = UncertaintyModel(
            measurand=measurand,
            function=lambda v: v["x"],
            sources=(
                source(
                    "x",
                    nominal_value=float(readings.mean()),
                    standard_uncertainty=float(readings.std(ddof=1) / math.sqrt(n_readings)),
                    degrees_of_freedom=n_readings - 1,
                ),
            ),
            assumptions="y = x",
        )
        result = propagate_linear(model)
        _, (lower, upper) = expand(
            result.value,
            result.standard_uncertainty,
            probability,
            result.effective_degrees_of_freedom,
        )
        hits += lower <= true_value <= upper
        _, (lower, upper) = expand(result.value, result.standard_uncertainty, probability)
        gaussian_hits += lower <= true_value <= upper

    # Binomial standard error of the empirical coverage is 0.15 % at 20 000 trials.
    assert hits / trials == pytest.approx(probability, abs=0.006)
    assert gaussian_hits / trials < probability - 0.02
