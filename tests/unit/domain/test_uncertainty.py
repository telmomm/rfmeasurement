from rfmeasurement.domain.enums import Distribution, UncertaintyType
from rfmeasurement.domain.uncertainty import UncertaintySource


def test_uncertainty_source_records_type_and_distribution():
    source = UncertaintySource(
        name="calibration",
        description="SOLT calibration residual",
        uncertainty_type=UncertaintyType.TYPE_B,
        distribution=Distribution.NORMAL,
        standard_uncertainty=0.02,
        unit="dB",
    )
    assert source.uncertainty_type is UncertaintyType.TYPE_B
    assert source.correlation == {}


def test_uncertainty_source_can_declare_correlation_to_another_source():
    source = UncertaintySource(
        name="s11_noise",
        description="Frequency-correlated VNA noise",
        uncertainty_type=UncertaintyType.TYPE_A,
        distribution=Distribution.NORMAL,
        standard_uncertainty=0.01,
        unit="linear",
        correlation={"s21_noise": 0.8},
    )
    assert source.correlation["s21_noise"] == 0.8
