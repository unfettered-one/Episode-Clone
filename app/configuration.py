import os
import json
import logging

from dotenv import load_dotenv
from errorhub.models import EnvironmentEnum

load_dotenv()

LOGGER = logging.getLogger(__name__)


class Settings:
    """
    Configuration settings for the application.
    """

    def __init__(self) -> None:
        self._config = {}
        self._openapi_key = os.getenv("OPENAI_API_KEY", None)
        self._huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN", None)
        self._gemini_key = os.getenv("GEMINI_API_KEY", None)
        self._config["jwt_secret_key"] = os.getenv("JWT_SECRET_KEY", None)
        self.load_env_variable()
        temp_env = os.getenv("ENVIRONMENT")
        if temp_env is not None:
            if temp_env == "production":
                self._config["environment"] = EnvironmentEnum.PRODUCTION
            elif temp_env == "staging":
                self._config["environment"] = EnvironmentEnum.STAGING
            else:
                self._config["environment"] = EnvironmentEnum.DEVELOPMENT
        else:
            self._config["environment"] = EnvironmentEnum.DEVELOPMENT

    def load_env_variable(self):
        config_json = f'{os.getenv("CONFIG_PATH")}/config.json'
        LOGGER.info("Loading config file %s", config_json)
        with open(config_json, encoding="utf-8") as f:
            self._config = json.load(f)

    def vector_db_path(self) -> str:
        """
        Returns the path to the vector database.
        """
        return self._config.get("vector_db_path", "./app/vector_db")

    def story_docs_path(self) -> str:
        """
        Returns the path to the story documents.
        """
        return self._config.get("story_docs_path", "./app/story_docs")

    def huggingface_token(self) -> str | None:
        """
        Returns the Hugging Face token.
        """
        return self._huggingface_token

    def get_gemini_key(self) -> str | None:
        return self._gemini_key

    def get_gemini_model(self) -> str:
        """
        Returns the Gemini model name.
        """
        return self._config["gemini_model_name"]

    def get_base_url(self) -> str:
        """
        Returns the base URL for the application.
        """
        return self._config.get("base_url", "http://127.0.0.1:8000")

    def get_secret_key(self) -> str:
        """
        Returns the secret key for JWT.
        """
        return self._config["jwt_secret_key"]

    def get_jwt_algorithm(self) -> str:
        """
        Returns the JWT algorithm.
        """
        return self._config.get("jwt_algorithm", "HS256")

    def get_environment(self) -> EnvironmentEnum:
        """
        Returns the current environment.
        """
        return self._config["environment"]

    def get_service_name(self) -> str:
        """
        Returns the service name.
        """
        return self._config.get("service_name", "Episode")


settings = Settings()