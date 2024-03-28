import json
import logging
from typing import Dict

from job_scraper.job_scraper import JobScraper
from job_scraper.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def load_configuration(filename: str) -> Dict:
    """
    Load configuration from a JSON file.

    Args:
        filename (str): The path to the JSON configuration file.

    Returns:
        Dict: The loaded configuration as a dictionary.
    """
    with open(filename) as f:
        return json.load(f)


def process_job_filter(job_filter: Dict) -> None:
    """
    Process a specific job filter.

    Args:
        job_filter (Dict): The job filter configuration.

    This function performs the following steps:
    1. Scrape listings based on the provided parameters.
    2. Filter the listings based on the keyword.
    3. Persist new listings to DynamoDB.
    4. Display new listings.
    5. Notify on new listings using Slack.
    """
    classification = job_filter.get("classification")
    keyword = job_filter.get("keyword")
    slack_webhook_secret = job_filter.get("slack_webhook_secret")
    country = job_filter.get("country")

    job_scraper = JobScraper(
        logger=logger,
        country=country,
        classification=classification,
        keyword=keyword,
    )

    logging.info("")
    logging.info(
        f"Starting: Country: {country} | Classification: {classification} | Keyword: {keyword}"  # noqa
    )

    # Get Today's and Yesterday's Listings.
    job_scraper.scrape_listings()

    # Filter the keyword from the list of listings
    job_scraper.filter_listings()

    count_listings_matching_criteria = len(job_scraper.get_listings().listings)

    if count_listings_matching_criteria == 0:
        logging.info(
            f"No listings matching the keyword '{keyword}' over the last 2 days!"  # noqa
        )
    else:
        logging.info(
            f"{count_listings_matching_criteria} listings found matching the keyword '{keyword}' over the last 2 days!"  # noqa
        )

        # insert to dynamo
        job_scraper.persist_new_listings(listings=job_scraper.get_listings())

        # Display new Listings
        job_scraper.display_new_listings(job_scraper.get_listings())

        # Notify on new listings
        job_scraper.notify_new_listings(
            listings=job_scraper.get_listings(),
            slack_webhook_secret=slack_webhook_secret,
        )


def lambda_handler(event, context):
    """
    Lambda function handler.

    This function reads the job filter configurations from a JSON file,
    processes each job filter, and logs the progress and results.

    Entry point when run in the cloud (AWS Lambda)
    """
    config = load_configuration("job_scraper/job_filters.json")

    for job_filter in config:
        process_job_filter(job_filter)
