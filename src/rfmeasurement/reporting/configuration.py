"""Capture the configuration behind an analysis result, so it can be reproduced.

docs/reproducibility.md: a final result should be traceable to its
"validation rules" and "uncertainty models" (among other things), and a
reproducible report should carry its "analysis configuration". This module
assembles that configuration from the objects involved in producing a
result, rather than inventing a new config format those objects must
conform to.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.linear import LinearPropagationResult
from rfmeasurement.uncertainty.monte_carlo import MonteCarloResult


@dataclass(slots=True, frozen=True)
class AnalysisConfiguration:
    """Everything needed to reproduce how a value was obtained from a measurement.

    ``validation_rules`` is ``(rule_id, rule_version)`` for every rule
    actually evaluated (from the measurement's own
    :class:`~rfmeasurement.domain.validation.ValidationReport`), not the
    full set of rules a validation engine knows about. ``propagation`` is
    only populated when :func:`build_configuration` is given evidence of
    which propagation algorithm actually ran (a :class:`LinearPropagationResult`
    or :class:`MonteCarloResult`) -- passing ``model`` alone does not imply a
    method, since a model can be used with either.
    """

    validation_rules: tuple[tuple[str, str | None], ...] = field(default_factory=tuple)
    uncertainty_assumptions: str | None = None
    uncertainty_source_names: tuple[str, ...] = field(default_factory=tuple)
    propagation: dict[str, object] = field(default_factory=dict)
    coverage_probability: float | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "validation_rules": [
                {"rule_id": rule_id, "rule_version": rule_version}
                for rule_id, rule_version in self.validation_rules
            ],
            "uncertainty_assumptions": self.uncertainty_assumptions,
            "uncertainty_source_names": list(self.uncertainty_source_names),
            "propagation": self.propagation,
            "coverage_probability": self.coverage_probability,
        }


def build_configuration(
    measurement: Measurement,
    *,
    model: UncertaintyModel | None = None,
    linear: LinearPropagationResult | None = None,
    monte_carlo: MonteCarloResult | None = None,
    coverage_probability: float | None = None,
) -> AnalysisConfiguration:
    """Assemble the configuration that produced (or would reproduce) a result.

    ``model``, ``linear`` and ``monte_carlo`` are all optional: not every
    measurement has gone through uncertainty propagation, and when it has,
    only the method actually used should be passed. If both ``linear`` and
    ``monte_carlo`` are given, ``monte_carlo`` takes precedence as the
    propagation actually reported.
    """
    validation_rules = tuple(
        (result.rule_id, result.rule_version) for result in measurement.validation.results
    )

    propagation: dict[str, object] = {}
    if monte_carlo is not None:
        propagation = {
            "method": "monte_carlo",
            "n_samples": monte_carlo.n_samples,
            "rng_state": monte_carlo.rng_state,
        }
    elif linear is not None:
        propagation = {
            "method": "linear",
            "sensitivity_coefficients": dict(linear.sensitivity_coefficients),
        }

    return AnalysisConfiguration(
        validation_rules=validation_rules,
        uncertainty_assumptions=model.assumptions if model is not None else None,
        uncertainty_source_names=tuple(s.name for s in model.sources) if model is not None else (),
        propagation=propagation,
        coverage_probability=coverage_probability,
    )
