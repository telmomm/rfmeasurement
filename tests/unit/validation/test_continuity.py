from _synthetic import one_port, one_port_with_discontinuity

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.validation.rules.continuity import ContinuityRule


def test_passes_on_a_smooth_response():
    result = ContinuityRule().evaluate(Measurement(data=one_port()))
    assert result.status is ValidationStatus.PASS


def test_warns_on_a_large_jump():
    result = ContinuityRule(max_jump_db=20.0).evaluate(
        Measurement(data=one_port_with_discontinuity())
    )
    assert result.status is ValidationStatus.WARNING
    assert result.evidence["max_jump_db"] > 20.0
