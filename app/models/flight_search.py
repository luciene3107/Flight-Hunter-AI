from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class FlightSearchModel(Base):

    __tablename__ = "flight_searches"

    id = Column(
        Integer,
        primary_key=True,
        index=True
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

    return_date = Column(
        String,
        nullable=True
    )

    max_price = Column(
        Float,
        nullable=False
    )

    active = Column(
        Boolean,
        default=True
    )

    last_price = Column(
        Float,
        nullable=True
    )