"""The central domain object: an RF measurement plus everything around it."""

from __future__ import annotations

from dataclasses import dataclass, field

import skrf as rf

from rfmeasurement.domain.analysis import AnalysisResult
from rfmeasurement.domain.context import MeasurementContext
from rfmeasurement.domain.provenance import ProvenanceRecord
from rfmeasurement.domain.validation import ValidationReport


@dataclass(slots=True)
class Measurement:
    """An RF measurement: data plus its context, provenance, validation and
    analysis history (docs/domain-model.md#measurement).

    ``data`` is not necessarily raw: it may already be calibrated,
    de-embedded or otherwise derived, as long as that processing is recorded
    in ``provenance``.
    """

    data: rf.Network
    context: MeasurementContext = field(default_factory=MeasurementContext)
    provenance: list[ProvenanceRecord] = field(default_factory=list)
    validation: ValidationReport = field(default_factory=ValidationReport)
    analysis_history: list[AnalysisResult] = field(default_factory=list)
