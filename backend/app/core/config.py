from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Fast Boiler"
    app_env: str = "development"
    log_level: str = "INFO"
    db_url: str = "postgresql+psycopg://fast_boiler:fast_boiler@postgres:5432/fast_boiler"
    secret_key: str = "replace-with-at-least-32-characters-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    seed_admin_email: str = "admin@example.com"
    seed_admin_username: str = "admin"
    seed_admin_password: str = "admin123"


settings = Settings()
