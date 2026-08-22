"""Level 1 data-integrity check: no missing or non-finite values."""

from __future__ import annotations

import numpy as np

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.validation import ValidationResult
from rfmeasurement.validation.base import ValidationRule


class FiniteValuesRule(ValidationRule):
    """Check that every S-parameter sample is finite (no NaN or Inf)."""

    identifier = "integrity.finite_values"
    description = "All S-parameter samples are finite."

    def _evaluate(self, measurement: Measurement) -> ValidationResult:
        s = measurement.data.s
        finite_mask = np.isfinite(s)
        n_bad = int((~finite_mask).sum())
        if n_bad:
            bad_indices = np.argwhere(~finite_mask)
            evidence = {
                "non_finite_count": n_bad,
                "first_bad_index": bad_indices[0].tolist(),
            }
            return ValidationResult(
                rule_id=self.identifier,
                status=ValidationStatus.FAIL,
                description=self.description,
                evidence=evidence,
                explanation=f"{n_bad} non-finite S-parameter sample(s) found.",
            )
        return ValidationResult(
            rule_id=self.identifier,
            status=ValidationStatus.PASS,
            description=self.description,
            evidence={"non_finite_count": 0},
        )
