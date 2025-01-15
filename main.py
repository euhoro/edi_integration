from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import requests  # For local testing of the endpoint
import httpx



from converters.x837_to_x835 import convert_x837_to_x835
from tests.common_test_utils import DateTimeEncoder



from models.EDI837.EDI837_idets import Edi837Idets

app = FastAPI()

# Enable CORS middleware to resolve CORS issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# ev3 = {'event': {'version': '0', 'id': 'ca926073-6a6d-bc77-2b54-ffe7fb1c74e4', 'detail-type': 'transaction.processed.v2', 'source': 'stedi.core', 'account': '613434567937', 'time': '2025-01-13T15:27:08Z', 'region': 'us-east-1', 'resources': ['https://core.us.stedi.com/2023-08-01/transactions/d8f64e1e-35ea-401f-ac21-20ea57a3a24e'], 'detail': {'transactionId': 'd8f64e1e-35ea-401f-ac21-20ea57a3a24e', 'direction': 'INBOUND', 'mode': 'production', 'fileExecutionId': 'ab6c6dce-2a4a-42fb-a2cc-b84fdc119737', 'processedAt': '2025-01-13T15:27:07.961Z', 'fragments': None, 'artifacts': [{'artifactType': 'application/edi-x12', 'usage': 'input', 'url': 'https://core.us.stedi.com/2023-08-01/transactions/d8f64e1e-35ea-401f-ac21-20ea57a3a24e/input', 'sizeBytes': 1399, 'model': 'transaction'}, {'artifactType': 'application/json', 'usage': 'output', 'url': 'https://core.us.stedi.com/2023-08-01/transactions/d8f64e1e-35ea-401f-ac21-20ea57a3a24e/output', 'sizeBytes': 11453, 'model': 'transaction'}], 'partnership': {'partnershipId': 'eupart_officea', 'partnershipType': 'x12', 'sender': {'profileId': 'officea'}, 'receiver': {'profileId': 'eupart'}}, 'x12': {'transactionSetting': {'guideId': '01JHFQHKRAAJJ190A2Z3371QYM', 'transactionSettingId': '01JHFQHNBB5EMJ9J35FHJHFZZ4'}, 'metadata': {'interchange': {'acknowledgmentRequestedCode': '1', 'controlNumber': 1}, 'functionalGroup': {'controlNumber': 3001, 'release': '005010X222A1', 'date': '2009-10-06', 'time': '12:48', 'functionalIdentifierCode': 'HC'}, 'transaction': {'controlNumber': '1234', 'transactionSetIdentifier': '837'}, 'receiver': {'applicationCode': 'PPPPP', 'isa': {'qualifier': 'ZZ', 'id': '111222333'}}, 'sender': {'applicationCode': 'SSSSSS', 'isa': {'qualifier': 'ZZ', 'id': '999888777'}}}}, 'connectionId': '01JHFF8EZTG55VWABFKAHB4G21'}}}
# ev = {'event': {'version': '0', 'id': '73dfff8c-3e2c-728a-58b7-68f1c73b6ba6', 'detail-type': 'transaction.processed.v2', 'source': 'stedi.core', 'account': '613434567937', 'time': '2025-01-13T15:21:35Z', 'region': 'us-east-1', 'resources': ['https://core.us.stedi.com/2023-08-01/transactions/bc1866c6-cacc-4134-8d9d-bbe724224036'], 'detail': {'transactionId': 'bc1866c6-cacc-4134-8d9d-bbe724224036', 'direction': 'INBOUND', 'mode': 'production', 'fileExecutionId': '4521b85e-115d-48b9-8b97-0feedb5e568b', 'processedAt': '2025-01-13T15:21:34.752Z', 'fragments': None, 'artifacts': [{'artifactType': 'application/edi-x12', 'usage': 'input', 'url': 'https://core.us.stedi.com/2023-08-01/transactions/bc1866c6-cacc-4134-8d9d-bbe724224036/input', 'sizeBytes': 1399, 'model': 'transaction'}, {'artifactType': 'application/json', 'usage': 'output', 'url': 'https://core.us.stedi.com/2023-08-01/transactions/bc1866c6-cacc-4134-8d9d-bbe724224036/output', 'sizeBytes': 11453, 'model': 'transaction'}], 'partnership': {'partnershipId': 'eupart_officea', 'partnershipType': 'x12', 'sender': {'profileId': 'officea'}, 'receiver': {'profileId': 'eupart'}}, 'x12': {'transactionSetting': {'guideId': '01JHFQHKRAAJJ190A2Z3371QYM', 'transactionSettingId': '01JHFQHNBB5EMJ9J35FHJHFZZ4'}, 'metadata': {'interchange': {'acknowledgmentRequestedCode': '1', 'controlNumber': 1}, 'functionalGroup': {'controlNumber': 3001, 'release': '005010X222A1', 'date': '2009-10-06', 'time': '12:48', 'functionalIdentifierCode': 'HC'}, 'transaction': {'controlNumber': '1234', 'transactionSetIdentifier': '837'}, 'receiver': {'applicationCode': 'PPPPP', 'isa': {'qualifier': 'ZZ', 'id': '111222333'}}, 'sender': {'applicationCode': 'SSSSSS', 'isa': {'qualifier': 'ZZ', 'id': '999888777'}}}}, 'connectionId': '01JHFF8EZTG55VWABFKAHB4G21'}}}
# ev2 ={'event': {'version': '0', 'id': 'ca926073-6a6d-bc77-2b54-ffe7fb1c74e4', 'detail-type': 'transaction.processed.v2', 'source': 'stedi.core', 'account': '613434567937', 'time': '2025-01-13T15:27:08Z', 'region': 'us-east-1', 'resources': ['https://core.us.stedi.com/2023-08-01/transactions/d8f64e1e-35ea-401f-ac21-20ea57a3a24e'], 'detail': {'transactionId': 'd8f64e1e-35ea-401f-ac21-20ea57a3a24e', 'direction': 'INBOUND', 'mode': 'production', 'fileExecutionId': 'ab6c6dce-2a4a-42fb-a2cc-b84fdc119737', 'processedAt': '2025-01-13T15:27:07.961Z', 'fragments': None, 'artifacts': [{'artifactType': 'application/edi-x12', 'usage': 'input', 'url': 'https://core.us.stedi.com/2023-08-01/transactions/d8f64e1e-35ea-401f-ac21-20ea57a3a24e/input', 'sizeBytes': 1399, 'model': 'transaction'}, {'artifactType': 'application/json', 'usage': 'output', 'url': 'https://core.us.stedi.com/2023-08-01/transactions/d8f64e1e-35ea-401f-ac21-20ea57a3a24e/output', 'sizeBytes': 11453, 'model': 'transaction'}], 'partnership': {'partnershipId': 'eupart_officea', 'partnershipType': 'x12', 'sender': {'profileId': 'officea'}, 'receiver': {'profileId': 'eupart'}}, 'x12': {'transactionSetting': {'guideId': '01JHFQHKRAAJJ190A2Z3371QYM', 'transactionSettingId': '01JHFQHNBB5EMJ9J35FHJHFZZ4'}, 'metadata': {'interchange': {'acknowledgmentRequestedCode': '1', 'controlNumber': 1}, 'functionalGroup': {'controlNumber': 3001, 'release': '005010X222A1', 'date': '2009-10-06', 'time': '12:48', 'functionalIdentifierCode': 'HC'}, 'transaction': {'controlNumber': '1234', 'transactionSetIdentifier': '837'}, 'receiver': {'applicationCode': 'PPPPP', 'isa': {'qualifier': 'ZZ', 'id': '111222333'}}, 'sender': {'applicationCode': 'SSSSSS', 'isa': {'qualifier': 'ZZ', 'id': '999888777'}}}}, 'connectionId': '01JHFF8EZTG55VWABFKAHB4G21'}}}



