from datetime import datetime, timedelta


class DatesHelper:
    def format_datetime_from_year_to_second(self, date: str) -> datetime:
        """
        Formats a datetime string to a datetime object with the
        format "%Y-%m-%dT%H:%M:%S".

        Args:
            date (str): The string representing the datetime.

        Returns:
            datetime: The formatted datetime object.
        """
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

    def format_datetime_to_date(self, date: str) -> datetime.date:
        """
        Formats a datetime string to a date object.

        Args:
            date (str): The string representing the datetime.

        Returns:
            datetime.date: The formatted date object.
        """
        return self.format_datetime_from_year_to_second(date).date()

    def get_datetime_now(self) -> datetime:
        """
        Get the current datetime.

        Returns:
            datetime: The current datetime.
        """
        return datetime.now()

    def get_datetime_now_in_date(self) -> datetime.date:
        """
        Get the current date.

        Returns:
            datetime.date: The current date.
        """
        return self.get_datetime_now().date()

    def get_datetime_days_ago(self, number_of_days: int) -> datetime:
        """
        Get the datetime from a specified number of days ago.

        Args:
            number_of_days (int): The number of days in the past.

        Returns:
            datetime: The datetime from the specified number of days ago.
        """
        return datetime.now() - timedelta(days=number_of_days)

    def get_date_days_ago(self, number_of_days: int) -> datetime.date:
        """
        Get the date from a specified number of days ago.

        Args:
            number_of_days (int): The number of days in the past.

        Returns:
            datetime.date: The date from the specified number of days ago.
        """
        return self.get_datetime_days_ago(number_of_days).date()
