from .slack_helper import SlackHelper
from .secrets_helper import SecretsHelper
from typing import List


class JobScraperNotify:
    def __init__(self) -> None:
        """ Constructor method"""
        self.slack_helper = SlackHelper()
        self.secrets_helper = SecretsHelper()

    def notify_new_listings(
        self, listings: List, slack_webhook_secret: str
    ) -> None:  # noqa
        """
        Sends message with new jobs

        Arguments:
            listings {List} -- List of new listings
            slack_webhook_secret {str} -- Name of the secret to retrieve the
                                    slack webhook to send the notification
                                    (e.g: mpenz-ws-slack-webhook)
        """

        for listing in listings:

            message_json = {
                "blocks": [
                    {
                        "type": "section",
                        "block_id": "section567",
                        "text": {
                            "type": "mrkdwn",
                            "text": "<{url}|{title}> \n Location: {location}"
                            "\n Area: {area} \n Advertiser: {advertiser}"
                            "\n Work Type: {workType}"
                            "\n Salary: {salary}".format(
                                url=listing["url"],
                                title=listing["title"],
                                location=listing["location"],
                                area=listing["area"],
                                advertiser=listing["advertiser"],
                                workType=listing["workType"],
                                salary=listing["salary"],
                            ),
                        },
                        "accessory": {
                            "type": "image",
                            "image_url": listing["logo_url"],
                            "alt_text": listing["advertiser"],
                        },
                    }
                ]
            }

            webhook = self.secrets_helper.get_secret(slack_webhook_secret)

            status_code = self.slack_helper.send_slack_message(
                webhook=webhook, json=message_json
            )
            if status_code == 200:
                print("Slack message has been sent")
