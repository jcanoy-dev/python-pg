from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Field() tells Pylance these will be populated automatically by Pydantic
    CLOUDFLARE_ACCOUNT_ID: str = Field(default=...)
    CLOUDFLARE_API_TOKEN: str = Field(default=...)
    D1_DATABASE_ID: str = Field(default=...)
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
