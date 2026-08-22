"""The quantity being reported (docs/domain-model.md#measurand)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Measurand:
    """Definition of a reportable RF quantity, independent of any particular value.

    Examples: S11 at a frequency, insertion loss, group delay, resonance
    frequency, loaded Q, bandwidth, effective permittivity.
    """

    name: str
    definition: str
    unit: str
    frequency_hz: float | None = None
