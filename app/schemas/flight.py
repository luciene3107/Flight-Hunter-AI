from pydantic import BaseModel


class Flight(BaseModel):
    company: str
    price: float
    duration: str
    stops: int

    departure_airport: str
    departure_time: str

    arrival_airport: str
    arrival_time: str

    flight_number: str