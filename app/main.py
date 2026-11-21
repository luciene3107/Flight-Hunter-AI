import secrets
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import engine
from app.database.deps import get_db
from app.models.flight_search import Base
from app.models import flight_alert  # noqa: F401 (registra a tabela flight_alerts)
from app.repositories.flight_repository import FlightRepository
from app.scheduler.runner import start_scheduler
from app.schemas.search import FlightSearch
from app.schemas.search_response import SearchResponse
from app.agents.flight_agent import FlightAgent


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Garante que todas as tabelas existam antes de usar o banco.
    # Nao derruba a aplicacao se o banco estiver temporariamente indisponivel.
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"⚠️ [Startup] Nao foi possivel criar as tabelas agora: {e}")

    # Inicia o scheduler quando a API sobe
    scheduler = start_scheduler()

    yield

    # Encerra o scheduler quando a API é desligada
    scheduler.shutdown()


app = FastAPI(
    title="Flight Hunter AI",
    version="1.0.0",
    description="API do agente inteligente para monitoramento de passagens aéreas.",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Bem-vinda ao Flight Hunter AI ✈️",
    }


@app.post("/search", response_model=SearchResponse)
def create_search(
    search: FlightSearch,
    db: Session = Depends(get_db),
):

    agent = FlightAgent()

    flights = agent.run(search)


    repository = FlightRepository(db)
    repository.save(search)


    return {
        "message": f"{len(flights)} voo(s) encontrado(s)",
        "max_price": search.max_price,
        "flights": flights,
    }


class AskRequest(BaseModel):
    message: str


def require_api_key(x_api_key: str | None = Header(default=None)):
    """Protege o /ask: exige o header X-API-Key igual a ASK_API_KEY."""

    if not settings.ASK_API_KEY:
        raise HTTPException(
            status_code=503, detail="ASK_API_KEY nao configurada no servidor."
        )

    if not x_api_key or not secrets.compare_digest(
        x_api_key, settings.ASK_API_KEY
    ):
        raise HTTPException(status_code=401, detail="API key invalida.")


@app.post("/ask", dependencies=[Depends(require_api_key)])
def ask(request: AskRequest):
    """Pergunta em linguagem natural: o agente (Claude) decide o que buscar."""

    try:
        flights = FlightAgent().run(request.message)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return {
        "answer": flights.answer,
        "flights": flights,
    }


@app.get("/searches")
def list_searches(db: Session = Depends(get_db)):

    repository = FlightRepository(db)

    searches = repository.get_all()

    return {
        "total": len(searches),
        "searches": searches,
    }