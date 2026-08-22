from rfmeasurement.domain.budget import UncertaintyBudget, UncertaintyContribution
from rfmeasurement.domain.enums import Distribution, UncertaintyType
from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty import UncertaintySource


def _contribution(name: str, variance: float) -> UncertaintyContribution:
    source = UncertaintySource(
        name=name,
        description="test source",
        uncertainty_type=UncertaintyType.TYPE_B,
        distribution=Distribution.NORMAL,
        standard_uncertainty=variance**0.5,
        unit="dB",
    )
    return UncertaintyContribution(
        source=source,
        sensitivity_coefficient=1.0,
        contribution=variance**0.5,
        variance_contribution=variance,
        percentage_of_variance=0.0,
    )


def test_ranked_orders_by_variance_contribution_descending():
    budget = UncertaintyBudget(
        measurand=Measurand(name="S21", definition="Insertion loss", unit="dB"),
        contributions=[_contribution("small", 0.01), _contribution("large", 1.0)],
        combined_standard_uncertainty=1.01**0.5,
    )
    assert [c.source.name for c in budget.ranked] == ["large", "small"]


def test_default_budget_has_no_contributions():
    budget = UncertaintyBudget(measurand=Measurand(name="S21", definition="x", unit="dB"))
    assert budget.contributions == []
    assert budget.ranked == []
