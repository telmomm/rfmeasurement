"""Capture the software environment a result was produced with (docs/reproducibility.md)."""

from __future__ import annotations

import platform
from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError, version

import rfmeasurement

_TRACKED_DEPENDENCIES = ("numpy", "scikit-rf", "scipy")


@dataclass(slots=True, frozen=True)
class SoftwareEnvironment:
    """A snapshot of the software that produced a result.

    docs/reproducibility.md: reproducible reports should carry "software
    version; Python version; dependency versions where useful". Only the
    project's own direct dependencies are tracked by name (see
    ``pyproject.toml``); this is not a full dependency-tree lock file --
    see docs/reproducibility.md's "Environment capture" for why that is
    treated as optional rather than mandatory.
    """

    rfmeasurement_version: str
    python_version: str
    platform: str
    dependency_versions: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "rfmeasurement_version": self.rfmeasurement_version,
            "python_version": self.python_version,
            "platform": self.platform,
            "dependency_versions": dict(self.dependency_versions),
        }


def capture_environment() -> SoftwareEnvironment:
    """Snapshot the currently running software environment."""
    dependency_versions: dict[str, str] = {}
    for name in _TRACKED_DEPENDENCIES:
        try:
            dependency_versions[name] = version(name)
        except PackageNotFoundError:
            continue
    return SoftwareEnvironment(
        rfmeasurement_version=rfmeasurement.__version__,
        python_version=platform.python_version(),
        platform=platform.platform(),
        dependency_versions=dependency_versions,
    )
