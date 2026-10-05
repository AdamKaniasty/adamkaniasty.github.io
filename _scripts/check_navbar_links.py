"""Check that every rendered navbar name links to the site homepage."""

import sys
from html.parser import HTMLParser
from pathlib import Path


class NavbarLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.home_links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "navbar-brand" in attrs.get("class", "").split():
            self.home_links.append(attrs.get("href"))


site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
expected = sys.argv[2] if len(sys.argv) > 2 else "/"
checked = 0
failures = []
for page in site.rglob("*.html"):
    parser = NavbarLinks()
    parser.feed(page.read_text(encoding="utf-8"))
    for href in parser.home_links:
        checked += 1
        if href != expected:
            failures.append(f"{page}: expected {expected!r}, got {href!r}")

if not checked:
    raise SystemExit("No navbar homepage links found; build the site first.")
if failures:
    raise SystemExit("\n".join(failures))
print(f"Verified {checked} navbar homepage links.")
