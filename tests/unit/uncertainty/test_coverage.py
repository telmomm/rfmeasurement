import pytest

from rfmeasurement.uncertainty.coverage import coverage_factor, coverage_interval_from_samples

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
