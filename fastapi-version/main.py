from fastapi import FastAPI
from pydantic import BaseModel
import json
import boto3
import os

app = FastAPI()

# Define bidrequest structure
class BidRequest(BaseModel):
    id: str
    imp: list
    site: dict
    device: dict
    user: dict

# NDJSON log file
LOG_FILE = "bid_requests.ndjson"

# Environment variables (set via ECS task or hardcoded if needed)
bucket_name = os.getenv("S3_BUCKET", "dsp-bid-logs-sivaganga")
s3_key = "logs/bid_requests.ndjson"

# Create S3 client
s3 = boto3.client("s3")

@app.post("/bid")
def handle_bid(request: BidRequest):
    # Convert request to dict
    request_dict = request.dict()

    # Log to file
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(request_dict) + "\n")

    # Upload to S3
    try:
        s3.upload_file(LOG_FILE, bucket_name, s3_key)
    except Exception as e:
        print(f"S3 upload failed: {e}")

    # Return bid response
    return {
        "id": request.id,
        "seatbid": [{
            "bid": [{
                "id": "bid1",
                "impid": request.imp[0]["id"],
                "price": 0.75,
                "adm": "<html>Your Ad Here</html>",
                "crid": "creative123"
            }]
        }]
    }
