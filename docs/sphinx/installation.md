# Installation

`rfmeasurement` is not yet released to PyPI. Install it from source for
development:

```bash
git clone https://github.com/telmomm/rfmeasurement.git
cd rfmeasurement
python -m pip install -e ".[dev]"
```

Supported Python versions: 3.10, 3.11, 3.12, 3.13.

The core package depends on [numpy](https://numpy.org/) and
[scikit-rf](https://scikit-rf.readthedocs.io/), which is used for all RF
network mathematics (see the project's
[scope](https://github.com/telmomm/rfmeasurement/blob/main/docs/scope.md)).
