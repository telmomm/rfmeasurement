"""Sphinx configuration for the published rfmeasurement documentation.

Most pages live under docs/sphinx/. The "Training" section
(docs/sphinx/training/) is a set of thin stub pages that each {include}
the corresponding project-specification file from docs/*.md and
docs/adr/, so those design/process documents are published in full on
Read the Docs without duplicating their content -- docs/*.md remains the
single source of truth, readable both directly on GitHub and here.
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
myst_heading_anchors = 3
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
