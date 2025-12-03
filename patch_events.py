from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from storage import load_events, save_events
from patch_reminders import scheduler, OUTPUT_EVENTS_ID

dp = Router()

# CallbackData для кнопок
event_cb = CallbackData("event", "action", "index")

INPUT_GROUP = -5012773570  # Группа для записи мероприятий
OUTPUT_GROUP = OUTPUT_EVENTS_ID  # Группа для просмотра и напоминаний

@dp.message(Command("add_event"))
async def add_event(message: types.Message):
    """Добавление мероприятия форматом: /add_event Название | YYYY-MM-DD | HH:MM | Кол-во"""
    try:
        text = message.text.split(" ", 1)[1]
        title, date, time, people = map(str.strip, text.split("|"))
        event = {"title": title, "date": date, "time": time, "people": people}
        events = load_events()
        events.append(event)
        save_events(events)
        await message.answer(f"Мероприятие '{title}' добавлено!")
        # Планируем напоминание за день
        from patch_reminders import schedule_event_reminder
        schedule_event_reminder(event)
    except Exception:
        await message.answer("Ошибка формата! Используй: /add_event Название | YYYY-MM-DD | HH:MM | Кол-во")

@dp.message(Command("list_events"))
async def list_events(message: types.Message):
    events = load_events()
    if not events:
        await message.answer("Список мероприятий пуст.")
        return
    for i, e in enumerate(events):
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("Удалить", callback_data=event_cb.new(action="delete", index=i)),
            InlineKeyboardButton("Редактировать", callback_data=event_cb.new(action="edit", index=i))
        )
        await message.answer(
            f"{i+1}. {e['title']} | {e['date']} {e['time']} | {e['people']} чел",
            reply_markup=kb
        )

@dp.callback_query(event_cb.filter())
async def callback_event(call: types.CallbackQuery, callback_data: dict):
    index = int(callback_data["index"])
    action = callback_data["action"]
    events = load_events()
    if action == "delete":
        if 0 <= index < len(events):
            removed = events.pop(index)
            save_events(events)
            await call.message.edit_text(f"Мероприятие '{removed['title']}' удалено!")
        await call.answer()
    elif action == "edit":
        await call.answer("Редактирование пока не реализовано.")
