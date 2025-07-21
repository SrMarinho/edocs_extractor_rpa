import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any
from src.utils.tools import local_path

@dataclass
class LoggerSettings:
    app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", "APP"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_dir: Path = field(default_factory=lambda: Path(os.getenv("LOG_DIR", "logs")))

@dataclass
class Drivers:
    edge: Dict[str, Any] = field(default_factory=lambda: {
        "path": os.getenv("EDGE_DRIVER_PATH", str(local_path() / "drivers" / "msedgedriver.exe"))
    })

TEMP_PATH = str(local_path() / "files" / "temp")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", str(local_path() / "files" / "zip"))
XML_DESTINATION_PATH = os.getenv("XML_FILE_FINAL_DESTINATION", str(local_path() / "files" / "xml"))