from typing import Dict, Any, Optional
from episode.aws_proxy.dynamoDb.util import get_dynamodb_client


class DynamoDBOperations:
    """
    Generic DynamoDB CRUD operations.
    This is the ONLY class you ever need to interact with.
    """

    def __init__(self, table_name: str, region_name: str) -> None:
        self.table_name = table_name
        self.client = get_dynamodb_client(region_name)

    def create_item(self, item: Dict[str, Any]) -> None:
        self.client.put_item(TableName=self.table_name, Item=self._serialize(item))

    def get_item(self, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        response = self.client.get_item(TableName=self.table_name, Key=self._serialize(key))
        return self._deserialize(response.get("Item"))

    def update_item(
        self,
        key: Dict[str, Any],
        update_expression: str,
        expression_values: Dict[str, Any],
        expression_names: Optional[Dict[str, str]] = None,
    ) -> None:
        params = {
            "TableName": self.table_name,
            "Key": self._serialize(key),
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": self._serialize(expression_values),
        }

        if expression_names:
            params["ExpressionAttributeNames"] = expression_names

        self.client.update_item(**params)

    def delete_item(self, key: Dict[str, Any]) -> None:
        self.client.delete_item(TableName=self.table_name, Key=self._serialize(key))

    def _serialize_value(self, value: Any) -> Dict[str, Any]:
        if isinstance(value, str):
            return {"S": value}

        elif isinstance(value, bool):
            return {"BOOL": value}

        elif isinstance(value, int) or isinstance(value, float):
            return {"N": str(value)}

        elif value is None:
            return {"NULL": True}

        elif isinstance(value, list):
            return {"L": [self._serialize_value(v) for v in value]}

        elif isinstance(value, dict):
            return {"M": {k: self._serialize_value(v) for k, v in value.items()}}

        else:
            raise ValueError(f"Unsupported type: {type(value)}")

    def _serialize(self, data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        return {k: self._serialize_value(v) for k, v in data.items()}

    def _deserialize_value(self, value: Dict[str, Any]) -> Any:
        dtype = next(iter(value))
        raw = value[dtype]

        if dtype == "S":
            return raw

        elif dtype == "N":
            return int(raw) if raw.isdigit() else float(raw)

        elif dtype == "BOOL":
            return raw

        elif dtype == "NULL":
            return None

        elif dtype == "L":
            return [self._deserialize_value(v) for v in raw]

        elif dtype == "M":
            return {k: self._deserialize_value(v) for k, v in raw.items()}

        else:
            return raw

    def _deserialize(self, item: Dict[str, Dict[str, Any]] | None):
        if not item:
            return None

        return {k: self._deserialize_value(v) for k, v in item.items()}
