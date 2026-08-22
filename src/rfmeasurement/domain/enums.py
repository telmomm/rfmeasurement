"""Shared enumerations for the rfmeasurement domain model."""

from enum import Enum


class MetadataConfidence(str, Enum):
    """How a piece of context metadata was obtained (docs/domain-model.md)."""

    MEASURED = "measured"
    SPECIFIED = "specified"
    ESTIMATED = "estimated"
    ASSUMED = "assumed"
    UNKNOWN = "unknown"


class ValidationStatus(str, Enum):
    """Outcome of a single validation rule (docs/measurement-quality.md)."""

    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    NOT_EVALUATED = "not_evaluated"


class UncertaintyType(str, Enum):
    """GUM Type A / Type B classification of an uncertainty source (docs/uncertainty.md)."""

    TYPE_A = "type_a"
    TYPE_B = "type_b"


class Distribution(str, Enum):
    """Probability distribution assumed for an uncertainty source (docs/uncertainty.md)."""

    NORMAL = "normal"
    UNIFORM = "uniform"
    TRIANGULAR = "triangular"
    EMPIRICAL = "empirical"
    DISCRETE = "discrete"
    CUSTOM = "custom"
