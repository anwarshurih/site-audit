"""Writes an HTML report that can be sent to a business owner."""

import html
from datetime import date

# plain-English advice shown next to each failed check
FIXES = {
    "HTTPS": "Install an SSL certificate (most hosts offer one free) so visitors don't see a 'Not secure' warning.",
    "Mobile friendly": "Add a viewport tag and a responsive layout so the site works on phones, where most visitors are.",
    "Page title": "Give the page a clear title under 60 characters, e.g. 'Business Name | Service in Town'.",
    "Meta description": "Add a short description (under 160 characters). It's the text Google shows under your link.",
    "Response time": "Speed up the server or hosting, and compress large images. Slow sites lose visitors.",
    "Main heading": "Use exactly one main heading (h1) that says what the business does.",
    "Image alt text": "Describe each image in a few words. It helps Google and people using screen readers.",
    "HTML size": "Remove unused code and plugins to make the page lighter.",
}

STYLE = """
body { font-family: system-ui, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 20px; color: #222; }
h1 { margin-bottom: 4px; }
.site { color: #666; margin-top: 0; }
.score { font-size: 3rem; font-weight: bold; margin: 20px 0; }
.good { color: #1a8a3a; } .ok { color: #d08a00; } .bad { color: #c62828; }
table { width: 100%; border-collapse: collapse; margin-top: 20px; }
th, td { text-align: left; padding: 10px; border-bottom: 1px solid #ddd; vertical-align: top; }
.pass { color: #1a8a3a; font-weight: bold; } .fail { color: #c62828; font-weight: bold; }
.fix { color: #555; font-size: 0.9rem; }
footer { margin-top: 40px; color: #999; font-size: 0.85rem; }
"""


def score_class(score):
    if score >= 80:
        return "good"
    if score >= 50:
        return "ok"
    return "bad"


def build_report(url, results, score):
    """Return the report as an HTML string."""
    rows = []
    for r in results:
        status = '<span class="pass">Pass</span>' if r.passed else '<span class="fail">Needs fixing</span>'
        detail = html.escape(r.message)
        if not r.passed and r.name in FIXES:
            detail += f'<div class="fix">How to fix: {html.escape(FIXES[r.name])}</div>'
        rows.append(f"<tr><td>{html.escape(r.name)}</td><td>{status}</td><td>{detail}</td></tr>")

    failed = sum(1 for r in results if not r.passed)
    summary = "No problems found." if failed == 0 else f"{failed} thing{'s' if failed > 1 else ''} to improve."

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Website report - {html.escape(url)}</title>
<style>{STYLE}</style>
</head>
<body>
<h1>Website health report</h1>
<p class="site">{html.escape(url)} &middot; {date.today().strftime("%d %B %Y")}</p>
<div class="score {score_class(score)}">{score}/100</div>
<p>{summary}</p>
<table>
<tr><th>Check</th><th>Result</th><th>Details</th></tr>
{"".join(rows)}
</table>
<footer>Generated with Site Audit</footer>
</body>
</html>
"""


def save_report(path, url, results, score):
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_report(url, results, score))
