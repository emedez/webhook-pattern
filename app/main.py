from typing import Any

from devtools import debug
from fastapi import FastAPI

app = FastAPI(
    title="Webhook Pattern",
)


@app.post(
    "/message",
    status_code=200,
)
async def send_message(
    payload: dict,
) -> Any:
    debug(payload)
    ...


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
