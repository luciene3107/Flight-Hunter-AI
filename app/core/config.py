from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL")

    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

    CURRENCY = "BRL"

    LANGUAGE = "pt-BR"

    COUNTRY = "br"


settings = Settings()