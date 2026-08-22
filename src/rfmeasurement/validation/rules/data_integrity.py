"""Level 1 data-integrity check: structural sanity of the measured data."""

from __future__ import annotations

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.validation import ValidationResult
from rfmeasurement.validation.base import ValidationRule


class StructuralIntegrityRule(ValidationRule):
    """Check that the S-parameter array shape matches the frequency grid and is square.

    Covers "valid dimensions" and "consistent port count" from
    docs/measurement-quality.md Level 1.
    """

    identifier = "integrity.structural"
    description = "S-parameter array shape is consistent with the frequency grid and port count."

    def _evaluate(self, measurement: Measurement) -> ValidationResult:
        network = measurement.data
        n_freq = network.frequency.npoints
        s_shape = network.s.shape
        evidence: dict[str, object] = {"s_shape": s_shape, "frequency_points": n_freq}

        if n_freq == 0:
            return ValidationResult(
                rule_id=self.identifier,
                status=ValidationStatus.FAIL,
                description=self.description,
                evidence=evidence,
                explanation="Measurement has no frequency points.",
            )
        if s_shape[0] != n_freq or s_shape[1] != s_shape[2]:
            return ValidationResult(
                rule_id=self.identifier,
                status=ValidationStatus.FAIL,
                description=self.description,
                evidence=evidence,
                explanation="S-parameter array is not (n_freq, n_ports, n_ports) shaped.",
            )
        return ValidationResult(
            rule_id=self.identifier,
            status=ValidationStatus.PASS,
            description=self.description,
            evidence=evidence,
        )
