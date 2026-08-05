from app.schemas.flight import Flight


class SerpApiParser:

    @staticmethod
    def parse(data: dict) -> list[Flight]:

        flights = []

        all_results = (
            data.get("best_flights", [])
            + data.get("other_flights", [])
        )

        for item in all_results:

            segments = item.get("flights", [])

            if not segments:
                continue

            first = segments[0]
            last = segments[-1]

            total_minutes = item.get("total_duration", 0)

            hours = total_minutes // 60
            minutes = total_minutes % 60

            duration = f"{hours}h {minutes}min"

            flights.append(
                Flight(
                    company=first.get("airline", "Unknown"),
                    price=float(item.get("price", 0)),
                    duration=duration,
                    stops=max(len(segments) - 1, 0),

                    departure_airport=first["departure_airport"]["id"],
                    departure_time=first["departure_airport"]["time"],

                    arrival_airport=last["arrival_airport"]["id"],
                    arrival_time=last["arrival_airport"]["time"],

                    flight_number=first.get("flight_number", ""),
                )
            )

        return flights