"""Compose validation rules into a structured QA report for a measurement."""

from __future__ import annotations

from collections.abc import Sequence

from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.validation import ValidationReport
from rfmeasurement.validation.base import ValidationRule
from rfmeasurement.validation.rules import (
    ContinuityRule,
    DynamicRangeIndicatorRule,
    FiniteValuesRule,
    FrequencyGridRule,
    PassivityRule,
    ReciprocityRule,
    StructuralIntegrityRule,
)

DEFAULT_RULES: tuple[ValidationRule, ...] = (
    StructuralIntegrityRule(),
    FiniteValuesRule(),
    FrequencyGridRule(),
    PassivityRule(),
    ReciprocityRule(),
    ContinuityRule(),
    DynamicRangeIndicatorRule(),
)


def validate(
    measurement: Measurement, rules: Sequence[ValidationRule] = DEFAULT_RULES
) -> ValidationReport:
    """Evaluate ``rules`` against ``measurement`` and return a structured report.

    Does not mutate ``measurement``; assign the result to
    ``measurement.validation`` explicitly if it should be attached.
    """
    return ValidationReport(results=[rule.evaluate(measurement) for rule in rules])
