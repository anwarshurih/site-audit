from site_audit.__main__ import read_sites


def test_read_sites_skips_blanks_and_comments(tmp_path):
    f = tmp_path / "sites.txt"
    f.write_text("# barbers in ealing\nexample.com\n\nexample.org\n")
    assert read_sites(f) == ["example.com", "example.org"]
