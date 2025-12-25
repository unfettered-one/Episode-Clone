from episode.aws_proxy.dynamoDb.client import DynamoDBClientManager
from botocore.client import BaseClient


def get_dynamodb_client(region_name: str) -> BaseClient:
    """
    Returns a singleton DynamoDB client per Lambda container.
    """
    return DynamoDBClientManager.get_client(region_name)
