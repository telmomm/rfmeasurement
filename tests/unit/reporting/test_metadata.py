import json

import numpy as np
from _fixtures import analysis_result, attenuator_measurement, uncertainty_model

from rfmeasurement.reporting.metadata import build_metadata
from rfmeasurement.uncertainty.monte_carlo import propagate_monte_carlo


def test_build_metadata_is_json_serializable():
    measurement = attenuator_measurement(with_provenance=True)
    model = uncertainty_model()
    result = analysis_result(model)
    monte_carlo = propagate_monte_carlo(model, n_samples=200, rng=np.random.default_rng(2))

    metadata = build_metadata(measurement, result, model=model, monte_carlo=monte_carlo)

    json.dumps(metadata)  # raises if anything is not JSON-serializable


def test_build_metadata_does_not_embed_raw_network_data():
    measurement = attenuator_measurement()
    model = uncertainty_model()
    result = analysis_result(model)

    metadata = build_metadata(measurement, result, model=model)

    assert metadata["input"]["name"] == "attenuator"
    assert metadata["input"]["number_of_ports"] == 2
    assert "s" not in metadata["input"]


def test_build_metadata_includes_provenance_only_when_present():
    with_provenance = attenuator_measurement(with_provenance=True)
    without_provenance = attenuator_measurement(with_provenance=False)
    model = uncertainty_model()
    result = analysis_result(model)

    assert build_metadata(with_provenance, result, model=model)["provenance"] is not None
    assert build_metadata(without_provenance, result, model=model)["provenance"] is None


def test_build_metadata_reports_a_level():
    measurement = attenuator_measurement(with_provenance=True)
    model = uncertainty_model()
    result = analysis_result(model)

    metadata = build_metadata(measurement, result, model=model)

    assert metadata["reproducibility_level"] == 4


def test_build_metadata_records_coverage_factor_and_degrees_of_freedom():
    measurement = attenuator_measurement()
    model = uncertainty_model()
    result = analysis_result(model)
    result.coverage_factor = 2.78
    result.effective_degrees_of_freedom = 4.0

    metadata = build_metadata(measurement, result, model=model)

    assert metadata["result"]["coverage_factor"] == 2.78
    assert metadata["result"]["effective_degrees_of_freedom"] == 4.0
