from app.database.connection import engine
from app.models.flight_search import Base

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso! 🎉")