from rfmeasurement.domain.enums import (
    Distribution,
    MetadataConfidence,
    UncertaintyType,
    ValidationStatus,
)


def test_validation_status_has_five_distinct_outcomes():
    assert len(set(ValidationStatus)) == 5
    assert {s.value for s in ValidationStatus} == {
        "pass",
        "warning",
        "fail",
        "not_applicable",
        "not_evaluated",
    }


def test_uncertainty_type_distinguishes_type_a_and_b():
    assert {t.value for t in UncertaintyType} == {"type_a", "type_b"}


def test_metadata_confidence_values():
    assert {c.value for c in MetadataConfidence} == {
        "measured",
        "specified",
        "estimated",
        "assumed",
        "unknown",
    }


def test_distribution_includes_documented_options():
    assert {"normal", "uniform", "triangular", "empirical", "discrete", "custom"} == {
        d.value for d in Distribution
    }
