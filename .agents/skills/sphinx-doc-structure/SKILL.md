---
name: sphinx-doc-structure
description: Use only for WsprryPi Sphinx documentation content structure, reStructuredText pages, docs/index.rst, docs/**/*.rst, toctrees, section hierarchy, cross references, tables, examples, and Sphinx warning cleanup. Do not use for CSS styling, RTD theme appearance, PHP UI files, JavaScript UI files, or generic Markdown outside the docs.
---

# Skill: sphinx-doc-structure

Use this skill when working on WsprryPi Sphinx documentation content, organization, page hierarchy, cross references, tables, examples, or technical explanations.

Do not use this skill for visual theme styling. Use the RTD theme skill for CSS, theme overrides, layout polish, or Read the Docs appearance work.

## Project context

WsprryPi documentation may describe:

- Raspberry Pi GPIO transmission backend
- Si5351 transmission backend
- WSPR operation
- QRSS operation
- FSKCW operation
- DFCW operation
- CLI usage
- Daemon or service behavior
- Band configuration
- INI configuration
- Transmission planning
- Filters and hardware setup
- Build and installation steps

Use these names consistently:

- WsprryPi
- WSPR
- QRSS
- FSKCW
- DFCW
- Si5351
- Raspberry Pi
- GPIO
- INI
- Sphinx
- Read the Docs

## Goals

Improve documentation clarity, structure, and maintainability.

Prioritize:

- Accurate technical organization
- Clear reader path from install to operation
- Good page titles and section hierarchy
- Helpful cross references
- Maintainable tables
- Clear examples
- Consistent terminology
- Minimal duplicated content

Prefer small, focused, reversible changes.

## Preferred files

Prefer editing these files when present:

- docs/index.rst
- docs/**/*.rst
- docs/conf.py
- docs/requirements.txt
- README.md

Do not edit generated files under:

```text
docs/_build/
_build/
```

## Hard rules

- Do not modify RTD theme styling or CSS unless explicitly requested.
- Do not edit generated files.
- Do not invent unsupported features.
- Do not imply GPIO and Si5351 backends behave identically unless documented code proves it.
- Do not rewrite large sections when a smaller structural fix is enough.
- Do not remove warnings, cautions, or hardware safety notes.
- Do not remove command examples unless they are wrong or obsolete.
- Do not rename project-specific terms without clear evidence.
- Do not change build commands unless the existing command is broken.
- Do not claim hardware behavior that is not documented or verified.

## Documentation style

Follow the project documentation style:

- Use `-` for unordered list bullets.
- Surround headings with exactly one blank line.
- Surround lists with one blank line before and after.
- Surround fenced code blocks with one blank line before and after.
- Always specify a language for fenced code blocks.
- Do not use emphasis as a heading.
- Avoid multiple consecutive blank lines.
- Keep spaces around Markdown table pipes.
- Prefer clear spelling over unexplained abbreviations.
- Expand uncommon abbreviations at first use.

For reStructuredText files:

- Use consistent heading levels within each file.
- Prefer explicit section labels for pages that are cross-referenced.
- Prefer `:ref:` links for internal cross references.
- Prefer `.. code-block:: bash` for shell commands.
- Prefer `.. code-block:: ini` for configuration snippets.
- Prefer list tables or simple tables that remain readable in source form.
- Keep tables narrow enough to maintain.

## Content organization guidance

Prefer a reader path like this when the existing docs allow it:

- Overview
- Hardware requirements
- Installation
- Configuration
- Basic operation
- Backend-specific behavior
- Band and filter configuration
- Advanced operation
- Troubleshooting
- Reference

Preserve the distinction between:

- Installation: getting WsprryPi installed and built
- Configuration: setting persistent options
- Operation: running or transmitting
- CLI mode: command-line operation
- Daemon mode: long-running service behavior
- GPIO backend: Raspberry Pi direct clocking path
- Si5351 backend: external synthesizer path
- Hardware notes: wiring, filters, output stages, and safety

## Cross-reference guidance

When adding or editing internal links:

- Prefer stable labels over bare page paths.
- Add labels above major sections that are likely to be referenced.
- Use descriptive link text.
- Avoid duplicate labels.
- Do not add excessive cross references that clutter the text.

Example pattern:

```rst
.. _configuration-overview:

Configuration
=============
```

Then reference it with:

```rst
See :ref:`configuration-overview`.
```

## Tables

Use tables for:

- Band defaults
- Configuration keys
- Backend capability comparisons
- CLI options
- Troubleshooting symptoms and fixes

Tables should have:

- Clear column names
- Short cell contents
- Consistent units
- Notes below the table when details are too long

Do not pack long paragraphs into table cells.

## Examples

Examples should be:

- Minimal
- Copyable
- Accurate for the documented mode
- Clearly labeled as examples

Shell examples should use:

```rst
.. code-block:: bash
```

Configuration examples should use:

```rst
.. code-block:: ini
```

Avoid examples that require undocumented assumptions.

## Technical accuracy checks

When editing WsprryPi documentation, check for these risks:

- Confusing WSPR, QRSS, FSKCW, and DFCW behavior
- Treating GPIO and Si5351 backends as identical
- Implying all bands are valid for all hardware paths
- Omitting low-pass filter or output filtering context
- Mixing daemon behavior with one-shot CLI behavior
- Mixing persistent INI configuration with runtime-only options
- Referring to removed options as current
- Referring to generated files as source files

## Validation

After changes, run the most appropriate available docs command:

```bash
make -j$(nproc) html
```

or:

```bash
sphinx-build -b html docs docs/_build/html
```

If the repository has a documented docs build command, use that instead.

Also check:

- No new Sphinx warnings were introduced.
- Internal references resolve.
- The generated HTML exists.
- The table of contents still makes sense.
- No generated files were changed unless explicitly requested.

## Reporting

When finished, report:

- Files changed
- Structural changes made
- Technical assumptions preserved
- Build command used
- Any warnings or failures
- Any unresolved documentation gaps
- Suggested follow-up work, if any

Do not claim browser, hardware, or on-air verification unless it was actually performed.
