import json

# from mapping.x222 import transform_json_aws837_after_jsonata
# from models.EDI837.EDI837_idets import Edi837Idets
from tests.common_test_utils import read_as_str
from utils.json_processor import transform_jsonata
from utils.s3_utils import download_s3_file, upload_s3_file, delete_s3_file

import logging

EUGEN_835_BUCKET = "eugen835"
EUGEN_837_BUCKET = "eugen837"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def lambda_handler(event, context):
    logger.info("Received Event: %s", event)
    """
    AWS Lambda handler to process JSON files.
    """
    # S3 Event Details
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    source_key = event["Records"][0]["s3"]["object"]["key"]
    destination_bucket = EUGEN_835_BUCKET
    destination_key = f"processed/{source_key}"

    # Download the file from S3
    input_file = "/tmp/input.json"
    download_s3_file(source_bucket, source_key, input_file)

    # processed_json = transform_jsonata(input_file, read_as_str('resources/f02_837_input_json_aws/x222-837.jsn'),
    #                                    transform_func=transform_json_aws837_after_jsonata)

    processed_json = transform_jsonata(input_file, read_as_str('resources/f02_837_input_json_aws/x222-837.jsn'))

    #edi_837 = Edi837Idets.parse_obj(processed_json)

    # Save processed result to a temporary location
    processed_file = "/tmp/transformed.json"
    with open(processed_file, "w") as outfile:
        json.dump(processed_json, outfile, indent=2)

    # Upload the result to the destination S3 bucket
    upload_s3_file(destination_bucket, destination_key, processed_file)

    # Delete source S3 bucket
    delete_s3_file(source_bucket, source_key)

    return {
        "statusCode": 200,
        "body": json.dumps(
            f"File processed and uploaded to {destination_bucket}/{destination_key}"
        ),
    }

#
# def lambda_handler(event, context):
#     logger.info("Received Event: %s", event)
#     """
#     AWS Lambda handler to move files between S3 buckets.
#     """
#     # S3 Event Details
#     source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
#     source_key = event["Records"][0]["s3"]["object"]["key"]
#     destination_bucket = EUGEN_835_BUCKET
#     destination_key = f"processed/{source_key}"
#
#     try:
#         import boto3
#         s3_client = boto3.client("s3", region_name="us-east-1")
#         # Copy file to the destination bucket
#         s3_client.copy_object(
#             Bucket=destination_bucket,
#             CopySource={"Bucket": source_bucket, "Key": source_key},
#             Key=destination_key,
#         )
#         # Delete the source file after copying
#         s3_client.delete_object(Bucket=source_bucket, Key=source_key)
#
#         logger.info(
#             f"Successfully moved file '{source_key}' from '{source_bucket}' to '{destination_bucket}/{destination_key}'")
#
#         return {
#             "statusCode": 200,
#             "body": json.dumps(
#                 f"File moved to {destination_bucket}/{destination_key}"
#             ),
#         }
#     except Exception as e:
#         logger.error(f"File moving failed: {e}")
#         return {
#             "statusCode": 500,
#             "body": json.dumps("Error occurred while moving the file."),
#         }
