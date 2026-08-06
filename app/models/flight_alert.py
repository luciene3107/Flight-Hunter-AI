from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.models.flight_search import Base


class FlightAlertModel(Base):

    __tablename__ = "flight_alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    flight_number = Column(
        String,
        nullable=False
    )

    origin = Column(
        String,
        nullable=False
    )

    destination = Column(
        String,
        nullable=False
    )

    departure_date = Column(
        String,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )