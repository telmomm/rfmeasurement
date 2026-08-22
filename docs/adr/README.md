# Architecture Decision Records

This directory records significant architectural and scientific-design
decisions, per the process defined in [governance.md](../governance.md).

Use [template.md](template.md) as the starting point for a new ADR.
Number ADRs sequentially (`0001-...`, `0002-...`) and never renumber or
delete an existing one; a superseded decision gets a new ADR that says
so.

| ADR | Title | Status |
| --- | --- | --- |
| [0001](0001-build-on-scikit-rf.md) | Build on top of scikit-rf rather than replacing it | accepted |
| [0002](0002-src-layout-and-module-boundaries.md) | Use a `src/` layout with domain-first module boundaries | accepted |
| [0003](0003-bsd-3-clause-license.md) | License the project under BSD-3-Clause | accepted |
| [0004](0004-supported-python-versions.md) | Support Python 3.10-3.13 | accepted |
