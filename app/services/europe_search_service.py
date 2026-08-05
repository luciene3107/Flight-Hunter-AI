from datetime import datetime, timedelta

from app.catalog.destination_service import DestinationService


class EuropeSearchService:

    def __init__(self):
        self.destination_service = DestinationService()

    def generate_dates(self, months=6):

        today = datetime.today()

        dates = []

        for month in range(months):

            date = today + timedelta(days=30 * month)

            dates.append(
                date.strftime("%Y-%m-%d")
            )

        return dates

    def get_destinations(self):

        return self.destination_service.get_all_cities("Europe")