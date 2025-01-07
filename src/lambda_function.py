import json

import boto3

from utils.json_processor import check_jsonata
from utils.s3_utils import download_s3_file, upload_s3_file


def lambda_handler(event, context):
    """
    AWS Lambda handler to process JSON files.
    """
    # S3 Event Details
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    source_key = event["Records"][0]["s3"]["object"]["key"]
    destination_bucket = "destination-bucket-name"
    destination_key = f"processed/{source_key}"

    # Download the file from S3
    input_file = "/tmp/input.json"
    download_s3_file(source_bucket, source_key, input_file)

    # Process the JSON file
    input_mapping = "/tmp/mapping.jsn"  # Add your mapping file here
    with open(input_mapping, "w") as mock_mapping:
        mock_mapping.write("{}")

    processed_json = check_jsonata(input_file, input_mapping)

    # Save processed result to a temporary location
    processed_file = "/tmp/transformed.json"
    with open(processed_file, "w") as outfile:
        json.dump(processed_json, outfile, indent=2)

    # Upload the result to the destination S3 bucket
    upload_s3_file(destination_bucket, destination_key, processed_file)

    return {
        "statusCode": 200,
        "body": json.dumps(
            f"File processed and uploaded to {destination_bucket}/{destination_key}"
        ),
    }
