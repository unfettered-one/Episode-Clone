output "lambda_dynamodb_policy_arn" {
  description = "ARN of the Lambda DynamoDB policy"
  value       = aws_iam_policy.lambda_dynamodb_policy.arn
}
