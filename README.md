# Telegram AI Vision Bot 🤖👁️

A scalable, asynchronous Telegram bot microservice built with **FastAPI** and **aiogram 3.x**. This bot integrates powerful **local AI models** for text generation (via Ollama) and image captioning (via HuggingFace's BLIP model), ensuring 100% privacy with absolutely no reliance on paid cloud API providers.

---

## 🚀 Features

- **Local LLM Integration:** Powered by [Ollama](https://ollama.com/), supporting models like `llama3`, `mistral`, or `phi3` for intelligent text generation.
- **Computer Vision:** Uses `Salesforce/blip-image-captioning-base` to automatically analyze and describe incoming images.
- **Multi-Modal Prompts:** Send a photo along with a text caption, and the bot will intelligently combine the AI-generated visual description with your query.
- **Contextual Memory:** Remembers the last N messages of the conversation for coherent context (in-memory storage).
- **Webhook Architecture:** Built on FastAPI, the bot strictly uses Telegram Webhooks for instant updates, avoiding long-polling overhead.

---

## 🏗️ Architecture Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn, aiogram
- **LLM Engine:** Ollama HTTP REST API
- **Vision Engine:** PyTorch, Transformers (HuggingFace)
- **Deployment:** Docker & Docker Compose (or native Python virtual environment)

---

## ⚙️ Prerequisites

Since the AI models run locally on your machine, ensure your system meets the minimum requirements:
- **RAM:** 8GB+ (16GB recommended for `llama3` + BLIP).
- **Disk Space:** ~10-15GB free space for model weights and Docker images.
- **Software:** Python 3.11 (for local run) OR Docker Desktop (for containerized run). 
- **Network:** [ngrok](https://ngrok.com/) to expose your local FastAPI port to Telegram's Webhook servers.

---

## 🛠️ Environment Configuration

1. Clone this repository.
2. Rename `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Populate the required variables in `.env`:
   - `BOT_TOKEN`: Your bot token from [@BotFather](https://t.me/BotFather).
   - `BASE_URL`: Your public HTTPS URL (e.g., from ngrok). No trailing slash.
   - `MODEL_NAME`: The model you want to run (e.g., `llama3`).
   - `OLLAMA_URL`: `http://ollama:11434` for Docker, or `http://127.0.0.1:11434` for local execution.

---

## 🚀 Installation & Launch

You can run this project in two ways depending on your system's resources.

### Option A: The "Bare Metal" Approach (Recommended for Windows)
*Running Docker on Windows via WSL2 can sometimes consume excessive disk space. Running natively is often faster and much lighter.*

1. **Install Ollama locally:** Download from [ollama.com](https://ollama.com/) and run `ollama run llama3` in your terminal to pre-download the model.
2. **Setup Python Environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate      # On Windows
    # source venv/bin/activate # On Unix/macOS
    ```
3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Expose port to Internet (in a separate terminal):**
    ```bash
    ngrok http 8000
    # Copy the given https:// URL and paste it intoBASE_URL in your .env file!
    ```
5. **Start the Bot:**
    ```bash
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

### Option B: Docker Compose
*Best for Linux servers or completely isolated environments.*

1. **Start ngrok** and update your `.env` file first.
2. Build and run the containers:
    ```bash
    docker-compose up -d --build
    ```
3. **Download the LLM:** Once the containers are running, download the Llama model into the Ollama container:
    ```bash
    docker exec -it ollama ollama run llama3
    ```

---

## 💬 Usage

Once the server is up and saying `INFO: Установлен Webhook`, open Telegram and talk to your bot!
- `/start` - Greeting message.
- `/help` - Available commands.
- `/reset` - Wipes the conversation context memory.
- **Send Text:** Simply send a question.
- **Send Photo:** The bot will "look" at it and explain what it sees using BLIP!
