from typing import Any

from devtools import debug
from fastapi import FastAPI
from mangum import Mangum

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
) -> Any:
    debug(payload)
    return payload


lambda_handler = Mangum(app)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
