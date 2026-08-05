class FlightPlanner:

    def create_plan(self, search):

        if search.search_type == "flexible":

            return [
                {
                    "tool": "search_flexible_flights",
                    "params": search
                }
            ]

        return [
            {
                "tool": "search_flights",
                "params": search
            }
        ]