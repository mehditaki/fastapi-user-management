"""Fastapi application config."""

from omegaconf import OmegaConf
from pydantic import EmailStr

from fastapi_user_management import __version__
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_CUSTOM_CONFIG = OmegaConf.load("settings.yaml")
class Settings(BaseSettings):
    SECRET_KEY: str = "1b4b4007cad00857be4cbc27e6b73882f4ba6344e10cbb45f667ca9c72ed821f"

    ADMIN_FULLNAME: str
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str

    TITLE: str = APP_CUSTOM_CONFIG.fastapi.title
    DESCRIPTION: str = APP_CUSTOM_CONFIG.fastapi.description

    VERSION: str = __version__

    DOCS_URL: str = APP_CUSTOM_CONFIG.fastapi.docs_url
    REDOC_URL: str = APP_CUSTOM_CONFIG.fastapi.redoc_url

    ALGORITHM: str = APP_CUSTOM_CONFIG.fastapi.algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        APP_CUSTOM_CONFIG.fastapi.access_token_expire_minutes
    )

    DATABASE_URI: str = APP_CUSTOM_CONFIG.database.uri
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


SETTINGS = Settings()
