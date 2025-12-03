from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from storage import load_events, load_notes
from main import bot

dp = None  # Патч не имеет команд, только scheduler
scheduler = AsyncIOScheduler()
scheduler.start()

OUTPUT_EVENTS_ID = -1003264984732
OUTPUT_NOTES_ID = -1003264984732

def schedule_event_reminder(event):
    event_dt = datetime.strptime(event['date'] + " " + event['time'], "%Y-%m-%d %H:%M")
    remind_time = event_dt - timedelta(days=1)
    if remind_time > datetime.now():
        scheduler.add_job(send_event_reminder, "date", run_date=remind_time, args=[event])

def schedule_note_reminder(title, dt):
    if dt > datetime.now():
        scheduler.add_job(send_note_reminder, "date", run_date=dt, args=[title])

async def send_event_reminder(event):
    await bot.send_message(OUTPUT_EVENTS_ID,
        f"Напоминание о мероприятии:\n{event['title']} | {event['date']} {event['time']} | {event['people']} чел"
    )

async def send_note_reminder(title):
    await bot.send_message(OUTPUT_NOTES_ID,
        f"Напоминание о заметке:\n{title}"
    )

# Планируем все существующие события при старте
for e in load_events():
    schedule_event_reminder(e)
for n in load_notes():
    dt = datetime.strptime(n['datetime'], "%Y-%m-%d %H:%M")
    schedule_note_reminder(n['title'], dt)
