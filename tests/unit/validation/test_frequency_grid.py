from _synthetic import one_port, one_port_with_disordered_frequency

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.validation.rules.frequency_grid import FrequencyGridRule


def test_passes_on_a_strictly_increasing_grid():
    result = FrequencyGridRule().evaluate(Measurement(data=one_port()))
    assert result.status is ValidationStatus.PASS
    assert result.evidence["n_duplicates"] == 0
    assert result.evidence["n_out_of_order"] == 0


def test_fails_on_out_of_order_and_duplicate_points():
    result = FrequencyGridRule().evaluate(
        Measurement(data=one_port_with_disordered_frequency())
    )
    assert result.status is ValidationStatus.FAIL
    assert result.evidence["n_duplicates"] >= 1
    assert result.evidence["n_out_of_order"] >= 1
