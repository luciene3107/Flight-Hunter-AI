from sqlalchemy.orm import Session

from app.models.flight_search import FlightSearchModel
from app.schemas.search import FlightSearch


class FlightRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, search: FlightSearch):

        db_search = FlightSearchModel(
            origin=search.origin,
            destination=search.destination,
            departure_date=search.departure_date,
            return_date=search.return_date,
            max_price=search.max_price,
            active=True,
            last_price=None
        )

        self.db.add(db_search)
        self.db.commit()
        self.db.refresh(db_search)

        return db_search

    def get_all(self):
        return self.db.query(FlightSearchModel).all()

    def get_active_searches(self):
        return (
            self.db.query(FlightSearchModel)
            .filter(FlightSearchModel.active == True)
            .all()
        )

    def update_last_price(self, search_id: int, price: float):

        search = (
            self.db.query(FlightSearchModel)
            .filter(FlightSearchModel.id == search_id)
            .first()
        )

        if search:
            search.last_price = price
            self.db.commit()

        return search

    def disable_search(self, search_id: int):

        search = (
            self.db.query(FlightSearchModel)
            .filter(FlightSearchModel.id == search_id)
            .first()
        )

        if search:
            search.active = False
            self.db.commit()

        return search