import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    REFRESH_TOKEN_EXPIRE_MINUTES: str
    REFRESH_TOKEN_SECRET_KEY: str

    BASE_URL: str
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
   
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    def get_media_dir(self):
        MEDIA_DIR: str = os.path.join("app", "media")
        os.makedirs(MEDIA_DIR, exist_ok=True)

        return MEDIA_DIR

        
settings = Settings()