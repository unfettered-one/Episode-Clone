resource "aws_iam_policy" "lambda_dynamodb_policy" {
  name        = "${var.service_name}-lambda-dynamodb-policy-${var.stage}"
  description = "IAM policy for Lambda to access DynamoDB tables for ${var.service_name}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DynamoDBAccess"
        Effect = "Allow"
        Action = [
          "dynamodb:*Item",
        ]
        Resource = "arn:aws:dynamodb:${var.region}:*:table/${var.service_name}-*"
      },
      {
        Sid    = "DynamoDBIndexAccess"
        Effect = "Allow"
        Action = [
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = "arn:aws:dynamodb:${var.region}:*:table/${var.service_name}-*/index/*"
      },
      {
        Sid    = "S3Access"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket",
          "s3:*"
        ]
        Resource = "arn:aws:s3:::${var.service_name}-*"
      }
    ]
  })

  tags = {
    Name        = "${var.service_name}-lambda-dynamodb-policy"
    Environment = var.stage
    Service     = var.service_name
  }
}
