import math

import pytest
from _helpers import source

from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.uncertainty.budget import build_budget

_MEASURAND = Measurand(name="y", definition="test output", unit="linear")


def test_equal_independent_sources_split_variance_evenly():
    sources = [
        source("a", nominal_value=0.0, standard_uncertainty=1.0),
        source("b", nominal_value=0.0, standard_uncertainty=1.0),
    ]
    combined = math.hypot(1.0, 1.0)
    budget = build_budget(_MEASURAND, sources, {"a": 1.0, "b": 1.0}, combined)
    assert budget.combined_standard_uncertainty == combined
    for contribution in budget.contributions:
        assert contribution.percentage_of_variance == pytest.approx(50.0)


def test_ranked_puts_dominant_contributor_first():
    sources = [
        source("small", nominal_value=0.0, standard_uncertainty=0.1),
        source("large", nominal_value=0.0, standard_uncertainty=1.0),
    ]
    combined = math.hypot(0.1, 1.0)
    budget = build_budget(_MEASURAND, sources, {"small": 1.0, "large": 1.0}, combined)
    assert budget.ranked[0].source.name == "large"


def test_sensitivity_coefficient_scales_contribution():
    sources = [source("a", nominal_value=0.0, standard_uncertainty=2.0)]
    budget = build_budget(_MEASURAND, sources, {"a": 3.0}, combined_standard_uncertainty=6.0)
    assert budget.contributions[0].contribution == pytest.approx(6.0)
    assert budget.contributions[0].percentage_of_variance == pytest.approx(100.0)
