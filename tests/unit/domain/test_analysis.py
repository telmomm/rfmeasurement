from rfmeasurement.domain.analysis import AnalysisResult
from rfmeasurement.domain.enums import ValidationStatus
from rfmeasurement.domain.measurand import Measurand


def test_analysis_result_defaults_to_not_evaluated():
    result = AnalysisResult(
        measurand=Measurand(name="S11", definition="Input reflection coefficient", unit="dB"),
        value=-12.3,
        unit="dB",
    )
    assert result.validation_status is ValidationStatus.NOT_EVALUATED
    assert result.standard_uncertainty is None
    assert result.contributing_sources == ()


def test_analysis_result_can_carry_a_coverage_interval():
    result = AnalysisResult(
        measurand=Measurand(name="S11", definition="Input reflection coefficient", unit="dB"),
        value=-12.3,
        unit="dB",
        standard_uncertainty=0.1,
        expanded_uncertainty=0.2,
        coverage_probability=0.95,
        coverage_interval=(-12.5, -12.1),
    )
    assert result.coverage_probability == 0.95
    assert result.coverage_interval == (-12.5, -12.1)
