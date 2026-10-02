"""Coverage intervals and expansion factors (docs/uncertainty.md)."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from statistics import NormalDist

import numpy as np
from scipy.special import stdtrit

from rfmeasurement.domain.uncertainty import UncertaintySource
from rfmeasurement.uncertainty.distributions import finite_degrees_of_freedom


def coverage_factor(coverage_probability: float, degrees_of_freedom: float | None = None) -> float:
    """The two-sided expansion factor k for a coverage probability.

    Assumes the combined estimate is approximately normally distributed,
    per the GUM's standard (non-Monte-Carlo) treatment. For non-Gaussian
    output distributions, use :func:`coverage_interval_from_samples` instead,
    which does not rely on this assumption.

    With ``degrees_of_freedom`` of ``None`` the standard uncertainty is
    treated as exactly known and k is the Gaussian factor (1.96 at 95 %).
    Otherwise k is the Student-t quantile for that many degrees of freedom
    (GUM G.3, Table G.2), typically the ``effective_degrees_of_freedom`` of a
    :class:`~rfmeasurement.uncertainty.linear.LinearPropagationResult`. The
    quantile is evaluated at the given, possibly non-integer, value rather
    than truncated to the next lower integer as a table lookup would be.
    """
    if not 0.0 < coverage_probability < 1.0:
        raise ValueError("coverage_probability must be in (0, 1)")
    if degrees_of_freedom is None or math.isinf(degrees_of_freedom):
        return NormalDist().inv_cdf(0.5 + coverage_probability / 2)
    _check_degrees_of_freedom(degrees_of_freedom)
    return float(stdtrit(degrees_of_freedom, 0.5 + coverage_probability / 2))


def expand(
    value: float,
    standard_uncertainty: float,
    coverage_probability: float,
    degrees_of_freedom: float | None = None,
) -> tuple[float, tuple[float, float]]:
    """Expanded uncertainty and coverage interval, assuming normality.

    Returns ``(expanded_uncertainty, (lower, upper))``. The API deliberately
    keeps ``expanded_uncertainty`` and the coverage probability that produced
    it side by side, rather than returning a bare interval, so a caller can
    never present it as a generic "confidence interval" without knowing its
    actual coverage probability. ``degrees_of_freedom`` selects the factor as
    in :func:`coverage_factor`.
    """
    k = coverage_factor(coverage_probability, degrees_of_freedom)
    expanded_uncertainty = k * standard_uncertainty
    return expanded_uncertainty, (value - expanded_uncertainty, value + expanded_uncertainty)


def effective_degrees_of_freedom(
    sources: Sequence[UncertaintySource],
    sensitivity_coefficients: Mapping[str, float],
    combined_standard_uncertainty: float,
) -> float | None:
    """Welch-Satterthwaite effective degrees of freedom (GUM G.4, eq. G.2b).

    ``nu_eff = u_c^4 / sum((c_i * u_i)^4 / nu_i)``. Sources whose
    ``degrees_of_freedom`` is ``None`` are exactly known and add nothing to
    the sum; if no source contributes, the result is ``None`` (the Gaussian
    factor applies).

    The formula assumes the inputs are uncorrelated. A source with finite
    degrees of freedom that declares a correlation raises
    :class:`NotImplementedError` rather than returning a number the formula
    does not justify.
    """
    names = {source.name for source in sources}
    correlated = {
        name
        for source in sources
        for other_name, correlation in source.correlation.items()
        if correlation != 0 and other_name in names
        for name in (source.name, other_name)
    }

    denominator = 0.0
    for source in sources:
        nu = finite_degrees_of_freedom(source)
        if nu is None:
            continue
        _check_degrees_of_freedom(nu, source.name)
        if source.name in correlated:
            raise NotImplementedError(
                "The Welch-Satterthwaite formula assumes uncorrelated inputs, but source "
                f"'{source.name}' has finite degrees of freedom and a nonzero correlation. "
                "Effective degrees of freedom are not implemented for that case; leave "
                "degrees_of_freedom unset to treat its standard uncertainty as exactly known."
            )
        contribution = sensitivity_coefficients[source.name] * source.standard_uncertainty
        denominator += contribution**4 / nu

    if denominator == 0.0:
        return None
    return combined_standard_uncertainty**4 / denominator


def coverage_interval_from_samples(
    samples: Sequence[float] | np.ndarray, coverage_probability: float
) -> tuple[float, float]:
    """A coverage interval read directly off Monte Carlo output samples.

    Does not assume normality (GUM Supplement 1 approach): the interval
    boundaries are the ``(1 - p) / 2`` and ``1 - (1 - p) / 2`` percentiles of
    the empirical output distribution.
    """
    if not 0.0 < coverage_probability < 1.0:
        raise ValueError("coverage_probability must be in (0, 1)")
    tail = (1.0 - coverage_probability) / 2
    lower, upper = np.percentile(np.asarray(samples), [tail * 100, (1 - tail) * 100])
    return float(lower), float(upper)


def _check_degrees_of_freedom(degrees_of_freedom: float, source_name: str | None = None) -> None:
    if not degrees_of_freedom > 0:
        owner = f" of source '{source_name}'" if source_name is not None else ""
        raise ValueError(f"degrees_of_freedom{owner} must be positive, got {degrees_of_freedom}.")
