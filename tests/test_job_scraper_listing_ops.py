import pytest  # noqa

from job_scraper.job_listings import JobListings
from job_scraper.pandas_helper import PandasHelper
from tests.job_scraper_fixtures import job_scraper  # noqa
from tests.job_scraper_fixtures import sample_listings  # noqa


def test_get_listings(job_scraper):  # noqa
    """
    Test JobListings object is being returned
    """
    assert isinstance(job_scraper.get_listings(), JobListings)


def test_filter_listings(job_scraper):  # noqa
    """
    Test listing filtering is working
    """
    job_scraper.filter_listings()

    filtered_listings = job_scraper.get_listings().listings
    assert len(filtered_listings) == 1
    assert all("data engineer" in listing.title.lower()
               for listing in filtered_listings)


def test_display_new_listings(mocker, job_scraper):  # noqa
    """
    Test display new listings when there are listings to display
    """
    display_dataframe_spy = mocker.spy(PandasHelper, 'display_dataframe')
    list_to_dataframe_spy = mocker.spy(PandasHelper, 'list_to_dataframe')

    job_scraper.display_new_listings(job_scraper.get_listings())

    assert list_to_dataframe_spy.call_count == 1
    assert display_dataframe_spy.call_count == 1


def test_display_new_listings_no_listings(mocker, job_scraper):  # noqa
    """
    Test display new listings when there are no listings to display
    """
    display_dataframe_spy = mocker.spy(PandasHelper, 'display_dataframe')
    list_to_dataframe_spy = mocker.spy(PandasHelper, 'list_to_dataframe')

    job_scraper.clear_listings()
    job_scraper.display_new_listings(job_scraper.get_listings())

    assert list_to_dataframe_spy.call_count == 1
    assert display_dataframe_spy.call_count == 0


def test_persist_new_listings_success(mocker, job_scraper):  # noqa
    """
    Test persisting valid new listings
    """
    mocked_dynamo_persist = mocker.patch(
        "job_scraper.dynamo_helper.DynamoHelper.dynamo_persist"
    )

    job_scraper.persist_new_listings(job_scraper.listings)

    assert mocked_dynamo_persist.call_count == 3
    assert mocked_dynamo_persist.call_args_list[0][0] == (
        'job-scraper',
        {"id": {"N": "1"}, "enriched": {"S": "NEW"}}
    )
    assert mocked_dynamo_persist.call_args_list[1][0] == (
        'job-scraper',
        {"id": {"N": "2"}, "enriched": {"S": "NEW"}}
    )


def test_persist_new_listings_duplicate(mocker, job_scraper):  # noqa
    """
    Test persisting duplicated listings
    """
    mocker.patch(
        "job_scraper.dynamo_helper.DynamoHelper.dynamo_persist",
        return_value="ItemAlreadyExists"
    )
    job_scraper.persist_new_listings(job_scraper.listings)

    # validates all listings got removed
    assert not job_scraper.listings.listings


def test_notify_new_listings(mocker, job_scraper):  # noqa
    """
    Smoke Test to verify notify_new_listings is working without logic errors
    """
    mocker.patch(
        "job_scraper.secrets_helper.SecretsHelper.get_secret"
    )
    mocker.patch(
        "job_scraper.slack_helper.SlackHelper.send_slack_message",
        return_value=200
    )

    job_scraper.notify_new_listings(job_scraper.listings, "test")


def test_create_slack_message(job_scraper):  # noqa
    """
    Smoke Test to verify create_slack_message is working without logic errors
    """
    job_scraper._create_slack_message(job_scraper.listings.listings[1])
