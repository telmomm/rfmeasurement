"""Structured outcome of a measurement-quality check (docs/measurement-quality.md)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from rfmeasurement.domain.enums import ValidationStatus


@dataclass(slots=True, frozen=True)
class ValidationResult:
    """The result of evaluating a single validation rule against a measurement.

    Validation is never represented only by a boolean: ``status`` is one of
    PASS / WARNING / FAIL / NOT_APPLICABLE / NOT_EVALUATED, and ``evidence``
    carries the structured data the rule based its decision on.
    """

    rule_id: str
    status: ValidationStatus
    description: str
    evidence: dict[str, object] = field(default_factory=dict)
    criterion: str | None = None
    explanation: str | None = None
    rule_version: str | None = None
    remediation: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class ValidationReport:
    """The collection of validation results produced for one measurement.

    docs/architecture.md lists ``ValidationReport`` alongside
    ``ValidationResult`` as one of the first stable domain objects.
    """

    results: list[ValidationResult] = field(default_factory=list)

    @property
    def has_failures(self) -> bool:
        return any(r.status is ValidationStatus.FAIL for r in self.results)

    @property
    def has_warnings(self) -> bool:
        return any(r.status is ValidationStatus.WARNING for r in self.results)

    def by_status(self, status: ValidationStatus) -> list[ValidationResult]:
        return [r for r in self.results if r.status is status]
