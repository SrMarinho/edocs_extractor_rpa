import os
import time
from pathlib import Path
from src.automation.pages.login_page import LoginPage
from src.core.use_cases.coletor_recebimentos import ColetorRecebimentos
from src.core.use_cases.download_recebimentos import DownloadRecebimentos
from src.core.use_cases.processador_recebimentos import ProcessadorRecebimentos
from src.core.use_cases.send_to_ts import SendToTs
from src.config.config import DOWNLOAD_PATH

class ExtratorRecebimentos:
    def __init__(
            self,
            login_page: LoginPage,
            coletor_recebimentos: ColetorRecebimentos,
            download_recebimentos: DownloadRecebimentos, 
            processador_recebimentos: ProcessadorRecebimentos,
            send_to_ts: SendToTs = None,  # Agora é opcional
        ):
        self.login_page = login_page
        self.coletor_recebimentos = coletor_recebimentos
        self.download_recebimentos = download_recebimentos
        self.processador_recebimentos = processador_recebimentos
        self.send_to_ts = send_to_ts
    
    def execute(self):
        try:
            # Login e coleta de dados
            self.login_page.logar()
            time.sleep(2)
            self.coletor_recebimentos.execute()
            time.sleep(5)
            
            # Download e processamento
            self.download_recebimentos.execute()
            time.sleep(120)  # Aguarda download
            self.download_recebimentos.quit()
            time.sleep(1)

            # Processa os arquivos ZIP baixados
            zip_dir = Path(DOWNLOAD_PATH)
            zip_files = [f for f in os.listdir(zip_dir) if f.endswith('.zip')]

            for zip in zip_files:
                self.processador_recebimentos.zip_file = zip
                self.processador_recebimentos.execute()

            time.sleep(2)

            # Envia para o Terminal Server (se configurado)
            if self.send_to_ts:
                self.send_to_ts.execute()
            
        except Exception as e:
            # Em caso de erro, tenta limpar os arquivos temporários
            try:
                self.processador_recebimentos.limpar_xml()
            except:
                pass  # Ignora erros na limpeza
            raise e  # Re-lança o erro original
