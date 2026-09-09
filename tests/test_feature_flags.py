"""Run with: python -m unittest discover -s tests."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


EXTENSIONS = Path(__file__).resolve().parents[1] / "docs" / "_ext"
sys.path.insert(0, str(EXTENSIONS))

from feature_flags import filter_pico
from sphinx.errors import ExtensionError


class PicoDocumentationTests(unittest.TestCase):
    def test_inline_list_selection_preserves_markdown(self):
        source = (
            "- GPIO\n<!-- if-wsprrypico -->\n- Pico\n"
            "<!-- else-wsprrypico -->\n- Si5351\n<!-- endif-wsprrypico -->\n"
        )
        self.assertEqual(filter_pico(source, False), "- GPIO\n- Si5351\n")
        self.assertEqual(filter_pico(source, True), "- GPIO\n- Pico\n")

    def test_malformed_markers_fail_the_build(self):
        for source in (
            "<!-- if-wsprrypico -->\n",
            "<!-- else-wsprrypico -->\n",
            "<!-- endif-wsprrypico -->\n",
            "<!-- if-wsprrypico -->\n<!-- if-wsprrypico -->\n",
            "<!-- if-wsprrypico -->\n<!-- else-wsprrypico -->\n"
            "<!-- else-wsprrypico -->\n",
        ):
            for enabled in (False, True):
                with self.subTest(source=source, enabled=enabled):
                    with self.assertRaises(ExtensionError):
                        filter_pico(source, enabled)

    def test_incremental_build_updates_pages_search_and_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / "source", root / "html"
            source.mkdir()
            (source / "conf.py").write_text(
                f"import sys\nsys.path.insert(0, {str(EXTENSIONS)!r})\n"
                "extensions = ['myst_parser', 'feature_flags']\n"
                "myst_heading_anchors = 3\n",
                encoding="utf-8",
            )
            (source / "index.md").write_text(
                "# Transmitters\n\nGPIO and Si5351 remain visible.\n\n"
                "<!-- if-wsprrypico -->\n"
                "See [Pico instructions](#picofeaturetoken).\n\n"
                "## Picofeaturetoken\n\nWsprryPico development instructions.\n"
                "<!-- endif-wsprrypico -->\n",
                encoding="utf-8",
            )
            # Reuse the output and environment: flag changes must invalidate both.
            for override, enabled in ((None, False), ("1", True), ("0", False)):
                command = [sys.executable, "-m", "sphinx", "-b", "html", "-W", "-q"]
                if override is not None:
                    command += ["-D", f"wsprrypico_docs={override}"]
                result = subprocess.run(
                    command + [str(source), str(output)],
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                for filename in ("index.html", "searchindex.js", "_sources/index.md.txt"):
                    content = (output / filename).read_text(encoding="utf-8")
                    with self.subTest(enabled=enabled, filename=filename):
                        self.assertEqual("picofeaturetoken" in content.lower(), enabled)
                        self.assertNotIn("<!-- if-wsprrypico -->", content)
                self.assertIn("GPIO and Si5351", (output / "index.html").read_text())


if __name__ == "__main__":
    unittest.main()
