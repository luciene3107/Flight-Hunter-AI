from app.services.europe_search_service import EuropeSearchService


service = EuropeSearchService()


print(
    service.get_destinations()
)


print(
    service.generate_dates(6)
)