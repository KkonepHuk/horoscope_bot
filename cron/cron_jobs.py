from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from cron.send_horoscopes import send_all_horoscopes_to_all_users
from horoscope_maker.main import get_all_horoscopes

def setup_cron_jobs():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        send_all_horoscopes_to_all_users,
        CronTrigger(hour=9, minute=0),  # Каждый день в 9:00
        #CronTrigger(minute='*'), # Каждую минуту
        name='Send daily horoscopes to users'
    )

    scheduler.add_job(
        get_all_horoscopes,
        CronTrigger(hour=0, minute=5),
        name='Generate daily horoscopes'
    )
    scheduler.start()
