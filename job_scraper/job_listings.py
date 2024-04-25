from dataclasses import dataclass
from typing import List


@dataclass
class JobListing:
    """
    Represents a job listing.

    Attributes:
        id (int): The unique identifier for the job listing.
        title (str): The title of the job listing.
        advertiser (str): The name of the company or
            entity advertising the job.
        location (str): The location of the job.
        area (str): The area or field of the job.
        work_type (str): The type of work
            (e.g., full-time, part-time, contract).
        salary (str): The salary range or compensation for the job.
        url (str): The URL of the job listing.
        logo_url (str): The URL of the company's logo.
    """

    id: int
    title: str
    advertiser: str
    location: str
    area: str
    work_type: str
    salary: str
    url: str
    logo_url: str


class JobListings:
    """
    Represents a collection of job listings.

    Methods:
        add_listing: Add a job listing to the collection.
        remove_listing: Remove a job listing from the collection.
        filter_listings: Filter the job listings based
            on a keyword in the title.
    """

    def __init__(self):
        self.listings: List[JobListing] = []

    def add_listing(self, listing: JobListing) -> None:
        """
        Add a job listing to the collection.

        Args:
            listing (JobListing): The job listing to add.
        """
        self.listings.append(listing)

    def remove_listing(self, listing: JobListing) -> None:
        """
        Remove a job listing from the collection.

        Args:
            listing (JobListing): The job listing to remove.
        """
        self.listings.remove(listing)

    def filter_listings(self, keyword: str) -> None:
        """
        Filter the job listings based on a keyword in the title.

        Args:
            keyword (str): The keyword to filter job listings by.
        """
        self.listings = [
            listing
            for listing in self.listings
            if keyword.lower() in listing.title.lower()
        ]

    def clear_listings(self) -> None:
        """
        Remove all job listings from the collection.
        """
        self.listings = []
