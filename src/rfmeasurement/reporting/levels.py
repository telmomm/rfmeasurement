"""Classify how reproducible a specific result actually is (docs/reproducibility.md).

docs/reproducibility.md defines five levels (0-4) and says: "The framework
should make these levels visible rather than claiming every result is
equally reproducible." A :class:`~rfmeasurement.domain.measurement.Measurement`
always carries its own input data, so levels reachable through this
framework start at 1 rather than 0 ("Result only", with no data at all,
describes a number reported with nothing behind it -- not how this
framework represents a result).
"""

from __future__ import annotations

from rfmeasurement.domain.analysis import AnalysisResult
from rfmeasurement.domain.measurement import Measurement
from rfmeasurement.reporting.configuration import AnalysisConfiguration
from rfmeasurement.reporting.environment import SoftwareEnvironment

LEVEL_DESCRIPTIONS: dict[int, str] = {
    1: "Result + input data.",
    2: "Result + data + analysis configuration.",
    3: "Result + data + configuration + software environment.",
    4: "Level 3 plus complete instrument/calibration/environment provenance.",
}


def reproducibility_level(
    measurement: Measurement,
    analysis_result: AnalysisResult,  # noqa: ARG001 -- part of the documented level definition
    *,
    configuration: AnalysisConfiguration | None = None,
    environment: SoftwareEnvironment | None = None,
) -> int:
    """Classify ``analysis_result`` on the docs/reproducibility.md 1-4 scale.

    -   **1** -- always true: ``measurement`` carries its own input data.
    -   **2** -- ``configuration`` is given and records at least one
        validation rule or propagation method.
    -   **3** -- ``environment`` (a captured
        :class:`~rfmeasurement.reporting.environment.SoftwareEnvironment`)
        is also given.
    -   **4** -- in addition, ``measurement`` has a non-empty provenance
        chain and its context names both the instrument and the
        calibration used.
    """
    has_configuration = configuration is not None and bool(
        configuration.validation_rules or configuration.propagation
    )
    if not has_configuration:
        return 1

    if environment is None:
        return 2

    complete_provenance = (
        bool(measurement.provenance)
        and measurement.context.instrument is not None
        and measurement.context.calibration is not None
    )
    return 4 if complete_provenance else 3