@app.post("/webhook")
async def webhook(request: Request):#handle duplicates -

    # Log the raw request body
    raw_body = await request.body()
    print("Raw Body:", raw_body.decode())
    # Parse JSON body
    payload1 = await request.json()
    print("Parsed Payload:", payload1)

    j837_url = [x for x in payload1['event']['detail']['artifacts'] if x['usage'] == 'output'][0]['url']
    token = 'mfa9vTe.y6liejBPpzYX7WKoaM9QIN8E'
    #j837_url = 'https://core.us.stedi.com/2023-08-01/transactions/749d5e9a-7195-4879-99bb-8a48038ea2c2/output'
    # Asynchronously download the file with Authorization header
    headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        response = await client.get(j837_url, headers=headers)

        # Handle redirect
        if response.status_code == 302:
            # redirect_url = response.headers.get("Location")
            # if redirect_url:
            #     response = await client.get(redirect_url, headers=headers)
            # Extract the location (pre-signed URL)
            redirect_url = response.headers.get("Location")
            if not redirect_url:
                raise HTTPException(status_code=500, detail="Redirect URL not found in headers")

            # Make another GET request to download from the pre-signed URL
            response = await client.get(redirect_url)

        # Check if the response is successful
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to download file. Status code: {response.status_code}"
            )

        # Parse the content of the downloaded file
        try:
            raw_data = response.text  # Assuming the response contains text data
            # Use Pydantic model to validate and parse the data (adjust "Edi837Idets" fields accordingly)
            e837 = Edi837Idets.model_validate(json.loads(raw_data))
            e835 = convert_x837_to_x835(e837, paid=False)

            return await process_835(e835, token)



        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse file: {str(e)}")
        return {"success"}



