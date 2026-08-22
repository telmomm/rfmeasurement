"""Sphinx configuration for the published rfmeasurement documentation.

This project is self-contained under docs/sphinx/: it does not build the
project-specification files in docs/*.md (see docs/index.md), which are
maintainer/contributor-facing rather than end-user API documentation.
"""

from __future__ import annotations

import rfmeasurement

project = "rfmeasurement"
copyright = "2026, rfmeasurement contributors"
author = "rfmeasurement contributors"
version = rfmeasurement.__version__
release = version

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

myst_enable_extensions = ["colon_fence"]
source_suffix = {".md": "markdown"}

autodoc_typehints = "description"
autodoc_member_order = "bysource"
napoleon_numpy_docstring = True
napoleon_google_docstring = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "skrf": ("https://scikit-rf.readthedocs.io/en/latest/", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
