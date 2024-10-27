import asyncio
import logging

import click

from src.config.config import get_settings
from src.infrastructure.database.init_db import create_tables
from src.repositories.postgres import PostgresImageRepository
from src.services.download import DownloadImageService
from src.services.google import GoogleImageService
from src.services.proccess import ProcessImageService
from src.use_cases.query_image import QueryImagesUseCase
from src.utils.image_utils import resize_image
from src.utils.logger import setup_logging

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--query",
    required=True,
    type=str,
    help='Search query for images ("cute kittens" ...)',
)
@click.option(
    "--max-results",
    required=True,
    type=int,
    help="Maximum number of images to retrieve (10, ...)",
)
def download_images(query, max_results):
    """
    Fetch and store images based on a search QUERY with a maximum of MAX_RESULTS
    """
    setup_logging()
    logger.info("Starting the Image Downloader CLI...")
    logger.debug(f"Received arguments - Query: {query}, Max Results: {max_results}")

    async def run():
        await run_image_query(query, max_results, logger)

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")


async def run_image_query(query: str, max_results: int, logger: logging.Logger):
    await create_tables()

    settings = get_settings()

    logger.debug("Initializing PostgreSQL repository...")
    img_rep = PostgresImageRepository(settings=settings)

    logger.debug("Initializing Google Image Search Service...")
    search_service = GoogleImageService()

    logger.debug("Initializing Image Download Service...")
    download_service = DownloadImageService()

    logger.debug("Initializing Image Processing Service...")
    process_service = (
        ProcessImageService(resize_image) if settings.max_image_size else None
    )

    use_case = QueryImagesUseCase(
        repository=img_rep,
        search_serivce=search_service,
        download_service=download_service,
        process_service=process_service,
        max_concurrent_tasks=10,
    )

    try:
        await use_case.process(query=query, max_results=max_results)

        logger.info("Image query and processing completed successfully.")

    except Exception as e:
        logger.exception(f"An error occurred during the image query process: {e}")
    finally:
        logger.info("CLI operation finished.")
