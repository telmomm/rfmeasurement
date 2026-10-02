"""Final reported result for one measurand (docs/domain-model.md#analysis-result)."""

from __future__ import annotations

from dataclasses import dataclass, field

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.provenance import ProvenanceRecord
from rfmeasurement.domain.uncertainty import UncertaintySource


@dataclass(slots=True)
class AnalysisResult:
    """A reported value for a measurand, with its uncertainty, validation
    status and provenance.

    The uncertainty fields here are a snapshot (standard/expanded
    uncertainty and a coverage interval); the propagation machinery that
    produces them is introduced in a later phase (docs/uncertainty.md).
    ``coverage_factor`` and ``effective_degrees_of_freedom`` record how
    ``expanded_uncertainty`` was obtained from ``standard_uncertainty``, so
    a Gaussian k = 1.96 interval can be told apart from a Student-t one;
    ``effective_degrees_of_freedom`` of ``None`` means the Gaussian factor
    was used.
    """

    measurand: Measurand
    value: complex | float
    unit: str
    provenance: tuple[ProvenanceRecord, ...] = field(default_factory=tuple)
    validation_status: ValidationStatus = ValidationStatus.NOT_EVALUATED
    standard_uncertainty: float | None = None
    expanded_uncertainty: float | None = None
    coverage_probability: float | None = None
    coverage_interval: tuple[float, float] | None = None
    contributing_sources: tuple[UncertaintySource, ...] = field(default_factory=tuple)
    coverage_factor: float | None = None
    effective_degrees_of_freedom: float | None = None
