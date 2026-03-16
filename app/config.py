from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token: str
    base_url: str
    webhook_path: str
    model_name: str
    
    max_context_messages: int = 10
    max_image_mb: int = 10
    env: str = "prod"
    log_level: str = "INFO"
    ollama_url: str = "http://ollama:11434"

    # Чтение из файла .env, игнорируем неизвестные переменные
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
