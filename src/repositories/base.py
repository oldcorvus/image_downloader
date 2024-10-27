from abc import ABC, abstractmethod
from typing import List

from src.domain.entities import Image


class ImageRepository(ABC):
    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError("Connect method not implemented")

    @abstractmethod
    async def disconnect(self) -> None:
        raise NotImplementedError("Disconnect method not implemented")

    @abstractmethod
    async def insert_image(self, image: Image) -> None:
        raise NotImplementedError("Insert method not implemented")

    @abstractmethod
    async def list_images(self, query: str) -> List[Image]:
        raise NotImplementedError("List method not implemented")
