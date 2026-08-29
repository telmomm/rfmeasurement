"""Pin the validation outcome for a real, lab-measured antenna.

Protects the exact behavior demonstrated in examples/03_real_measurement.py
against silent changes (e.g. to PassivityRule's default tolerance). The data
is a real "ring slot" antenna measurement, frozen in tests/data/ (originally
from scikit-rf's own bundled example data, skrf.data.ring_slot_meas and
skrf.data.ring_slot -- see tests/data/README.md).
"""

from __future__ import annotations

from pathlib import Path

import skrf as rf

from rfmeasurement.domain import Measurement
from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.validation import validate

_DATA_DIR = Path(__file__).parent.parent / "data"


def test_raw_1port_measurement_fails_passivity_but_is_otherwise_clean():
    """A real antenna reflection measurement, not engineered to pass or fail anything."""
    network = rf.Network(str(_DATA_DIR / "ring_slot_measured.s1p"))
    report = validate(Measurement(data=network))
    by_id = {r.rule_id: r for r in report.results}

    assert by_id["integrity.structural"].status is ValidationStatus.PASS
    assert by_id["integrity.finite_values"].status is ValidationStatus.PASS
    assert by_id["integrity.frequency_grid"].status is ValidationStatus.PASS
    assert by_id["physics.passivity"].status is ValidationStatus.FAIL
    assert by_id["physics.reciprocity"].status is ValidationStatus.NOT_APPLICABLE
    assert by_id["quality.continuity"].status is ValidationStatus.PASS
    assert by_id["quality.dynamic_range"].status is ValidationStatus.PASS


def test_2port_representation_passes_every_default_rule():
    network = rf.Network(str(_DATA_DIR / "ring_slot.s2p"))
    report = validate(Measurement(data=network))

    assert report.has_failures is False
    assert report.has_warnings is False
