from .pandas_helper import PandasHelper
from typing import List


class JobScraperPandas:
    def __init__(self) -> None:
        """ Constructor method"""
        self.pandas_helper = PandasHelper()

    def display_listings(self, listings: List) -> None:
        """
        Display listings

        Arguments:
            df_listings {pd.DataFrame} -- Listings Dataframe
        """
        listings_df = self.pandas_helper.list_to_dataframe(listings)

        print("")
        if listings_df.shape[0] > 0:
            self.pandas_helper.display_dataframe(
                listings_df, ["id", "title", "advertiser", "url"]
            )
        else:
            print("No listings to display!")
        print("")
