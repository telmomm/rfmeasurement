from _synthetic import one_port, one_port_with_nonfinite

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.validation.rules.finite_values import FiniteValuesRule


def test_passes_when_all_values_finite():
    result = FiniteValuesRule().evaluate(Measurement(data=one_port()))
    assert result.status is ValidationStatus.PASS
    assert result.evidence["non_finite_count"] == 0


def test_fails_when_a_value_is_nan():
    result = FiniteValuesRule().evaluate(Measurement(data=one_port_with_nonfinite()))
    assert result.status is ValidationStatus.FAIL
    assert result.evidence["non_finite_count"] == 1
