from apscheduler.schedulers.background import BackgroundScheduler

from app.scheduler.tasks import check_flights_job


def start_scheduler():

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        check_flights_job,
        trigger="interval",
        hours=6, 
        id="flight_monitor",
        replace_existing=True,
    )

    scheduler.start()

    print("🚀 Scheduler iniciado com sucesso!")

    return scheduler