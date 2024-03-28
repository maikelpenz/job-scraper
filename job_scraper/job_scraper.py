import copy
import datetime
import logging
from enum import Enum
from typing import List

import requests

from .dates_helper import DatesHelper
from .dynamo_helper import DynamoHelper
from .job_listings import JobListings, JobListing
from .pandas_helper import PandasHelper
from .secrets_helper import SecretsHelper
from .slack_helper import SlackHelper


class Country(Enum):
    """
    Enumeration representing countries.

    Each country has a siteKey and a location for job search.
    """

    NZ = {"siteKey": "NZ-Main", "where": "All+New+Zealand"}
    AU = {"siteKey": "AU-Main", "where": "All+Australia"}


class JobScraper:
    def __init__(
        self,
        logger: logging.Logger,
        country: str,
        classification: int,
        keyword: str,
    ) -> None:  # noqa
        """
        Constructor method

        Args:
            logger (logging.Logger): Logger object for logging messages.
            country (str): Country code (e.g., 'AU' or 'NZ').
            classification (int): Job classification from the website.
            keyword (str): Keyword to filter listings (e.g., 'data').
        """
        self.base_scrape_url = "https://www.seek.co.nz/api/chalice-search/v4/search?siteKey={}&sourcesystem=houston&where={}&page={}&seekSelectAllPages=true&classification={}&include=seodata&isDesktop=true&sortmode=ListedDate"  # noqa
        self.country = country
        self.classification = classification
        self.keyword = keyword.lower()
        self.dates_helper = DatesHelper()
        self.dynamo_helper = DynamoHelper()
        self.listings = JobListings()
        self.logger = logger or logging.getLogger(__name__)
        self.pandas_helper = PandasHelper(logger=self.logger)
        self.secrets_helper = SecretsHelper()
        self.slack_helper = SlackHelper()

    def scrape_listings(self) -> None:
        """Scrape job listings."""
        self.dates_to_filter = self._calculate_dates_to_filter()

        current_page = 1
        while True:
            # keep track of listings before new page.
            current_listings = copy.deepcopy(self.listings.listings)
            # get page listings
            logging.info(f"scraping page: {current_page}")
            self._scrape_page_listings(current_page)
            # if list didn't change stop execution
            if self.listings.listings == current_listings:
                break

            current_page += 1

    def _scrape_page_listings(self, page: int) -> None:
        """
        Scrape job listings from the given page.

        Args:
            page (int): Page number.
        """
        scrape_country = Country[self.country]
        site_key = scrape_country.value["siteKey"]
        where = scrape_country.value["where"]

        url = self.base_scrape_url.format(
            site_key, where, page, self.classification
        )
        listings_to_process = self._call_scrape_url(url)

        for listing in listings_to_process:
            if self._should_include_listing(listing):
                self._process_listing(listing)

    def _call_scrape_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors.
            return response.json()["data"]
        except (requests.RequestException, KeyError) as e:
            logging.error(f"Error fetching listings: {e}")
            return None

    def _calculate_dates_to_filter(self) -> List[datetime.date]:
        """
        Calculate what dates to consider while scraping.

        Returns:
            list: A list containing two datetime.date objects representing
                yesterday and today, respectively.
        """
        date_filter_today = self.dates_helper.get_datetime_now_in_date()
        date_filter_yesterday = self.dates_helper.get_date_days_ago(
            number_of_days=1
        )  # noqa
        return [date_filter_yesterday, date_filter_today]

    def _should_include_listing(self, listing: dict) -> bool:
        """
        Check if the listing should be included based on the date filter.

        Args:
            listing (dict): The listing data dictionary.

        Returns:
            bool: True if the listing should be included, False otherwise.
        """
        listing_date = listing.get("listingDate", "")[:-1]
        listing_date = self.dates_helper.format_datetime_to_date(listing_date)
        return listing_date in self.dates_to_filter

    def _process_listing(self, listing: dict) -> None:
        """
        Process a single listing and add it to the listings collection.

        Args:
            listing (dict): The listing data dictionary.
        """
        listing_id = listing.get("id", "")
        listing_url = (
            f"https://www.seek.co.{self.country.lower()}/job/{listing_id}"
        )
        branding = (
            listing.get("branding", {})
            .get("assets", {})
            .get("logo", {})
            .get("strategies", {})
            .get("jdpLogo", "")
        )
        listing_logo_url = (
            branding
            if branding
            else "https://www.seek.co.nz/content/images/logos/logo-seek-share2.png"  # noqa
        )

        self.listings.add_listing(
            JobListing(
                id=listing_id,
                title=listing.get("title", ""),
                advertiser=listing.get("advertiser", {}).get(
                    "description", ""
                ),
                location=listing.get("location", ""),
                area=listing.get("area", listing.get("location", "")),
                work_type=listing.get("workType", ""),
                salary=listing.get("salary", ""),
                url=listing_url,
                logo_url=listing_logo_url,
            )
        )

    def get_listings(self) -> JobListings:
        """
        Get the current state of the JobListings object.

        Returns:
            JobListings: The current state of the JobListings object.
        """
        return self.listings

    def clear_listings(self) -> JobListings:
        """
        Clear the JobListings object.

        Returns:
            JobListings: The current state of the JobListings object.
        """
        return self.listings.clear_listings()

    def filter_listings(self) -> int:
        """
        Filter listings based on a keyword.

        This method filters the JobListings object
            associated with the JobScraper instance
        based on the keyword provided during initialization.
        """
        self.listings.filter_listings(self.keyword)

    def display_new_listings(self, listings: JobListings) -> None:
        """
        Display new listings.

        Args:
            listings (JobListings): The JobListings object
                containing new listings.
        """
        listings_df = self.pandas_helper.list_to_dataframe(listings.listings)
        if listings_df.shape[0] > 0:
            logging.info("New listings identified:")
            self.pandas_helper.display_dataframe(
                listings_df, ["id", "title", "advertiser", "url"]
            )
        else:
            logging.info(
                "All new listings have been processed before. Nothing to do!"
            )

    def persist_new_listings(self, listings: JobListings) -> None:
        """
        Persist new listings to DynamoDB.

        Args:
            listings (JobListings): The JobListings object containing listings.
        """
        listings_to_persist = copy.deepcopy(listings.listings)
        for listing in listings_to_persist:
            response = self.dynamo_helper.dynamo_persist(
                "job-scraper",
                {"id": {"N": str(listing.id)}, "enriched": {"S": "NEW"}},
            )
            if response == "ItemAlreadyExists":
                listings.remove_listing(listing)

    def notify_new_listings(
        self, listings: JobListings, slack_webhook_secret: str
    ) -> None:  # noqa
        """
        Sends Slack messages with new job listings.

        Args:
            listings (JobListings): The JobListings object
                containing new listings.
            slack_webhook_secret (str): The name of the secret to
                retrieve the Slack webhook.
        """
        slack_webhook = self.secrets_helper.get_secret(slack_webhook_secret)
        for listing in listings.listings:
            message_json = self._create_slack_message(listing)
            try:
                status_code = self.slack_helper.send_slack_message(
                    webhook=slack_webhook, json=message_json
                )
                if status_code == 200:
                    logging.info("Slack message has been sent")
            except Exception as e:
                logging.error(f"Error sending Slack message: {e}")

    def _create_slack_message(self, listing: JobListing) -> dict:
        """
        Create a Slack message JSON object for a given listing.

        Args:
            listing (JobListing): Listing information.

        Returns:
            dict: Slack message JSON object.
        """
        return {
            "blocks": [
                {
                    "type": "section",
                    "block_id": "section567",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{listing.url}|{listing.title}> \n"
                        f"Location: {listing.location}\n"
                        f"Area: {listing.area}\n"
                        f"Advertiser: {listing.advertiser}\n"
                        f"Work Type: {listing.work_type}\n"
                        f"Salary: {listing.salary}",
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": listing.logo_url,
                        "alt_text": listing.advertiser,
                    },
                }
            ]
        }
