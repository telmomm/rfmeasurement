"""Monte Carlo uncertainty propagation (GUM Supplement 1 style)."""

from __future__ import annotations

import math
import warnings
from dataclasses import dataclass

import numpy as np

from rfmeasurement.domain.enums import Distribution
from rfmeasurement.domain.uncertainty import UncertaintySource
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.covariance import build_covariance_matrix
from rfmeasurement.uncertainty.distributions import (
    MissingNominalValueError,
    finite_degrees_of_freedom,
    sample_source,
)


@dataclass(slots=True)
class MonteCarloResult:
    """Output of a Monte Carlo propagation run.

    ``standard_error`` is the Monte Carlo standard error of
    ``standard_uncertainty`` itself, not of ``value``: the estimated output
    standard deviation is itself uncertain, with precision that improves as
    ``1 / sqrt(n_samples)``. Increase ``n_samples`` if ``standard_error`` is
    not small relative to ``standard_uncertainty``.

    ``rng_state`` is the JSON-serializable state of the random generator
    exactly as it stood before sampling began (docs/reproducibility.md:
    "the random generator should be explicit; the seed should be
    recordable"). Recording it, rather than just a seed integer, lets a run
    be reproduced even when the caller supplied an already-advanced
    generator rather than a freshly-seeded one.

    When a source declares finite ``degrees_of_freedom`` it is sampled from
    a t-distribution, whose standard deviation is ``sqrt(nu / (nu - 2))``
    times its ``standard_uncertainty``. ``standard_uncertainty`` here is
    therefore larger than the one linear propagation reports for the same
    model (JCGM 101 vs. the GUM), and does not converge at all for
    ``nu <= 2`` (:func:`propagate_monte_carlo` warns); the coverage interval
    read off ``samples`` is valid in either case.
    """

    value: float
    standard_uncertainty: float
    standard_error: float
    n_samples: int
    samples: np.ndarray
    rng_state: dict[str, object]


def propagate_monte_carlo(
    model: UncertaintyModel,
    *,
    n_samples: int = 10_000,
    rng: np.random.Generator | None = None,
) -> MonteCarloResult:
    """Propagate uncertainty through ``model.function`` by sampling each source.

    The preferred general-purpose method for nonlinear models and
    non-Gaussian distributions (docs/uncertainty.md). Correlated sources are
    only supported when all correlated sources are NORMALly distributed
    (sampled jointly via a multivariate normal); a correlation involving any
    other distribution raises :class:`NotImplementedError` rather than
    silently ignoring it.

    A NORMAL source with finite ``degrees_of_freedom`` is sampled from a
    scaled and shifted t-distribution (JCGM 101, 6.4.9.2), so that
    :func:`~rfmeasurement.uncertainty.coverage.coverage_interval_from_samples`
    accounts for its standard uncertainty being an estimate. Such a source
    must be uncorrelated.
    """
    for source in model.sources:
        nu = finite_degrees_of_freedom(source)
        if nu is not None and nu <= 2:
            warnings.warn(
                f"UncertaintySource '{source.name}' has degrees_of_freedom <= 2: its "
                "t-distribution has no finite variance, so the Monte Carlo standard_uncertainty "
                "does not converge. Use the coverage interval of the samples instead.",
                RuntimeWarning,
                stacklevel=2,
            )

    rng = rng if rng is not None else np.random.default_rng(42)
    rng_state = dict(rng.bit_generator.state)
    samples = _sample_all_sources(model.sources, rng, n_samples)

    outputs = np.empty(n_samples)
    for i in range(n_samples):
        outputs[i] = model.function({name: values[i] for name, values in samples.items()})

    value = float(np.mean(outputs))
    standard_uncertainty = float(np.std(outputs, ddof=1))
    standard_error = (
        standard_uncertainty / math.sqrt(2 * (n_samples - 1)) if n_samples > 1 else float("nan")
    )
    return MonteCarloResult(
        value=value,
        standard_uncertainty=standard_uncertainty,
        standard_error=standard_error,
        n_samples=n_samples,
        samples=outputs,
        rng_state=rng_state,
    )


def _sample_all_sources(
    sources: tuple[UncertaintySource, ...], rng: np.random.Generator, n_samples: int
) -> dict[str, np.ndarray]:
    _validate_correlation_support(sources)

    samples: dict[str, np.ndarray] = {}
    normal_sources = [s for s in sources if _is_jointly_normal(s)]
    if normal_sources:
        means = []
        for source in normal_sources:
            if source.nominal_value is None:
                raise MissingNominalValueError(
                    f"UncertaintySource '{source.name}' has no nominal_value; required for "
                    "sampling."
                )
            means.append(source.nominal_value)
        covariance = build_covariance_matrix(normal_sources)
        draws = rng.multivariate_normal(
            mean=means, cov=covariance, size=n_samples, check_valid="raise"
        )
        for i, source in enumerate(normal_sources):
            samples[source.name] = draws[:, i]

    for source in sources:
        if not _is_jointly_normal(source):
            samples[source.name] = sample_source(source, rng, n_samples)

    return samples


def _is_jointly_normal(source: UncertaintySource) -> bool:
    return source.distribution is Distribution.NORMAL and finite_degrees_of_freedom(source) is None


def _validate_correlation_support(sources: tuple[UncertaintySource, ...]) -> None:
    normal_names = {s.name for s in sources if _is_jointly_normal(s)}
    for source in sources:
        for other_name, correlation in source.correlation.items():
            if correlation == 0:
                continue
            if source.name not in normal_names or other_name not in normal_names:
                raise NotImplementedError(
                    "Correlated Monte Carlo sampling is only implemented between normally "
                    "distributed sources without finite degrees of freedom; got a nonzero "
                    f"correlation between '{source.name}' ({source.distribution.value}) and "
                    f"'{other_name}'."
                )
