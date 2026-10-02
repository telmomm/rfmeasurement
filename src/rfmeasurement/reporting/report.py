"""Render a human-readable Markdown report from an analysis result's metadata.

docs/reproducibility.md: reports should contain "software version; Python
version; dependency versions where useful; analysis configuration; input
identifiers; validation summary; uncertainty summary." This renders exactly
that, from the same metadata package :func:`build_metadata` assembles for
machine consumption, so the two never drift apart.
"""

from __future__ import annotations

from typing import Any

from rfmeasurement.domain.analysis import AnalysisResult
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.reporting.levels import LEVEL_DESCRIPTIONS
from rfmeasurement.reporting.metadata import build_metadata
from rfmeasurement.uncertainty.linear import LinearPropagationResult
from rfmeasurement.uncertainty.monte_carlo import MonteCarloResult


def generate_report(
    measurement: Measurement,
    analysis_result: AnalysisResult,
    *,
    model: UncertaintyModel | None = None,
    linear: LinearPropagationResult | None = None,
    monte_carlo: MonteCarloResult | None = None,
) -> str:
    """Render a Markdown reproducibility report for ``analysis_result``.

    See :func:`rfmeasurement.reporting.metadata.build_metadata` for what
    ``model``/``linear``/``monte_carlo`` are for; the same metadata package
    backs both this report and :func:`build_metadata`'s JSON output.
    """
    metadata = build_metadata(
        measurement, analysis_result, model=model, linear=linear, monte_carlo=monte_carlo
    )
    lines: list[str] = []

    measurand_name = metadata["result"]["measurand"]["name"]
    lines.append(f"# Analysis report: {measurand_name}")
    lines.append("")
    lines.append(_result_section(metadata))
    lines.append(_input_section(metadata))
    lines.append(_validation_section(metadata))
    lines.append(_configuration_section(metadata))
    lines.append(_environment_section(metadata))
    lines.append(_reproducibility_section(metadata))
    return "\n".join(lines).rstrip() + "\n"


def _format_value(value: dict[str, float] | float) -> str:
    if isinstance(value, dict):
        return f"{value['real']:g}{value['imag']:+g}j"
    return f"{value:g}"


def _result_section(metadata: dict[str, Any]) -> str:
    result = metadata["result"]
    lines = ["## Result", ""]
    lines.append(f"- value: {_format_value(result['value'])} {result['unit']}")
    if result["standard_uncertainty"] is not None:
        lines.append(f"- standard uncertainty: {result['standard_uncertainty']:g} {result['unit']}")
    if result["expanded_uncertainty"] is not None:
        coverage_details = []
        if result["coverage_probability"] is not None:
            coverage_details.append(f"{result['coverage_probability']:.0%} coverage")
        if result["coverage_factor"] is not None:
            coverage_details.append(f"k = {result['coverage_factor']:.3g}")
        if result["effective_degrees_of_freedom"] is not None:
            coverage_details.append(
                f"effective degrees of freedom = {result['effective_degrees_of_freedom']:.1f}"
            )
        coverage_text = f" ({', '.join(coverage_details)})" if coverage_details else ""
        lines.append(
            f"- expanded uncertainty: {result['expanded_uncertainty']:g} "
            f"{result['unit']}{coverage_text}"
        )
    if result["coverage_interval"] is not None:
        lo, hi = result["coverage_interval"]
        lines.append(f"- coverage interval: [{lo:g}, {hi:g}] {result['unit']}")
    lines.append(f"- validation status at analysis time: {result['validation_status']}")
    lines.append("")
    return "\n".join(lines)


def _input_section(metadata: dict[str, Any]) -> str:
    input_info = metadata["input"]
    lo, hi = input_info["frequency_range_hz"]
    lines = [
        "## Input",
        "",
        f"- network: {input_info['name'] or '(unnamed)'}",
        f"- ports: {input_info['number_of_ports']}",
        f"- frequency range: {lo:g}-{hi:g} Hz",
        "",
    ]
    return "\n".join(lines)


def _validation_section(metadata: dict[str, Any]) -> str:
    validation = metadata["validation"]
    lines = ["## Validation summary", ""]
    if not validation["results"]:
        lines.append("No validation rules were evaluated.")
    else:
        overall = "FAIL" if validation["has_failures"] else "OK"
        lines.append(f"Overall: {overall} (warnings={validation['has_warnings']})")
        lines.append("")
        for result in validation["results"]:
            lines.append(
                f"- [{result['status'].upper()}] {result['rule_id']}: {result['description']}"
            )
    lines.append("")
    return "\n".join(lines)


def _configuration_section(metadata: dict[str, Any]) -> str:
    configuration = metadata["configuration"]
    lines = ["## Analysis configuration", ""]
    if configuration["validation_rules"]:
        rule_ids = ", ".join(rule["rule_id"] for rule in configuration["validation_rules"])
        lines.append(f"- validation rules evaluated: {rule_ids}")
    if configuration["propagation"]:
        lines.append(f"- uncertainty propagation: {configuration['propagation']['method']}")
    if configuration["uncertainty_assumptions"]:
        lines.append(f"- uncertainty model assumptions: {configuration['uncertainty_assumptions']}")
    if configuration["uncertainty_source_names"]:
        sources = ", ".join(configuration["uncertainty_source_names"])
        lines.append(f"- uncertainty sources: {sources}")
    if len(lines) == 2:
        lines.append("No analysis configuration was recorded.")
    lines.append("")
    return "\n".join(lines)


def _environment_section(metadata: dict[str, Any]) -> str:
    environment = metadata["environment"]
    lines = [
        "## Software environment",
        "",
        f"- rfmeasurement: {environment['rfmeasurement_version']}",
        f"- Python: {environment['python_version']}",
    ]
    for name, dependency_version in environment["dependency_versions"].items():
        lines.append(f"- {name}: {dependency_version}")
    lines.append("")
    return "\n".join(lines)


def _reproducibility_section(metadata: dict[str, Any]) -> str:
    level = metadata["reproducibility_level"]
    description = LEVEL_DESCRIPTIONS[level]
    lines = [
        "## Reproducibility level",
        "",
        f"**Level {level}**: {description}",
        "",
        "See docs/reproducibility.md for the full level definitions.",
    ]
    return "\n".join(lines)
