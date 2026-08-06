from app.services.flight_service import FlightService
from app.schemas.search import FlightSearch

params = FlightSearch(
    origin="GIG",
    destination="FCO",
    departure_date="2027-03-16",
    return_date="2027-03-30",
    max_price=5000
)


service = FlightService()

result = service.search(params)

print("\n✈️ Resultado:")
for flight in result:
    print(flight)