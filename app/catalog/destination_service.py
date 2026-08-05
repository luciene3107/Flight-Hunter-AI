from app.catalog.destinations import DESTINATIONS


class DestinationService:

    def get_region(self, region: str):

        return DESTINATIONS.get(region, {})


    def get_country(self, region: str, country: str):

        region_data = DESTINATIONS.get(region, {})

        return region_data.get(country, {})


    def get_all_cities(self, region: str):

        cities = {}

        region_data = DESTINATIONS.get(region, {})

        for country in region_data.values():

            cities.update(country)

        return cities