import subprocess
import time
from src.logger_instance import logger

class TerminalServer:
    def __init__(self, host: str):
        self.host = host

    def connect(self):
        try:
            # Inicia a conexão RDP
            cmd = f'mstsc /v:{self.host}'
            subprocess.Popen(cmd, shell=True)
            return True
        except Exception as e:
            logger.error(f"Erro ao conectar: {str(e)}")
            return False

    def disconnect(self):
        try:
            cmd = 'taskkill /F /IM mstsc.exe'
            subprocess.run(cmd, shell=True, capture_output=True)
            return True
        except Exception as e:
            logger.error(f"Erro ao desconectar: {str(e)}")
            return False
