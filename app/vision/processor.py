import io
import torch
import asyncio
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

class VisionProcessor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Модель загружается при старте
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).to(self.device)

    async def generate_caption(self, image_bytes: bytes) -> str:
        """Асинхронный адаптер для синхронной обработки изображения."""
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            # Переносим тяжелое вычисление в отдельный пул потоков
            return await asyncio.to_thread(self._process_image, image)
        except Exception as e:
            return f"Ошибка обработки изображения: {str(e)}"

    def _process_image(self, image: Image.Image) -> str:
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs)
        return self.processor.decode(out[0], skip_special_tokens=True)

    def process_ocr(self, image: Image.Image) -> str:
        """Базовая архитектура для интеграции Tesseract OCR."""
        # import pytesseract
        # return pytesseract.image_to_string(image, lang='rus+eng')
        pass
