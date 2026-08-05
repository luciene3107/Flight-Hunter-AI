import json

from app.llm.client import LLMClient


class FlightExtractor:

    def __init__(self):
        self.llm = LLMClient.get_llm()

        with open(
            "app/prompts/extract_search.txt",
            encoding="utf-8"
        ) as f:

            self.prompt = f.read()

    def extract(self, user_message: str):

        response = self.llm.invoke(
            [
                (
                    "system",
                    self.prompt
                ),
                (
                    "human",
                    user_message
                )
            ]
        )

        return json.loads(response.content)