"""Command line entry point:  python -m site_audit example.com"""

import argparse
import sys

import requests

from .audit import audit


def print_report(url, page, results, total):
    print(f"\nAudit for {page.url}")
    print("-" * 50)
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        print(f"[{mark}] {r.name:<18} {r.message}")
    print("-" * 50)
    print(f"Score: {total}/100\n")


def main():
    parser = argparse.ArgumentParser(description="Check a website for common problems.")
    parser.add_argument("url", help="website to check, e.g. example.com")
    args = parser.parse_args()

    try:
        page, results, total = audit(args.url)
    except requests.RequestException as e:
        print(f"Could not load {args.url}: {e}")
        sys.exit(1)

    print_report(args.url, page, results, total)


if __name__ == "__main__":
    main()
