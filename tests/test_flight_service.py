from app.services.flight_service import FlightService
from app.schemas.search import FlightSearch

params = FlightSearch(
    origin="GIG",
    destination="JPA",
    departure_date="2026-11-10",
    return_date="2026-11-15",
    max_price=2000
)


service = FlightService()

result = service.search(params)

print("\n✈️ Resultado:")
for flight in result:
    print(flight)