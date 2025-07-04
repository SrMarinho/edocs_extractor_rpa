import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class LoggerSettings:
    app_name: str = os.getenv("APP_NAME", "APP")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_dir: Path = Path("logs")


download_directory = fr"{os.getenv("XML_COMPRESSED_FILES_DESTINATION")}"