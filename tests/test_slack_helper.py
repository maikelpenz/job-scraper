import pytest

from job_scraper.slack_helper import SlackHelper, SlackException

slack_helper = SlackHelper()


def test_send_slack_message_wrong_webhook():
    slack_message_json = {"text": "Unit test message"}
    webhook = "https://hooks.slack.com/services/WRONG/WRONG/WRONG"

    with pytest.raises(SlackException) as e:
        assert slack_helper.send_slack_message(webhook, slack_message_json)
    assert str(e.value) == "Invalid Slack Webhook"
