from _fixtures import analysis_result, attenuator_measurement, uncertainty_model

from rfmeasurement.reporting.configuration import build_configuration
from rfmeasurement.reporting.environment import capture_environment
from rfmeasurement.reporting.levels import reproducibility_level


def test_bare_measurement_is_level_1():
    measurement = attenuator_measurement()
    model = uncertainty_model()
    result = analysis_result(model)
    assert reproducibility_level(measurement, result) == 1


def test_adding_configuration_reaches_level_2():
    measurement = attenuator_measurement()
    model = uncertainty_model()
    result = analysis_result(model)
    configuration = build_configuration(measurement, model=model)
    assert reproducibility_level(measurement, result, configuration=configuration) == 2


def test_adding_environment_reaches_level_3():
    measurement = attenuator_measurement()  # instrument/calibration set, but no provenance
    model = uncertainty_model()
    result = analysis_result(model)
    configuration = build_configuration(measurement, model=model)
    environment = capture_environment()
    level = reproducibility_level(
        measurement, result, configuration=configuration, environment=environment
    )
    assert level == 3


def test_full_provenance_and_context_reaches_level_4():
    measurement = attenuator_measurement(with_provenance=True)
    model = uncertainty_model()
    result = analysis_result(model)
    configuration = build_configuration(measurement, model=model)
    environment = capture_environment()
    level = reproducibility_level(
        measurement, result, configuration=configuration, environment=environment
    )
    assert level == 4


def test_missing_instrument_caps_level_at_3_even_with_provenance():
    measurement = attenuator_measurement(with_provenance=True)
    measurement.context.instrument = None
    model = uncertainty_model()
    result = analysis_result(model)
    configuration = build_configuration(measurement, model=model)
    environment = capture_environment()
    level = reproducibility_level(
        measurement, result, configuration=configuration, environment=environment
    )
    assert level == 3
