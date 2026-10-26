
project = 'Connecting AI Applications with MCPs'
copyright = '2026, Kristian Rother'
author = 'Kristian Rother'
release = '1.0'
html_title = project

extensions = [
    'sphinx_design',
    'sphinx_copybutton',
    'myst_parser',
    'sphinxcontrib.cairosvgconverter',
    'sphinxcontrib.mermaid',
    ]


# render ```mermaid code blocks in Markdown files as diagrams
myst_fence_as_directive = ['mermaid']

templates_path = ['_templates']
exclude_patterns = ['README.md', 'notes.md', 'planning.md', 'models.md', 'mermaid_charts.md', 'build', '_build', 'Thumbs.db', '.DS_Store', '.venv/*']

language = 'en'

# ---- Options for HTML output ----
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_logo = "_static/academis_logo.png"
html_favicon = "_static/favicon.ico"

html_css_files = [
    "academis.css",
]

html_theme_options = {
    "source_branch": "main",
    "source_repository": "https://github.com/krother/mcp_course",
    "source_directory": "",
}
