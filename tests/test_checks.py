from bs4 import BeautifulSoup

from site_audit.audit import Page, score
from site_audit import checks


def make_page(html, url="https://example.com", load_time=0.5):
    return Page(url, html, BeautifulSoup(html, "html.parser"), load_time, 200)


GOOD = """<html lang="en"><head><title>Joe's Barbers | Ealing</title>
<link rel="icon" href="/favicon.ico">
<meta property="og:title" content="Joe's Barbers">
<meta property="og:description" content="Walk-in barbers">
<meta property="og:image" content="https://example.com/shop.jpg">
<meta name="description" content="Walk-in barbers in Ealing.">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head><body><h1>Joe's Barbers</h1><img src="a.jpg" alt="shop"></body></html>"""

BAD = "<html><head></head><body><img src='a.jpg'><h1>a</h1><h1>b</h1></body></html>"


def test_good_page_passes_everything():
    page = make_page(GOOD)
    results = [c(page) for c in checks.ALL_CHECKS]
    assert all(r.passed for r in results)
    assert score(results) == 100


def test_bad_page_fails():
    page = make_page(BAD, url="http://example.com", load_time=3)
    assert not checks.check_https(page).passed
    assert not checks.check_title(page).passed
    assert not checks.check_mobile(page).passed
    assert not checks.check_h1(page).passed
    assert not checks.check_image_alt(page).passed
    assert not checks.check_speed(page).passed


def test_long_title():
    page = make_page("<title>" + "x" * 80 + "</title>")
    assert not checks.check_title(page).passed


def test_missing_extras():
    page = make_page("<html><head><title>x</title></head><body></body></html>")
    assert not checks.check_favicon(page).passed
    assert not checks.check_language(page).passed
    result = checks.check_social_preview(page)
    assert not result.passed
    assert "og:image" in result.message


def test_apple_touch_icon_counts_as_favicon():
    page = make_page('<link rel="apple-touch-icon" href="/icon.png">')
    assert checks.check_favicon(page).passed
