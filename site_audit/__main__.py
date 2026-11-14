"""Command line entry point.

    python -m site_audit example.com
    python -m site_audit --file sites.txt --csv results.csv
"""

import argparse
import csv
import os
import re
import sys

import requests

from .audit import audit
from .report import save_report


def print_report(page, results, total):
    print(f"\nAudit for {page.url}")
    print("-" * 50)
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        print(f"[{mark}] {r.name:<18} {r.message}")
    print("-" * 50)
    print(f"Score: {total}/100\n")


def read_sites(path):
    """Read one website per line, skipping blank lines and # comments."""
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def save_csv(rows, path):
    """Save a summary of every site (score + what failed) to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["site", "score", "problems"])
        writer.writerows(rows)
    print(f"Saved results for {len(rows)} sites to {path}")


def save_html(target, site, url, results, total, several):
    """Save one report file, or one per site inside a folder when checking several."""
    if several:
        os.makedirs(target, exist_ok=True)
        name = re.sub(r"[^a-zA-Z0-9.-]", "_", site.replace("https://", "").replace("http://", "")).strip("_")
        path = os.path.join(target, f"{name}.html")
    else:
        path = target
    save_report(path, url, results, total)
    print(f"Saved report to {path}\n")


def main():
    parser = argparse.ArgumentParser(description="Check websites for common problems.")
    parser.add_argument("urls", nargs="*", help="websites to check, e.g. example.com")
    parser.add_argument("-f", "--file", help="text file with one website per line")
    parser.add_argument("--csv", help="save a summary of all results to this CSV file")
    parser.add_argument("--html", help="save an HTML report (one site), or a folder of reports (several sites)")
    args = parser.parse_args()

    sites = list(args.urls)
    if args.file:
        sites += read_sites(args.file)
    if not sites:
        parser.error("give at least one website, or a file with --file")

    rows = []
    for site in sites:
        try:
            page, results, total = audit(site)
        except requests.RequestException as e:
            print(f"Could not load {site}: {e}\n")
            rows.append([site, "", "could not load site"])
            continue

        print_report(page, results, total)
        if args.html:
            save_html(args.html, site, page.url, results, total, several=len(sites) > 1)
        problems = "; ".join(r.name for r in results if not r.passed)
        rows.append([site, total, problems])

    # with more than one site, show the worst ones first (best leads for Kova)
    if len(rows) > 1:
        scored = sorted((r for r in rows if r[1] != ""), key=lambda r: r[1])
        print("Summary (worst first):")
        for site, total, problems in scored:
            print(f"  {total:>3}/100  {site}")
        print()

    if args.csv:
        save_csv(rows, args.csv)

    if all(r[1] == "" for r in rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
