import json
import pytest
import boto3
from moto import mock_aws

from lambda_function import lambda_handler, EUGEN_835_BUCKET, EUGEN_837_BUCKET


# @mock_aws
# def test_my_model_save():
#     conn = boto3.resource("s3", region_name="us-east-1")
#     # We need to create the bucket since this is all in Moto's 'virtual' AWS account
#     conn.create_bucket(Bucket="mybucket")
#
#     model_instance = MyModel("steve", "is awesome")
#     model_instance.save()
#
#     body = conn.Object("mybucket", "steve").get()[
#         "Body"].read().decode("utf-8")
#
#     assert body == "is awesome"


# Fixture for mocked S3 setup
@pytest.fixture
def s3_setup():
    """
    Set up mock S3 buckets and upload a sample file for testing.
    """
        #with mock_s3():  # Mocks all S3 interactions within this context
    #s3 = boto3.client("s3", region_name="us-east-1")
    with mock_aws():
        conn = boto3.resource("s3", region_name="us-east-1")
        # We need to create the bucket since this is all in Moto's 'virtual' AWS account

        src = EUGEN_837_BUCKET
        dst = EUGEN_835_BUCKET


        conn.create_bucket(Bucket=src)
        conn.create_bucket(Bucket=dst)
        # Create the source and destination buckets
        #source_bucket = "source-bucket-name"
        #destination_bucket = "destination-bucket-name"
        #s3.create_bucket(Bucket=source_bucket)
        #s3.create_bucket(Bucket=destination_bucket)

        # Upload a dummy file to the source bucket for testing file movement
        source_key = "sample.json"
        s3 = boto3.client("s3", region_name="us-east-1")
        #s3.put_object(Bucket="mybucket", Key=self.name, Body=self.value)
        s3.put_object(
            Bucket=src,
            Key=source_key,
            Body=json.dumps({"key": "value"}),  # Dummy JSON data
        )

        yield s3, src, dst, source_key

@mock_aws
# Test Lambda handler using the mocked S3 setup
def test_lambda_handler_move_object(s3_setup):
    """
    Test the functionality of moving objects between S3 buckets.
    """
    # Setup mock S3 environment
    s3, source_bucket, destination_bucket, source_key = s3_setup

    # Prepare a dummy event for the Lambda handler
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": source_bucket},
                    "object": {"key": source_key},
                }
            }
        ]
    }
    """
    {
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "eugen837"
        },
        "object": {
          "key": "dummy.json"
        }
      }
    }
  ]
}
"""

    # Invoke the Lambda handler
    response = lambda_handler(event, None)

    # Assert that the Lambda response indicates success
    assert response["statusCode"] == 200
    #assert f"File moved to {destination_bucket}/processed/{source_key}" in response["body"]
    assert f"File processed and uploaded to {destination_bucket}/processed/{source_key}" in response["body"]

    # Verify the object exists in the destination bucket
    objects_in_destination = s3.list_objects_v2(Bucket=destination_bucket, Prefix=f"processed/{source_key}")
    assert "Contents" in objects_in_destination
    assert len(objects_in_destination["Contents"]) == 1

    # Verify the object no longer exists in the source bucket
    objects_in_source = s3.list_objects_v2(Bucket=source_bucket, Prefix=source_key)
    assert "Contents" not in objects_in_source
