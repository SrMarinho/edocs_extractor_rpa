import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any

@dataclass
class LoggerSettings:
    app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", "APP"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_dir: Path = field(default_factory=lambda: Path(os.getenv("LOG_DIR", "logs")))

@dataclass
class Drivers:
    edge: Dict[str, Any] = field(default_factory=lambda: {
        "path": os.getenv("EDGE_DRIVER_PATH")
    })

def get_download_directory() -> str:
    """Função para carregar o diretório de download quando chamada"""
    return rf"{os.getenv("XML_COMPRESSED_FILES_DESTINATION")}"

TEMP_PATH = rf"{os.getcwd()}\files\temp"
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", rf"{os.getcwd()}\files\zip")
XML_DESTINATION_PATH = os.getenv("XML_FILE_FINAL_DESTINATION", rf"{os.getcwd()}\files\xml")