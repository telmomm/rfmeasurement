"""Level 3 measurement-quality indicator: suspicious discontinuities between adjacent points."""

from __future__ import annotations

import numpy as np

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.validation import ValidationResult
from rfmeasurement.validation.base import ValidationRule


class ContinuityRule(ValidationRule):
    """Flag abrupt jumps in S-parameter magnitude between adjacent frequency points.

    This is a heuristic indicator (docs/measurement-quality.md Level 3), not
    a physical-consistency requirement: a real discontinuity in a DUT's
    response (e.g. a filter edge) can legitimately produce a large jump. A
    WARNING here means "worth a second look", not "invalid measurement".
    """

    identifier = "quality.continuity"
    description = (
        "No S-parameter magnitude jump between adjacent frequency points exceeds the threshold."
    )

    def __init__(self, max_jump_db: float = 20.0) -> None:
        self.max_jump_db = max_jump_db

    def _evaluate(self, measurement: Measurement) -> ValidationResult:
        s = measurement.data.s
        if s.shape[0] < 2:
            return ValidationResult(
                rule_id=self.identifier,
                status=ValidationStatus.NOT_EVALUATED,
                description=self.description,
                explanation="Fewer than two frequency points; continuity is undefined.",
            )

        mag_db = 20 * np.log10(np.maximum(np.abs(s), 1e-20))
        jumps_db = np.abs(np.diff(mag_db, axis=0))
        max_jump = float(np.max(jumps_db))
        worst = np.unravel_index(np.argmax(jumps_db), jumps_db.shape)
        evidence = {
            "max_jump_db": max_jump,
            "threshold_db": self.max_jump_db,
            "worst_location": {
                "frequency_index": int(worst[0]),
                "output_port": int(worst[1]),
                "input_port": int(worst[2]),
            },
        }
        status = ValidationStatus.WARNING if max_jump > self.max_jump_db else ValidationStatus.PASS
        return ValidationResult(
            rule_id=self.identifier,
            status=status,
            description=self.description,
            evidence=evidence,
        )
