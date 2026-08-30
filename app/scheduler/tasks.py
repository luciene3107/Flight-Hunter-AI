from app.database.connection import SessionLocal
from app.repositories.flight_repository import FlightRepository
from app.repositories.flight_alert_repository import FlightAlertRepository
from app.services.flight_service import FlightService
from app.services.telegram_service import TelegramService


def check_flights_job():

    print("⏰ [Scheduler] Executando rotina automática de monitoramento de voos...")

    db = SessionLocal()

    try:
        repository = FlightRepository(db)
        alert_repository = FlightAlertRepository(db)

        searches = repository.get_all()

        # Monitorar somente Madrid e Roma
        searches = [
            search
            for search in searches
            if search.destination in ["MAD", "FCO"]
        ]

        if not searches:
            print("⏰ [Scheduler] Nenhum monitoramento cadastrado no momento.")
            return

        print(
            f"⏰ [Scheduler] Encontrado(s) {len(searches)} monitoramento(s) para verificar."
        )

        service = FlightService()
        telegram = TelegramService()

        for search_model in searches:

            flights = service.search(search_model)

            print(
                f"✈️ [Busca ID {search_model.id}] "
                f"Rota: {search_model.origin} -> {search_model.destination} "
                f"| Voos encontrados: {len(flights)}"
            )

            if flights:

                for flight in flights:

                    if not alert_repository.should_alert(flight, search_model):

                        print(
                            f"⛔ Alerta recente sem queda de preço: {flight.flight_number}"
                        )
                        continue

                    message = (
                        "✈️ *Promoção Encontrada!*\n\n"
                        f"📍 Rota: `{flight.departure_airport} → {flight.arrival_airport}`\n"
                        f"📅 Ida: `{search_model.departure_date}`\n"
                        f"🏢 Companhia: *{flight.company}*\n"
                        f"✈️ Voo: `{flight.flight_number}`\n"
                        f"🕒 Horário: `{flight.departure_time} → {flight.arrival_time}`\n"
                        f"⏱️ Duração: `{flight.duration}`\n"
                        f"🛑 Escalas: `{flight.stops}`\n"
                        f"💰 Preço: *R$ {flight.price:.2f}*\n"
                        f"🎯 Seu teto: *R$ {search_model.max_price:.2f}*"
                    )

                    telegram.send_message(message)

                    alert_repository.save(
                        flight,
                        search_model
                    )

    except Exception as e:
        print(f"❌ [Scheduler] Erro ao executar monitoramento: {e}")

    finally:
        db.close()

    print("⏰ [Scheduler] Verificação concluída com sucesso!")