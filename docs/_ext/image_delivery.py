"""Add initial-HTML image loading and layout hints to documentation pages."""

from __future__ import annotations

from urllib.parse import urlparse

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.images import get_image_size
from sphinx.writers.html5 import HTML5Translator


class ImageDeliveryHTMLTranslator(HTML5Translator):
    """Emit asynchronous decoding hints for rendered raster images."""

    def visit_image(self, node: nodes.image) -> None:
        body_start = len(self.body)
        super().visit_image(node)

        for index in range(body_start, len(self.body)):
            if "<img " in self.body[index]:
                loading = (
                    'loading="eager" ' if node.get("loading") == "eager" else ""
                )
                self.body[index] = self.body[index].replace(
                    "<img ", f'<img decoding="async" {loading}', 1
                )
                break


def configure_image_delivery(
    app: Sphinx, doctree: nodes.document, docname: str
) -> None:
    """Keep the first local content image eager and defer later images.

    The first content image may be visible in the initial viewport. Keeping it
    eager avoids delaying explanatory content without requiring page-specific
    exceptions. All later content images are safe progressive-disclosure
    candidates. The navigation logo is emitted by the theme template and is
    intentionally outside this transform.
    """

    first_local_image = True

    for image in doctree.findall(nodes.image):
        uri = image.get("uri", "")
        parsed = urlparse(uri)
        if parsed.scheme or uri.startswith("data:"):
            continue

        image["loading"] = "eager" if first_local_image else "lazy"
        first_local_image = False

        if "width" in image and "height" in image:
            continue

        size = get_image_size(app.srcdir / uri)
        if size is None:
            continue

        image["width"] = str(size[0])
        image["height"] = str(size[1])


def setup(app: Sphinx) -> dict[str, bool]:
    app.connect("doctree-resolved", configure_image_delivery)
    app.set_translator("html", ImageDeliveryHTMLTranslator, override=True)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
