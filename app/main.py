import json
import logging
from typing import Any

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
    root_path="/Prod",
)


@app.post(
    "/message",
    status_code=200,
)
async def send_message(
    payload: dict,
    sqs_client=Depends(deps.get_sqs_client),
) -> Any:
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

    return sqs_response


def process_message(event, context):
    for record in event["Records"]:
        message = json.loads(record["body"])
        debug(message)
        try:
            item = json.loads(
                json_util.dumps(jsonable_encoder(message))
            )
            dynamodb_client = deps.get_dynamodb_client()
            dynamodb_client.put_item(
                TableName=settings.DYNAMO_TABLE,
                Item=item,
            )
        except Exception as e:
            logging.exception(e)


lambda_handler = Mangum(app)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
