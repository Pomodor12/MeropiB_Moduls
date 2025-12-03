import asyncio
from aiogram import Bot, Dispatcher
from patch_events import dp as dp_events
from patch_notes import dp as dp_notes
from patch_reminders import set_bot, check_urgent_events  # убрали dp

TOKEN = "7999077800:AAGAlfz6ho1xAP2spR8k_18rGy4CPdWRo3k"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Передаем bot в патчи
set_bot(bot)

# Подключаем маршрутизаторы
dp.include_router(dp_events)
dp.include_router(dp_notes)

async def main():
    try:
        print("Бот запущен")
        # запускаем срочные уведомления после инициализации бота
        check_urgent_events()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())


