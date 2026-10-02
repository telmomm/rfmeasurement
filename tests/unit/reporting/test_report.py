from _fixtures import analysis_result, attenuator_measurement, uncertainty_model

from rfmeasurement.reporting.report import generate_report


def test_report_includes_every_documented_section():
    measurement = attenuator_measurement(with_provenance=True)
    model = uncertainty_model()
    result = analysis_result(model)

    report = generate_report(measurement, result, model=model)

    assert "# Analysis report: IL" in report
    assert "## Result" in report
    assert "## Input" in report
    assert "## Validation summary" in report
    assert "## Analysis configuration" in report
    assert "## Software environment" in report
    assert "## Reproducibility level" in report
    assert "**Level 4**" in report


def test_report_is_plain_text_markdown():
    measurement = attenuator_measurement()
    model = uncertainty_model()
    result = analysis_result(model)

    report = generate_report(measurement, result, model=model)

    assert isinstance(report, str)
    assert report.endswith("\n")
    assert not report.endswith("\n\n")


def test_report_states_coverage_factor_and_degrees_of_freedom():
    measurement = attenuator_measurement()
    model = uncertainty_model()
    result = analysis_result(model)
    result.coverage_factor = 2.78
    result.effective_degrees_of_freedom = 4.0

    report = generate_report(measurement, result, model=model)

    assert "(95% coverage, k = 2.78, effective degrees of freedom = 4.0)" in report


def test_report_omits_coverage_factor_when_not_recorded():
    measurement = attenuator_measurement()
    model = uncertainty_model()

    report = generate_report(measurement, analysis_result(model), model=model)

    assert "(95% coverage)" in report
