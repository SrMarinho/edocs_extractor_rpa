import os
from pathlib import Path
import zipfile
import shutil
from src.config.config import TEMP_PATH, XML_DESTINATION_PATH, DOWNLOAD_PATH
from src.logger_instance import logger

class ProcessadorRecebimentos:
    def __init__(self):
        self.zip_path = Path(DOWNLOAD_PATH)
        self.temp_dir = Path(TEMP_PATH)
        self.zip_file = None

    def execute(self):
        if not self.zip_file:
            logger.warning("É necessário indicar o um arquivo")
            raise ValueError("É necessário indicar o um arquivo")

        self._extrair_zip()
        self._filtrar_arquivos()
        self._mover_validos()
        self._limpar_temp()

    def _extrair_zip(self):
        try:
            self.temp_dir.mkdir(exist_ok=True)


            with zipfile.ZipFile(self.zip_path / self.zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir / self.zip_file)
        except Exception as e:
            logger.error(f"Erro ao tentar extrair zip - {str(e)}")
            raise
            
    def _filtrar_arquivos(self):
        try:
            # Filtrando arquivos para penas apenas os que não possuem NFe-OPCIEN
            self.arquivos_validos = [
                f for f in (self.temp_dir / self.zip_file).glob("*.xml") 
                if "NFe-OPCIEN" not in f.name
            ]
        except Exception as e:
            logger.error(f"Erro ao tentar filtrar arquivos - {str(e)}")
            raise
        
    def _mover_validos(self):
        try:
            destino_final = Path(XML_DESTINATION_PATH)
            destino_final.mkdir(parents=True, exist_ok=True)
            
            for arquivo in self.arquivos_validos:
                shutil.move(str(arquivo), str(destino_final))
        except Exception as e:
            logger.error(f"Erro ao tentar mover arquivos filtrados - {str(e)}")
            raise
            
    def _limpar_temp(self):
        try:
            shutil.rmtree(self.temp_dir / self.zip_file)
            # (self.zip_path / self.zip_file).unlink()
        except Exception as e:
            logger.error(f"Erro ao limpar pasta temp - {str(e)}")
            raise