import logging
from typing import List

import aiohttp

from src.config.config import get_settings
from src.services.base import ImageSearchService

logger = logging.getLogger(__name__)


class GoogleImageService(ImageSearchService):
    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self):
        self.settings = get_settings()

    async def fetch_image_urls(self, query: str, max_results: int) -> List[str]:
        image_urls: List[str] = []
        start = 1
        per_page = 10

        async with aiohttp.ClientSession() as session:
            while len(image_urls) < max_results:
                params = {
                    "key": self.settings.google_api_key,
                    "cx": self.settings.google_cse_id,
                    "q": query,
                    "searchType": "image",
                    "start": start,
                    "num": min(per_page, max_results - len(image_urls)),
                }
                try:
                    async with session.get(self.BASE_URL, params=params) as resp:
                        if resp.status != 200:
                            logger.error(f"Error fetching image URLs: {resp.status}")
                            resp.raise_for_status()
                        data = await resp.json()
                        items = data.get("items", [])
                        if not items:
                            logger.info("No more images found")
                            break
                        fetched_urls = [
                            item["link"] for item in items if "link" in item
                        ]
                        image_urls.extend(fetched_urls)
                        logger.info(f"Fetched {len(fetched_urls)} image URLs")
                        start += per_page

                except aiohttp.ClientError as e:
                    logger.exception(f"HTTP error occurred: {e}")
                    raise
                except Exception as e:
                    logger.exception(f"Unexpected error occurred: {e}")
                    raise

        return image_urls[:max_results]
