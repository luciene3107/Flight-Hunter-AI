from app.schemas.flight import Flight


def search_flights(
    origin,
    destination,
    departure_date,
    return_date=None
):

    return [
        Flight(
            company="Azul",
            price=820,
            duration="2h 45min",
            stops=0,
            departure_airport=origin,
            departure_time="08:00",
            arrival_airport=destination,
            arrival_time="10:45",
            flight_number="AD820"
        ),

        Flight(
            company="LATAM",
            price=910,
            duration="3h 10min",
            stops=1,
            departure_airport=origin,
            departure_time="12:30",
            arrival_airport=destination,
            arrival_time="15:40",
            flight_number="LA910"
        ),

        Flight(
            company="Gol",
            price=980,
            duration="3h 20min",
            stops=1,
            departure_airport=origin,
            departure_time="18:00",
            arrival_airport=destination,
            arrival_time="21:20",
            flight_number="G3980"
        )
    ]