@app.post("/webhook2")
async def webhook2(request: Request):#implement duplication
    token = 'mfa9vTe.y6liejBPpzYX7WKoaM9QIN8E'  # Replace with your actual token
    j837_url = 'https://core.us.stedi.com/2023-08-01/transactions/749d5e9a-7195-4879-99bb-8a48038ea2c2/output'

    # Add proper Authorization header
    headers = {"Authorization": token}

    # Asynchronously download the file with Authorization header
    async with httpx.AsyncClient(follow_redirects=False) as client:
        response = await client.get(j837_url, headers=headers)

        # Handle redirect
        if response.status_code == 302:

            redirect_url = response.headers.get("Location")
            if not redirect_url:
                raise HTTPException(status_code=500, detail="Redirect URL not found in headers")

            # Make another GET request to download from the pre-signed URL
            response = await client.get(redirect_url)

        # Check if the response is successful
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to download file. Status code: {response.status_code}"
            )

        # Parse the content of the downloaded file
        try:
            raw_data = response.text  # Assuming the response contains text data
            # Use Pydantic model to validate and parse the data (adjust "Edi837Idets" fields accordingly)
            e837 = Edi837Idets.model_validate(json.loads(raw_data))
            e835 = convert_x837_to_x835(e837,paid=False)

            return await process_835(e835, token)



        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse file: {str(e)}")
        return {"success"}


async def process_835(payload_835, token):
    partnership_id = "eupart_officea"
    transaction_setting_id = "005010X221A1-835"
    filename = f"my-output-file.edi-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Prepare URL
    url = (
        f"https://core.us.stedi.com/2023-08-01/"
        f"partnerships/{partnership_id}/transactions/{transaction_setting_id}"
    )

    # Prepare headers
    headers = {
        "Authorization": token,  # Replace with actual token
        "Content-Type": "application/json",
    }

    # Invoke the dict conversion
    transaction_data = payload_835.model_dump()  # Pydantic's built-in dict conversion

    transaction_data = json.loads(json.dumps(payload_835, cls=DateTimeEncoder))
    # transaction_data = payload.dict()     # For Pydantic v1.x (alternative option)

    # Form the payload for the POST request
    post_data = {
        "filename": filename,
        "transaction": transaction_data,  # Clean dict ready for JSON serialization
    }

    # Send the HTTP POST request
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=post_data, headers=headers)
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except httpx.RequestError as req_err:
            return {"error": f"Request error: {str(req_err)}"}
        except httpx.HTTPStatusError as http_err:
            return {
                "error": f"HTTP status error: {http_err.response.status_code} - {http_err.response.text}"
            }


# Main method to run the application
if __name__ == "__main__":
    # Run the FastAPI app
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # Optional: Test the webhook endpoint with a default sample payload
    def test_webhook():
        url = "http://127.0.0.1:8000/webhook"
        sample_payload = {"a": "b"}
        response = requests.post(url, json=sample_payload)
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.json())

    # Uncomment the line below to run the test when the script is executed
    # test_webhook()
