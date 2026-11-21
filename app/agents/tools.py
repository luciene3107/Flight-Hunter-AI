import json

from app.catalog.destination_service import DestinationService
from app.core.logger import logger
from app.schemas.search import FlightSearch
from app.services.airport_service import AirportService
from app.services.europe_search_service import EuropeSearchService
from app.services.flight_service import FlightService


TOOL_DEFINITIONS = [
    {
        "name": "find_airport_code",
        "description": (
            "Converte o nome de uma cidade no código IATA do aeroporto "
            "(ex.: 'Rio de Janeiro' -> 'GIG'). Retorna null se não encontrar."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "Nome da cidade."},
            },
            "required": ["city"],
        },
    },
    {
        "name": "list_destinations",
        "description": (
            "Lista os destinos monitorados de uma região (cidade -> código IATA). "
            "Use para buscas abertas como 'Europa barata'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "region": {"type": "string", "description": "Ex.: 'Europe'."},
            },
            "required": ["region"],
        },
    },
    {
        "name": "search_flights",
        "description": (
            "Busca voos reais (Google Flights) entre dois aeroportos em uma data. "
            "Retorna os mais baratos, ordenados por preço, em BRL."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "origin": {"type": "string", "description": "IATA de origem."},
                "destination": {"type": "string", "description": "IATA de destino."},
                "departure_date": {"type": "string", "description": "YYYY-MM-DD."},
                "return_date": {
                    "type": "string",
                    "description": "YYYY-MM-DD. Omita para só ida.",
                },
                "max_price": {
                    "type": "number",
                    "description": "Preço máximo em BRL. 0 ou omitido = sem limite.",
                },
            },
            "required": ["origin", "destination", "departure_date"],
        },
    },
]


class FlightTools:
    """Ferramentas do agente. Guarda em `self.flights` todos os voos encontrados."""

    def __init__(self):
        self.service = FlightService()
        self.europe_service = EuropeSearchService()
        self.destinations = DestinationService()
        self.airports = AirportService()
        self.flights = []

    # ---- caminho deterministico (requisicoes estruturadas da API) ----

    def search_flights(self, search):

        result = self.service.search(search)

        self.flights.extend(result)

        return result

    def search_flexible_flights(self, search):

        logger.info("Busca flexivel iniciada")

        dates = self.europe_service.generate_dates(search.months or 6)

        for city, airport in self.europe_service.get_destinations().items():

            for date in dates:

                logger.info(f"Buscando {city} - {date}")

                self.search_flights(
                    FlightSearch(
                        origin=search.origin,
                        destination=airport,
                        departure_date=date,
                        return_date=None,
                        max_price=search.max_price,
                    )
                )

        return self.flights

    # ---- caminho do agente LLM ----

    def execute(self, name: str, args: dict) -> str:
        """Executa uma tool pedida pelo Claude e devolve o resultado como JSON."""

        try:

            if name == "find_airport_code":
                return json.dumps({"iata": self.airports.get_code(args["city"])})

            if name == "list_destinations":
                return json.dumps(
                    self.destinations.get_all_cities(args["region"]),
                    ensure_ascii=False,
                )

            if name == "search_flights":
                search = FlightSearch(
                    origin=args["origin"].upper(),
                    destination=args["destination"].upper(),
                    departure_date=args["departure_date"],
                    return_date=args.get("return_date") or None,
                    max_price=args.get("max_price") or 0,
                )

                flights = self.search_flights(search)

                return json.dumps(
                    [f.model_dump() for f in flights], ensure_ascii=False
                )

            return json.dumps({"error": f"Tool desconhecida: {name}"})

        except Exception as e:

            logger.error(f"Erro na tool {name}: {e}")

            return json.dumps({"error": str(e)})
