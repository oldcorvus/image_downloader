import asyncio
import logging

from src.domain.entities import Image
from src.repositories.base import ImageRepository
from src.services.base import (
    BaseDownloadImageService,
    BaseProcessImageService,
    ImageSearchService,
)

logger = logging.getLogger(__name__)


class QueryImagesUseCase:
    def __init__(
        self,
        repository: ImageRepository,
        search_serivce: ImageSearchService,
        download_service: BaseDownloadImageService,
        process_service=BaseProcessImageService,
        max_concurrent_tasks: int = 10,
    ):
        self.search_serivce = search_serivce
        self.download_service = download_service
        self.process_service = process_service
        self.repository = repository
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)

    async def process(self, query: str, max_results: int):
        logger.info(
            f"Starting image query use case for query: '{query}' with max_results: {max_results}"
        )
        try:
            await self.repository.connect()
            image_urls = await self.search_serivce.fetch_image_urls(
                query=query, max_results=max_results
            )
            logger.info(f"Found {len(image_urls)} image URLs for query '{query}'")

            tasks = [self._process(query, url) for url in image_urls]

            await asyncio.gather(*tasks, return_exceptions=True)

            logger.info(
                f"Completed processing and storing {len(image_urls)} images for query '{query}'"
            )
        except Exception as e:
            logger.exception(f"An error occurred during the image query use case: {e}")
            raise
        finally:
            await self.repository.disconnect()

    async def _process(self, query: str, url: str):
        async with self.semaphore:
            try:
                logger.debug(f"Downloading image from URL: {url}")
                image_data = await self.download_service.download_image(url)
                if not image_data:
                    logger.warning(f"No data downloaded for URL: {url}")
                    return
                if self.process_service:
                    logger.debug(f"Processing image from URL: {url}")
                    (
                        processed_data,
                        width,
                        height,
                    ) = await self.process_service.process_image(image_data)
                image = Image(
                    query=query,
                    image_url=url,
                    image_data=processed_data,
                    height=height,
                    width=width,
                )
                await self.repository.insert_image(image)
                logger.info(f"Successfully processed and stored image from URL: {url}")
            except Exception as e:
                logger.exception(f"Failed to process image from URL '{url}': {e}")
