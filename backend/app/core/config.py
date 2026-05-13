from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """从环境变量或 `.env` 加载应用配置。"""

    app_name: str = "Driving Scene Multimodal Review Workbench"
    app_env: str = "local"
    database_url: str = "sqlite:///./data/app.sqlite3"
    upload_dir: str = "./data/uploads"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
