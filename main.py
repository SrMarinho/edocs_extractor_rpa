import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from src.automation.tasks.extrator_recebimentos import ExtratorRecebimentos
from src.core.use_cases.coletor_recebimentos import ColetorRecebimentos
import src.config.config as config
from src.automation.pages.login_page import LoginPage
from src.automation.pages.nfe.recebimentos_page import (
    RecebimentosPage, 
    RecebimentosFilter, 
)
from src.automation.pages.inicial.segundo_plano_page import SegundoPlanoPage
from src.core.use_cases.download_recebimentos import DownloadRecebimentos
from src.core.use_cases.processador_recebimentos import ProcessadorRecebimentos
from src.automation.tasks.extrator_recebimentos import ExtratorRecebimentos
from src.utils.webdriver_utils import setup_edge_options
from src.core.entities.terminal_server import TerminalServer
from src.core.use_cases.send_to_ts import SendToTs
from src.logger_instance import logger


def main():
    try:
        options = setup_edge_options(config.DOWNLOAD_PATH)
        service = Service(executable_path=config.Drivers().edge["path"])
        
        with webdriver.Edge(service=service, options=options) as driver:
            # Inicialização das páginas/services
            login_page = LoginPage(driver, os.getenv("EDOCS_USERNAME"), os.getenv("EDOCS_PASSWORD"))
            recebimentos_page = RecebimentosPage(
                driver, 
                RecebimentosFilter(
                    **RecebimentosFilter.get_params()["filtros"]
                    )
                )
            
            ExtratorRecebimentos(
                login_page,
                ColetorRecebimentos(recebimentos_page),
                DownloadRecebimentos(SegundoPlanoPage(driver)),
                ProcessadorRecebimentos()
            ).execute()

    except Exception as e:
        logger.critical(f"Erro crítico: {e}", exc_info=True)
        if 'driver' in locals():
            driver.save_screenshot("erro_critico.png")
        raise
    
if __name__ == "__main__":
    main()