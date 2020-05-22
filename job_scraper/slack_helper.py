import requests


class SlackException(Exception):
    pass


class SlackHelper:
    """
    Class to communicate with Slack
    """

    def __init__(self) -> None:
        """ Constructor method"""
        self.headers = {"Content-Type": "application/json"}

    def send_slack_message(self, webhook: str, json: str) -> int:
        """ Sends slack message

        Arguments:
            json {str} -- json document
        """
        try:
            response = requests.post(
                url=webhook,
                json=json,
                headers=self.headers
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 403:
                raise SlackException("Invalid Slack Webhook")
        else:
            status_code = response.status_code

        return status_code
