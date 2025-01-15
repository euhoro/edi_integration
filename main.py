from datetime import datetime
import json
import os

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import uvicorn

from converters.x837_to_x835 import convert_x837_to_x835
from models.EDI837.EDI837_idets import Edi837Idets
from tests.common_test_utils import DateTimeEncoder

# === CONSTANTS ===
TOKEN = os.getenv("FASTAPI_AUTH_TOKEN", 'mfa9vTe.y6liejBPpzYX7WKoaM9QIN8E')
PARTNERSHIP_ID = "eupart_officea"
TRANSACTION_SETTING_ID = "005010X221A1-835"
STEDI_API_URL = "https://core.us.stedi.com/2023-08-01"

# === APPLICATION INITIALIZATION ===
app = FastAPI()

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Note: Replace "*" with specific origin(s) in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === UTILITY FUNCTIONS ===
async def fetch_and_parse_edi837(j837_url, token):
    """
    Fetches and parses the EDI837 data given a URL and authorization token.

    Args:
        j837_url (str): The URL of the EDI837 file.
        token (str): Authorization token.

    Returns:
        Parsed and validated EDI837 model.
    """
    headers = {"Authorization": token}

    async with httpx.AsyncClient() as client:
        response = await client.get(j837_url, headers=headers)

        # Handle redirect if necessary
        if response.status_code == 302:
            redirect_url = response.headers.get("Location")
            if not redirect_url:
                raise HTTPException(status_code=500, detail="Redirect URL not found in headers")
            response = await client.get(redirect_url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to download file. Status code: {response.status_code}",
            )

        try:
            raw_data = response.text
            return Edi837Idets.model_validate(json.loads(raw_data))
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse EDI837 file: {str(e)}",
            )


async def process_835(payload_835, token):
    """
    Processes the EDI835 payload and sends it to the appropriate endpoint.

    Args:
        payload_835 (BaseModel): The EDI835 payload to process.
        token (str): Authorization token.

    Returns:
        dict: Response from the endpoint.
    """
    filename = f"output-file-{datetime.now().strftime('%Y%m%d%H%M%S')}.edi"
    url = f"{STEDI_API_URL}/partnerships/{PARTNERSHIP_ID}/transactions/{TRANSACTION_SETTING_ID}"

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }

    transaction_data = json.loads(json.dumps(payload_835, cls=DateTimeEncoder))
    post_data = {
        "filename": filename,
        "transaction": transaction_data,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=post_data, headers=headers)
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except httpx.RequestError as req_err:
            return {"error": f"Request error: {str(req_err)}"}
        except httpx.HTTPStatusError as http_err:
            return {
                "error": f"HTTP error {http_err.response.status_code}: {http_err.response.text}"
            }


# === ROUTE HANDLERS ===
@app.post("/webhook")
async def webhook(request: Request):
    """
    Handles incoming webhook events to process EDI837 files.

    Args:
        request (Request): Incoming HTTP request.

    Returns:
        dict: Processed response or error details.
    """
    raw_body = await request.body()
    print("Raw Body:", raw_body.decode())  # Debugging log, replace with proper logging in production.

    payload = await request.json()

    try:
        j837_url = next(
            (
                artifact["url"]
                for artifact in payload["event"]["detail"]["artifacts"]
                if artifact["usage"] == "output"
            ),
            None,
        )
        if not j837_url:
            raise HTTPException(status_code=400, detail="No 'output' artifact URL found")

        e837_data = await fetch_and_parse_edi837(j837_url, TOKEN)
        e835_data = convert_x837_to_x835(e837_data, paid=False)

        return await process_835(e835_data, TOKEN)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")


# === MAIN ===
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
