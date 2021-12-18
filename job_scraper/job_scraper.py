import json
from typing import List

import requests

from .dates_helper import DatesHelper


class JobScraper:
    def __init__(self, country: str, classification: int, keyword: str) -> None:  # noqa
        """Constructor method

        Arguments:
            country {str} -- e.g: AU or NZ
            classification {int} -- Job Classification (from the website)
            keyword {str} -- Keyword to filter listings (e.g: data)
        """
        self.country = country
        self.classification = classification
        self.keyword = keyword
        self.listings = set()
        self.enriched_listings = []
        self.dates_helper = DatesHelper()

    def get_listings(self):
        return self.listings

    def get_enriched_listings(self):
        return self.enriched_listings

    def scrape_listings(self):
        """
        Get Listings

        returns:
            {set} -- Unique collection of Listing Id's
        """
        current_page = 1
        while True:
            # keep track of listings before new page.
            current_listings = self.listings

            # get page listings
            print(f"page: {current_page}")
            listings_page = self.scrape_page_listings(current_page)

            # merge new listings with the existing list
            self.listings = self.listings.union(listings_page)

            # if list didn't change stop execution
            if current_listings == self.listings:
                break

            current_page += 1

    def scrape_page_listings(self, page: int) -> set:
        """
        Get Listings from given Page

        Arguments:
            page {int} -- website page

        returns:
            {set} -- Unique collection of Listing Id's
        """
        country_url = {
            "NZ": {"siteKey": "NZ-Main", "where": "All+New+Zealand"},
            "AU": {"siteKey": "AU-Main", "where": "All+Australia"},
        }
        site_key = country_url.get(self.country).get("siteKey")
        where = country_url.get(self.country).get("where")

        url = f"https://jobsearch-api.cloud.seek.com.au/search?siteKey={site_key}&sourcesystem=houston&where={where}&page={page}&seekSelectAllPages=true&classification={self.classification}&include=seodata&isDesktop=true&sortmode=ListedDate"  # noqa
        response = requests.get(url)
        response = json.loads(response.text)
        response = response["data"]

        date_filter_today = self.dates_helper.get_datetime_now_in_date()
        date_filter_yesterday = self.dates_helper.get_date_days_ago(
            number_of_days=1
        )  # noqa
        dates_filter = [date_filter_yesterday, date_filter_today]

        return set(
            (
                listing["id"],
                listing["title"],
            )  # return listing id and title
            for listing in response  # for every listing in reponse
            # only for listings that match my date filter
            if self.dates_helper.format_datetime_to_date(
                listing["listingDate"][:-1]
            )  # noqa
            in dates_filter
        )

    def filter_listings(self):
        """
        Filter listings based on a keyword

        Arguments:
            listings {set}

        returns:
            {set}
        """
        self.listings = (
            (listing[0], listing[1])  # return listing id and title
            for listing in self.listings  # for every listing in listings
            # only for titles considered on the keyword filter
            if self.keyword.lower() in listing[1].lower()
        )

    def enrich_listing_details(self) -> List:
        """
        Add details to new listings

        Arguments:
            listings {list}

        returns:
            {list}
        """

        for listing in self.listings:
            listing_id, listing_title = listing

            url = f"https://chalice-experience-api.cloud.seek.com.au/job/{listing_id}"  # noqa
            response = requests.get(url)
            response = json.loads(response.text)

            listing_url = (
                f"https://www.seek.co.nz/job/{listing_id}"
                if self.country == "NZ"
                else f"https://www.seek.com.au/job/{listing_id}"
            )

            listing_details = {
                "id": listing_id,
                "title": listing_title,
                "advertiser": response["advertiser"]["description"],
                "location": response["locationHierarchy"]["city"],
                "area": response["locationHierarchy"]["area"],
                "workType": response["workType"],
                "salary": response["salary"],
                "url": listing_url,
                "logo_url": response["branding"]["assets"]["logo"]["url"]
                if "branding" in response
                and "assets" in response["branding"]
                and "logo" in response["branding"]["assets"]
                else "https://www.seek.co.nz/content/images/logos/logo-seek-share2.png",  # noqa
            }

            self.enriched_listings.append(listing_details)
