import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.bot.handlers import router

logging.basicConfig(level=getattr(logging, settings.log_level.upper()))
logger = logging.getLogger(__name__)

bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
dp.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Установка webhook при старте
    webhook_url = f"{settings.base_url}{settings.webhook_path}"
    await bot.set_webhook(
        url=webhook_url, 
        allowed_updates=dp.resolve_used_update_types(), 
        drop_pending_updates=True
    )
    logger.info(f"Установлен Webhook: {webhook_url}")
    yield
    # Очистка при завершении работы сервиса
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Webhook удален.")

app = FastAPI(lifespan=lifespan)

# Эндпоинт обрабатывает только POST-запросы
@app.post(settings.webhook_path)
async def webhook_handler(request: Request):
    update_data = await request.json()
    update = Update(**update_data)
    await dp.feed_update(bot=bot, update=update)
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
