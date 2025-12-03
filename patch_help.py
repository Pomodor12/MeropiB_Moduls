from aiogram import Router
from aiogram.filters import Command

dp = Router()

@dp.message(Command("help"))
async def help_cmd(message):
    text = (
        "/add_event Название | YYYY-MM-DD | HH:MM | Кол-во — добавить мероприятие\n"
        "/list_events — список мероприятий\n"
        "/note Название | YYYY-MM-DD HH:MM — добавить заметку\n"
        "/notes — список заметок\n"
        "Кнопки удаления и редактирования доступны под сообщениями\n"
    )
    await message.answer(text)
