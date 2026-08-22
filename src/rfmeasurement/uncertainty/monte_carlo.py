"""Monte Carlo uncertainty propagation (GUM Supplement 1 style)."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from rfmeasurement.domain.enums import Distribution
from rfmeasurement.domain.uncertainty import UncertaintySource
from rfmeasurement.domain.uncertainty_model import UncertaintyModel
from rfmeasurement.uncertainty.covariance import build_covariance_matrix
from rfmeasurement.uncertainty.distributions import MissingNominalValueError, sample_source


@dataclass(slots=True)
class MonteCarloResult:
    """Output of a Monte Carlo propagation run.

    ``standard_error`` is the Monte Carlo standard error of
    ``standard_uncertainty`` itself, not of ``value``: the estimated output
    standard deviation is itself uncertain, with precision that improves as
    ``1 / sqrt(n_samples)``. Increase ``n_samples`` if ``standard_error`` is
    not small relative to ``standard_uncertainty``.
    """

    value: float
    standard_uncertainty: float
    standard_error: float
    n_samples: int
    samples: np.ndarray


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
    """
    rng = rng if rng is not None else np.random.default_rng()
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
    )


def _sample_all_sources(
    sources: tuple[UncertaintySource, ...], rng: np.random.Generator, n_samples: int
) -> dict[str, np.ndarray]:
    _validate_correlation_support(sources)

    samples: dict[str, np.ndarray] = {}
    normal_sources = [s for s in sources if s.distribution is Distribution.NORMAL]
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
        if source.distribution is not Distribution.NORMAL:
            samples[source.name] = sample_source(source, rng, n_samples)

    return samples


def _validate_correlation_support(sources: tuple[UncertaintySource, ...]) -> None:
    normal_names = {s.name for s in sources if s.distribution is Distribution.NORMAL}
    for source in sources:
        for other_name, correlation in source.correlation.items():
            if correlation == 0:
                continue
            if source.name not in normal_names or other_name not in normal_names:
                raise NotImplementedError(
                    "Correlated Monte Carlo sampling is only implemented between normally "
                    f"distributed sources; got a nonzero correlation between '{source.name}' "
                    f"({source.distribution.value}) and '{other_name}'."
                )
