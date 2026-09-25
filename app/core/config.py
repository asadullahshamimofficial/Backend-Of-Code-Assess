from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    FRONTEND_ORIGIN: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
    DB_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()