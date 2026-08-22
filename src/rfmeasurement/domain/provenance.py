"""A single step in a measurement's processing history (docs/reproducibility.md)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True, frozen=True)
class ProvenanceRecord:
    """One node in the provenance graph: an operation applied to produce data.

    A sequence of records forms the transformation chain described in
    docs/reproducibility.md (raw measurement -> calibration -> de-embedding
    -> ... -> reported result).
    """

    operation: str
    software_version: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    parameters: dict[str, object] = field(default_factory=dict)
    inputs: tuple[str, ...] = field(default_factory=tuple)
    notes: str | None = None
