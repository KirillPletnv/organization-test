from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://orgs_user:orgs_password@localhost:5432/orgs_db"
    API_KEY: str = "secret-api-key-12345"
    DEBUG: bool = True
    APP_NAME: str = "Organization Directory"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()  