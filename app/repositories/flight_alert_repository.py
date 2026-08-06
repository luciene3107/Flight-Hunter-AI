from app.models.flight_alert import FlightAlertModel


class FlightAlertRepository:

    def __init__(self, db):
        self.db = db


    def exists(self, flight, search):

        alert = (
            self.db.query(FlightAlertModel)
            .filter(
                FlightAlertModel.flight_number == flight.flight_number,
                FlightAlertModel.origin == flight.departure_airport,
                FlightAlertModel.destination == flight.arrival_airport,
                FlightAlertModel.departure_date == str(search.departure_date),
            )
            .first()
        )

        return alert is not None


    def save(self, flight, search):

        alert = FlightAlertModel(
            flight_number=flight.flight_number,
            origin=flight.departure_airport,
            destination=flight.arrival_airport,
            departure_date=str(search.departure_date),
            price=flight.price,
        )

        self.db.add(alert)
        self.db.commit()