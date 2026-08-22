"""Base interface for a composable measurement-quality check."""

from __future__ import annotations

from abc import ABC, abstractmethod

from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.validation import ValidationResult


class ValidationRule(ABC):
    """A single, composable measurement-quality check.

    Conceptually: identifier, description, applicability, evaluate(measurement)
    -> result, per docs/architecture.md. A rule that does not apply to a given
    measurement (e.g. reciprocity on a one-port network) must say so
    explicitly via :meth:`is_applicable` rather than silently passing.
    """

    identifier: str
    description: str

    def is_applicable(self, measurement: Measurement) -> bool:
        return True

    @abstractmethod
    def _evaluate(self, measurement: Measurement) -> ValidationResult:
        """Run the check. Only called when :meth:`is_applicable` is True."""

    def evaluate(self, measurement: Measurement) -> ValidationResult:
        if not self.is_applicable(measurement):
            return ValidationResult(
                rule_id=self.identifier,
                status=ValidationStatus.NOT_APPLICABLE,
                description=self.description,
                explanation="Rule is not applicable to this measurement.",
            )
        return self._evaluate(measurement)
