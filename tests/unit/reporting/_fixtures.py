"""Shared fixtures for reporting-module tests: a small but complete analysis."""

from __future__ import annotations

import numpy as np
import skrf as rf

from rfmeasurement.domain import (
    AnalysisResult,
    Distribution,
    Measurand,
    Measurement,
    MeasurementContext,
    ProvenanceRecord,
    UncertaintySource,
    UncertaintyType,
)
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.monte_carlo import propagate_monte_carlo
from rfmeasurement.validation import validate


def attenuator_measurement(*, with_provenance: bool = False) -> Measurement:
    frequency = rf.Frequency(1, 3, 101, unit="GHz")
    n = frequency.npoints
    s = np.zeros((n, 2, 2), dtype=complex)
    s[:, 0, 0] = 0.05
    s[:, 1, 1] = 0.05
    s[:, 0, 1] = 0.316
    s[:, 1, 0] = 0.316
    network = rf.Network(frequency=frequency, s=s, name="attenuator")
    context = MeasurementContext(
        dut="10 dB fixed attenuator",
        instrument="Simulated VNA",
        calibration="SOLT",
    )
    provenance = (
        [ProvenanceRecord(operation="import_touchstone", software_version="0.1.0.dev0")]
        if with_provenance
        else []
    )
    measurement = Measurement(data=network, context=context, provenance=provenance)
    measurement.validation = validate(measurement)
    return measurement


def uncertainty_model() -> UncertaintyModel:
    source = UncertaintySource(
        name="vna_noise",
        description="Receiver noise",
        uncertainty_type=UncertaintyType.TYPE_A,
        distribution=Distribution.NORMAL,
        standard_uncertainty=0.002,
        unit="linear magnitude",
        nominal_value=0.316,
    )
    measurand = Measurand(name="IL", definition="Insertion loss", unit="dB", frequency_hz=2e9)
    return UncertaintyModel(
        measurand=measurand,
        function=lambda values: -20 * np.log10(values["vna_noise"]),
        sources=(source,),
        assumptions="vna_noise is the only significant contributor.",
    )


def analysis_result(model: UncertaintyModel) -> AnalysisResult:
    monte_carlo = propagate_monte_carlo(model, n_samples=2000, rng=np.random.default_rng(1))
    return AnalysisResult(
        measurand=model.measurand,
        value=monte_carlo.value,
        unit=model.measurand.unit,
        standard_uncertainty=monte_carlo.standard_uncertainty,
        expanded_uncertainty=2 * monte_carlo.standard_uncertainty,
        coverage_probability=0.95,
        coverage_interval=(
            monte_carlo.value - 2 * monte_carlo.standard_uncertainty,
            monte_carlo.value + 2 * monte_carlo.standard_uncertainty,
        ),
        contributing_sources=model.sources,
    )
