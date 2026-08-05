from app.services.flight_service import FlightService
from app.services.europe_search_service import EuropeSearchService
from app.schemas.search import FlightSearch


class FlightTools:

    def __init__(self):

        self.service = FlightService()
        self.europe_service = EuropeSearchService()


    def search_flights(self, search):

        return self.service.search(search)


    def search_flexible_flights(self, search):

        print("🌍 Busca flexível iniciada")

        destinations = self.europe_service.get_destinations()

        dates = self.europe_service.generate_dates(
            search.months
        )

        flights = []


        for city, airport in destinations.items():

            for date in dates:

                print(
                    f"🔎 Buscando {city} - {date}"
                )


                flexible_search = FlightSearch(

                    origin=search.origin,

                    destination=airport,

                    departure_date=date,

                    return_date=None,

                    max_price=search.max_price
                )


                result = self.service.search(
                    flexible_search
                )


                flights.extend(result)


        return flights