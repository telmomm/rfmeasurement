"""Link a measurement's ProvenanceRecords into a queryable, acyclic graph.

docs/reproducibility.md describes provenance as a directed history from raw
measurement through to a reported result. A single record only knows its own
immediate ``inputs``; this module resolves a whole collection of records into
a graph that can be traversed and audited as a unit.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.provenance import ProvenanceRecord


class ProvenanceCycleError(ValueError):
    """Raised when provenance records reference each other in a cycle."""


@dataclass(slots=True, frozen=True)
class ProvenanceGraph:
    """A directed acyclic graph of ProvenanceRecords, linked by record_id/inputs.

    An edge runs from an input identifier to the record that consumed it.
    Identifiers in ``inputs`` that do not match any record's ``record_id``
    are external sources (e.g. a raw dataset or instrument reading): they
    appear as source nodes in :meth:`external_sources` rather than being
    treated as an error.
    """

    records: Mapping[str, ProvenanceRecord]

    @classmethod
    def from_records(cls, records: Iterable[ProvenanceRecord]) -> ProvenanceGraph:
        """Build a graph from a flat collection of records, validating it is acyclic."""
        by_id: dict[str, ProvenanceRecord] = {}
        for record in records:
            if record.record_id in by_id:
                raise ValueError(f"duplicate provenance record_id: {record.record_id!r}")
            by_id[record.record_id] = record
        graph = cls(records=by_id)
        graph.topological_order()
        return graph

    @classmethod
    def from_measurement(cls, measurement: Measurement) -> ProvenanceGraph:
        """Build a graph from a measurement's recorded processing history."""
        return cls.from_records(measurement.provenance)

    @property
    def external_sources(self) -> tuple[str, ...]:
        """Identifiers referenced as inputs but not produced by any record here."""
        referenced = {source for record in self.records.values() for source in record.inputs}
        return tuple(sorted(referenced - self.records.keys()))

    def edges(self) -> tuple[tuple[str, str], ...]:
        """``(source_id, record_id)`` pairs; ``source_id`` may be external."""
        return tuple(
            (source, record.record_id)
            for record in self.records.values()
            for source in record.inputs
        )

    def ancestors(self, record_id: str) -> tuple[str, ...]:
        """Ids of every known record feeding into ``record_id``, transitively."""
        seen: set[str] = set()
        stack = list(self.records[record_id].inputs)
        while stack:
            current = stack.pop()
            if current in seen or current not in self.records:
                continue
            seen.add(current)
            stack.extend(self.records[current].inputs)
        return tuple(sorted(seen))

    def descendants(self, record_id: str) -> tuple[str, ...]:
        """Ids of every record (transitively) derived from ``record_id``."""
        children: dict[str, list[str]] = {}
        for record in self.records.values():
            for source in record.inputs:
                children.setdefault(source, []).append(record.record_id)

        seen: set[str] = set()
        stack = list(children.get(record_id, []))
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            stack.extend(children.get(current, []))
        return tuple(sorted(seen))

    def topological_order(self) -> tuple[str, ...]:
        """Record ids ordered so each record follows every record it depends on.

        Raises :class:`ProvenanceCycleError` if the records reference each
        other in a cycle.
        """
        state: dict[str, int] = {}  # 0 = in progress, 1 = done
        order: list[str] = []

        def visit(record_id: str, path: tuple[str, ...]) -> None:
            status = state.get(record_id)
            if status == 1:
                return
            if status == 0:
                cycle = " -> ".join((*path, record_id))
                raise ProvenanceCycleError(f"cycle detected in provenance graph: {cycle}")
            state[record_id] = 0
            for source in self.records[record_id].inputs:
                if source in self.records:
                    visit(source, (*path, record_id))
            state[record_id] = 1
            order.append(record_id)

        for record_id in self.records:
            visit(record_id, ())
        return tuple(order)

    def to_dict(self) -> dict[str, object]:
        """A JSON-serializable structural summary of the graph."""
        return {
            "nodes": [
                {
                    "record_id": record.record_id,
                    "operation": record.operation,
                    "software_version": record.software_version,
                    "timestamp": record.timestamp.isoformat(),
                    "inputs": list(record.inputs),
                    "parameters": record.parameters,
                    "notes": record.notes,
                }
                for record in self.records.values()
            ],
            "edges": [{"from": source, "to": target} for source, target in self.edges()],
            "external_sources": list(self.external_sources),
        }
