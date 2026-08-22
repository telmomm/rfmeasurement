from rfmeasurement.domain.context import MeasurementContext
from rfmeasurement.domain.enums import MetadataConfidence


def test_default_context_has_no_assumptions():
    context = MeasurementContext()
    assert context.instrument is None
    assert context.sweep_settings == {}
    assert context.confidence == {}


def test_confidence_records_how_a_field_was_obtained():
    context = MeasurementContext(
        temperature_c=23.0,
        confidence={"temperature_c": MetadataConfidence.ESTIMATED},
    )
    assert context.confidence["temperature_c"] is MetadataConfidence.ESTIMATED


def test_frequency_range_is_a_pair():
    context = MeasurementContext(frequency_range_hz=(1e9, 2e9))
    assert context.frequency_range_hz == (1e9, 2e9)
