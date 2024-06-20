import logging

from employee_management.core.configurations.configuration import configuration

logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=configuration.logging_level, format=logging_format)

logger = logging


def format_logger_name(logger_name: str) -> str:
    logger_name = logger_name.lower().replace(" ", "_")
    return logger_name
