import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiohttp import web

from patch_events import dp as dp_events
from patch_notes import dp as dp_notes
from patch_reminders import dp as dp_reminders
from patch_help import dp as dp_help

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"https://<YOUR-RENDER-SERVICE>.onrender.com{WEBHOOK_PATH}"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем патчи
dp.include_router(dp_events)
dp.include_router(dp_notes)
dp.include_router(dp_reminders)
dp.include_router(dp_help)

# ---------------- Webhook handler ----------------
async def handle(request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(update)
    return web.Response()

# ---------------- App ----------------
app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle)

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(app):
    await bot.delete_webhook()

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, port=PORT)
