"""Check the built portfolio as a crawler that never executes JavaScript.

Usage: python3 _scripts/check_seo.py [_site]
Only the standard library is required, including in deployment CI.
"""

import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.robotparser import RobotFileParser


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.h1 = ""
        self.text = ""
        self.meta = {}
        self.canonicals = []
        self.links = []
        self.assets = []
        self.images = []
        self.ids = set()
        self.schema = []
        self.active = []
        self.json_buffer = None
        self.nested_links = False
        self.heading_levels = []
        self.main_count = 0
        self.refresh = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "main":
            self.main_count += 1
        if tag == "meta":
            self.meta[a.get("name", a.get("property"))] = a.get("content", "")
            self.refresh |= a.get("http-equiv", "").lower() == "refresh"
        if tag == "link" and a.get("rel") == "canonical":
            self.canonicals.append(a.get("href"))
        if tag == "a":
            self.nested_links |= "a" in self.active
            self.links.append(a.get("href", ""))
        if tag in {"script", "img", "source"} and a.get("src"):
            self.assets.append(a["src"])
        if tag == "link" and a.get("rel") == "stylesheet":
            self.assets.append(a.get("href", ""))
        if tag == "source":
            self.assets += [entry.strip().split()[0] for entry in a.get("srcset", "").split(",") if entry.strip()]
        if tag == "img":
            self.images.append(a)
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_levels.append(int(tag[1]))
        if tag == "script" and a.get("type") == "application/ld+json":
            self.json_buffer = ""
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.active.append(tag)

    def handle_endtag(self, tag):
        if tag == "script" and self.json_buffer is not None:
            self.schema.append(json.loads(self.json_buffer))
            self.json_buffer = None
        if tag in self.active:
            index = len(self.active) - 1 - self.active[::-1].index(tag)
            del self.active[index:]

    def handle_data(self, text):
        if self.json_buffer is not None:
            self.json_buffer += text
        if "title" in self.active:
            self.title += text
        if "h1" in self.active:
            self.h1 += text
        if "main" in self.active and "script" not in self.active and "style" not in self.active:
            self.text += text + " "


root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
origin = "https://adamkaniasty.com"
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


def file_for(url):
    path = unquote(urlsplit(url).path).lstrip("/")
    target = root / path
    if target.is_dir() or path.endswith("/") or not path:
        target = target / "index.html"
    return target


pages = {}
for file in sorted(root.rglob("*.html")):
    if "assets" in file.relative_to(root).parts:
        continue
    rel = file.relative_to(root).as_posix()
    route = "/" + rel.removesuffix("index.html")
    try:
        pages[route] = Page(file.read_text(encoding="utf-8"))
    except (ValueError, json.JSONDecodeError) as exc:
        errors.append(f"{route}: invalid JSON-LD: {exc}")

check(bool(pages), "No HTML found; build the site first.")
indexed = {url: page for url, page in pages.items() if "noindex" not in page.meta.get("robots", "")}
for field, values in {
    "title": [page.title.strip() for page in indexed.values()],
    "description": [page.meta.get("description") for page in indexed.values()],
}.items():
    for value, count in Counter(values).items():
        check(bool(value) and count == 1, f"Missing or duplicate {field}: {value!r} ({count})")

