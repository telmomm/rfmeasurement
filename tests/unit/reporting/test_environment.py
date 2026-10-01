import rfmeasurement
from rfmeasurement.reporting.environment import capture_environment


def test_capture_environment_reports_own_version():
    environment = capture_environment()
    assert environment.rfmeasurement_version == rfmeasurement.__version__
    assert environment.python_version
    assert environment.platform


def test_capture_environment_tracks_direct_dependencies():
    environment = capture_environment()
    assert "numpy" in environment.dependency_versions
    assert "scikit-rf" in environment.dependency_versions


def test_to_dict_is_json_serializable():
    import json

    environment = capture_environment()
    payload = json.dumps(environment.to_dict())
    decoded = json.loads(payload)
    assert decoded["rfmeasurement_version"] == rfmeasurement.__version__
