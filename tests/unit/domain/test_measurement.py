import numpy as np
import skrf as rf

from rfmeasurement.domain.measurement import Measurement


def _one_port_network() -> rf.Network:
    frequency = rf.Frequency(1, 2, 2, unit="GHz")
    s = np.zeros((2, 1, 1), dtype=complex)
    return rf.Network(frequency=frequency, s=s)


def test_measurement_wraps_a_network_with_empty_defaults():
    measurement = Measurement(data=_one_port_network())
    assert measurement.provenance == []
    assert measurement.analysis_history == []
    assert measurement.validation.results == []
    assert measurement.context.instrument is None


def test_measurement_data_is_the_underlying_network():
    network = _one_port_network()
    measurement = Measurement(data=network)
    assert measurement.data is network
    assert measurement.data.number_of_ports == 1
