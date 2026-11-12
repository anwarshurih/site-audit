"""The individual checks run against a web page.

Each check gets the page info and returns a Result saying if it passed,
how important it is and a short message explaining what was found.
"""

from dataclasses import dataclass


@dataclass
class Result:
    name: str
    passed: bool
    message: str
    weight: int = 1  # how much this check counts towards the score


def check_https(page):
    if page.url.startswith("https://"):
        return Result("HTTPS", True, "Site uses HTTPS", weight=3)
    return Result("HTTPS", False, "Site is not using HTTPS (browsers show it as 'Not secure')", weight=3)


def check_title(page):
    title = page.soup.title.string.strip() if page.soup.title and page.soup.title.string else ""
    if not title:
        return Result("Page title", False, "Missing <title> tag", weight=2)
    if len(title) > 60:
        return Result("Page title", False, f"Title is {len(title)} characters (Google cuts off after ~60)", weight=2)
    return Result("Page title", True, f'"{title}"', weight=2)


def check_meta_description(page):
    tag = page.soup.find("meta", attrs={"name": "description"})
    content = tag.get("content", "").strip() if tag else ""
    if not content:
        return Result("Meta description", False, "No meta description, so Google will guess what to show", weight=2)
    if len(content) > 160:
        return Result("Meta description", False, f"Description is {len(content)} characters (aim for under 160)", weight=2)
    return Result("Meta description", True, f"{len(content)} characters", weight=2)


def check_mobile(page):
    tag = page.soup.find("meta", attrs={"name": "viewport"})
    if tag and "width=device-width" in tag.get("content", ""):
        return Result("Mobile friendly", True, "Has a viewport tag", weight=3)
    return Result("Mobile friendly", False, "No viewport tag, so the site will look tiny on phones", weight=3)


def check_h1(page):
    count = len(page.soup.find_all("h1"))
    if count == 1:
        return Result("Main heading", True, "Exactly one <h1>")
    if count == 0:
        return Result("Main heading", False, "No <h1> heading on the page")
    return Result("Main heading", False, f"{count} <h1> headings (should be one)")


def check_image_alt(page):
    images = page.soup.find_all("img")
    missing = [img for img in images if not img.get("alt")]
    if not images:
        return Result("Image alt text", True, "No images on the page")
    if missing:
        return Result("Image alt text", False, f"{len(missing)} of {len(images)} images have no alt text")
    return Result("Image alt text", True, f"All {len(images)} images have alt text")


def check_speed(page):
    seconds = page.load_time
    if seconds <= 1.5:
        return Result("Response time", True, f"{seconds:.2f}s", weight=2)
    return Result("Response time", False, f"{seconds:.2f}s (slow, aim for under 1.5s)", weight=2)


def check_page_size(page):
    kb = len(page.html.encode("utf-8")) / 1024
    if kb <= 500:
        return Result("HTML size", True, f"{kb:.0f} KB")
    return Result("HTML size", False, f"{kb:.0f} KB of HTML (quite heavy)")


# every check that gets run, in the order they appear in the report
ALL_CHECKS = [
    check_https,
    check_mobile,
    check_title,
    check_meta_description,
    check_speed,
    check_h1,
    check_image_alt,
    check_page_size,
]
