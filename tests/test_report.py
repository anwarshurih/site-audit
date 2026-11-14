from site_audit.checks import Result
from site_audit.report import build_report


def test_report_shows_score_and_fixes():
    results = [
        Result("HTTPS", True, "Site uses HTTPS", 3),
        Result("Mobile friendly", False, "No viewport tag", 3),
    ]
    page = build_report("https://example.com", results, 50)
    assert "50/100" in page
    assert "Needs fixing" in page
    assert "How to fix" in page
    assert "1 thing to improve" in page


def test_report_escapes_html():
    results = [Result("Page title", True, '"<script>alert(1)</script>"', 2)]
    page = build_report("https://example.com", results, 100)
    assert "<script>alert" not in page
