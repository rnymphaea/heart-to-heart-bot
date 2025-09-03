from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from aiogram import Bot

class Settings(BaseSettings):
    bot_token_file: str = "/run/secrets/bot_token"
    postgres_password_file: str = "/run/secrets/postgres_password"

    postgres_user: str = "postgres"
    postgres_db_name: str = "h2hdb"
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
        
    @property
    def bot_token(self) -> str:
        token_path = Path(self.bot_token_file)
        if not token_path.exists():
            raise FileNotFoundError(f"Bot token file not found: {token_path}")

        return token_path.read_text().strip()


    @property
    def database_url(self) -> str:
        url = self._database_url(engine="asyncpg")
        return url
    
    @property
    def database_migrate_url(self) -> str:
        url = self._database_url(engine="psycopg2")
        return url
    
    def _database_url(self, engine: str) -> str:
        pg_pass_path = Path(self.postgres_password_file)
        if not pg_pass_path.exists():
            raise FileNotFoundError(f"Postgres password file not found: {pg_pass_path}")

        password = pg_pass_path.read_text().strip()

        return (
            f"postgresql+{engine}://{self.postgres_user}:"
            f"{password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db_name}"
        )



settings = Settings()
bot = Bot(token=settings.bot_token) 
