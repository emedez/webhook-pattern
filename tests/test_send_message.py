import time

import boto3
from devtools import debug
from fastapi.testclient import TestClient
from dynamodb_json import json_util

from app.settings import settings


def test_send_message(client: TestClient):
    endpoint_url = "/message"
    payload = {
        "name": "Johnny Bravo",
        "age": 16
    }
    r = client.post(
        endpoint_url,
        json=payload,
    )
    assert r.status_code == 200
    response_json = r.json()
    debug(response_json)

    # give it time to process the queue
    # TODO: adjust time if needed
    time.sleep(5)

    boto_session = boto3.session.Session()
    dynamodb_client = boto_session.client("dynamodb")
    response = dynamodb_client.get_item(
        TableName=settings.DYNAMO_TABLE,
        Key={
            "message_id": {"S": response_json.get("message_id")},
        }
    )
    debug(response)
    assert "Item" in response
    if "Item" in response:
        item = response["Item"]
        debug(item)
        item = json_util.loads(item)
        assert payload.get("name") == item.get("name")
        assert payload.get("age") == item.get("age")

