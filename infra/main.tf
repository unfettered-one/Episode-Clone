module "auth_service" {
  source = "github.com/unfettered-one/Infra//core?ref=main"

  service_name = "episode"
  stage        = var.stage
  region       = var.region

  use_container = true
  use_zip       = false
  use_ecr       = false

  lambda_image_uri = var.lambda_image_uri
  lambda_handler   = "episode.main.mangum_handler"

  lambda_execution_policy_arn = aws_iam_policy.lambda_dynamodb_policy.arn
  environment_variables = {
    ENVIRONMENT              = var.stage
    JWT_SECRET_KEY           = data.aws_ssm_parameter.jwt_secret.value
    GEMINI_API_KEY           = data.aws_ssm_parameter.GEMINI_API_KEY.value
    HUGGINGFACEHUB_API_TOKEN = data.aws_ssm_parameter.HUGGINGFACEHUB_API_TOKEN.value
    story_docs_path          = "./app/story_docs"
    vector_db_path           = "./app/vector_db"
    gemini_model_name        = "gemini-2.5-flash"
  }

  create_http_api = false
  enable_dynamodb = false
}
