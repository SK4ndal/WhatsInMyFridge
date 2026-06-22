from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "WhatsInMyFridge API"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/whats_in_my_fridge"
    allowed_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_prefix="WIMF_")


settings = Settings()
