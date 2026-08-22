from _synthetic import active_two_port, matched_two_port

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.validation.engine import DEFAULT_RULES, validate


def test_default_rules_cover_every_roadmap_item():
    identifiers = {rule.identifier for rule in DEFAULT_RULES}
    assert identifiers == {
        "integrity.structural",
        "integrity.finite_values",
        "integrity.frequency_grid",
        "physics.passivity",
        "physics.reciprocity",
        "quality.continuity",
        "quality.dynamic_range",
    }


def test_validate_produces_a_structured_report_for_a_clean_measurement():
    report = validate(Measurement(data=matched_two_port()))
    assert len(report.results) == len(DEFAULT_RULES)
    assert report.has_failures is False


def test_validate_surfaces_a_physical_consistency_failure():
    report = validate(Measurement(data=active_two_port()))
    assert report.has_failures is True
    failed_ids = {r.rule_id for r in report.by_status(ValidationStatus.FAIL)}
    assert "physics.passivity" in failed_ids


def test_validate_does_not_mutate_the_measurement():
    measurement = Measurement(data=matched_two_port())
    validate(measurement)
    assert measurement.validation.results == []
