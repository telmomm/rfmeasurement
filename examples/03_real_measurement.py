"""Does a real, lab-measured antenna pass the same QA checks as a synthetic one?

Examples 01 and 02 use synthetic data because `rfmeasurement` does not yet
have a Touchstone/instrument adapter of its own -- but scikit-rf, which the
project builds on (see docs/scope.md), ships real measured Touchstone data
as installed package data. This example validates two real VNA measurements
of the same "ring slot" antenna from scikit-rf's own tutorials:

- ``skrf.data.ring_slot_meas``: the raw 1-port measurement (75-110 GHz,
  101 points), taken with real lab equipment.
- ``skrf.data.ring_slot``: a 2-port representation of the same antenna
  (75-110 GHz, 201 points) used elsewhere in scikit-rf's own tutorials.

Unlike examples 01/02, this data was not engineered to pass or fail
anything -- whatever the validation engine reports here is a genuine
property of a real measurement, not a demonstration I constructed. No
uncertainty propagation is attempted: the original files carry no
documented uncertainty sources, and inventing one would go against the
project's own principle of not presenting a number as meaningful without a
defensible measurement model (docs/uncertainty.md).

Run with:
    python examples/03_real_measurement.py
"""

from __future__ import annotations

import skrf as rf
import skrf.data

from rfmeasurement.domain import Measurement, MeasurementContext, MetadataConfidence
from rfmeasurement.validation import validate


def _build_measurement(network: rf.Network) -> Measurement:
    """Wrap a real scikit-rf measurement, being honest about what is unknown.

    The original Touchstone files carry almost no acquisition metadata
    beyond the swept frequency range -- a common situation with real-world
    data, and exactly what MeasurementContext.confidence is for: instrument,
    calibration, and operator are left as None (simply unknown) rather than
    guessed at.
    """
    context = MeasurementContext(
        dut=network.name,
        frequency_range_hz=(network.frequency.start, network.frequency.stop),
        confidence={
            "dut": MetadataConfidence.SPECIFIED,  # taken from the file's own network name
            "frequency_range_hz": MetadataConfidence.MEASURED,  # the VNA's own swept range
        },
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
    print(
        f"\nOverall: {'FAIL' if report.has_failures else 'OK'}"
        f" (failures={report.has_failures}, warnings={report.has_warnings})"
    )


def main() -> None:
    one_port = _build_measurement(skrf.data.ring_slot_meas)
    _print_report("Ring slot antenna, raw 1-port measurement", one_port)

    two_port = _build_measurement(skrf.data.ring_slot)
    _print_report("Ring slot antenna, 2-port representation", two_port)

    print(
        "\nNote: a FAIL on physics.passivity for real measured data does not by "
        "itself mean the measurement is unusable -- it can reflect measurement "
        "noise or calibration residuals near the validity boundary, rather than "
        "a data-integrity problem. See docs/measurement-quality.md's distinction "
        "between failed universal integrity checks and failed physical "
        "assumptions."
    )


if __name__ == "__main__":
    main()
