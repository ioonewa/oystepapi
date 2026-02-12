from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Bot
    bot_token: str = Field(..., env="BOT_TOKEN")

    # JWT
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_ttl_seconds: int = Field(default=5*60, env="JWT_TTL_SECONDS")

    # Database
    db_host: str = Field(..., env="DB_HOST")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_port: int = Field(default=5432, env="DB_PORT")

    # 2GIS
    map_service_token: str = Field(..., env="MAP_SERVICE_TOKEN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
