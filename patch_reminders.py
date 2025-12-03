from aiogram import Router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from storage import load_events, load_notes
from patch_events import send_event_reminder
from patch_notes import send_note_reminder

dp = Router()
scheduler = AsyncIOScheduler()
scheduler.start()

OUTPUT_EVENTS_ID = -1003264984732  # группа для мероприятий
OUTPUT_NOTES_ID = -1003264984732   # группа для заметок

bot_instance = None

def set_bot(bot):
    global bot_instance
    bot_instance = bot

# --- Еженедельный отчёт ---
def weekly_report():
    now = datetime.now()
    week_end = now + timedelta(days=7)
    events = load_events()
    message = "📅 Предстоящие мероприятия на неделю:\n\n"
    days = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

    for e in events:
        event_dt = datetime.strptime(e['date'] + " " + e['time'], "%Y-%m-%d %H:%M")
        if now <= event_dt <= week_end:
            weekday = days[event_dt.weekday()]
            message += f"{weekday}: {e['title']} | {e['date']} {e['time']} | {e['people']} чел\n"

    if bot_instance and message.strip():
        import asyncio
        asyncio.create_task(bot_instance.send_message(OUTPUT_EVENTS_ID, message))

# --- Срочные уведомления (меньше 6 дней до события) ---
def check_urgent_events():
    events = load_events()
    now = datetime.now()
    import asyncio
    for e in events:
        event_dt = datetime.strptime(e['date'] + " " + e['time'], "%Y-%m-%d %H:%M")
        delta = event_dt - now
        if timedelta(0) < delta < timedelta(days=6):
            asyncio.create_task(send_event_reminder(bot_instance, e))

# Планируем еженедельный отчёт по понедельникам в 09:00
scheduler.add_job(weekly_report, "cron", day_of_week="mon", hour=9, minute=0)
check_urgent_events()
