import rfmeasurement


def test_version_is_defined():
    assert isinstance(rfmeasurement.__version__, str)
    assert rfmeasurement.__version__
