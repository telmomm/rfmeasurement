from _synthetic import active_two_port, matched_two_port, nonreciprocal_two_port, one_port

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.validation.rules.physical_consistency import PassivityRule, ReciprocityRule


def test_passivity_passes_for_matched_network():
    result = PassivityRule().evaluate(Measurement(data=matched_two_port()))
    assert result.status is ValidationStatus.PASS


def test_passivity_fails_for_active_network():
    result = PassivityRule().evaluate(Measurement(data=active_two_port()))
    assert result.status is ValidationStatus.FAIL


def test_reciprocity_passes_for_symmetric_network():
    result = ReciprocityRule().evaluate(Measurement(data=matched_two_port()))
    assert result.status is ValidationStatus.PASS


def test_reciprocity_fails_for_isolator_like_network():
    result = ReciprocityRule().evaluate(Measurement(data=nonreciprocal_two_port()))
    assert result.status is ValidationStatus.FAIL


def test_reciprocity_not_applicable_to_one_port():
    result = ReciprocityRule().evaluate(Measurement(data=one_port()))
    assert result.status is ValidationStatus.NOT_APPLICABLE
