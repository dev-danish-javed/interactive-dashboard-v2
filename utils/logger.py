import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(filename)s:%(funcName)s:%(lineno)d — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger_map = {}

def get_logger(service_name: str) -> logging.Logger:
    """
    Get a logger with the given name
    :param name: The name of the service
    :return: The logger
    """
    if service_name not in logger_map:
        logger_map[service_name] = logging.getLogger(service_name)
    return logger_map[service_name]