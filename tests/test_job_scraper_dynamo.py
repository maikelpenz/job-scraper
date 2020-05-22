import os

import pytest
from moto import mock_dynamodb2
import boto3


from job_scraper.job_scraper_dynamo import JobScraperDynamo


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
    job_scraper_dynamo = JobScraperDynamo()
    table_name = "jobs"
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

    return job_scraper_dynamo, params, item


@mock_dynamodb2
def test_persist_listings_success(dynamodb, dynamo_parameters, capsys):
    """
    Attempt to display an empty dataframe
    """
    job_scraper_dynamo, params, item = dynamo_parameters
    dynamodb.create_table(**params)

    listings = [
        {
            "id": 41343512,
            "title": "Job Title",
            "advertiser": "Advertiser",
            "location": "Auckland",
            "area": "Manukau & East Auckland",
            "workType": "Full Time",
            "salary": "$70,000 - $85,000",
            "url": "",
            "logo_url": "",
        }
    ]

    job_scraper_dynamo.persist_listings(listings)
    captured = capsys.readouterr()
    assert "Inserted listing 41343512 to Dynamo table" in captured.out


@mock_dynamodb2
def test_persist_listings_duplicate(dynamodb, dynamo_parameters, capsys):
    """
    Attempt to display an empty dataframe
    """
    job_scraper_dynamo, params, item = dynamo_parameters
    dynamodb.create_table(**params)

    listings = [
        {
            "id": 41343512,
            "title": "Job Title",
            "advertiser": "Advertiser",
            "location": "Auckland",
            "area": "Manukau & East Auckland",
            "workType": "Full Time",
            "salary": "$70,000 - $85,000",
            "url": "",
            "logo_url": "",
        },
        {
            "id": 41343512,
            "title": "Job Title",
            "advertiser": "Advertiser",
            "location": "Auckland",
            "area": "Manukau & East Auckland",
            "workType": "Full Time",
            "salary": "$70,000 - $85,000",
            "url": "",
            "logo_url": "",
        },
    ]

    job_scraper_dynamo.persist_listings(listings)
    captured = capsys.readouterr()
    assert "Listing 41343512 exists in Dynamo. Skipping" in captured.out
