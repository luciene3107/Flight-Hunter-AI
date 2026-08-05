import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class LLMClient:

    @staticmethod
    def get_llm():

        return ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=os.getenv("MODEL_NAME"),
            temperature=0
        )