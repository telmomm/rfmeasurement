from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.validation import ValidationReport, ValidationResult


def _result(status: ValidationStatus, rule_id: str) -> ValidationResult:
    return ValidationResult(rule_id=rule_id, status=status, description="test rule")


def test_empty_report_has_no_failures_or_warnings():
    report = ValidationReport()
    assert report.has_failures is False
    assert report.has_warnings is False


def test_report_detects_failures_and_warnings():
    report = ValidationReport(
        results=[
            _result(ValidationStatus.PASS, "integrity.finite_values"),
            _result(ValidationStatus.WARNING, "quality.dynamic_range"),
            _result(ValidationStatus.FAIL, "physics.passivity"),
        ]
    )
    assert report.has_failures is True
    assert report.has_warnings is True
    assert [r.rule_id for r in report.by_status(ValidationStatus.FAIL)] == ["physics.passivity"]


def test_result_is_never_a_bare_boolean():
    result = _result(ValidationStatus.NOT_APPLICABLE, "physics.reciprocity")
    assert result.status is ValidationStatus.NOT_APPLICABLE
    assert isinstance(result.evidence, dict)
