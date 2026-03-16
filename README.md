# Telegram AI Vision Bot

Асинхронный FastAPI-микросервис для Telegram бота, работающий исключительно через Webhook.
Интегрирован с локальными моделями AI: LLM (на базе Ollama) и Image Captioning (на базе BLIP), что позволяет запускать бота без облачных API.

## Подготовка к запуску 🚀

1. Склонируйте репозиторий.
2. Скопируйте шаблон переменных окружения:
   `cp .env.example .env`
3. Отредактируйте `.env`:
   - Выставьте `BOT_TOKEN`
   - Укажите белый `BASE_URL`, на который Telegram будет слать webhook (например домен или адрес ngrok).
   - `MODEL_NAME` (например, `llama3` или `mistral`).

## Запуск проекта 🐳

Проект настроен для запуска одной командой:
```bash
docker-compose up -d --build
```

**Важно:** Т.к. модели Ollama весят много, после старта первого контейнера вам нужно "скачать" желаемую LLM вручную:
```bash
docker exec -it ollama ollama run llama3
```

## Архитектура системы 🏗️
- **Бот (`aiogram` + FastAPI):** Обрабатывает webhook POST-эндпоинты. Сохраняет историю диалогов в in-memory словаре формата `dict[int, list]`.
- **VisionProcessor:** Работает поверх модели `Salesforce/blip-image-captioning-base`. Принимает байты фото из Telegram API без сохранения на диск (in-memory bytes buffer). Разметка OCR подготовлена.
- **LLM Client:** Обращается через HTTP API к контейнеру `ollama`, скармливая историю диалога.
