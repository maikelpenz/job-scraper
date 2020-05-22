from datetime import datetime, timedelta


class DatesHelper:
    def format_datetime_from_year_to_second(self, date: str) -> datetime:
        """
        Formats a datetime entry to "%Y-%m-%dT%H:%M:%S"

        Arguments:
            date {str} -- The string datetime

        returns:
            {datetime}
        """
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

    def format_datetime_to_date(self, date: str) -> datetime.date:
        """
        Formats a datetime entry to date

        Arguments:
            date {str} -- The string datetime

        returns:
            {datetime.date}
        """
        return self.format_datetime_from_year_to_second(date).date()

    def get_datetime_now(self) -> datetime:
        """
        Get current datetime

        returns:
            {datetime}
        """
        return datetime.now()

    def get_datetime_now_in_date(self) -> datetime.date:
        """
        Get current datetime in date

        returns:
            {datetime.date}
        """
        return self.get_datetime_now().date()

    def get_datetime_days_ago(self, number_of_days: int) -> datetime:
        """
        Get the datetime calculating number of days in the past

        Arguments:
            number_of_days {int} -- Number of days in the past

        returns:
            {datetime}
        """
        return datetime.now() - timedelta(days=number_of_days)

    def get_date_days_ago(self, number_of_days: int) -> datetime.date:
        """
        Get the date calculating number of days in the past

        Arguments:
            number_of_days {int} -- Number of days in the past

        returns:
            {datetime.date}
        """
        return self.get_datetime_days_ago(number_of_days).date()
