import boto3

s3 = boto3.client("s3")


def download_s3_file(bucket_name, key, local_file):
    """
    Download a file from S3 to the local environment.
    """
    s3.download_file(bucket_name, key, local_file)


def upload_s3_file(bucket_name, key, local_file):
    """
    Upload a file from the local environment to an S3 bucket.
    """
    s3.upload_file(local_file, bucket_name, key)
