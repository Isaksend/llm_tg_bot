from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from typing import Dict, List
from collections import defaultdict
import logging


from app.config import settings
from app.llm.client import OllamaClient
from app.vision.processor import VisionProcessor

router = Router()
llm_client = OllamaClient()
vision_processor = VisionProcessor()

# Хранилище контекста: user_id -> список сообщений
context_storage: Dict[int, List[Dict[str, str]]] = defaultdict(list)
SYSTEM_PROMPT = "Ты полезный AI-ассистент. Отвечай кратко, грамотно и по делу."

def get_context(user_id: int) -> List[Dict[str, str]]:
    if not context_storage[user_id]:
        context_storage[user_id].append({"role": "system", "content": SYSTEM_PROMPT})
    return context_storage[user_id]

def add_message(user_id: int, role: str, content: str):
    ctx = get_context(user_id)
    ctx.append({"role": role, "content": content})
    # Усекаем контекст, оставляя системный промпт (index=0)
    while len(ctx) > settings.max_context_messages + 1:
        ctx.pop(1)

text_router = Router()
router.include_router(text_router)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я AI-ассистент с функциями зрения. Отправь мне текст или фотографию.")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Команды:\n/start - Начать\n/help - Помощь\n/reset - Очистить контекст диалога")

@router.message(Command("reset"))
async def cmd_reset(message: Message):
    user_id = message.from_user.id
    if user_id in context_storage:
        context_storage[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    await message.answer("Контекст диалога успешно очищен.")

@router.message(F.photo)
async def handle_photo(message: Message, bot: Bot):
    photo = message.photo[-1]
    limit_bytes = settings.max_image_mb * 1024 * 1024
    
    if photo.file_size > limit_bytes:
        await message.answer(f"Размер изображения превышает лимит в {settings.max_image_mb} МБ.")
        return

    status_msg = await message.answer("👀 Изучаю изображение...")
    
    try:
        file_info = await bot.get_file(photo.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        image_bytes = downloaded_file.read()

        caption = await vision_processor.generate_caption(image_bytes)
        user_text = message.caption or ""
        
        if user_text:
            combined_prompt = f"На изображении: {caption}\nЗапрос пользователя: {user_text}"
        else:
            combined_prompt = f"Опиши подробнее то, что изображено: {caption}"

        add_message(message.from_user.id, "user", combined_prompt)
        await status_msg.edit_text("🧠 Генерирую ответ...")
        
        response = await llm_client.generate_response(get_context(message.from_user.id))
        add_message(message.from_user.id, "assistant", response)
        
        await status_msg.edit_text(response)
    except Exception as e:
        logging.exception("Ошибка при обработке фото")
        await status_msg.edit_text("❌ Произошла ошибка при обработке изображения или запроса к нейросети. Попробуйте еще раз позже.")

@router.message(F.text)
async def handle_text(message: Message):
    status_msg = await message.answer("🧠 Думаю...")
    user_id = message.from_user.id
    
    try:
        add_message(user_id, "user", message.text)
        response = await llm_client.generate_response(get_context(user_id))
        add_message(user_id, "assistant", response)
        
        await status_msg.edit_text(response)
    except Exception as e:
        logging.exception("Ошибка при обработке текста")
        await status_msg.edit_text("❌ Произошла ошибка при обращении к языковой модели. Убедитесь, что модель Ollama запущена.")
