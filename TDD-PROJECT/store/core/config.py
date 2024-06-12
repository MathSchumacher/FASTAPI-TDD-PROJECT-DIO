from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"

    DATABASE_URL: str = "mongodb://localhost:27017"

    model_config = SettingsConfigDict(env_file=".eny")


settings = Settings()
