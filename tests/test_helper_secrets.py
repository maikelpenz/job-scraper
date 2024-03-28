import base64
import os

import boto3
import pytest
from moto import mock_secretsmanager

from job_scraper.secrets_helper import SecretsException, SecretsHelper


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def secretsmanager(aws_credentials):
    with mock_secretsmanager():
        yield boto3.client("secretsmanager", region_name="us-east-1")


@mock_secretsmanager
def test_get_secret_text(secretsmanager):
    secretsmanager.create_secret(
        Name="mock-mpenz-ws-slack-webhook",
        SecretString='{"mock-mpenz-ws-slack-webhook":"fake-value"}',
    )

    secrets_helper = SecretsHelper()

    result = secrets_helper.get_secret("mock-mpenz-ws-slack-webhook")
    assert result == "fake-value"


@mock_secretsmanager
def test_get_secret_binary(secretsmanager):

    # base 64 encodes bytes to ASCII characters
    binary_message = base64.b64encode(b"fake-value")
    secretsmanager.create_secret(
        Name="mock-mpenz-ws-slack-webhook", SecretBinary=binary_message
    )

    secrets_helper = SecretsHelper()

    result = secrets_helper.get_secret("mock-mpenz-ws-slack-webhook")
    assert result == b"fake-value"


@mock_secretsmanager
def test_get_secret_invalid_secret_name(secretsmanager):

    secretsmanager.create_secret(
        Name="mock-mpenz-ws-slack-webhook",
        SecretString='{"mock-mpenz-ws-slack-webhook":"fake-value"}',
    )

    secrets_helper = SecretsHelper()

    with pytest.raises(SecretsException) as e:
        assert secrets_helper.get_secret("wrong-mock-mpenz-ws-slack-webhook")

    msg = "Secret 'wrong-mock-mpenz-ws-slack-webhook' doesn't exist"
    assert str(e.value) == msg
