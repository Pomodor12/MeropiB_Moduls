from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from storage import load_events, save_events
from patch_reminders import OUTPUT_EVENTS_ID, bot_instance

dp = Router()

# --- Функция для отправки уведомлений ---
async def send_event_reminder(bot, event):
    text = f"📌 Напоминание о мероприятии:\n{event['title']} | {event['date']} {event['time']} | {event['people']} чел"
    if bot:
        await bot.send_message(OUTPUT_EVENTS_ID, text)

# --- Добавление мероприятия ---
@dp.message(Command(commands=["add_event"]))
async def add_event(message: types.Message):
    try:
        # Формат ввода: /add_event Название | YYYY-MM-DD | HH:MM | количество человек
        parts = message.text.split("|")
        title = parts[0].replace("/add_event", "").strip()
        date = parts[1].strip()
        time = parts[2].strip()
        people = int(parts[3].strip())
        
        events = load_events()
        event_id = len(events) + 1
        events.append({
            "id": event_id,
            "title": title,
            "date": date,
            "time": time,
            "people": people
        })
        save_events(events)
        await message.answer(f"✅ Мероприятие '{title}' добавлено с id {event_id}.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

# --- Список мероприятий с кнопками удаления ---
@dp.message(Command(commands=["list_events"]))
async def list_events(message: types.Message):
    events = load_events()
    if not events:
        await message.answer("Список мероприятий пуст.")
        return
    for e in events:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Удалить", callback_data=f"del_event:{e['id']}")]
        ])
        await message.answer(f"{e['id']}. {e['title']} | {e['date']} {e['time']} | {e['people']} чел", reply_markup=kb)

# --- Удаление мероприятий через кнопки ---
@dp.callback_query(lambda c: c.data and c.data.startswith("del_event"))
async def delete_event_callback(callback: types.CallbackQuery):
    try:
        event_id = int(callback.data.split(":")[1])
        events = load_events()
        events = [e for e in events if e['id'] != event_id]
        save_events(events)
        await callback.message.edit_text(f"🗑 Мероприятие {event_id} удалено.")
        await callback.answer()
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")



