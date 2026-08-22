# Security Policy

`rfmeasurement` is a scientific analysis library. It does not itself
open network connections or execute untrusted code, but it does parse
measurement files (e.g. Touchstone) that may come from external sources.

## Reporting a vulnerability

If you discover a security issue (e.g. a crafted input file that causes
unsafe behavior), please report it privately using GitHub's
["Report a vulnerability"](https://github.com/telmomm/rfmeasurement/security/advisories/new)
feature rather than opening a public issue.

Please include:

- a description of the issue and its potential impact;
- steps or a minimal example to reproduce it;
- the affected version.

## Supported versions

Security fixes are provided for the latest released version until the
project reaches a stable 1.0 API, at which point a supported-versions
table will be published here.
