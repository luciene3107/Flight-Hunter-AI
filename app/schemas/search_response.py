from pydantic import BaseModel

from app.schemas.flight import Flight


class SearchResponse(BaseModel):
    message: str
    max_price: float
    flights: list[Flight]