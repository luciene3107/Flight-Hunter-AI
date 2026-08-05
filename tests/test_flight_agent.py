from app.agents.flight_agent import FlightAgent


agent = FlightAgent()


message = """
Quero viajar do Rio de Janeiro para João Pessoa
no dia 10/11/2026 até R$600
"""


result = agent.run(message)


print("\n✈️ Resultado final:")

for flight in result:
    print(flight)