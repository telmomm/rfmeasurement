from datetime import datetime, timezone

from rfmeasurement.domain.provenance import ProvenanceRecord


def test_provenance_record_defaults_to_now_in_utc():
    record = ProvenanceRecord(operation="import_touchstone", software_version="0.1.0.dev0")
    assert record.timestamp.tzinfo is not None
    assert record.timestamp.tzinfo.utcoffset(record.timestamp) == timezone.utc.utcoffset(None)
    assert record.parameters == {}
    assert record.inputs == ()


def test_provenance_record_can_reference_prior_inputs():
    record = ProvenanceRecord(
        operation="de_embed",
        software_version="0.1.0.dev0",
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        parameters={"method": "short-open"},
        inputs=("raw-measurement-001",),
    )
    assert record.inputs == ("raw-measurement-001",)
    assert record.parameters["method"] == "short-open"
