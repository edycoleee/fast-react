from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Fast Boiler"
    app_env: str = "development"
    log_level: str = "INFO"
    db_url: str = "postgresql+psycopg://fast_boiler:fast_boiler@postgres:5432/fast_boiler"


settings = Settings()

