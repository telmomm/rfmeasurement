"""Shared UncertaintySource builder for scientific-reference tests.

Deliberately named differently from tests/unit/uncertainty/_helpers.py:
pytest imports test-directory helper modules as top-level modules (no
package __init__.py), so two files sharing the same name in different
directories would collide in sys.modules.
"""

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
