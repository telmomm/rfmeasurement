"""Assemble a ranked uncertainty budget from a propagation result."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from rfmeasurement.domain.budget import UncertaintyBudget, UncertaintyContribution
from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty import UncertaintySource


def build_budget(
    measurand: Measurand,
    sources: Sequence[UncertaintySource],
    sensitivity_coefficients: Mapping[str, float],
    combined_standard_uncertainty: float,
) -> UncertaintyBudget:
    """Build a ranked uncertainty budget from a linear-propagation-style result.

    ``sensitivity_coefficients`` and ``combined_standard_uncertainty`` are
    typically taken directly from a
    :class:`~rfmeasurement.uncertainty.linear.LinearPropagationResult`.
    """
    total_variance = combined_standard_uncertainty**2
    contributions = []
    for source in sources:
        coefficient = sensitivity_coefficients[source.name]
        contribution = abs(coefficient) * source.standard_uncertainty
        variance_contribution = contribution**2
        percentage = (variance_contribution / total_variance * 100) if total_variance > 0 else 0.0
        contributions.append(
            UncertaintyContribution(
                source=source,
                sensitivity_coefficient=coefficient,
                contribution=contribution,
                variance_contribution=variance_contribution,
                percentage_of_variance=percentage,
            )
        )
    return UncertaintyBudget(
        measurand=measurand,
        contributions=contributions,
        combined_standard_uncertainty=combined_standard_uncertainty,
    )
