"""Reproducible, machine- and human-readable reporting (docs/reproducibility.md)."""

from rfmeasurement.reporting.configuration import AnalysisConfiguration, build_configuration
from rfmeasurement.reporting.environment import SoftwareEnvironment, capture_environment
from rfmeasurement.reporting.levels import LEVEL_DESCRIPTIONS, reproducibility_level
from rfmeasurement.reporting.metadata import build_metadata
from rfmeasurement.reporting.report import generate_report

__all__ = [
    "LEVEL_DESCRIPTIONS",
    "AnalysisConfiguration",
    "SoftwareEnvironment",
    "build_configuration",
    "build_metadata",
    "capture_environment",
    "generate_report",
    "reproducibility_level",
]
