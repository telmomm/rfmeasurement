"""A ranked breakdown of a combined uncertainty into its contributing sources."""

from __future__ import annotations

from dataclasses import dataclass, field

from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty import UncertaintySource


@dataclass(slots=True, frozen=True)
class UncertaintyContribution:
    """One source's contribution to a combined standard uncertainty.

    ``percentage_of_variance`` is this source's own variance contribution
    (``contribution ** 2``) as a share of the total combined variance. When
    sources are correlated, individual contributions do not include the
    covariance cross-terms, so percentages across all contributions will not
    generally sum to 100%; the cross-terms are only reflected in
    ``UncertaintyBudget.combined_standard_uncertainty``.
    """

    source: UncertaintySource
    sensitivity_coefficient: float
    contribution: float
    variance_contribution: float
    percentage_of_variance: float


@dataclass(slots=True)
class UncertaintyBudget:
    """The combined uncertainty for one measurand, broken down by source.

    docs/uncertainty.md: "It should be possible to rank contributors."
    """

    measurand: Measurand
    contributions: list[UncertaintyContribution] = field(default_factory=list)
    combined_standard_uncertainty: float = 0.0

    @property
    def ranked(self) -> list[UncertaintyContribution]:
        """Contributions ordered from largest to smallest variance contribution."""
        return sorted(self.contributions, key=lambda c: c.variance_contribution, reverse=True)
