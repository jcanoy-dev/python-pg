from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Removing Field() keeps them required but tells Pylance/Pydantic 
    # to look at system environment variables if no .env file exists.
    CLOUDFLARE_ACCOUNT_ID: str
    CLOUDFLARE_API_TOKEN: str
    D1_DATABASE_ID: str

    # env_file_encoding ensures it reads the file correctly locally
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
