import anthropic

from app.core.config import settings


class LLMClient:

    @staticmethod
    def get_client() -> anthropic.Anthropic:

        if not settings.ANTHROPIC_API_KEY:
            raise RuntimeError(
                "ANTHROPIC_API_KEY nao configurada. Defina no .env."
            )

        return anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
