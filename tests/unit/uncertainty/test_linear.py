import pytest
from _helpers import source

from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.distributions import MissingNominalValueError
from rfmeasurement.uncertainty.linear import propagate_linear

_MEASURAND = Measurand(name="y", definition="test output", unit="linear")

# Analytical GUM reference cases (independent sum, correlated sum, nonlinear
# sensitivity) live in tests/scientific/test_gum_linear_propagation.py. This
# file covers defensive/error-handling behavior only.


def test_missing_nominal_value_raises():
    sources = (source("x", nominal_value=None, standard_uncertainty=0.1),)
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x"],
        sources=sources,
        assumptions="n/a",
    )
    with pytest.raises(MissingNominalValueError):
        propagate_linear(model)


def test_invalid_correlation_structure_yields_negative_variance():
    """Three pairwise correlations of -0.9 cannot jointly be a valid correlation matrix."""
    sources = (
        source(
            "x1",
            nominal_value=0.0,
            standard_uncertainty=1.0,
            correlation={"x2": -0.9, "x3": -0.9},
        ),
        source("x2", nominal_value=0.0, standard_uncertainty=1.0, correlation={"x3": -0.9}),
        source("x3", nominal_value=0.0, standard_uncertainty=1.0),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x1"] + v["x2"] + v["x3"],
        sources=sources,
        assumptions="Deliberately invalid correlation structure, for testing.",
    )
    with pytest.raises(ValueError, match="do not form a valid"):
        propagate_linear(model)
