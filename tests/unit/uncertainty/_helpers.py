"""Shared UncertaintySource builders for uncertainty-engine tests."""

from __future__ import annotations

from rfmeasurement.domain.enums import Distribution, UncertaintyType
from rfmeasurement.domain.uncertainty import UncertaintySource


def source(
    name: str,
    *,
    nominal_value: float | None,
    standard_uncertainty: float,
    distribution: Distribution = Distribution.NORMAL,
    correlation: dict[str, float] | None = None,
) -> UncertaintySource:
    return UncertaintySource(
        name=name,
        description=f"synthetic source {name}",
        uncertainty_type=UncertaintyType.TYPE_B,
        distribution=distribution,
        standard_uncertainty=standard_uncertainty,
        unit="linear",
        nominal_value=nominal_value,
        correlation=correlation or {},
    )
