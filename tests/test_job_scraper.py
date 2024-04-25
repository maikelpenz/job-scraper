import copy
from datetime import datetime, timedelta
import pytest  # noqa

from tests.job_scraper_fixtures import job_scraper  # noqa
from tests.job_scraper_fixtures import sample_listings  # noqa
from tests.job_scraper_fixtures import sample_url_payload  # noqa


def test_scrape_listings(mocker, job_scraper):  # noqa
    """
    Test scrape_listings. This is almost a smoke test because
        actual scrapping is not happening.
    """
    mocker.patch.object(
        job_scraper, "_scrape_page_listings", side_effect=[None, None]
    )
    original_listings = copy.deepcopy(job_scraper.listings.listings)
    job_scraper.scrape_listings()
    assert original_listings == job_scraper.listings.listings


def test_calculate_dates_to_filter(job_scraper):  # noqa
    """
    Test calculate_dates_to_filter
    """
    func_dates = job_scraper._calculate_dates_to_filter()
    assert_dates = [
        (datetime.now() - timedelta(days=1)).date(),
        datetime.now().date(),
    ]
    assert func_dates == assert_dates


def test_scrape_page_listings(mocker, job_scraper, sample_url_payload):  # noqa
    """
    Test _scrape_page_listings processes 2 new listings successfully
    """
    job_scraper.dates_to_filter = job_scraper._calculate_dates_to_filter()

    mocker.patch(
        "job_scraper.job_scraper.JobScraper._call_scrape_url",
        return_value=sample_url_payload,
    )
    mocker.patch(
        "job_scraper.job_scraper.JobScraper._should_include_listing",
        return_value=True,
    )
    process_listing_spy = mocker.spy(job_scraper, "_process_listing")
    job_scraper._scrape_page_listings(1)

    assert len(job_scraper.get_listings().listings) == 5
    assert process_listing_spy.call_count == 2


def test_should_include_listing(job_scraper, sample_url_payload):  # noqa
    """
    Test _should_include_listing with listing that is not recent
    """
    job_scraper.dates_to_filter = job_scraper._calculate_dates_to_filter()
    assert job_scraper._should_include_listing(sample_url_payload[0]) is False


def test_process_listing(job_scraper, sample_url_payload):  # noqa
    """
    Test _process_listing can add 2 new listings successfully
    """
    assert len(job_scraper.get_listings().listings) == 3

    for listing in sample_url_payload:
        job_scraper._process_listing(listing)

    assert len(job_scraper.get_listings().listings) == 5
