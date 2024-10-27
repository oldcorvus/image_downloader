import asyncio
import logging
from typing import List

from src.domain.entities import Image
from src.repositories.base import ImageRepository

logger = logging.getLogger(__name__)


class InMemoryImageRepository(ImageRepository):
    def __init__(self):
        self._images = {}
        self._lock = asyncio.Lock()
        self.connected = False

    async def connect(self) -> None:
        async with self._lock:
            if not self.connected:
                self.connected = True
                logger.info("In-memory repository connected")

    async def disconnect(self) -> None:
        async with self._lock:
            if self.connected:
                self.connected = False
                self._images.clear()
                logger.info("In-memory repository disconnected and cleared")
            else:
                logger.warning("In-memory repository is not connected")

    async def insert_image(self, image: Image) -> None:
        if not self.connected:
            raise ConnectionError("Repository not connected.")

        async with self._lock:
            self._images[image.image_url] = image
            logger.info(f"Inserted image with URL: {image.image_url}")

    async def list_images(self, query: str) -> List[Image]:
        if not self.connected:
            raise ConnectionError("Repository not connected.")

        async with self._lock:
            matched_images = [
                image for image in self._images.values() if image.query == query
            ]
            logger.info(f"Listed {len(matched_images)} images for query: '{query}'")
            return matched_images
