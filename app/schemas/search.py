from pydantic import BaseModel


class FlightSearch(BaseModel):

    search_type: str = "specific"

    origin: str

    destination: str = ""

    region: str = ""

    country: str = ""

    cities: list[str] = []

    tags: list[str] = []

    departure_date: str = ""

    return_date: str | None = None

    months: int = 0

    flexible_dates: bool = False

    max_price: float = 5000