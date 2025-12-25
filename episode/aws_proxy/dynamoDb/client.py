import boto3
import threading
from typing import Optional
from botocore.client import BaseClient

class DynamoDBClientManager:
    _client: Optional[BaseClient] = None
    _region: Optional[str] = None
    _lock = threading.Lock()  # makes it thread-safe

    @classmethod
    def get_client(cls, region_name: str)-> BaseClient:
        if cls._client is None:
            with cls._lock:
                if cls._client is None:
                    cls._client = boto3.client("dynamodb", region_name=region_name)
                    cls._region = region_name

        return cls._client