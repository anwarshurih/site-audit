# Site Audit

A command line tool that checks a website for common problems: no HTTPS, not mobile friendly, missing SEO tags, slow responses and more. It gives each site a score out of 100.

I built it to quickly check small business websites before offering to improve them.

## Usage

```
pip install -r requirements.txt
python -m site_audit example.com
```

Example output:

```
Audit for https://example.com/
--------------------------------------------------
[PASS] HTTPS              Site uses HTTPS
[PASS] Mobile friendly    Has a viewport tag
[PASS] Page title         "Example Domain"
[FAIL] Meta description   No meta description, so Google will guess what to show
...
--------------------------------------------------
Score: 78/100
```

## Checks

- HTTPS
- Mobile viewport
- Page title and meta description
- Response time
- One main heading
- Image alt text
- HTML size

## Running the tests

```
pip install pytest
pytest
```

## Plans

- Check lots of sites at once from a CSV file
- HTML report you can send to a client
- Broken link checker
