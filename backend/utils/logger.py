import logging

class CustomLogger:
    def __init__(self, logger_name=__name__):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self._setup_handlers()

    def _setup_handlers(self):
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('app.log')

        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.WARNING)

        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
    def log(self,message, level='info'):
        if level == 'debug':
            self.debug(message)
        elif level == 'info':
            self.info(message)
        elif level == 'warning':
            self.warning(message)
        elif level == 'error':
            self.error(message)
        elif level == 'critical':
            self.critical(message)
        else:
            self.info(message)
# Usage example
logger = CustomLogger(__name__)
logger.info("This is an info message")
