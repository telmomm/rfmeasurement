"""The measurement model tying uncertainty sources to a measurand's value."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty import UncertaintySource


@dataclass(slots=True)
class UncertaintyModel:
    """The function relating uncertainty sources to a measurand's value, plus assumptions.

    docs/uncertainty.md: "A valid uncertainty result requires a defensible
    measurement model and documented assumptions." ``function`` maps a
    mapping of source name to value onto the measurand's output value; it is
    called once per Monte Carlo sample and near the nominal point for linear
    propagation, so it should be cheap and side-effect free. ``sensitivity``,
    if given, supplies analytic partial derivatives per source name so linear
    propagation does not have to estimate them numerically.
    """

    measurand: Measurand
    function: Callable[[Mapping[str, float]], float]
    sources: tuple[UncertaintySource, ...]
    assumptions: str
    sensitivity: Mapping[str, float] | None = None
