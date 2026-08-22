"""Build a covariance matrix from independent standard uncertainties and declared correlations."""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np

from rfmeasurement.domain.uncertainty import UncertaintySource


def build_covariance_matrix(sources: Sequence[UncertaintySource]) -> np.ndarray:
    """Assemble the covariance matrix implied by each source's declared correlations.

    ``rfmeasurement`` never assumes independence (docs/uncertainty.md):
    off-diagonal terms come only from ``UncertaintySource.correlation``.
    Correlation only needs to be declared on one of the two sources; if
    declared on both, the two values must agree.
    """
    names = [s.name for s in sources]
    index = {name: i for i, name in enumerate(names)}
    n = len(sources)
    covariance = np.zeros((n, n))
    for i, source in enumerate(sources):
        covariance[i, i] = source.standard_uncertainty**2

    for i, source in enumerate(sources):
        for other_name, correlation in source.correlation.items():
            if other_name not in index:
                continue
            if not -1.0 <= correlation <= 1.0:
                raise ValueError(
                    f"Correlation coefficient between '{source.name}' and '{other_name}' "
                    f"must be in [-1, 1], got {correlation}."
                )
            j = index[other_name]
            value = correlation * source.standard_uncertainty * sources[j].standard_uncertainty
            existing = covariance[i, j]
            if existing != 0.0 and not math.isclose(existing, value, rel_tol=1e-9, abs_tol=1e-12):
                raise ValueError(
                    f"Inconsistent correlation declared between '{source.name}' and "
                    f"'{other_name}'."
                )
            covariance[i, j] = value
            covariance[j, i] = value
    return covariance
