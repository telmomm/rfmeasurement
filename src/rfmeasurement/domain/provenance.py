"""A single step in a measurement's processing history (docs/reproducibility.md)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(slots=True, frozen=True)
class ProvenanceRecord:
    """One node in the provenance graph: an operation applied to produce data.

    A sequence of records forms the transformation chain described in
    docs/reproducibility.md (raw measurement -> calibration -> de-embedding
    -> ... -> reported result). ``record_id`` identifies this node so other
    records can reference it in ``inputs``; an input that does not match any
    known record's ``record_id`` is an external source (e.g. a raw dataset
    or instrument reading) rather than a broken link -- see
    :class:`rfmeasurement.provenance.graph.ProvenanceGraph`.
    """

    operation: str
    software_version: str
    record_id: str = field(default_factory=lambda: uuid4().hex)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    parameters: dict[str, object] = field(default_factory=dict)
    inputs: tuple[str, ...] = field(default_factory=tuple)
    notes: str | None = None
