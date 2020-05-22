from job_scraper.job_scraper_pandas import JobScraperPandas


def test_display_empty_dataframe(capsys):
    """
    Attempt to display an empty dataframe
    """
    job_scraper_pandas = JobScraperPandas()
    listings = []

    job_scraper_pandas.display_listings(listings)
    captured = capsys.readouterr()
    assert "No listings to display!" in captured.out