for route, page in pages.items():
    check(page.heading_levels.count(1) == 1, f"{route}: expected one H1")
    check(page.main_count == 1, f"{route}: expected one main landmark")
    check(bool(page.h1.strip()) and len(page.text.strip()) > 60, f"{route}: empty crawler content")
    check(not page.nested_links, f"{route}: nested anchor elements")
    for previous, level in zip(page.heading_levels, page.heading_levels[1:]):
        check(level <= previous + 1, f"{route}: heading skips H{previous} to H{level}")
    check(len(page.canonicals) == 1, f"{route}: expected one canonical")
    if route in indexed:
        check(page.canonicals == [origin + route], f"{route}: canonical mismatch {page.canonicals}")
    check(page.meta.get("og:url") == page.canonicals[0], f"{route}: OG URL mismatch")
    for tag in ["og:title", "og:description", "og:image", "twitter:title", "twitter:description", "twitter:image"]:
        check(bool(page.meta.get(tag)), f"{route}: missing {tag}")
    check(page.meta.get("og:title") == page.title.strip(), f"{route}: social title mismatch")
    check(page.meta.get("og:description") == page.meta.get("description"), f"{route}: social description mismatch")
    check(file_for(page.meta.get("og:image", "")).is_file(), f"{route}: preview image missing")
    check(bool(page.schema), f"{route}: missing JSON-LD")
    for graph in page.schema:
        check(graph.get("@context") == "https://schema.org", f"{route}: wrong schema context")
        nodes = graph.get("@graph", [])
        people = [node for node in nodes if node.get("@type") == "Person"]
        check(len(people) == 1 and people[0].get("@id") == origin + "/#person", f"{route}: inconsistent Person")
        if people:
            check(people[0].get("sameAs") == ["https://www.linkedin.com/in/adam-kaniasty/", "https://github.com/AdamKaniasty"], f"{route}: incorrect identity profiles")
        if route != "/" and route in indexed:
            crumbs = [node for node in nodes if node.get("@type") == "BreadcrumbList"]
            check(len(crumbs) == 1, f"{route}: missing breadcrumb schema")
    for image in page.images:
        check("alt" in image, f"{route}: missing image alt")
        check(image.get("alt") != "personal/me.jpg", f"{route}: filename portrait alt")
    for href in page.links + page.assets:
        if href.startswith(("mailto:", "tel:", "data:", "javascript:")):
            continue
        absolute = urljoin(origin + route, href)
        parsed = urlsplit(absolute)
        if parsed.netloc != "adamkaniasty.com":
            continue
        target = file_for(absolute)
        check(bool(href) and target.is_file(), f"{route}: broken local target {href!r}")
        if parsed.fragment and target.suffix == ".html" and target.is_file():
            dest = Page(target.read_text(encoding="utf-8"))
            check(unquote(parsed.fragment) in dest.ids, f"{route}: missing fragment {href}")

required = {
    "/": ["Adam Kaniasty", "Google", "Agent Development Lifecycle", "Python", "Java"],
    "/cv/": ["Google", "Box", "Warsaw University of Technology", "Mi-Crow"],
    "/projects/": ["Mi-Crow", "xLungs", "APPI", "Kubernetes", "RL Doom"],
    "/publications/": ["Radiomic", "2025", "10.62036/ISD.2025.112"],
    "/talks/": ["RAG", "embeddings", "BEST Hacking League"],
}
for slug, terms in {
    "mi-crow": ["autoencoder", "Hubert Kowalski", "PyTorch"],
    "xlungs": ["RabbitMQ", "Java", "radiologists"],
    "appi-marketplace": ["Pinecone", "FastAPI", "Azure"],
    "appi-synapse": ["MongoDB", "React", "LangChain"],
    "kubernetes-autoscaling": ["DDQN", "Jenkins", "Helm"],
    "rl-doom": ["PPO", "A2C", "TensorBoard"],
    "cansat-terrain": ["ResNet18", "224", "Trailblazer"],
}.items():
    required[f"/projects/{slug}/"] = terms
for route, terms in required.items():
    check(route in indexed, f"{route}: required indexable page missing")
    if route in pages:
        for term in terms:
            check(term.lower() in pages[route].text.lower(), f"{route}: fact not in static HTML: {term}")

ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [element.text for element in ET.parse(root / "sitemap.xml").findall("s:url/s:loc", ns)]
check(len(urls) == len(set(urls)), "Duplicate sitemap URLs")
for route in indexed:
    check(origin + route in urls, f"{route}: missing from sitemap")
for url in urls:
    check(urlsplit(url).netloc == "adamkaniasty.com" and url.startswith("https://"), f"Noncanonical sitemap URL: {url}")
    check(file_for(url).is_file(), f"Sitemap target missing: {url}")
    check(urlsplit(url).path in indexed, f"Sitemap includes excluded/duplicate content: {url}")
robot_text = (root / "robots.txt").read_text()
robot = RobotFileParser()
robot.parse(robot_text.splitlines())
check("Sitemap: https://adamkaniasty.com/sitemap.xml" in robot_text, "Wrong robots sitemap")
for bot in ["Googlebot", "Bingbot", "OAI-SearchBot"]:
    for route in required:
        check(robot.can_fetch(bot, origin + route), f"{bot} blocked on {route}")
for route in indexed:
    if route != "/":
        inbound = any(urlsplit(urljoin(origin + parent, href)).path == route for parent, p in pages.items() if parent != route for href in p.links)
        check(inbound, f"{route}: orphaned page")
check("/404.html" in pages and "noindex" in pages["/404.html"].meta.get("robots", "") and not pages["/404.html"].refresh, "404 must be noindex without redirect")
check(not (root / "docs").exists(), "Internal audit docs leaked into build")
check(not any("announcement_" in url for url in urls), "Template news leaked into sitemap")
if errors:
    raise SystemExit("\n".join(dict.fromkeys(errors)))
print(f"Verified {len(pages)} HTML pages, {len(indexed)} indexable URLs, metadata, JSON-LD, links, static facts, sitemap and crawler permissions.")
