from app.agents.flight_agent import FlightAgent


message = "Quero viajar do Rio de Janeiro para João Pessoa dia 10/12/2026 até R$1500"

result = FlightAgent().run(message)

print("\n🤖", result.answer)

for flight in result:
    print(flight)
