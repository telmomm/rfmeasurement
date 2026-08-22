from _synthetic import one_port, one_port_near_noise_floor

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.validation.rules.dynamic_range import DynamicRangeIndicatorRule


def test_passes_when_well_above_noise_floor():
    result = DynamicRangeIndicatorRule(noise_floor_db=-100.0, margin_db=6.0).evaluate(
        Measurement(data=one_port(magnitude=0.5))
    )
    assert result.status is ValidationStatus.PASS


def test_warns_when_close_to_noise_floor():
    result = DynamicRangeIndicatorRule(noise_floor_db=-100.0, margin_db=6.0).evaluate(
        Measurement(data=one_port_near_noise_floor())
    )
    assert result.status is ValidationStatus.WARNING
    assert result.evidence["min_magnitude_db"] < -94.0
