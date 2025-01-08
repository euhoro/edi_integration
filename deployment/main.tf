provider "aws" {
  region = "us-east-1" # Your AWS region
}

# S3 Buckets
resource "aws_s3_bucket" "source_bucket" {
  bucket = "eugen837"
  acl    = "private"
}

resource "aws_s3_bucket" "destination_bucket" {
  bucket = "eugen835"
  acl    = "private"
}

# Lambda Execution Role
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda-s3-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = { Service = "lambda.amazonaws.com" }
      }
    ]
  })

  # Attach permissions
  inline_policy {
    name = "s3-access-policy"
    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          # Permissions for reading, writing, and deleting objects
          Action   = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
          Effect   = "Allow",
          Resource = [
            "arn:aws:s3:::eugen835/*", # Destination bucket
            "arn:aws:s3:::eugen837/*"  # Source bucket
          ]
        },
        {
          # Permissions for listing the buckets if needed
          Action   = ["s3:ListBucket"],
          Effect   = "Allow",
          Resource = [
            "arn:aws:s3:::eugen835",
            "arn:aws:s3:::eugen837"
          ]
        }
      ]
    })
  }
}

# Lambda Function
resource "aws_lambda_function" "process_json" {
  function_name = "eugen-process-json-lambda"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.lambda_exec_role.arn
  filename      = "../lambda-code.zip" # Replace with the correct ZIP path

  # Add Layer
  layers = [
    "arn:aws:lambda:us-east-1:975050130895:layer:eugen_lambda_layers2:1"
  ]

  # Increase timeout
  timeout = 30

  environment {
    variables = {
      DESTINATION_S3_BUCKET = aws_s3_bucket.destination_bucket.bucket
    }
  }
}

# S3 Bucket Notification (Trigger Lambda on Object Create Events)
resource "aws_s3_bucket_notification" "source_bucket_notification" {
  bucket = aws_s3_bucket.source_bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.process_json.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

# Lambda Permission to Allow S3 to Trigger the Function
resource "aws_lambda_permission" "allow_s3_trigger" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.process_json.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.source_bucket.arn
}