from .utils.logger import CustomLogger
from src.config.config import LoggerSettings


logger = CustomLogger(LoggerSettings).get_logger()