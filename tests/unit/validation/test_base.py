from _synthetic import one_port

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.validation import ValidationResult
from rfmeasurement.validation.base import ValidationRule


class _NeverApplicable(ValidationRule):
    identifier = "test.never_applicable"
    description = "Always inapplicable."

    def is_applicable(self, measurement: Measurement) -> bool:
        return False

    def _evaluate(self, measurement: Measurement) -> ValidationResult:  # pragma: no cover
        raise AssertionError("should not be called when not applicable")


def test_not_applicable_rule_skips_evaluate():
    result = _NeverApplicable().evaluate(Measurement(data=one_port()))
    assert result.status is ValidationStatus.NOT_APPLICABLE
    assert result.rule_id == "test.never_applicable"
