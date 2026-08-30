from datetime import datetime, timedelta

from app.models.flight_alert import FlightAlertModel


class FlightAlertRepository:

    # Tempo mínimo entre dois alertas do mesmo voo quando o preço não caiu
    COOLDOWN = timedelta(hours=24)

    def __init__(self, db):
        self.db = db


    def _last_alert(self, flight, search):

        return (
            self.db.query(FlightAlertModel)
            .filter(
                FlightAlertModel.flight_number == flight.flight_number,
                FlightAlertModel.origin == flight.departure_airport,
                FlightAlertModel.destination == flight.arrival_airport,
                FlightAlertModel.departure_date == str(search.departure_date),
            )
            .order_by(FlightAlertModel.created_at.desc())
            .first()
        )


    def should_alert(self, flight, search):

        last = self._last_alert(flight, search)

        # Nunca alertado antes -> envia
        if last is None:
            return True

        # Preço caiu em relação ao último alerta -> vale reenviar
        if flight.price < last.price:
            return True

        # Passou tempo suficiente desde o último alerta -> reenvia
        created_at = last.created_at or datetime.utcnow()

        if datetime.utcnow() - created_at >= self.COOLDOWN:
            return True

        return False


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
