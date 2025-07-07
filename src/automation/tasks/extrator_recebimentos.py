import os
import time
from pathlib import Path
from src.automation.pages.login_page import LoginPage
from src.core.use_cases.coletor_recebimentos import ColetorRecebimentos
from src.core.use_cases.download_recebimentos import DownloadRecebimentos
from src.core.use_cases.processador_recebimentos import ProcessadorRecebimentos
from src.config.config import DOWNLOAD_PATH

class ExtratorRecebimentos:
    def __init__(
            self,
            login_page: LoginPage,
            coletor_recebimentos: ColetorRecebimentos,
            download_recebimentos: DownloadRecebimentos, 
            processador_recebimentos: ProcessadorRecebimentos
        ):
        self.login_page = login_page
        self.coletor_recebimentos = coletor_recebimentos
        self.download_recebimentos = download_recebimentos
        self.processador_recebimentos = processador_recebimentos
    
    def execute(self):
        self.login_page.logar()
        time.sleep(2)
        # self.coletor_recebimentos.execute()
        # time.sleep(30)
        self.download_recebimentos.execute()
        time.sleep(30)

        zip_dir = Path(DOWNLOAD_PATH)

        zip_files = [f for f in os.listdir(zip_dir) if f.endswith('.zip')]

        for zip in zip_files:
            self.processador_recebimentos.zip_file = zip
            self.processador_recebimentos.execute()
