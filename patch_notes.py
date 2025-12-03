from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from storage import load_notes, save_notes
from patch_reminders import scheduler, OUTPUT_NOTES_ID
from datetime import datetime

dp = Router()
note_cb = CallbackData("note", "action", "index")

INPUT_GROUP = -5012773570
OUTPUT_GROUP = -1003264984732

@dp.message(Command("note"))
async def add_note(message: types.Message):
    """Добавление заметки: /note Название | YYYY-MM-DD HH:MM"""
    try:
        text = message.text.split(" ", 1)[1]
        title, dt_str = map(str.strip, text.split("|"))
        remind_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        notes = load_notes()
        notes.append({"title": title, "datetime": remind_time.strftime("%Y-%m-%d %H:%M")})
        save_notes(notes)
        await message.answer(f"Заметка '{title}' добавлена!")
        # Планируем напоминание
        from patch_reminders import schedule_note_reminder
        schedule_note_reminder(title, remind_time)
    except Exception:
        await message.answer("Ошибка формата! Используй: /note Название | YYYY-MM-DD HH:MM")

@dp.message(Command("notes"))
async def list_notes(message: types.Message):
    notes = load_notes()
    if not notes:
        await message.answer("Список заметок пуст.")
        return
    for i, note in enumerate(notes):
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("Удалить", callback_data=note_cb.new(action="delete", index=i)),
            InlineKeyboardButton("Редактировать", callback_data=note_cb.new(action="edit", index=i))
        )
        await message.answer(f"{i+1}. {note['title']} | {note['datetime']}", reply_markup=kb)

@dp.callback_query(note_cb.filter())
async def callback_note(call: types.CallbackQuery, callback_data: dict):
    index = int(callback_data["index"])
    action = callback_data["action"]
    notes = load_notes()
    if action == "delete":
        if 0 <= index < len(notes):
            removed = notes.pop(index)
            save_notes(notes)
            await call.message.edit_text(f"Заметка '{removed['title']}' удалена!")
        await call.answer()
    elif action == "edit":
        await call.answer("Редактирование пока не реализовано.")
