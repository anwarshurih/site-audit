import http.server
import threading

import pytest
from bs4 import BeautifulSoup

from site_audit.audit import Page
from site_audit.links import check_links, find_links


def make_page(html, url="https://example.com/shop/"):
    return Page(url, html, BeautifulSoup(html, "html.parser"), 0.1, 200)


def test_find_links_makes_absolute_and_skips_junk():
    html = """
    <a href="/about">About</a>
    <a href="contact">Contact</a>
    <a href="https://other.com/x#top">Other</a>
    <a href="https://other.com/x">Dupe</a>
    <a href="mailto:a@b.com">Email</a>
    <a href="#menu">Menu</a>
    """
    assert find_links(make_page(html)) == [
        "https://example.com/about",
        "https://example.com/shop/contact",
        "https://other.com/x",
    ]


@pytest.fixture
def local_site(monkeypatch):
    """A tiny local web server where /ok works and everything else is a 404."""
    monkeypatch.setenv("NO_PROXY", "127.0.0.1")  # make sure requests goes straight to it
    class Handler(http.server.BaseHTTPRequestHandler):
        def _reply(self):
            self.send_response(200 if self.path == "/ok" else 404)
            self.end_headers()

        do_GET = do_HEAD = _reply

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


def test_check_links_finds_broken(local_site):
    page = make_page('<a href="/ok">a</a><a href="/missing">b</a>', url=local_site + "/")
    result = check_links(page)
    assert not result.passed
    assert "1 of 2" in result.message


def test_check_links_all_ok(local_site):
    page = make_page('<a href="/ok">a</a>', url=local_site + "/")
    assert check_links(page).passed
