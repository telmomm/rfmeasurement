import numpy as np
from _fixtures import attenuator_measurement, uncertainty_model

from rfmeasurement.reporting.configuration import build_configuration
from rfmeasurement.uncertainty.linear import propagate_linear
from rfmeasurement.uncertainty.monte_carlo import propagate_monte_carlo


def test_configuration_without_uncertainty_model_only_captures_validation():
    measurement = attenuator_measurement()
    configuration = build_configuration(measurement)
    assert configuration.validation_rules
    assert configuration.uncertainty_assumptions is None
    assert configuration.propagation == {}


def test_configuration_with_monte_carlo_records_method_and_rng_state():
    measurement = attenuator_measurement()
    model = uncertainty_model()
    monte_carlo = propagate_monte_carlo(model, n_samples=500, rng=np.random.default_rng(3))

    configuration = build_configuration(
        measurement, model=model, monte_carlo=monte_carlo, coverage_probability=0.95
    )

    assert configuration.propagation["method"] == "monte_carlo"
    assert configuration.propagation["n_samples"] == 500
    assert configuration.propagation["rng_state"] == monte_carlo.rng_state
    assert configuration.uncertainty_assumptions == model.assumptions
    assert configuration.uncertainty_source_names == ("vna_noise",)
    assert configuration.coverage_probability == 0.95


def test_configuration_with_model_only_does_not_guess_a_propagation_method():
    """Passing just a model is not evidence of which algorithm ran (if any)."""
    measurement = attenuator_measurement()
    model = uncertainty_model()
    configuration = build_configuration(measurement, model=model)
    assert configuration.propagation == {}
    assert configuration.uncertainty_assumptions == model.assumptions


def test_configuration_with_linear_result_records_method_and_sensitivities():
    measurement = attenuator_measurement()
    model = uncertainty_model()
    linear = propagate_linear(model)

    configuration = build_configuration(measurement, model=model, linear=linear)

    assert configuration.propagation["method"] == "linear"
    assert configuration.propagation["sensitivity_coefficients"] == linear.sensitivity_coefficients


def test_monte_carlo_takes_precedence_over_linear_when_both_given():
    measurement = attenuator_measurement()
    model = uncertainty_model()
    linear = propagate_linear(model)
    monte_carlo = propagate_monte_carlo(model, n_samples=500, rng=np.random.default_rng(3))

    configuration = build_configuration(
        measurement, model=model, linear=linear, monte_carlo=monte_carlo
    )

    assert configuration.propagation["method"] == "monte_carlo"


def test_to_dict_is_json_serializable():
    import json

    measurement = attenuator_measurement()
    model = uncertainty_model()
    configuration = build_configuration(measurement, model=model)
    json.dumps(configuration.to_dict())
