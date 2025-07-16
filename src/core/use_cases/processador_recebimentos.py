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
        logger.info(f"Iniciando processamentos dos recebimentos para {self.zip_file}")
        if not self.zip_file:
            logger.warning("É necessário indicar o um arquivo")
            raise ValueError("É necessário indicar o um arquivo")

        self._extrair_zip()
        self._filtrar_arquivos()
        self._mover_validos()
        self._limpar_temp()

    def _extrair_zip(self):
        logger.info(f"Extraindo {self.zip_file} para {self.temp_dir / self.zip_file}")
        try:
            self.temp_dir.mkdir(exist_ok=True)

            with zipfile.ZipFile(self.zip_path / self.zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir / self.zip_file)
        except Exception as e:
            logger.error(f"Erro ao tentar extrair zip - {str(e)}")
            raise
            
    def _filtrar_arquivos(self):
        logger.info(f"Filtrando arquivos de {self.temp_dir / self.zip_file}")
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
        logger.info(f"Movendo arquivos validos de {self.temp_dir / self.zip_file} para {Path(XML_DESTINATION_PATH)}")
        try:
            destino_final = Path(XML_DESTINATION_PATH)
            destino_final.mkdir(parents=True, exist_ok=True)
            
            for arquivo in self.arquivos_validos:
                try:
                    destino = destino_final / arquivo.name
                    
                    # Se o arquivo já existir no destino, encontra um novo nome
                    counter = 1
                    while destino.exists():
                        nome_base = arquivo.stem
                        extensao = arquivo.suffix
                        novo_nome = f"{nome_base}_{counter}{extensao}"
                        destino = destino_final / novo_nome
                        counter += 1
                    
                    shutil.move(str(arquivo), str(destino))
                except Exception as e:
                    logger.warning(f"Erro ao tentar mover arquivo {str(arquivo)} para {destino_final} - {str(e)}")
        except Exception as e:
            logger.error(f"Erro ao tentar mover arquivos filtrados - {str(e)}")
            raise
            
    def _limpar_temp(self):
        logger.info(f"Limpando pasta temporaria {self.temp_dir / self.zip_file}")
        try:
            shutil.rmtree(self.temp_dir / self.zip_file)
            logger.info(f"Removendo arquivo {(self.zip_path / self.zip_file)}")
            (self.zip_path / self.zip_file).unlink()
        except Exception as e:
            logger.error(f"Erro ao limpar pasta temp - {str(e)}")
            raise
    
    def limpar_xml(self):
        logger.info(f"Limpando arquivos XML da pasta {Path(XML_DESTINATION_PATH)}")
        try:
            destino_final = Path(XML_DESTINATION_PATH)
            # Cria a pasta se não existir
            destino_final.mkdir(parents=True, exist_ok=True)
            
            # Remove apenas os arquivos XML da pasta
            for arquivo in destino_final.glob('*.xml'):
                try:
                    arquivo.unlink()
                    logger.info(f"Arquivo {arquivo.name} removido com sucesso")
                except Exception as e:
                    logger.warning(f"Erro ao remover arquivo {arquivo.name}: {str(e)}")
            
            logger.info(f"Limpeza de arquivos XML concluída")
        except Exception as e:
            logger.error(f"Erro ao tentar limpar arquivos XML: {str(e)}")
            raise
