import os
import sys
from pathlib import Path
from src.logger_instance import logger

def local_path():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        logger.info(str(Path(os.path.abspath(sys._MEIPASS))))
        return Path(os.path.abspath(sys._MEIPASS))
    return Path(os.path.abspath("."))