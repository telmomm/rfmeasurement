"""Core domain model: stable scientific concepts, independent of instruments.

See docs/domain-model.md and docs/architecture.md.
"""

from rfmeasurement.domain.analysis import AnalysisResult
from rfmeasurement.domain.budget import UncertaintyBudget, UncertaintyContribution
from rfmeasurement.domain.context import MeasurementContext
from rfmeasurement.domain.enums import (
    Distribution,
    MetadataConfidence,
    UncertaintyType,
    ValidationStatus,
)
from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.provenance import ProvenanceRecord
from rfmeasurement.domain.uncertainty import UncertaintySource
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.domain.validation import ValidationReport, ValidationResult

__all__ = [
    "AnalysisResult",
    "Distribution",
    "Measurand",
    "Measurement",
    "MeasurementContext",
    "MetadataConfidence",
    "ProvenanceRecord",
    "UncertaintyBudget",
    "UncertaintyContribution",
    "UncertaintyModel",
    "UncertaintySource",
    "UncertaintyType",
    "ValidationReport",
    "ValidationResult",
    "ValidationStatus",
]
