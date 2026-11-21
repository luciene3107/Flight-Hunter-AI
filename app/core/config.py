from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL")

    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")

    CURRENCY = "BRL"

    LANGUAGE = "pt-BR"

    COUNTRY = "br"


settings = Settings()