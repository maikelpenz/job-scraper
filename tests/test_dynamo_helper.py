import os

import boto3
import pytest
from moto import mock_dynamodb2

from job_scraper.dynamo_helper import DynamoException, DynamoHelper


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def dynamodb(aws_credentials):
    with mock_dynamodb2():
        yield boto3.client("dynamodb", region_name="us-east-1")


@pytest.fixture
def dynamo_parameters():
    dynamo_helper = DynamoHelper()
    table_name = "jobs_mock"
    item = {"id": {"N": "1000"}}
    params = {
        "TableName": table_name,
        "KeySchema": [{"AttributeName": "id", "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": "id", "AttributeType": "N"}],  # noqa
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },  # noqa
    }

    return dynamo_helper, table_name, params, item


@mock_dynamodb2
def test_dynamo_persist_success(dynamodb, dynamo_parameters):
    dynamo_helper, table_name, params, item = dynamo_parameters
    dynamodb.create_table(**params)
    dynamo_helper.dynamo_persist(table_name, item)


@mock_dynamodb2
def test_dynamo_persist_item_exists(dynamodb, dynamo_parameters):
    dynamo_helper, table_name, params, item = dynamo_parameters

    # Create the table
    dynamodb.create_table(**params)

    # Insert a record to force existence when calling our method
    response = dynamodb.put_item(TableName=table_name, Item=item)

    response = dynamo_helper.dynamo_persist(table_name, item)

    assert response == "ItemAlreadyExists"


@mock_dynamodb2
def test_dynamo_persist_invalid_table_name(dynamodb, dynamo_parameters):
    dynamo_helper, table_name, params, item = dynamo_parameters

    with pytest.raises(DynamoException) as e:
        assert dynamo_helper.dynamo_persist(table_name, item)
    assert str(e.value) == "Dynamo table does not exist"
