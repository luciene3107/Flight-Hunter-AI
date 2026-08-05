from app.providers.mock_provider import search_flights as mock_search_flights
from app.providers.serpapi_provider import SerpApiProvider
from app.core.logger import logger


class FlightService:

    def __init__(self):
        self.serpapi_provider = SerpApiProvider()


    def search(self, search_params):

        logger.info(
            f"Preço máximo recebido: {search_params.max_price}"
        )


        # Busca na SerpApi
        try:

            flights = self.serpapi_provider.search(search_params)

        except Exception as e:

            logger.error(
                f"Erro ao buscar na SerpApi: {e}"
            )

            flights = []


        # Fallback para MockProvider
        if not flights:

            logger.warning(
                "SerpApi sem retorno. Usando MockProvider..."
            )

            flights = mock_search_flights(
                origin=search_params.origin,
                destination=search_params.destination,
                departure_date=search_params.departure_date,
                return_date=search_params.return_date,
            )


        # Filtra pelo preço máximo somente quando informado
        if search_params.max_price > 0:

            filtered_flights = [
                flight
                for flight in flights
                if flight.price <= search_params.max_price
            ]

        else:

            filtered_flights = flights


        if flights and not filtered_flights:

            logger.warning(
                "Nenhum voo encontrado dentro do preço máximo informado."
            )


        # Ordena pelo menor preço
        filtered_flights.sort(
            key=lambda flight: flight.price
        )


        # Retorna somente os 10 mais baratos
        filtered_flights = filtered_flights[:10]


        logger.info(
            f"{len(filtered_flights)} voo(s) retornado(s)."
        )


        return filtered_flights