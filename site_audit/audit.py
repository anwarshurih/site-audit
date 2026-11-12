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


def audit(url):
    page = fetch(url)
    results = [check(page) for check in ALL_CHECKS]
    return page, results, score(results)
