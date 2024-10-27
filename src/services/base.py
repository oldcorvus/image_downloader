from abc import ABC, abstractmethod
from typing import List


class ImageSearchService(ABC):
    @abstractmethod
    async def fetch_image_urls(self, query: str, max_results: int) -> List[str]:
        """
        Fetches image URLs from Google Custom Search API based on the search query
        """
        raise NotImplementedError("Method `fetch_image_urls` must be implimented")
