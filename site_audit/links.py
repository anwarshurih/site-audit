"""Broken link checker.

This one is slower than the other checks because it has to visit every link,
so it only runs when you pass --links.
"""

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urldefrag

import requests

from .checks import Result

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; SiteAudit/0.1)"}
MAX_LINKS = 50  # don't hammer big sites


def find_links(page):
    """All http(s) links on the page, made absolute, without duplicates."""
    links = []
    for a in page.soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        url, _ = urldefrag(urljoin(page.url, href))  # drop #section parts
        if url.startswith(("http://", "https://")) and url not in links:
            links.append(url)
    return links[:MAX_LINKS]


def is_broken(url, timeout=10):
    """True if the link gives an error. Some sites block HEAD, so retry with GET."""
    try:
        response = requests.head(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if response.status_code in (403, 405) or response.status_code >= 500:
            response = requests.get(url, headers=HEADERS, timeout=timeout, stream=True)
        return response.status_code >= 400
    except requests.RequestException:
        return True


def check_links(page, workers=8):
    links = find_links(page)
    if not links:
        return Result("Broken links", True, "No links to check")

    # check several links at the same time so it doesn't take ages
    with ThreadPoolExecutor(max_workers=workers) as pool:
        broken = [url for url, bad in zip(links, pool.map(is_broken, links)) if bad]

    if broken:
        shown = ", ".join(broken[:3]) + (" ..." if len(broken) > 3 else "")
        return Result("Broken links", False, f"{len(broken)} of {len(links)} links are broken: {shown}", weight=2)
    return Result("Broken links", True, f"All {len(links)} links work", weight=2)
