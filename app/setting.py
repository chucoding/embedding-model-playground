from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Settings class for configuration

    This class provides a configuration interface for various settings used in the application.
    It uses the Pydantic BaseSettings class to load settings from environment variables.
    """
    OPENAI_API_KEY: str = ""             # OpenAI API key
    NCP_CLOVASTUDIO_API_KEY: str = ""    # NCP Clova Studio API key

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
