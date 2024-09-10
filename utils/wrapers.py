import functools
from logger_config import logger


def log_request(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Копируем kwargs и удаляем первый элемент
        if kwargs:
            kwargs_to_log = dict(list(kwargs.items())[1:])
        else:
            kwargs_to_log = kwargs

        # Логирование args, если они есть
        if args:
            logger.info(f"Executing {func.__name__} with args: {args} and kwargs: {kwargs_to_log}")
        else:
            logger.info(f"Executing {func.__name__} with kwargs: {kwargs_to_log}")

        # Выполнение функции
        result = await func(*args, **kwargs)

        # Логирование завершения функции
        if args:
            logger.info(f"{func.__name__} executed successfully with args: {args} and kwargs: {kwargs_to_log}")
        else:
            logger.info(f"{func.__name__} executed successfully with kwargs: {kwargs_to_log}")

        return result

    return wrapper


def log_users_request(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__} with {kwargs}")
        result = await func(*args, **kwargs)
        logger.info(f"{func.__name__} executed successfully with {kwargs}")
        return result

    return wrapper
