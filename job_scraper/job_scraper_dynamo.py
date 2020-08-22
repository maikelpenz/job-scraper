from .dynamo_helper import DynamoHelper
from typing import List


class JobScraperDynamo:
    def __init__(self) -> None:
        """ Constructor method"""
        self.dynamo_helper = DynamoHelper()

    def persist_listings(self, listings: List) -> List:
        """
        Persist listings to Dynamo DB

        Arguments:
            dataframe {pd.DataFrame} -- Listings Dataframe

        returns:
            {List} -- List of new listings that couldn't be found in Dynamo
        """

        # list(listings) is needed to delete from a copy of the listing
        for listing in list(listings):
            listing_id = str(listing["id"])

            response = self.dynamo_helper.dynamo_persist(
                "job-scraper", 
                {
                    "id": {"N": listing_id}, 
                    "enriched": {"S": "NEW"}
                }
            )
            if response == "ItemAlreadyExists":
                listings.remove(listing)
                print(f"Listing {listing_id} exists in Dynamo. Skipping")
            else:
                print(f"Inserted listing {listing_id} to Dynamo table")

        return listings
