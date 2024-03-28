import boto3
from botocore.exceptions import ClientError


class DynamoException(Exception):
    """
    Exception class for DynamoDB operations.

    This exception is raised when an error occurs during DynamoDB operations,
    such as querying, inserting, updating, or deleting data.
    """
    pass


class DynamoHelper:
    def __init__(self) -> None:
        """ Constructor method"""
        self.client = boto3.client("dynamodb", region_name="us-east-1")

    def dynamo_persist(self, table_name: str, item: dict) -> dict:
        """
        Insert a JSON document into a DynamoDB table.

        Args:
            table_name (str): The name of the DynamoDB table.
            item (dict): The item to insert into the table.

        Returns:
            dict: Response from DynamoDB after the operation.

        Raises:
            DynamoException: If there is an issue with DynamoDB operations.
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
