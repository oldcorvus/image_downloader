import asyncio
import logging

import aiohttp

from src.services.base import BaseDownloadImageService

logger = logging.getLogger(__name__)


class DownloadImageService(BaseDownloadImageService):
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    async def download_image(self, url: str) -> bytes:
        """
        Downloads an image from the specified URL
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        logger.info(f"Successfully downloaded image from {url}")
                        result = await response.read()
                        return result
                    else:
                        logger.error(
                            f"Failed to download {url}: Status {response.status}"
                        )
            except aiohttp.ClientError as e:
                logger.exception(f"HTTP error occurred while downloading {url}: {e}")
            except asyncio.TimeoutError:
                logger.exception(f"Timeout occurred while downloading {url}")
            except Exception as e:
                logger.exception(
                    f"Unexpected error occurred while downloading {url}: {e}"
                )
                raise
        return b""
