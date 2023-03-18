import json
import logging
import uuid
from typing import Any

import boto3
from devtools import debug
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from mangum import Mangum
from dynamodb_json import json_util

import deps
from settings import settings

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel("DEBUG")

app = FastAPI(
    title="Webhook Pattern",
    root_path=settings.API_ROOT_PATH,
)


@app.post(
    "/message",
    status_code=200,
)
async def send_message(
    payload: dict,
    sqs_client=Depends(deps.get_sqs_client),
) -> Any:
    payload["message_id"] = str(uuid.uuid4())
    debug(payload)

    try:
        sqs_response = sqs_client.send_message(
            QueueUrl=settings.QUEUE_URL,
            MessageBody=json.dumps(
                jsonable_encoder(payload),
            ),
        )
        debug(sqs_response)
    except Exception as e:
        logging.error(f"Sent message failed: {e}")
        raise

    return payload


def process_message(event, context):
    for record in event["Records"]:
        message = json.loads(record["body"])
        debug(message)
        try:
            item = json.loads(
                json_util.dumps(jsonable_encoder(message))
            )
            boto_session = boto3.session.Session()
            dynamodb_client = boto_session.client("dynamodb")
            dynamodb_client.put_item(
                TableName=settings.DYNAMO_TABLE,
                Item=item,
            )
        except Exception as e:
            logging.exception(e)


lambda_handler = Mangum(app, lifespan="off")


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
