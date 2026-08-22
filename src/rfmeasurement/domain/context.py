"""Measurement acquisition context (docs/domain-model.md#measurement-context)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from rfmeasurement.domain.enums import MetadataConfidence


@dataclass(slots=True)
class MeasurementContext:
    """Everything about how a measurement was acquired, besides the data itself.

    A field left as ``None`` is simply unknown. Use ``confidence`` to record
    how a *known* field's value was obtained (measured, specified, estimated,
    assumed) rather than implicitly treating every field as directly measured.
    """

    dut: str | None = None
    operator: str | None = None
    instrument: str | None = None
    calibration: str | None = None
    cables: str | None = None
    fixture: str | None = None
    temperature_c: float | None = None
    humidity_percent: float | None = None
    pressure_pa: float | None = None
    rf_power_dbm: float | None = None
    if_bandwidth_hz: float | None = None
    averaging: int | None = None
    sweep_settings: dict[str, object] = field(default_factory=dict)
    frequency_range_hz: tuple[float, float] | None = None
    timestamp: datetime | None = None
    confidence: dict[str, MetadataConfidence] = field(default_factory=dict)
