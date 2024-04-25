from job_scraper.dates_helper import DatesHelper
from datetime import datetime, timedelta

dates_helper = DatesHelper()


def test_format_datetime_from_year_to_second():
    date_par = "2020-05-21T14:00:00"
    date = dates_helper.format_datetime_from_year_to_second(date_par)
    assert str(date) == "2020-05-21 14:00:00"


def test_format_datetime_to_date():
    date_par = "2020-05-21T14:00:00"
    date = dates_helper.format_datetime_to_date(date_par)
    assert str(date) == "2020-05-21"


def test_get_datetime_now():
    assert abs(dates_helper.get_datetime_now().timestamp() -
               datetime.now().timestamp()) < 1


def test_get_datetime_now_in_date():
    assert (
        dates_helper.get_datetime_now_in_date()
        == dates_helper.get_datetime_now().date()
    )


def test_get_datetime_days_ago():
    days = 3
    date_time_days_ago_func = dates_helper.get_datetime_days_ago(days)
    date_time_days_ago = datetime.now() - timedelta(days=days)
    assert abs(date_time_days_ago_func.timestamp() -
               date_time_days_ago.timestamp()) < 1


def test_get_date_days_ago():
    days = 3
    date_days_ago_func = dates_helper.get_datetime_days_ago(days).date()
    date_days_ago = (datetime.now() - timedelta(days=days)).date()
    assert date_days_ago_func == date_days_ago
