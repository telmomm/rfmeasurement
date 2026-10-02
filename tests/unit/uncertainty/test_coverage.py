import math

import pytest
from _helpers import source

from rfmeasurement.uncertainty.coverage import (
    coverage_factor,
    coverage_interval_from_samples,
    effective_degrees_of_freedom,
)

# Coverage-factor and interval reference-value checks live in
# tests/scientific/test_coverage_factors.py. This file covers
# defensive/error-handling behavior only.


def test_coverage_factor_rejects_invalid_probability():
    with pytest.raises(ValueError):
        coverage_factor(1.0)
    with pytest.raises(ValueError):
        coverage_factor(0.0)


def test_coverage_interval_from_samples_rejects_invalid_probability():
    with pytest.raises(ValueError):
        coverage_interval_from_samples([1.0, 2.0, 3.0], 1.0)


@pytest.mark.parametrize("degrees_of_freedom", [0, -1, math.nan])
def test_coverage_factor_rejects_invalid_degrees_of_freedom(degrees_of_freedom):
    with pytest.raises(ValueError, match="degrees_of_freedom"):
        coverage_factor(0.95, degrees_of_freedom)


def test_effective_degrees_of_freedom_rejects_invalid_source_degrees_of_freedom():
    sources = (source("x", nominal_value=0.0, standard_uncertainty=1.0, degrees_of_freedom=0),)
    with pytest.raises(ValueError, match="'x'"):
        effective_degrees_of_freedom(sources, {"x": 1.0}, 1.0)


def test_effective_degrees_of_freedom_ignores_sources_that_do_not_contribute():
    sources = (
        source("x1", nominal_value=0.0, standard_uncertainty=1.0),
        source("x2", nominal_value=0.0, standard_uncertainty=1.0, degrees_of_freedom=3),
    )
    assert effective_degrees_of_freedom(sources, {"x1": 1.0, "x2": 0.0}, 1.0) is None
