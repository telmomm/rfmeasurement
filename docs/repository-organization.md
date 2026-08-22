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
│   ├── uncertainty.md
│   ├── measurement-quality.md
│   ├── reproducibility.md
│   ├── roadmap.md
│   ├── repository-organization.md
│   ├── testing-validation.md
│   ├── contributing.md
│   ├── governance.md
│   ├── joss-strategy.md
│   └── research-plan.md
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
└── SECURITY.md
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

A documentation system such as MkDocs or Sphinx may be introduced after
the Markdown information architecture stabilises.

The source of truth remains Markdown.

## Releases

Use semantic versioning where practical.

Every release should have:

-   changelog entry;
-   tests passing;
-   version tag;
-   release notes;
-   reproducibility information.
