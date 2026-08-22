# JOSS Strategy

## Why JOSS is a design constraint

The project is intended as research software, not simply as a Python
utility.

JOSS currently expects open-source research software to have an obvious
research application, meaningful contribution, public development
history, good documentation, tests, community pathways and evidence of
research impact.

The project should therefore be developed with those requirements in
mind from day one.

## Core JOSS requirements to design for

### Open source

Use an OSI-approved license and include the full license text in
`LICENSE`.

### Public development

The repository should be public from the beginning.

Do not develop the complete project privately and publish a repository
shortly before submission.

### Sustained history

JOSS currently expects more than six months of public development
history before submission.

The development should show iteration rather than a single large code
dump.

### Research use

The project needs evidence that researchers actually use it.

Possible evidence:

-   research papers;
-   preprints;
-   laboratory workflows;
-   external users;
-   integrations;
-   reproducible benchmark studies.

### Documentation

The project should have:

-   installation instructions;
-   statement of need;
-   tutorials;
-   API documentation;
-   scientific background;
-   examples;
-   contribution guidelines.

### Tests

Scientific functionality should be covered by automated tests and
independently validated reference cases.

### Community

Provide:

-   issue tracker;
-   contribution guide;
-   code of conduct;
-   support expectations;
-   public discussions where appropriate.

## JOSS paper strategy

The future `paper/paper.md` should be short and focused.

Expected structure:

1.  Summary
2.  Statement of Need
3.  State of the Field
4.  Software Design
5.  Research Impact Statement
6.  AI Usage Disclosure
7.  References

The paper should not become the software manual. API details belong in
the documentation.

## Research impact strategy

Do not rely on statements such as:

> "This software will be useful to researchers."

Instead, generate evidence:

-   use the library in our own research;
-   publish reproducible examples;
-   release benchmark datasets;
-   invite external users;
-   collect issues and feedback;
-   document integrations;
-   cite the software in research outputs.

## JOSS readiness gate

Do not submit until all of these are true:

-   [ ] public repository older than six months;
-   [ ] sustained development history;
-   [ ] tagged releases;
-   [ ] documented research use;
-   [ ] complete core functionality;
-   [ ] automated tests;
-   [ ] CI;
-   [ ] API documentation;
-   [ ] tutorials;
-   [ ] contribution process;
-   [ ] OSI-approved license;
-   [ ] citation metadata;
-   [x] archived release with DOI;
-   [ ] JOSS paper draft;
-   [ ] AI usage disclosure.

JOSS requirements can change. Before submission, the project must check
the current official JOSS documentation rather than relying on this
document.
