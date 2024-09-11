from loguru import logger

logger.add("fastapi-logs/fastapi-efk.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB",
           compression="zip")
