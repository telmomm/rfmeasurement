import numpy as np
import pytest
from _helpers import source

from rfmeasurement.domain.enums import Distribution
from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.monte_carlo import propagate_monte_carlo

_MEASURAND = Measurand(name="y", definition="test output", unit="linear")

# Analytical/cross-implementation agreement cases live in
# tests/scientific/test_monte_carlo_agreement.py. This file covers
# software-correctness (reproducibility, error handling) only.


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
