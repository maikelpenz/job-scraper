from typing import List

import pandas as pd


class PandasException(Exception):
    pass


class PandasHelper:
    def __init__(self):
        """ Constructor method"""

        pd.set_option("display.max_rows", 500)
        pd.set_option("display.max_columns", 500)
        pd.set_option("display.width", 1000)

    def list_to_dataframe(self, lst_df):
        return pd.DataFrame(lst_df)

    def display_dataframe(self, dataframe: pd.DataFrame, columns: List) -> None:  # noqa
        """
        Prints dataframe columns and values

        Arguments:
            dataframe {pd.Dataframe} -- dataframe to display
            columns {List} -- What columns to display
        """
        print(dataframe[columns].to_markdown())
