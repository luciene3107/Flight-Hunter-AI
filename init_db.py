from app.database.connection import engine
from app.models.flight_search import Base
from app.models import flight_alert  # noqa: F401 (registra a tabela flight_alerts)

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso! 🎉")