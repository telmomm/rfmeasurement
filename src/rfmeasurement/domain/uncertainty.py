"""An independent uncertainty contributor (docs/uncertainty.md)."""

from __future__ import annotations

from dataclasses import dataclass, field

from rfmeasurement.domain.enums import Distribution, UncertaintyType


@dataclass(slots=True, frozen=True)
class UncertaintySource:
    """One contributor to a measurand's combined uncertainty.

    Represented independently of any specific combined result so that a
    budget can later rank contributors and correlations between sources can
    be modelled explicitly rather than assumed away (docs/uncertainty.md).
    ``correlation`` maps another source's ``name`` to a correlation
    coefficient in [-1, 1].
    """

    name: str
    description: str
    uncertainty_type: UncertaintyType
    distribution: Distribution
    standard_uncertainty: float
    unit: str
    nominal_value: float | None = None
    correlation: dict[str, float] = field(default_factory=dict)
    source_reference: str | None = None
    assumptions: str | None = None
