from app.agents.flight_agent import FlightAgent


agent = FlightAgent()


message = """
Quero encontrar passagens baratas para Europa
nos próximos 6 meses saindo do Rio de Janeiro.
"""


result = agent.run(message)


print("\n✈️ Resultado:")
print(result)