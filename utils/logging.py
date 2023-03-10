from loguru import logger


logger.add('debug.log')


def log_api_request(func):
    def wrapper(*args, **kwargs):
        logger.info("API Request: {0}", func.__name__)
        return func(*args, **kwargs)
    return wrapper
