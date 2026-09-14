import pytest

from rfmeasurement.domain.provenance import ProvenanceRecord
from rfmeasurement.provenance.graph import ProvenanceCycleError, ProvenanceGraph


def _record(record_id: str, inputs: tuple[str, ...] = ()) -> ProvenanceRecord:
    return ProvenanceRecord(
        operation="op",
        software_version="0.1.0.dev0",
        record_id=record_id,
        inputs=inputs,
    )


def test_from_records_orders_dependencies_before_dependents():
    raw = _record("raw")
    calibrated = _record("calibrated", inputs=("raw",))
    deembedded = _record("deembedded", inputs=("calibrated",))

    graph = ProvenanceGraph.from_records([deembedded, calibrated, raw])

    order = graph.topological_order()
    assert order.index("raw") < order.index("calibrated") < order.index("deembedded")


def test_external_inputs_are_not_errors():
    imported = _record("imported", inputs=("dut-serial-001",))

    graph = ProvenanceGraph.from_records([imported])

    assert graph.external_sources == ("dut-serial-001",)
    assert graph.ancestors("imported") == ()


def test_ancestors_and_descendants_are_transitive():
    raw = _record("raw")
    calibrated = _record("calibrated", inputs=("raw",))
    result = _record("result", inputs=("calibrated",))

    graph = ProvenanceGraph.from_records([raw, calibrated, result])

    assert graph.ancestors("result") == ("calibrated", "raw")
    assert graph.descendants("raw") == ("calibrated", "result")
    assert graph.ancestors("raw") == ()
    assert graph.descendants("result") == ()


def test_duplicate_record_id_is_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        ProvenanceGraph.from_records([_record("a"), _record("a")])


def test_cycle_is_detected():
    a = _record("a", inputs=("b",))
    b = _record("b", inputs=("a",))

    with pytest.raises(ProvenanceCycleError):
        ProvenanceGraph.from_records([a, b])


def test_to_dict_is_json_serializable_and_captures_structure():
    import json

    raw = _record("raw")
    result = _record("result", inputs=("raw",))
    graph = ProvenanceGraph.from_records([raw, result])

    payload = json.dumps(graph.to_dict())
    decoded = json.loads(payload)

    assert {node["record_id"] for node in decoded["nodes"]} == {"raw", "result"}
    assert decoded["edges"] == [{"from": "raw", "to": "result"}]
    assert decoded["external_sources"] == []


def test_from_measurement_uses_measurement_provenance():
    import numpy as np
    import skrf as rf

    from rfmeasurement.domain.measurement import Measurement

    frequency = rf.Frequency(1, 2, 2, unit="GHz")
    network = rf.Network(frequency=frequency, s=np.zeros((2, 1, 1), dtype=complex))
    measurement = Measurement(data=network, provenance=[_record("raw")])

    graph = ProvenanceGraph.from_measurement(measurement)

    assert graph.topological_order() == ("raw",)
