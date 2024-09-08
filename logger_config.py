from loguru import logger

logger.add("info_about_book_api.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB",
           compression="zip")
