import boto3
from botocore.exceptions import ClientError


class DynamoException(Exception):
    pass


class DynamoHelper:
    def __init__(self) -> None:
        """ Constructor method"""
        self.client = boto3.client("dynamodb", region_name="us-east-1")

    def dynamo_persist(self, table_name: str, item: dict) -> None:
        """ Insert json documents to Dynamo table

        Arguments:
            table_name {str} -- Dynamo table name
            item {dict} -- What to insert
        """
        try:
            response = self.client.put_item(
                TableName=table_name,
                Item=item,
                ConditionExpression=f"attribute_not_exists(id)",  # noqa: F541
            )
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ConditionalCheckFailedException":
                response = "ItemAlreadyExists"
            elif error_code == "ResourceNotFoundException":
                raise DynamoException("Dynamo table does not exist")
            else:
                raise e

        return response
