import asyncio
from aiogram import Bot, Dispatcher
from patch_events import dp as dp_events
from patch_notes import dp as dp_notes
from patch_reminders import dp as dp_reminders, set_bot

TOKEN = "ВАШ_ТОКЕН"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Передаем bot в патчи
set_bot(bot)

# Подключаем все маршрутизаторы
dp.include_router(dp_events)
dp.include_router(dp_notes)
dp.include_router(dp_reminders)

async def main():
    try:
        print("Бот запущен")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

