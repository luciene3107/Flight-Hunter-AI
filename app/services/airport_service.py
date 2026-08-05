import csv
import os
import unicodedata

from rapidfuzz import process, fuzz


class AirportService:

    def __init__(self):
        self.airports = self.load_airports()

    def normalize(self, text):

        if not text:
            return ""

        text = text.lower().strip()

        text = unicodedata.normalize("NFD", text)

        text = "".join(char for char in text if unicodedata.category(char) != "Mn")

        return text

    def load_airports(self):

        airports = {}

        file_path = os.path.join("app", "data", "airports.csv")

        with open(file_path, encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                city = row.get("municipality")
                iata = row.get("iata_code")
                airport_type = row.get("type")

                # Ignora aeroportos sem cidade ou sem código IATA
                if not city or not iata:
                    continue

                # Mantém apenas aeroportos comerciais
                if airport_type not in ["large_airport", "medium_airport"]:
                    continue

                city_normalized = self.normalize(city)

                if city_normalized not in airports:

                    airports[city_normalized] = iata

        return airports

    def get_code(self, city):
        if not city:
            return None


        normalized_city = self.normalize(city)


        # Busca exata
        if normalized_city in self.airports:

            return self.airports[
                normalized_city
            ]


        # Busca por início do nome
        starts_with_matches = [
            name
            for name in self.airports.keys()
            if name.startswith(normalized_city)
        ]


        if starts_with_matches:

            match = starts_with_matches[0]

            print(
                f"🔎 Aeroporto encontrado por início: "
                f"{city} → {match}"
            )

            return self.airports[match]


        # Busca aproximada
        result = process.extractOne(
            normalized_city,
            self.airports.keys(),
            scorer=fuzz.WRatio
        )


        if result:

            match, score, _ = result

            print(
                f"🔎 Aeroporto aproximado: "
                f"{city} → {match} ({score}%)"
            )


            if score >= 85:

                return self.airports[match]


        print(
            f"⚠️ Aeroporto não encontrado: {city}"
        )

        return None