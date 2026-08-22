"""Level 2 physical-consistency checks: passivity and reciprocity."""

from __future__ import annotations

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.validation import ValidationResult
from rfmeasurement.validation.base import ValidationRule


class PassivityRule(ValidationRule):
    """Check that the network does not exhibit gain (S^H S <= I) at any frequency.

    Non-passivity does not automatically mean the measurement is invalid: it
    is expected for active devices. Per the "important distinction" in
    docs/measurement-quality.md, treat a FAIL here as a failed *assumption*
    the caller opted into, not a universal integrity failure.
    """

    identifier = "physics.passivity"
    description = "Network does not exhibit gain (S^H S <= I) at any frequency."

    def __init__(self, tol: float = 1e-6) -> None:
        self.tol = tol

    def _evaluate(self, measurement: Measurement) -> ValidationResult:
        network = measurement.data
        is_passive = network.is_passive(tol=self.tol)
        status = ValidationStatus.PASS if is_passive else ValidationStatus.FAIL
        return ValidationResult(
            rule_id=self.identifier,
            status=status,
            description=self.description,
            evidence={"is_passive": is_passive, "tolerance": self.tol},
            explanation=(
                None
                if is_passive
                else "Network gain exceeds the passivity tolerance at one or more frequencies."
            ),
        )


class ReciprocityRule(ValidationRule):
    """Check that the network is reciprocal (S equals its transpose).

    Not applicable to one-port networks, where reciprocity is trivially true
    and therefore not a meaningful check. Non-reciprocity is expected for
    devices such as isolators and amplifiers, so a FAIL here reflects a
    failed assumption rather than a universal defect.
    """

    identifier = "physics.reciprocity"
    description = "Network is reciprocal (S equals its transpose)."

    def __init__(self, tol: float = 1e-6) -> None:
        self.tol = tol

    def is_applicable(self, measurement: Measurement) -> bool:
        return measurement.data.nports > 1

    def _evaluate(self, measurement: Measurement) -> ValidationResult:
        network = measurement.data
        is_reciprocal = network.is_reciprocal(tol=self.tol)
        status = ValidationStatus.PASS if is_reciprocal else ValidationStatus.FAIL
        return ValidationResult(
            rule_id=self.identifier,
            status=status,
            description=self.description,
            evidence={"is_reciprocal": is_reciprocal, "tolerance": self.tol},
            explanation=(
                None if is_reciprocal else "S-parameter matrix is not symmetric within tolerance."
            ),
        )
