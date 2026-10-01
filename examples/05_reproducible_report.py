"""Can an external user reproduce this result from a clean environment?

Completes the story from examples 01/02/04: the same attenuator
insertion-loss measurement is validated, propagated both ways, and now
assembled into the machine-readable metadata package and human-readable
report that docs/reproducibility.md calls for -- software/Python versions,
analysis configuration (validation rules, uncertainty model, propagation
method and RNG state), input identifiers, validation summary, uncertainty
summary, and an explicit reproducibility level (0-4) rather than a claim
that every result is equally reproducible.

Run with:
    python examples/05_reproducible_report.py
"""

from __future__ import annotations

import json
import math

import numpy as np
import skrf as rf

from rfmeasurement import __version__
from rfmeasurement.domain import (
    AnalysisResult,
    Distribution,
    Measurand,
    Measurement,
    MeasurementContext,
    ProvenanceRecord,
    UncertaintySource,
    UncertaintyType,
    ValidationStatus,
)
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.reporting import build_metadata, generate_report
from rfmeasurement.uncertainty import expand, propagate_linear, propagate_monte_carlo
from rfmeasurement.validation import validate

SEED = 42
NOMINAL_MAGNITUDE = 0.316  # |S21| of the ~10 dB attenuator from example 01
COVERAGE_PROBABILITY = 0.95


def _build_measurement() -> Measurement:
    frequency = rf.Frequency(1, 3, 101, unit="GHz")
    s = np.zeros((frequency.npoints, 2, 2), dtype=complex)
    s[:, 0, 0] = 0.05
    s[:, 1, 1] = 0.05
    s[:, 0, 1] = NOMINAL_MAGNITUDE
    s[:, 1, 0] = NOMINAL_MAGNITUDE
    network = rf.Network(frequency=frequency, s=s, name="attenuator-0042")

    context = MeasurementContext(
        dut="10 dB fixed attenuator, s/n 0042",
        instrument="Simulated VNA",
        calibration="SOLT",
        rf_power_dbm=-10.0,
    )
    provenance = [
        ProvenanceRecord(
            operation="import_touchstone",
            software_version=__version__,
            inputs=("vna-sweep-2026-01-01.s2p",),
        ),
        ProvenanceRecord(
            operation="apply_calibration",
            software_version=__version__,
            parameters={"method": "SOLT"},
        ),
    ]
    return Measurement(data=network, context=context, provenance=provenance)


def _insertion_loss_db(values: dict) -> float:
    measured = NOMINAL_MAGNITUDE + values["vna_noise"] + values["calibration"]
    return -20 * math.log10(measured)


def _build_model() -> UncertaintyModel:
    vna_noise = UncertaintySource(
        name="vna_noise",
        description="Receiver noise / trace repeatability",
        uncertainty_type=UncertaintyType.TYPE_A,
        distribution=Distribution.NORMAL,
        standard_uncertainty=0.002,
        unit="linear magnitude",
        nominal_value=0.0,
    )
    calibration = UncertaintySource(
        name="calibration",
        description="Residual calibration-standard uncertainty",
        uncertainty_type=UncertaintyType.TYPE_B,
        distribution=Distribution.UNIFORM,
        standard_uncertainty=0.02 / math.sqrt(3),
        unit="linear magnitude",
        nominal_value=0.0,
        source_reference="Calibration kit datasheet",
    )
    measurand = Measurand(
        name="IL", definition="Insertion loss, -20*log10(|S21|)", unit="dB", frequency_hz=2e9
    )
    return UncertaintyModel(
        measurand=measurand,
        function=_insertion_loss_db,
        sources=(vna_noise, calibration),
        assumptions=(
            "vna_noise and calibration are independent and additive perturbations to the "
            "linear-magnitude reading around its nominal value."
        ),
    )


def main() -> None:
    measurement = _build_measurement()
    measurement.validation = validate(measurement)

    model = _build_model()
    linear = propagate_linear(model)
    monte_carlo = propagate_monte_carlo(model, n_samples=100_000, rng=np.random.default_rng(SEED))
    expanded, coverage_interval = expand(
        linear.value, linear.standard_uncertainty, COVERAGE_PROBABILITY
    )

    if measurement.validation.has_failures:
        validation_status = ValidationStatus.FAIL
    elif measurement.validation.has_warnings:
        validation_status = ValidationStatus.WARNING
    else:
        validation_status = ValidationStatus.PASS

    result = AnalysisResult(
        measurand=model.measurand,
        value=linear.value,
        unit=model.measurand.unit,
        validation_status=validation_status,
        standard_uncertainty=linear.standard_uncertainty,
        expanded_uncertainty=expanded,
        coverage_probability=COVERAGE_PROBABILITY,
        coverage_interval=coverage_interval,
        contributing_sources=model.sources,
    )

    report = generate_report(
        measurement, result, model=model, linear=linear, monte_carlo=monte_carlo
    )
    print(report)

    metadata = build_metadata(
        measurement, result, model=model, linear=linear, monte_carlo=monte_carlo
    )
    print("Machine-readable metadata (JSON, truncated to the configuration section)")
    print("-------------------------------------------------------------------------")
    print(json.dumps(metadata["configuration"], indent=2, default=str))


if __name__ == "__main__":
    main()
