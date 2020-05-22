import base64
import json

import boto3
from botocore.exceptions import ClientError


class SecretsException(Exception):
    pass


class SecretsHelper:
    """
    Class to communicate with AWS secrets
    """

    def __init__(self) -> None:
        """ Constructor method"""
        self.client = boto3.client("secretsmanager", region_name="us-east-1")

    def get_secret(self, secret_name: str) -> str:
        """
        Reads the slack webhook from secrets manager

        Arguments:
            secret_name {str} -- Name of the slack webhook secret stored on AWS

        returns:
            {str} -- Slack webhook
        """

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                raise SecretsException(f"Secret '{secret_name}' doesn't exist")
            else:
                raise e
        else:
            if "SecretString" in get_secret_value_response:
                secret = get_secret_value_response["SecretString"]
                secret = json.loads(secret)
                secret = secret.get(secret_name)
            else:
                secret = get_secret_value_response["SecretBinary"]
                secret = base64.b64decode(secret)

        return secret
