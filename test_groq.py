from app.llm.client import LLMClient

llm = LLMClient.get_llm()

response = llm.invoke(
    "Responda apenas com a palavra: Conectado"
)

print(response.content)