import requests


class SlackException(Exception):
    """
    An exception raised for errors related to Slack communication.

    This exception is raised when encountering an invalid
        Slack webhook or when there's an issue sending a message.
    """
    pass


class SlackHelper:
    """
    Class to communicate with Slack
    """

    def __init__(self) -> None:
        """ Constructor method"""
        self.headers = {"Content-Type": "application/json"}

    def send_slack_message(self, webhook: str, json: str) -> int:
        """
        Send a message to Slack using a webhook.

        Args:
            webhook (str): The webhook URL provided by Slack to send messages.
            json (dict): The JSON document containing the message to be sent.

        Returns:
            int: The HTTP status code of the response.

        Raises:
            SlackException: If there's an error sending the message,
                such as an invalid webhook URL.
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
