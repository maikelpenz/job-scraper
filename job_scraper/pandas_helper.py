import logging
from typing import List

import pandas as pd


class PandasException(Exception):
    """
    A custom exception raised for errors related to Pandas.

    Example of pandas operations are data manipulation,
        loading, or transformation.
    """
    pass


class PandasHelper:
    def __init__(self, logger: logging.Logger):
        """ Constructor method"""
        self.logger = logger or logging.getLogger(__name__)

        pd.set_option("display.max_rows", 500)
        pd.set_option("display.max_columns", 500)
        pd.set_option("display.width", 1000)

    def list_to_dataframe(self, lst_df: List) -> pd.DataFrame:
        """
        Convert a list of dictionaries to a DataFrame.

        Args:
            lst_df (List): List of dictionaries representing DataFrame rows.

        Returns:
            pd.DataFrame: DataFrame created from the list of dictionaries.
        """
        return pd.DataFrame(lst_df)

    def display_dataframe(self, dataframe: pd.DataFrame, columns: List) -> None:  # noqa
        """
        Display selected columns of a DataFrame in a tabular format.

        Args:
            dataframe (pd.DataFrame): DataFrame to display.
            columns (List): List of column names to include in the display.
        """
        logging.info(dataframe[columns].to_markdown())
