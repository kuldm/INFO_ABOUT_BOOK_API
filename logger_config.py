import logging
import logging.handlers


# class LoggerSetup:
#
#     def __init__(self) -> None:
#         self.logger = logging.getLogger('')
#         self.setup_logging()
#
#     def setup_logging(self):
#         # add log format
#         LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#         logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
#
#         #configure formmater for logger
#         formatter = logging.Formatter(LOG_FORMAT)
#
#         # configure console handler
#         console= logging.StreamHandler()
#         console.setFormatter(formatter)
#
#         # configure TimeRotatingFileHandler
#         log_file = f"logs/fastapi-efk.log"
#         file = logging.handlers.TimedRotatingFileHandler(filename=log_file, when="midnight", backupCount=5)
#         file.setFormatter(formatter)
#
#         # add handlers
#         self.logger.addHandler(console)
#         self.logger.addHandler(file)

class LoggerSetup:
    def __init__(self) -> None:
        self.logger = logging.getLogger('')
        self.setup_logging()

    def setup_logging(self):
        # Очищаем все существующие обработчики
        self.logger.handlers.clear()

        # Настраиваем уровень логирования
        self.logger.setLevel(logging.INFO)

        # Настраиваем формат
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(LOG_FORMAT)

        # Настраиваем консольный обработчик
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        # Настраиваем файловый обработчик
        log_file = "logs/fastapi-efk.log"
        file = logging.handlers.TimedRotatingFileHandler(filename=log_file, when="midnight", backupCount=2)
        file.setFormatter(formatter)
        self.logger.addHandler(file)

        # Настраиваем второй файловый обработчик
        log_file2 = "fastapi-logs/fastapi-efk.log"
        file2 = logging.handlers.TimedRotatingFileHandler(filename=log_file2, when="midnight", backupCount=2)
        file2.setFormatter(formatter)
        self.logger.addHandler(file2)
