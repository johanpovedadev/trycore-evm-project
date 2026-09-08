from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    fastapi_env: str = "development"
    debug: bool = True
    secret_key: str = "your-secret-key"

    database_url: str = "postgresql://trycore_user:trycore_password@localhost:5432/trycore_evm"
    db_echo: bool = False

    host: str = "0.0.0.0"
    port: int = 8000

    frontend_url: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
