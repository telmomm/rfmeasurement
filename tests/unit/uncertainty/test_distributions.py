import math

import numpy as np
import pytest
from _helpers import source

from rfmeasurement.domain.enums import Distribution
from rfmeasurement.uncertainty.distributions import (
    MissingNominalValueError,
    sample_source,
    standard_uncertainty_from_half_width,
)


def test_uniform_half_width_conversion_matches_gum():
    assert standard_uncertainty_from_half_width(Distribution.UNIFORM, 3.0) == pytest.approx(
        3.0 / math.sqrt(3)
    )


def test_triangular_half_width_conversion_matches_gum():
    assert standard_uncertainty_from_half_width(Distribution.TRIANGULAR, 6.0) == pytest.approx(
        6.0 / math.sqrt(6)
    )


def test_half_width_conversion_undefined_for_normal():
    with pytest.raises(NotImplementedError):
        standard_uncertainty_from_half_width(Distribution.NORMAL, 1.0)


def test_negative_half_width_rejected():
    with pytest.raises(ValueError):
        standard_uncertainty_from_half_width(Distribution.UNIFORM, -1.0)


def test_normal_samples_match_nominal_and_standard_uncertainty():
    rng = np.random.default_rng(0)
    s = source("x", nominal_value=10.0, standard_uncertainty=2.0, distribution=Distribution.NORMAL)
    samples = sample_source(s, rng, 200_000)
    assert samples.mean() == pytest.approx(10.0, abs=0.02)
    assert samples.std(ddof=1) == pytest.approx(2.0, rel=0.01)


def test_uniform_samples_stay_within_bounds_and_match_standard_uncertainty():
    rng = np.random.default_rng(1)
    u = 1.0
    s = source("x", nominal_value=0.0, standard_uncertainty=u, distribution=Distribution.UNIFORM)
    samples = sample_source(s, rng, 200_000)
    half_width = u * math.sqrt(3)
    assert samples.min() >= -half_width
    assert samples.max() <= half_width
    assert samples.std(ddof=1) == pytest.approx(u, rel=0.01)


def test_sampling_requires_nominal_value():
    s = source("x", nominal_value=None, standard_uncertainty=1.0)
    with pytest.raises(MissingNominalValueError):
        sample_source(s, np.random.default_rng(0), 10)


def test_sampling_unsupported_distribution_raises():
    s = source(
        "x", nominal_value=0.0, standard_uncertainty=1.0, distribution=Distribution.EMPIRICAL
    )
    with pytest.raises(NotImplementedError):
        sample_source(s, np.random.default_rng(0), 10)


def test_finite_degrees_of_freedom_on_non_normal_source_raises():
    s = source(
        "x",
        nominal_value=0.0,
        standard_uncertainty=1.0,
        distribution=Distribution.UNIFORM,
        degrees_of_freedom=4,
    )
    with pytest.raises(NotImplementedError, match="degrees of freedom"):
        sample_source(s, np.random.default_rng(0), 10)


def test_infinite_degrees_of_freedom_samples_like_an_exactly_known_source():
    exact = source("x", nominal_value=10.0, standard_uncertainty=2.0)
    infinite = source(
        "x", nominal_value=10.0, standard_uncertainty=2.0, degrees_of_freedom=math.inf
    )
    np.testing.assert_array_equal(
        sample_source(exact, np.random.default_rng(0), 100),
        sample_source(infinite, np.random.default_rng(0), 100),
    )
