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

### Checking lots of sites

Put one website per line in a text file (lines starting with `#` are ignored):

```
# barbers in Ealing
joesbarbers.co.uk
fadeandco.com
```

Then run:

```
python -m site_audit --file sites.txt --csv results.csv
```

It prints a summary with the worst sites first and saves everything to `results.csv`, which opens in Excel or Google Sheets.

### Reports for clients

Add `--html` to save a clean report you can send to the business owner. It shows the score, every check and a plain-English "how to fix" for each problem:

```
python -m site_audit joesbarbers.co.uk --html report.html
```

With several sites, give a folder name instead and you get one report per site:

```
python -m site_audit --file sites.txt --html reports
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

- Broken link checker
