data "aws_ssm_parameter" "jwt_secret" {
  name            = "jwt_secret"
  with_decryption = true
}

data "aws_ssm_parameter" "GEMINI_API_KEY" {
  name            = "GEMINI_API_KEY"
  with_decryption = true
}

data "aws_ssm_parameter" "HUGGINGFACEHUB_API_TOKEN" {
  name            = "HUGGINGFACEHUB_API_TOKEN"
  with_decryption = true
}

data "aws_ssm_parameter" "episode_base_url" {
  name            = "episode_base_url"
  with_decryption = true
}
