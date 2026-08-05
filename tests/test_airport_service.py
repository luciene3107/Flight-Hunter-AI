from app.services.airport_service import AirportService


airport = AirportService()


cities = [
    "Rio de Janeiro",
    "rio",
    "joao pessoa",
    "Paris",
    "New York",
    "Madrid"
]


for city in cities:
    print(
        city,
        "→",
        airport.get_code(city)
    )