from aiogram import Router, types
from aiogram.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from storage import load_notes, save_notes
from patch_reminders import OUTPUT_NOTES_ID, bot_instance

dp = Router()

async def send_note_reminder(bot, note):
    text = f"📝 Напоминание о заметке:\n{note['title']} | {note['date']} {note.get('time','')}"
    if bot:
        await bot.send_message(OUTPUT_NOTES_ID, text)

@dp.message(Text(startswith="/add_note"))
async def add_note(message: types.Message):
    try:
        parts = message.text.split("|")
        title = parts[0].replace("/add_note", "").strip()
        date = parts[1].strip()
        time = parts[2].strip() if len(parts) > 2 else ""
        notes = load_notes()
        note_id = len(notes) + 1
        notes.append({"id": note_id, "title": title, "date": date, "time": time})
        save_notes(notes)
        await message.answer(f"✅ Заметка '{title}' добавлена с id {note_id}.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

@dp.message(Text(startswith="/list_notes"))
async def list_notes(message: types.Message):
    notes = load_notes()
    if not notes:
        await message.answer("Список заметок пуст.")
        return
    for n in notes:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Удалить", callback_data=f"del_note:{n['id']}")]
        ])
        await message.answer(f"{n['id']}. {n['title']} | {n['date']} {n.get('time','')}", reply_markup=kb)

@dp.callback_query(lambda c: c.data and c.data.startswith("del_note"))
async def delete_note_callback(callback: types.CallbackQuery):
    try:
        note_id = int(callback.data.split(":")[1])
        notes = load_notes()
        notes = [n for n in notes if n['id'] != note_id]
        save_notes(notes)
        await callback.message.edit_text(f"🗑 Заметка {note_id} удалена.")
        await callback.answer()
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")
from aiogram import Router, types
from aiogram.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from storage import load_notes, save_notes
from patch_reminders import OUTPUT_NOTES_ID, bot_instance

dp = Router()

async def send_note_reminder(bot, note):
    text = f"📝 Напоминание о заметке:\n{note['title']} | {note['date']} {note.get('time','')}"
    if bot:
        await bot.send_message(OUTPUT_NOTES_ID, text)

@dp.message(Text(startswith="/add_note"))
async def add_note(message: types.Message):
    try:
        parts = message.text.split("|")
        title = parts[0].replace("/add_note", "").strip()
        date = parts[1].strip()
        time = parts[2].strip() if len(parts) > 2 else ""
        notes = load_notes()
        note_id = len(notes) + 1
        notes.append({"id": note_id, "title": title, "date": date, "time": time})
        save_notes(notes)
        await message.answer(f"✅ Заметка '{title}' добавлена с id {note_id}.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

@dp.message(Text(startswith="/list_notes"))
async def list_notes(message: types.Message):
    notes = load_notes()
    if not notes:
        await message.answer("Список заметок пуст.")
        return
    for n in notes:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Удалить", callback_data=f"del_note:{n['id']}")]
        ])
        await message.answer(f"{n['id']}. {n['title']} | {n['date']} {n.get('time','')}", reply_markup=kb)

@dp.callback_query(lambda c: c.data and c.data.startswith("del_note"))
async def delete_note_callback(callback: types.CallbackQuery):
    try:
        note_id = int(callback.data.split(":")[1])
        notes = load_notes()
        notes = [n for n in notes if n['id'] != note_id]
        save_notes(notes)
        await callback.message.edit_text(f"🗑 Заметка {note_id} удалена.")
        await callback.answer()
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")

