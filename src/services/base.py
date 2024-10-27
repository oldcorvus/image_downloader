from abc import ABC, abstractmethod
from typing import Callable, List, Tuple


class ImageSearchService(ABC):
    @abstractmethod
    async def fetch_image_urls(self, query: str, max_results: int) -> List[str]:
        """
        Fetches image URLs from Google Custom Search API based on the search query
        """
        raise NotImplementedError("Method `fetch_image_urls` must be implimented")


class BaseProcessImageService(ABC):
    def __init__(self, processing_func: Callable[[bytes], Tuple[bytes, int, int]]):
        self.processing_func = processing_func

    @abstractmethod
    async def process_image(self, image_data: bytes) -> Tuple[bytes, int, int]:
        """
        Processes the image data (resizing ,...)
        """
        raise NotImplementedError("Method `proccess_image` must be implimented")


class BaseDownloadImageService(ABC):
    @abstractmethod
    async def download_image(self, url: str) -> bytes:
        """
        Downloads an image from the specified URL
        """
        raise NotImplementedError("Method `download_image` must be implimented")
