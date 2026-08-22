# Repository Organisation

## Proposed top-level structure

``` text
rfmeasurement/
├── src/
│   └── rfmeasurement/
│       ├── domain/
│       ├── io/
│       ├── validation/
│       ├── uncertainty/
│       ├── provenance/
│       ├── analysis/
│       ├── reporting/
│       └── integrations/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── scientific/
│   ├── regression/
│   └── data/
│
├── docs/
│   ├── index.md
│   ├── vision.md
│   ├── scope.md
│   ├── requirements.md
│   ├── architecture.md
│   ├── domain-model.md
│   ├── api-specification.md
│   ├── uncertainty.md
│   ├── measurement-quality.md
│   ├── reproducibility.md
│   ├── roadmap.md
│   ├── repository-organization.md
│   ├── testing-validation.md
│   ├── contributing.md
│   ├── governance.md
│   ├── joss-strategy.md
│   ├── research-plan.md
│   ├── adr/
│   └── sphinx/            <- published user documentation (see below)
│
├── examples/
├── benchmarks/
├── paper/
│   ├── paper.md
│   └── paper.bib
│
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── dependabot.yml
│
├── pyproject.toml
├── README.md
├── LICENSE
├── CITATION.cff
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── .readthedocs.yaml
```

## Packaging

Use a modern `pyproject.toml`-based package.

The `src/` layout is preferred to avoid accidental imports from the
repository root.

## Tests

Tests should be separated by purpose:

### Unit

Small deterministic tests for individual functions/classes.

### Integration

Tests across multiple modules.

### Scientific

Tests against analytical or independently verified scientific
references.

### Regression

Tests protecting known bugs and published examples.

### Data

Small test datasets only. Large datasets should be archived externally
and downloaded explicitly for benchmark workflows.

## Examples

Examples must be executable.

A good example should answer a real scientific question rather than
merely demonstrate syntax.

Examples should be version-controlled and tested where practical.

## Documentation build

The project maintains two separate bodies of documentation:

-   `docs/*.md` and `docs/adr/` --- the project design and process
    specification (vision, scope, requirements, roadmap, governance,
    ADRs). This is maintainer/contributor-facing and is read directly on
    GitHub; it is not built into a separate site.
-   `docs/sphinx/` --- the published, user-facing documentation
    (installation, API reference generated from docstrings via
    `sphinx.ext.autodoc`, and eventually tutorials/examples). Built with
    [Sphinx](https://www.sphinx-doc.org/) and
    [MyST](https://myst-parser.readthedocs.io/) so that Markdown remains
    the source format, and published on
    [Read the Docs](https://readthedocs.org/) once the repository is
    connected there, matching the approach used by `scikit-rf`.

Build locally with:

``` bash
python -m pip install -e ".[docs]"
sphinx-build -b html docs/sphinx docs/sphinx/_build/html
```

CI builds the Sphinx documentation with warnings treated as errors, so
that broken cross-references or docstring issues are caught before merge.

## Releases

Use semantic versioning where practical.

Every release should have:

-   changelog entry;
-   tests passing;
-   version tag;
-   release notes;
-   reproducibility information.
