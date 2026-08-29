# rfmeasurement

[![PyPI](https://img.shields.io/pypi/v/rfmeasurement.svg)](https://pypi.org/project/rfmeasurement/)
[![Documentation Status](https://readthedocs.org/projects/rfmeasurement/badge/?version=latest)](https://rfmeasurement.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22058515.svg)](https://doi.org/10.5281/zenodo.22058515)

An open-source Python framework for uncertainty-aware validation and
reproducible analysis of RF measurements.

> **Status: early alpha (`0.1.0`).** The public API is not yet stable and
> may change without notice between `0.x` releases. See the
> [roadmap](docs/roadmap.md) for current progress and the
> [changelog](CHANGELOG.md) for release notes.

**Documentation:** <https://rfmeasurement.readthedocs.io/en/latest/>

## Statement of need

RF measurement data (S-parameters and related quantities) is commonly
analyzed without a structured record of measurement quality, uncertainty,
or provenance. `rfmeasurement` adds a layer on top of established RF
network-analysis tooling to turn raw measurement data into **validated,
uncertainty-aware, reproducible scientific results**.

> Do not only report an RF result. Report how the result was obtained,
> how trustworthy the measurement is, and what uncertainty contributes to
> the final value.

`rfmeasurement` does not replace [scikit-rf](https://scikit-rf.readthedocs.io/);
it builds on it, focusing on measurement provenance, measurement-quality
assessment, uncertainty modelling and propagation, and reproducible
reporting. See [docs/scope.md](docs/scope.md) for the boundary between the
two projects.

## Documentation

The published documentation (installation, API reference, contributing,
license) is at <https://rfmeasurement.readthedocs.io/en/latest/>.

The full design and development specification lives in [docs/](docs/index.md):

- [Vision](docs/vision.md)
- [Scope](docs/scope.md)
- [Requirements](docs/requirements.md)
- [Architecture](docs/architecture.md)
- [Domain model](docs/domain-model.md)
- [API specification](docs/api-specification.md)
- [Uncertainty](docs/uncertainty.md)
- [Measurement quality](docs/measurement-quality.md)
- [Reproducibility](docs/reproducibility.md)
- [Roadmap](docs/roadmap.md)
- [Repository organisation](docs/repository-organization.md)
- [Testing and validation](docs/testing-validation.md)
- [Architecture Decision Records](docs/adr/)

## Installation

```bash
pip install rfmeasurement
```

For development, see [CONTRIBUTING.md](CONTRIBUTING.md#getting-started) for
setting up a virtual environment and installing with the `dev` extra.

Supported Python versions: 3.10, 3.11, 3.12, 3.13.

## Development

```bash
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to propose changes,
including scientific contributions.

## Citation

If you use `rfmeasurement` in research, please cite it using the metadata
in [CITATION.cff](CITATION.cff). Every release is archived on Zenodo:
[10.5281/zenodo.22058515](https://doi.org/10.5281/zenodo.22058515) (this DOI
always resolves to the latest version).

## License

BSD 3-Clause License. See [LICENSE](LICENSE).

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
