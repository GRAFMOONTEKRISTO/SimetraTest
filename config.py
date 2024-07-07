from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return (f"postgresql+asyncpg://"
                f"{self.DB_USER}:"
                f"{self.DB_PASS}@"
                f"{self.DB_HOST}:"
                f"{self.DB_PORT}/"
                f"{self.DB_NAME}")

    # POSTGRES_DB: str
    # POSTGRES_USER:str
    # POSTGRES_PASSWORD:str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
