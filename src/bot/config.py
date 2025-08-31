from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token_file: str = "BOT_TOKEN_FILE"
    bot_token: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    def __init__(self):
        super().__init__()

        token_path = Path(self.bot_token_file)
        if not token_path.exists():
            raise FileNotFoundError(f"Bot token file not found: {token_path}")

        self.bot_token = token_path.read_text().strip()
