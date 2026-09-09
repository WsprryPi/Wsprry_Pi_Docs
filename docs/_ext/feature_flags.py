"""Remove optional content before parsing and from published page sources."""

from pathlib import Path

from sphinx.errors import ExtensionError
from sphinx.search import js_index


START = "<!-- if-wsprrypico -->"
ELSE = "<!-- else-wsprrypico -->"
END = "<!-- endif-wsprrypico -->"


def filter_pico(source, enabled):
    """Select marked blocks without inserting whitespace into Markdown lists."""
    result = []
    active = None
    seen_else = False
    for number, line in enumerate(source.splitlines(keepends=True), 1):
        marker = line.strip()
        if marker == START:
            if active is not None:
                raise ExtensionError(f"Nested Pico block at line {number}")
            active, seen_else = enabled, False
        elif marker == ELSE:
            if active is None or seen_else:
                raise ExtensionError(f"Unexpected Pico else at line {number}")
            active, seen_else = not enabled, True
        elif marker == END:
            if active is None:
                raise ExtensionError(f"Unexpected Pico end at line {number}")
            active = None
        else:
            if active is not False:
                result.append(line)
                continue
    if active is not None:
        raise ExtensionError("Unclosed Pico block")
    return "".join(result)


def filter_source(app, docname, source):
    source[0] = filter_pico(source[0], app.config.wsprrypico_docs)


def filter_published_sources(app, exception):
    """Filter copied sources and remove orphaned incremental search terms."""
    if exception is not None or app.builder.format != "html":
        return
    for path in (Path(app.outdir) / "_sources").rglob("*"):
        if path.is_file():
            source = path.read_text(encoding=app.config.source_encoding)
            if START in source:
                path.write_text(
                    filter_pico(source, app.config.wsprrypico_docs),
                    encoding=app.config.source_encoding,
                )

    # Sphinx can retain old words mapped to empty lists after reindexing pages.
    # They have no search results, but still disclose hidden terminology.
    index_path = Path(app.outdir) / "searchindex.js"
    if index_path.is_file():
        index = js_index.loads(index_path.read_text(encoding="utf-8"))
        for key in ("terms", "titleterms"):
            index[key] = {word: docs for word, docs in index[key].items() if docs != []}
        index_path.write_text(js_index.dumps(index), encoding="utf-8")


def setup(app):
    # Changing the flag invalidates the environment, including search and TOCs.
    app.add_config_value("wsprrypico_docs", False, "env", types={bool})
    app.connect("source-read", filter_source)
    app.connect("build-finished", filter_published_sources)
    return {"version": "1", "parallel_read_safe": True, "parallel_write_safe": True}
