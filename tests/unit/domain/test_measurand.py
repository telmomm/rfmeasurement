from dataclasses import FrozenInstanceError

import pytest

from rfmeasurement.domain.measurand import Measurand


def test_measurand_carries_definition_and_unit():
    m = Measurand(name="S11", definition="Input reflection coefficient", unit="dB")
    assert m.unit == "dB"
    assert m.frequency_hz is None


def test_measurand_is_immutable():
    m = Measurand(name="S11", definition="Input reflection coefficient", unit="dB")
    with pytest.raises(FrozenInstanceError):
        m.unit = "linear"
