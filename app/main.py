from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

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


@app.get("/searches")
def list_searches(db: Session = Depends(get_db)):

    repository = FlightRepository(db)

    searches = repository.get_all()

    return {
        "total": len(searches),
        "searches": searches,
    }