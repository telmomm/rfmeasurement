"""Per-distribution sampling and Type B half-width conversions (docs/uncertainty.md)."""

from __future__ import annotations

import math

import numpy as np

from rfmeasurement.domain.enums import Distribution
from rfmeasurement.domain.uncertainty import UncertaintySource


class MissingNominalValueError(ValueError):
    """Raised when an operation needs a source's nominal_value, but it is None."""


def standard_uncertainty_from_half_width(distribution: Distribution, half_width: float) -> float:
    """Convert a Type B half-width (e.g. a datasheet +/- tolerance) to a standard uncertainty.

    Only defined for bounded distributions with a closed-form conversion.
    NORMAL uncertainty should be specified directly as a standard deviation,
    and EMPIRICAL/DISCRETE/CUSTOM distributions require actual sample or
    point data rather than a single half-width.
    """
    if half_width < 0:
        raise ValueError("half_width must be non-negative")
    if distribution is Distribution.UNIFORM:
        return half_width / math.sqrt(3)
    if distribution is Distribution.TRIANGULAR:
        return half_width / math.sqrt(6)
    raise NotImplementedError(
        f"No half-width conversion is defined for distribution '{distribution.value}'."
    )


def finite_degrees_of_freedom(source: UncertaintySource) -> float | None:
    """``source.degrees_of_freedom``, or ``None`` if its standard uncertainty is exactly known."""
    nu = source.degrees_of_freedom
    return None if nu is None or math.isinf(nu) else nu


def sample_source(
    source: UncertaintySource, rng: np.random.Generator, n_samples: int
) -> np.ndarray:
    """Draw independent samples from one uncertainty source's marginal distribution.

    Does not account for correlation with other sources; see
    :func:`rfmeasurement.uncertainty.monte_carlo.propagate_monte_carlo`, which
    handles correlated NORMAL sources jointly before falling back to this
    function for everything else.

    A NORMAL source with finite ``degrees_of_freedom`` is drawn from a
    scaled and shifted t-distribution, ``nominal + u * t_nu`` (JCGM 101,
    6.4.9.2), because its standard uncertainty is itself an estimate. Other
    distributions have no such treatment, so finite degrees of freedom on
    them raise :class:`NotImplementedError`.
    """
    if source.nominal_value is None:
        raise MissingNominalValueError(
            f"UncertaintySource '{source.name}' has no nominal_value; required for sampling."
        )
    nominal = source.nominal_value
    u = source.standard_uncertainty

    nu = finite_degrees_of_freedom(source)
    if nu is not None:
        if source.distribution is not Distribution.NORMAL:
            raise NotImplementedError(
                "Monte Carlo sampling with finite degrees of freedom is only implemented for "
                f"normally distributed sources; source '{source.name}' is "
                f"{source.distribution.value}."
            )
        return np.asarray(nominal + u * rng.standard_t(nu, size=n_samples))
    if source.distribution is Distribution.NORMAL:
        return np.asarray(rng.normal(nominal, u, size=n_samples))
    if source.distribution is Distribution.UNIFORM:
        half_width = u * math.sqrt(3)
        return np.asarray(rng.uniform(nominal - half_width, nominal + half_width, size=n_samples))
    if source.distribution is Distribution.TRIANGULAR:
        half_width = u * math.sqrt(6)
        return np.asarray(
            rng.triangular(nominal - half_width, nominal, nominal + half_width, size=n_samples)
        )
    raise NotImplementedError(
        f"Monte Carlo sampling is not implemented for distribution "
        f"'{source.distribution.value}' (source '{source.name}'). EMPIRICAL, DISCRETE and "
        "CUSTOM distributions require caller-supplied sample data, which this engine does "
        "not yet accept."
    )
