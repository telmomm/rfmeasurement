"""Assemble a JSON-serializable metadata package for one analysis result.

docs/reproducibility.md: "The project should provide a machine-readable
representation of analysis metadata... Binary scientific data should not be
forced into JSON": the underlying network (``measurement.data``) is
referenced by name/frequency range here, not embedded -- it stays in its
own established format (Touchstone, scikit-rf's own serialization, etc.).
"""

from __future__ import annotations

from typing import Any

from rfmeasurement.domain.analysis import AnalysisResult
from rfmeasurement.domain.context import MeasurementContext
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.domain.validation import ValidationReport
from rfmeasurement.provenance import ProvenanceGraph
from rfmeasurement.reporting.configuration import build_configuration
from rfmeasurement.reporting.environment import SoftwareEnvironment, capture_environment
from rfmeasurement.reporting.levels import reproducibility_level
from rfmeasurement.uncertainty.linear import LinearPropagationResult
from rfmeasurement.uncertainty.monte_carlo import MonteCarloResult


def build_metadata(
    measurement: Measurement,
    analysis_result: AnalysisResult,
    *,
    model: UncertaintyModel | None = None,
    linear: LinearPropagationResult | None = None,
    monte_carlo: MonteCarloResult | None = None,
    environment: SoftwareEnvironment | None = None,
) -> dict[str, Any]:
    """Build the full machine-readable metadata package for ``analysis_result``.

    ``model``, ``linear`` and ``monte_carlo`` are optional and only needed to
    record how uncertainty was propagated (see
    :func:`rfmeasurement.reporting.configuration.build_configuration`).
    ``environment`` defaults to the currently running environment; pass an
    explicit one to describe how a *previous* result was produced instead.
    """
    environment = environment if environment is not None else capture_environment()
    configuration = build_configuration(
        measurement,
        model=model,
        linear=linear,
        monte_carlo=monte_carlo,
        coverage_probability=analysis_result.coverage_probability,
    )
    provenance = (
        ProvenanceGraph.from_measurement(measurement).to_dict() if measurement.provenance else None
    )
    level = reproducibility_level(
        measurement, analysis_result, configuration=configuration, environment=environment
    )

    network = measurement.data
    return {
        "environment": environment.to_dict(),
        "input": {
            "name": network.name,
            "number_of_ports": network.number_of_ports,
            "frequency_range_hz": list(
                measurement.context.frequency_range_hz
                or (network.frequency.start, network.frequency.stop)
            ),
        },
        "context": _context_to_dict(measurement.context),
        "validation": _validation_summary(measurement.validation),
        "provenance": provenance,
        "configuration": configuration.to_dict(),
        "result": _result_to_dict(analysis_result),
        "reproducibility_level": level,
    }


def _context_to_dict(context: MeasurementContext) -> dict[str, Any]:
    return {
        "dut": context.dut,
        "operator": context.operator,
        "instrument": context.instrument,
        "calibration": context.calibration,
        "cables": context.cables,
        "fixture": context.fixture,
        "temperature_c": context.temperature_c,
        "humidity_percent": context.humidity_percent,
        "pressure_pa": context.pressure_pa,
        "rf_power_dbm": context.rf_power_dbm,
        "if_bandwidth_hz": context.if_bandwidth_hz,
        "averaging": context.averaging,
        "sweep_settings": context.sweep_settings,
        "frequency_range_hz": (
            list(context.frequency_range_hz) if context.frequency_range_hz else None
        ),
        "timestamp": context.timestamp.isoformat() if context.timestamp else None,
        "confidence": {field: value.value for field, value in context.confidence.items()},
    }


def _validation_summary(report: ValidationReport) -> dict[str, Any]:
    return {
        "has_failures": report.has_failures,
        "has_warnings": report.has_warnings,
        "results": [
            {
                "rule_id": result.rule_id,
                "status": result.status.value,
                "description": result.description,
                "rule_version": result.rule_version,
            }
            for result in report.results
        ],
    }


def _complex_to_dict(value: complex | float) -> dict[str, float] | float:
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    return value


def _result_to_dict(result: AnalysisResult) -> dict[str, Any]:
    return {
        "measurand": {
            "name": result.measurand.name,
            "definition": result.measurand.definition,
            "unit": result.measurand.unit,
            "frequency_hz": result.measurand.frequency_hz,
        },
        "value": _complex_to_dict(result.value),
        "unit": result.unit,
        "validation_status": result.validation_status.value,
        "standard_uncertainty": result.standard_uncertainty,
        "expanded_uncertainty": result.expanded_uncertainty,
        "coverage_probability": result.coverage_probability,
        "coverage_interval": list(result.coverage_interval) if result.coverage_interval else None,
        "contributing_sources": [source.name for source in result.contributing_sources],
    }
