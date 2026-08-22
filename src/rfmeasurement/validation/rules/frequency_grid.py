"""Level 1 data-integrity check: frequency-grid consistency."""

from __future__ import annotations

import numpy as np

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.validation import ValidationResult
from rfmeasurement.validation.base import ValidationRule


class FrequencyGridRule(ValidationRule):
    """Check that the frequency grid is strictly increasing, with no duplicate points.

    Covers both "frequency ordering" and "duplicate frequency points" from
    docs/measurement-quality.md Level 1, since a duplicate point is simply a
    violation of strict monotonicity.
    """

    identifier = "integrity.frequency_grid"
    description = "Frequency points are strictly increasing with no duplicates."

    def _evaluate(self, measurement: Measurement) -> ValidationResult:
        freq_hz = measurement.data.frequency.f
        if freq_hz.size < 2:
            return ValidationResult(
                rule_id=self.identifier,
                status=ValidationStatus.PASS,
                description=self.description,
                evidence={"n_points": int(freq_hz.size)},
            )

        diffs = np.diff(freq_hz)
        n_duplicates = int(np.sum(diffs == 0))
        n_out_of_order = int(np.sum(diffs < 0))
        evidence: dict[str, object] = {
            "n_points": int(freq_hz.size),
            "n_duplicates": n_duplicates,
            "n_out_of_order": n_out_of_order,
        }
        if n_duplicates or n_out_of_order:
            return ValidationResult(
                rule_id=self.identifier,
                status=ValidationStatus.FAIL,
                description=self.description,
                evidence=evidence,
                explanation="Frequency grid is not strictly increasing.",
            )
        return ValidationResult(
            rule_id=self.identifier,
            status=ValidationStatus.PASS,
            description=self.description,
            evidence=evidence,
        )
