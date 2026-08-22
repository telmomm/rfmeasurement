import numpy as np
import pytest
from _helpers import source

from rfmeasurement.uncertainty.covariance import build_covariance_matrix


def test_independent_sources_give_diagonal_covariance():
    sources = [
        source("a", nominal_value=0.0, standard_uncertainty=2.0),
        source("b", nominal_value=0.0, standard_uncertainty=3.0),
    ]
    cov = build_covariance_matrix(sources)
    np.testing.assert_allclose(cov, [[4.0, 0.0], [0.0, 9.0]])


def test_declared_correlation_fills_symmetric_off_diagonal():
    sources = [
        source("a", nominal_value=0.0, standard_uncertainty=2.0, correlation={"b": 0.5}),
        source("b", nominal_value=0.0, standard_uncertainty=3.0),
    ]
    cov = build_covariance_matrix(sources)
    expected_off_diagonal = 0.5 * 2.0 * 3.0
    assert cov[0, 1] == pytest.approx(expected_off_diagonal)
    assert cov[1, 0] == pytest.approx(expected_off_diagonal)


def test_correlation_out_of_range_raises():
    sources = [
        source("a", nominal_value=0.0, standard_uncertainty=1.0, correlation={"b": 1.5}),
        source("b", nominal_value=0.0, standard_uncertainty=1.0),
    ]
    with pytest.raises(ValueError, match=r"\[-1, 1\]"):
        build_covariance_matrix(sources)


def test_inconsistent_bidirectional_correlation_raises():
    sources = [
        source("a", nominal_value=0.0, standard_uncertainty=1.0, correlation={"b": 0.5}),
        source("b", nominal_value=0.0, standard_uncertainty=1.0, correlation={"a": -0.5}),
    ]
    with pytest.raises(ValueError, match="Inconsistent correlation"):
        build_covariance_matrix(sources)
