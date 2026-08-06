from app.database.connection import SessionLocal
from app.repositories.flight_repository import FlightRepository


db = SessionLocal()

try:
    repository = FlightRepository(db)

    searches = repository.get_all()

    for search in searches:
        print(
            f"ID: {search.id} | "
            f"{search.origin} -> {search.destination} | "
            f"Preço: {search.max_price}"
        )

finally:
    db.close()