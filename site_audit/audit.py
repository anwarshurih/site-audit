"""Downloads a page and runs all the checks on it."""

import time
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from .checks import ALL_CHECKS

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; SiteAudit/0.1)"}


@dataclass
class Page:
    url: str          # final url after any redirects
    html: str
    soup: BeautifulSoup
    load_time: float  # seconds
    status: int


def fetch(url, timeout=15):
    """Download a page and time how long it takes."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    start = time.perf_counter()
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    load_time = time.perf_counter() - start

    soup = BeautifulSoup(response.text, "html.parser")
    return Page(response.url, response.text, soup, load_time, response.status_code)


def score(results):
    """Score out of 100, weighted by how important each check is."""
    total = sum(r.weight for r in results)
    passed = sum(r.weight for r in results if r.passed)
    return round(passed / total * 100) if total else 0


def audit(url, check_links=False):
    page = fetch(url)
    results = [check(page) for check in ALL_CHECKS]
    if check_links:
        from .links import check_links as run_link_check
        results.append(run_link_check(page))
    return page, results, score(results)
