"""GUM first-order (linear) uncertainty propagation."""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass

import numpy as np

from rfmeasurement.domain.uncertainty import UncertaintySource
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.covariance import build_covariance_matrix
from rfmeasurement.uncertainty.distributions import MissingNominalValueError


@dataclass(slots=True)
class LinearPropagationResult:
    """First-order Taylor (GUM) propagation result.

    ``standard_uncertainty`` includes correlation cross-terms via the full
    covariance matrix (``u_c(y)^2 = c^T . Sigma . c``), not just a sum of
    squares. ``sensitivity_coefficients`` are the partial derivatives used,
    whether supplied analytically via ``UncertaintyModel.sensitivity`` or
    estimated by central finite differences.
    """

    value: float
    standard_uncertainty: float
    sensitivity_coefficients: dict[str, float]


def propagate_linear(
    model: UncertaintyModel, *, relative_step: float = 1e-6
) -> LinearPropagationResult:
    """Propagate uncertainty through ``model.function`` via a first-order Taylor expansion.

    Useful for approximately linear models, fast estimates, and sensitivity
    analysis (docs/uncertainty.md). For strongly nonlinear models, prefer
    :func:`rfmeasurement.uncertainty.monte_carlo.propagate_monte_carlo`.
    """
    nominal = _nominal_values(model.sources)
    value = model.function(nominal)

    sensitivities = dict(model.sensitivity) if model.sensitivity else {}
    for source in model.sources:
        if source.name not in sensitivities:
            sensitivities[source.name] = _finite_difference(
                model.function, nominal, source.name, relative_step
            )

    coefficients = np.array([sensitivities[s.name] for s in model.sources])
    covariance = build_covariance_matrix(model.sources)
    variance = float(coefficients @ covariance @ coefficients)
    if variance < 0:
        raise ValueError(
            "Combined variance is negative: the declared correlations do not form a valid "
            "(positive semi-definite) covariance matrix."
        )
    return LinearPropagationResult(
        value=value,
        standard_uncertainty=math.sqrt(variance),
        sensitivity_coefficients=sensitivities,
    )


def _nominal_values(sources: tuple[UncertaintySource, ...]) -> dict[str, float]:
    values: dict[str, float] = {}
    for source in sources:
        if source.nominal_value is None:
            raise MissingNominalValueError(
                f"UncertaintySource '{source.name}' has no nominal_value; required for "
                "propagation."
            )
        values[source.name] = source.nominal_value
    return values


def _finite_difference(
    function: Callable[[Mapping[str, float]], float],
    nominal: Mapping[str, float],
    name: str,
    relative_step: float,
) -> float:
    h = relative_step * max(abs(nominal[name]), 1.0)
    plus = dict(nominal)
    plus[name] = nominal[name] + h
    minus = dict(nominal)
    minus[name] = nominal[name] - h
    return (function(plus) - function(minus)) / (2 * h)
