from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str
    
    # API Keys
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
