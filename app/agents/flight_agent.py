from datetime import date

from app.agents.planner import FlightPlanner
from app.agents.tools import TOOL_DEFINITIONS, FlightTools
from app.core.config import settings
from app.core.logger import logger
from app.llm.client import LLMClient

MAX_STEPS = 12


class AgentResult(list):
    """Lista de voos (compatível com o uso antigo) + resposta em texto do agente."""

    answer: str = ""


class FlightAgent:

    def __init__(self):

        self.planner = FlightPlanner()

    def run(self, search) -> AgentResult:
        """
        - str: linguagem natural -> loop de tool use com o Claude.
        - FlightSearch: requisição estruturada -> plano determinístico (sem LLM).
        """

        tools = FlightTools()

        if isinstance(search, str):
            answer = self._run_llm(search, tools)
        else:
            answer = self._run_plan(search, tools)

        result = AgentResult(self._dedupe(tools.flights))
        result.answer = answer

        return result

    # ---- plano fixo ----

    def _run_plan(self, search, tools):

        for action in self.planner.create_plan(search):

            getattr(
                tools, action["tool"]
            )(action["params"])

        return ""

    # ---- agente com Claude ----

    def _run_llm(self, message: str, tools: FlightTools) -> str:

        client = LLMClient.get_client()

        with open("app/prompts/agent_system.txt", encoding="utf-8") as f:
            system = f.read().format(today=date.today().isoformat())

        messages = [{"role": "user", "content": message}]

        for _ in range(MAX_STEPS):

            response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=2048,
                system=system,
                tools=TOOL_DEFINITIONS,
                messages=messages,
            )

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":

                return "".join(
                    block.text for block in response.content if block.type == "text"
                )

            results = []

            for block in response.content:

                if block.type == "tool_use":

                    logger.info(f"[Agent] {block.name}({block.input})")

                    results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tools.execute(block.name, block.input),
                        }
                    )

            messages.append({"role": "user", "content": results})

        logger.warning("Agente atingiu o limite de passos.")

        return "Não consegui concluir a busca dentro do limite de passos."

    @staticmethod
    def _dedupe(flights):

        unique = {}

        for f in flights:

            unique.setdefault((f.flight_number, f.departure_time, f.price), f)

        return sorted(unique.values(), key=lambda f: f.price)
