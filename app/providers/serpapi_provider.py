import requests

from app.core.config import settings
from app.providers.parsers.serpapi_parser import SerpApiParser
from app.core.logger import logger


class SerpApiProvider:

    BASE_URL = "https://serpapi.com/search.json"

    def search(self, search):

        params = {
            "engine": "google_flights",
            "departure_id": search.origin,
            "arrival_id": search.destination,
            "outbound_date": search.departure_date,
            "return_date": search.return_date,
            "currency": settings.CURRENCY,
            "hl": settings.LANGUAGE,
            "gl": settings.COUNTRY,
            "api_key": settings.SERPAPI_API_KEY,
        }

        # Sem data de volta, o Google Flights exige type=2 (somente ida)
        if not search.return_date:
            params["type"] = 2

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:
            raise Exception(f"SerpApi: {data['error']}")

        flights = SerpApiParser.parse(data)

        logger.info(f"Best Flights: {len(data.get('best_flights', []))}")

        logger.info(f"Other Flights: {len(data.get('other_flights', []))}")

        logger.info(f"Total processado: {len(flights)}")

        return flights