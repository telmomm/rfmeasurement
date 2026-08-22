from _synthetic import matched_two_port

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.validation.rules.data_integrity import StructuralIntegrityRule


def test_passes_on_a_well_formed_network():
    result = StructuralIntegrityRule().evaluate(Measurement(data=matched_two_port()))
    assert result.status is ValidationStatus.PASS


def test_fails_when_s_array_no_longer_matches_frequency_grid():
    network = matched_two_port(n_points=3)
    network.s = network.s[:2]  # desynchronize s from the 3-point frequency grid
    result = StructuralIntegrityRule().evaluate(Measurement(data=network))
    assert result.status is ValidationStatus.FAIL
    assert result.evidence["frequency_points"] == 3
