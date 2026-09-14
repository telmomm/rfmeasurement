"""How was this number produced?

Continues the story from examples/01_validate_measurement.py and
examples/02_propagate_uncertainty.py: the same attenuator insertion-loss
result went through import, calibration, validation and two independent
uncertainty-propagation methods before being reported. Phase 3 already lets
each of those steps attach a `ProvenanceRecord` to the measurement; this
example builds the actual `ProvenanceGraph` over that history so the final
result can be audited back to its raw input, per docs/reproducibility.md.

No new computation happens here -- the recorded steps mirror examples
01/02, condensed into provenance entries so the graph has something
realistic to link together.

Run with:
    python examples/04_provenance_graph.py
"""

from __future__ import annotations

import json

import numpy as np
import skrf as rf

from rfmeasurement import __version__
from rfmeasurement.domain import Measurement, MeasurementContext, ProvenanceRecord
from rfmeasurement.provenance import ProvenanceGraph


def _build_measurement_with_history() -> Measurement:
    """Attach one ProvenanceRecord per processing step, oldest first.

    `inputs` links each step to the record(s) it was derived from;
    `raw.inputs` names the original VNA sweep file, which is external to
    this measurement's own history (it was never itself a ProvenanceRecord).
    """
    raw = ProvenanceRecord(
        operation="import_touchstone",
        software_version=__version__,
        inputs=("vna-sweep-2026-01-01.s2p",),
    )
    calibrated = ProvenanceRecord(
        operation="apply_calibration",
        software_version=__version__,
        parameters={"method": "SOLT"},
        inputs=(raw.record_id,),
    )
    validated = ProvenanceRecord(
        operation="validate",
        software_version=__version__,
        parameters={"rules": "DEFAULT_RULES"},
        inputs=(calibrated.record_id,),
    )
    linear = ProvenanceRecord(
        operation="propagate_uncertainty_linear",
        software_version=__version__,
        inputs=(calibrated.record_id,),
    )
    monte_carlo = ProvenanceRecord(
        operation="propagate_uncertainty_monte_carlo",
        software_version=__version__,
        parameters={"n_samples": 100_000, "seed": 42},
        inputs=(calibrated.record_id,),
    )
    reported = ProvenanceRecord(
        operation="report_result",
        software_version=__version__,
        notes="Insertion loss at 2 GHz, reported with 95% coverage interval",
        inputs=(validated.record_id, linear.record_id, monte_carlo.record_id),
    )

    frequency = rf.Frequency(1, 3, 101, unit="GHz")
    network = rf.Network(frequency=frequency, s=np.zeros((frequency.npoints, 2, 2), dtype=complex))
    context = MeasurementContext(dut="10 dB fixed attenuator", instrument="Simulated VNA")
    return Measurement(
        data=network,
        context=context,
        provenance=[raw, calibrated, validated, linear, monte_carlo, reported],
    )


def main() -> None:
    measurement = _build_measurement_with_history()
    graph = ProvenanceGraph.from_measurement(measurement)

    reported_id = measurement.provenance[-1].record_id

    print("Processing order (oldest first)")
    print("--------------------------------")
    for record_id in graph.topological_order():
        record = graph.records[record_id]
        print(f"{record.operation:32} [{record_id[:8]}]")

    print(f"\nEverything behind the reported result [{reported_id[:8]}]")
    print("--------------------------------------------------------")
    for ancestor_id in graph.ancestors(reported_id):
        print(f"- {graph.records[ancestor_id].operation} [{ancestor_id[:8]}]")

    print("\nExternal sources referenced but not themselves recorded here")
    print("--------------------------------------------------------------")
    for source in graph.external_sources:
        print(f"- {source}")

    print("\nMachine-readable graph (JSON)")
    print("-----------------------------")
    print(json.dumps(graph.to_dict(), indent=2, default=str))


if __name__ == "__main__":
    main()
