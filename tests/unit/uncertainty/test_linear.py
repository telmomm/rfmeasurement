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


@pytest.mark.parametrize("declared_on", ["x1", "x2"])
def test_correlated_source_with_finite_degrees_of_freedom_raises(declared_on):
    """Welch-Satterthwaite assumes uncorrelated inputs, whichever side declares the correlation."""
    sources = (
        source(
            "x1",
            nominal_value=0.0,
            standard_uncertainty=1.0,
            degrees_of_freedom=4,
            correlation={"x2": 0.5} if declared_on == "x1" else None,
        ),
        source(
            "x2",
            nominal_value=0.0,
            standard_uncertainty=1.0,
            correlation={"x1": 0.5} if declared_on == "x2" else None,
        ),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x1"] + v["x2"],
        sources=sources,
        assumptions="n/a",
    )
    with pytest.raises(NotImplementedError, match="Welch-Satterthwaite"):
        propagate_linear(model)


def test_correlation_between_exactly_known_sources_keeps_effective_degrees_of_freedom():
    sources = (
        source("x1", nominal_value=0.0, standard_uncertainty=1.0, correlation={"x2": 1.0}),
        source("x2", nominal_value=0.0, standard_uncertainty=1.0),
        source("x3", nominal_value=0.0, standard_uncertainty=2.0, degrees_of_freedom=4),
    )
    model = UncertaintyModel(
        measurand=_MEASURAND,
        function=lambda v: v["x1"] + v["x2"] + v["x3"],
        sources=sources,
        assumptions="n/a",
    )
    result = propagate_linear(model)
    # u_c^2 = (1 + 1)^2 + 2^2 = 8; nu_eff = 8^2 / (2^4 / 4) = 16.
    assert result.effective_degrees_of_freedom == pytest.approx(16.0)
