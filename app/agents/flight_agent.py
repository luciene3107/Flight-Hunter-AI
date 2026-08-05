from app.agents.planner import FlightPlanner
from app.agents.tools import FlightTools
from app.llm.extractor import FlightExtractor
from app.schemas.search import FlightSearch


class FlightAgent:

    def __init__(self):

        self.planner = FlightPlanner()
        self.tools = FlightTools()
        self.extractor = FlightExtractor()


    def run(self, search):

        print("🚀 Agent recebeu:")
        print(search)

        if isinstance(search, str):

            data = self.extractor.extract(search)

            print("🔎 Dados extraídos:")
            print(data)

            search = FlightSearch(**data)

            print("📦 FlightSearch criado:")
            print(search)


        plan = self.planner.create_plan(search)

        print("🧠 Plano:")
        print(plan)

        flights = []


        for action in plan:

            if action["tool"] == "search_flights":

                result = self.tools.search_flights(
                    action["params"]
                )


            elif action["tool"] == "search_flexible_flights":

                result = self.tools.search_flexible_flights(
                    action["params"]
                )


            else:
                result = []


            print("✈️ Resultado da Tool:")
            print(result)

            flights.extend(result)


        return flights