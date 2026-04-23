---
name: rtd-theme-customizer
description: Use only for Sphinx documentation using sphinx-rtd-theme or Read the Docs theme files, including docs/conf.py, docs/_static CSS, docs/_templates, RTD sidebar/search/layout issues, and Sphinx HTML theme polish. Do not use for generic website CSS, application UI CSS, PHP UI files, JavaScript app layout, or non-Sphinx styling.
---

# Skill: rtd-theme-customizer

Use this skill when working on WsprryPi documentation, Sphinx configuration, Read the Docs styling, or documentation describing WsprryPi components and behavior.

## Project context

WsprryPi documentation may cover:

- Raspberry Pi GPIO and Si5351 transmission backends
- WSPR, QRSS, FSKCW, and DFCW operation
- Daemon, CLI, and web UI behavior
- Operation and setup workflows
- CLI and daemon behavior
- Hardware setup, filters, bands, and transmitter configuration

The UI has an operation-focused landing page and a setup/configuration view. Do not blur these concepts in documentation.

Use these names consistently:

- WsprryPi
- WSPR
- QRSS
- FSKCW
- DFCW
- Si5351
- Raspberry Pi
- Read the Docs
- Sphinx

## Goals

Improve documentation readability, maintainability, and visual polish without breaking Sphinx, Read the Docs behavior, sidebar navigation, search, mobile layout, or generated documentation output.

Prefer small, focused, reversible changes.

## Preferred files

Prefer editing these files when present:

- docs/conf.py
- docs/index.rst
- docs/**/*.rst
- docs/_static/css/custom.css
- docs/_static/custom.css
- docs/_templates/layout.html
- docs/requirements.txt
- docs/Makefile
- docs/make.bat

If custom CSS is needed and no custom CSS file exists, create:

docs/_static/css/custom.css

Then ensure docs/conf.py contains:

html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

If either setting already exists, update it instead of duplicating it.

## Hard rules

- Do not edit generated files under _build.
- Do not edit third-party theme package files.
- Do not disable search.
- Do not remove or replace the RTD sidebar.
- Do not break mobile navigation.
- Do not use JavaScript unless CSS cannot solve the issue.
- Do not use !important unless RTD specificity requires it.
- Do not rewrite technical content unless requested.
- Do not rename WsprryPi project terms.
- Do not introduce dark-mode behavior unless requested.
- Do not make broad generated-documentation changes without explaining why.

## Markdown and documentation style

Follow the project documentation style:

- Surround headings with exactly one blank line.
- Surround lists with one blank line before and after.
- Surround fenced code blocks with one blank line before and after.
- Always specify a language for fenced code blocks.
- Do not use emphasis as a heading.
- Avoid multiple consecutive blank lines.
- Use - for unordered list bullets.
- Keep spaces around Markdown table pipes.
- Prefer clear spelling over unexplained abbreviations.
- Expand uncommon abbreviations at first use.

## RTD visual priorities

Improve these in order:

- Main content readability
- Heading spacing and hierarchy
- Code block legibility
- Inline code contrast
- Tables on narrow screens
- Admonition spacing
- Sidebar usability
- API/reference page readability
- Print/export behavior

## CSS guidance

Prefer scoped RTD selectors:

.wy-nav-content
.rst-content
.rst-content .section
.rst-content table.docutils
.rst-content div[class^="highlight"]

Prefer CSS variables where useful:

:root {
    --wsprrypi-docs-content-width: 960px;
    --wsprrypi-docs-line-height: 1.65;
}

Avoid broad global selectors unless necessary.

Use comments sparingly, but make them useful.

## WsprryPi-specific content guidance

Preserve the distinction between:

- Operation page: normal transmitter operation and status
- Setup page: configuration and system setup
- CLI mode: command-line operation
- Daemon mode: long-running service behavior
- GPIO backend: Raspberry Pi direct clocking path
- Si5351 backend: external synthesizer path

When documenting bands, configuration, or transmitter behavior, avoid implying that all hardware paths behave identically unless the code proves it.

## Validation

After changes, run the most appropriate available docs command:

make -j$(nproc) html

or:

sphinx-build -b html docs docs/_build/html

If the repository has a documented docs build command, use that instead.

Also check:

- No new Sphinx warnings were introduced.
- The generated HTML exists.
- Search assets are generated.
- The sidebar still renders.
- Tables remain usable on narrow screens.
- Code blocks remain readable.
- No _build files are committed unless explicitly requested.

## Reporting

When finished, report:

- Files changed
- Why each file changed
- Build command used
- Any warnings or failures
- Any visual checks actually performed
- Any remaining risks

Do not claim browser or screenshot verification unless it was actually done.
