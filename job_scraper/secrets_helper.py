import base64
import json

import boto3
from botocore.exceptions import ClientError


class SecretsException(Exception):
    """
    An exception raised for errors related to AWS Secrets Manager.

    This exception is raised when a secret doesn't exist or when
    there's an issue retrieving it.
    """

    pass


class SecretsHelper:
    """
    Class to communicate with AWS secrets
    """

    def __init__(self) -> None:
        """Constructor method"""
        self.client = boto3.client("secretsmanager", region_name="us-east-1")

    def get_secret(self, secret_name: str) -> str:
        """
        Retrieve the value of a secret from AWS Secrets Manager.

        Args:
            secret_name (str): The name of the secret stored
                in AWS Secrets Manager.

        Returns:
            str: The value of the secret.

        Raises:
            SecretsException: If the secret doesn't exist or if there's
                an error retrieving it.
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
