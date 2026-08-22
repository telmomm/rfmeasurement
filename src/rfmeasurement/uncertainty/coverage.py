"""Coverage intervals and expansion factors (docs/uncertainty.md)."""

from __future__ import annotations

from collections.abc import Sequence
from statistics import NormalDist

import numpy as np


def coverage_factor(coverage_probability: float) -> float:
    """The two-sided Gaussian expansion factor k for a coverage probability.

    Assumes the combined estimate is approximately normally distributed,
    per the GUM's standard (non-Monte-Carlo) treatment. For non-Gaussian
    output distributions, use :func:`coverage_interval_from_samples` instead,
    which does not rely on this assumption.
    """
    if not 0.0 < coverage_probability < 1.0:
        raise ValueError("coverage_probability must be in (0, 1)")
    return NormalDist().inv_cdf(0.5 + coverage_probability / 2)


def expand(
    value: float, standard_uncertainty: float, coverage_probability: float
) -> tuple[float, tuple[float, float]]:
    """Expanded uncertainty and coverage interval, assuming normality.

    Returns ``(expanded_uncertainty, (lower, upper))``. The API deliberately
    keeps ``expanded_uncertainty`` and the coverage probability that produced
    it side by side, rather than returning a bare interval, so a caller can
    never present it as a generic "confidence interval" without knowing its
    actual coverage probability.
    """
    k = coverage_factor(coverage_probability)
    expanded_uncertainty = k * standard_uncertainty
    return expanded_uncertainty, (value - expanded_uncertainty, value + expanded_uncertainty)


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
