"""Level 3 measurement-quality indicator: proximity to a configured noise-floor margin."""

from __future__ import annotations

import numpy as np

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.validation import ValidationResult
from rfmeasurement.validation.base import ValidationRule


class DynamicRangeIndicatorRule(ValidationRule):
    """Flag S-parameter samples close to a configurable noise-floor threshold.

    This is an indicator, not a measured noise floor: it reports how close
    the smallest observed |S| magnitude is to ``noise_floor_db``, which the
    caller must set based on their instrument's actual noise floor. Per the
    "quality score" caution in docs/measurement-quality.md, this rule exposes
    the underlying minimum; it does not claim to know the true instrument
    noise floor.
    """

    identifier = "quality.dynamic_range"
    description = (
        "Smallest observed S-parameter magnitude is above the configured noise-floor margin."
    )

    def __init__(self, noise_floor_db: float = -100.0, margin_db: float = 6.0) -> None:
        self.noise_floor_db = noise_floor_db
        self.margin_db = margin_db

    def _evaluate(self, measurement: Measurement) -> ValidationResult:
        s = measurement.data.s
        mag_db = 20 * np.log10(np.maximum(np.abs(s), 1e-20))
        min_db = float(np.min(mag_db))
        threshold = self.noise_floor_db + self.margin_db
        evidence: dict[str, object] = {
            "min_magnitude_db": min_db,
            "noise_floor_db": self.noise_floor_db,
            "margin_db": self.margin_db,
        }
        status = ValidationStatus.WARNING if min_db < threshold else ValidationStatus.PASS
        return ValidationResult(
            rule_id=self.identifier,
            status=status,
            description=self.description,
            evidence=evidence,
            explanation=(
                None
                if status is ValidationStatus.PASS
                else "Smallest observed magnitude is within the noise-floor margin."
            ),
        )
