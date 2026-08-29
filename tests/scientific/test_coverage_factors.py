"""Coverage factors and intervals checked against known GUM/NIST reference values.

Reference: JCGM 100:2008 (GUM) clause 6, and NIST TN 1297, section 6, for
the standard k=1/k=2/k=1.96 coverage-factor conventions.
"""

from __future__ import annotations

import numpy as np
import pytest

from rfmeasurement.uncertainty.coverage import (
    coverage_factor,
    coverage_interval_from_samples,
    expand,
)


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
