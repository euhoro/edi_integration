import json

from utils.json_processor import check_jsonata
from utils.s3_utils import download_s3_file, upload_s3_file


import logging

EUGEN_835_BUCKET = "eugen835"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#
# def lambda_handler(event, context):
#     logger.info("Received Event: %s", event)
#     """
#     AWS Lambda handler to process JSON files.
#     """
#     # S3 Event Details
#     source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
#     source_key = event["Records"][0]["s3"]["object"]["key"]
#     destination_bucket = "destination-bucket-name"
#     destination_key = f"processed/{source_key}"
#
#     # Download the file from S3
#     input_file = "/tmp/input.json"
#     download_s3_file(source_bucket, source_key, input_file)
#
#     # Process the JSON file
#     input_mapping = "/tmp/mapping.jsn"  # Add your mapping file here
#     with open(input_mapping, "w") as mock_mapping:
#         mock_mapping.write("{}")
#
#     processed_json = check_jsonata(input_file, input_mapping)
#
#     # Save processed result to a temporary location
#     processed_file = "/tmp/transformed.json"
#     with open(processed_file, "w") as outfile:
#         json.dump(processed_json, outfile, indent=2)
#
#     # Upload the result to the destination S3 bucket
#     upload_s3_file(destination_bucket, destination_key, processed_file)
#
#     return {
#         "statusCode": 200,
#         "body": json.dumps(
#             f"File processed and uploaded to {destination_bucket}/{destination_key}"
#         ),
#     }


def lambda_handler(event, context):
    logger.info("Received Event: %s", event)
    """
    AWS Lambda handler to move files between S3 buckets.
    """
    # S3 Event Details
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    source_key = event["Records"][0]["s3"]["object"]["key"]
    destination_bucket = EUGEN_835_BUCKET
    destination_key = f"processed/{source_key}"

    try:
        import boto3
        s3_client = boto3.client("s3", region_name="us-east-1")
        # Copy file to the destination bucket
        s3_client.copy_object(
            Bucket=destination_bucket,
            CopySource={"Bucket": source_bucket, "Key": source_key},
            Key=destination_key,
        )
        # Delete the source file after copying
        s3_client.delete_object(Bucket=source_bucket, Key=source_key)

        logger.info(
            f"Successfully moved file '{source_key}' from '{source_bucket}' to '{destination_bucket}/{destination_key}'")

        return {
            "statusCode": 200,
            "body": json.dumps(
                f"File moved to {destination_bucket}/{destination_key}"
            ),
        }
    except Exception as e:
        logger.error(f"File moving failed: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps("Error occurred while moving the file."),
        }