"""Is this RF measurement trustworthy enough to analyze?

This example builds two synthetic 2-port measurements of a 10 dB
attenuator swept from 1-3 GHz -- one representative of a clean VNA trace,
one with realistic problems -- and runs the Phase 2 validation engine on
each to see how the structured QA report tells them apart.

No real instrument or file is involved yet: `rfmeasurement` does not have
a data adapter (Touchstone, PyVISA, ...) until a later development phase,
so the input data is synthesized directly with scikit-rf. See
docs/scope.md and docs/repository-organization.md.

Run with:
    python examples/01_validate_measurement.py
"""

from __future__ import annotations

import numpy as np
import skrf as rf

from rfmeasurement.domain import Measurement, MeasurementContext, MetadataConfidence
from rfmeasurement.validation import validate

SEED = 42  # fixed for reproducibility, per docs/reproducibility.md


def _attenuator_network(*, add_realistic_noise: bool, corrupt_one_point: bool) -> rf.Network:
    """A synthetic 10 dB attenuator: passive, reciprocal, matched."""
    frequency = rf.Frequency(1, 3, 101, unit="GHz")
    n = frequency.npoints

    s = np.zeros((n, 2, 2), dtype=complex)
    s[:, 0, 0] = 0.05  # small reflection, ~ -26 dB
    s[:, 1, 1] = 0.05
    s[:, 0, 1] = 0.316  # ~ -10 dB transmission
    s[:, 1, 0] = 0.316

    if add_realistic_noise:
        rng = np.random.default_rng(SEED)
        noise = rng.normal(scale=0.002, size=s.shape) + 1j * rng.normal(scale=0.002, size=s.shape)
        s = s + noise
        # The DUT itself is physically reciprocal; keep S12 == S21 exactly so this
        # measurement demonstrates a clean PASS rather than realistic receiver-to-receiver
        # noise, which would also make S12 and S21 differ slightly on a real instrument.
        s[:, 1, 0] = s[:, 0, 1]

    if corrupt_one_point:
        # Simulate a dropped sample mid-sweep, e.g. a momentary acquisition glitch.
        s[n // 2, 1, 0] = np.nan

    return rf.Network(frequency=frequency, s=s)


def _build_measurement(*, add_realistic_noise: bool, corrupt_one_point: bool) -> Measurement:
    network = _attenuator_network(
        add_realistic_noise=add_realistic_noise, corrupt_one_point=corrupt_one_point
    )
    context = MeasurementContext(
        dut="10 dB fixed attenuator, s/n 0042",
        instrument="Simulated VNA",
        calibration="SOLT",
        temperature_c=23.0,
        rf_power_dbm=-10.0,
        confidence={"temperature_c": MetadataConfidence.ESTIMATED},
    )
    return Measurement(data=network, context=context)


def _print_report(title: str, measurement: Measurement) -> None:
    report = validate(measurement)
    print(f"\n{title}")
    print("-" * len(title))
    for result in report.results:
        print(f"[{result.status.value.upper():14}] {result.rule_id}: {result.description}")
        if result.explanation:
            print(f"                 -> {result.explanation}")
    print(f"\nOverall: {'FAIL' if report.has_failures else 'OK'}"
          f" (failures={report.has_failures}, warnings={report.has_warnings})")


def main() -> None:
    clean = _build_measurement(add_realistic_noise=True, corrupt_one_point=False)
    _print_report("Clean measurement", clean)

    corrupted = _build_measurement(add_realistic_noise=True, corrupt_one_point=True)
    _print_report("Measurement with a dropped sample", corrupted)


if __name__ == "__main__":
    main()
