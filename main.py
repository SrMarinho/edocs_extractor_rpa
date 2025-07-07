import os
import time
from selenium import webdriver
import tempfile
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from src.automation.tasks.extrator_recebimentos import ExtratorRecebimentos
from src.core.use_cases.coletor_recebimentos import ColetorRecebimentos
import src.config.config as config
from src.automation.pages.login_page import LoginPage
from src.automation.pages.nfe.recebimentos_page import (
    RecebimentosPage, 
    RecebimentosFilter, 
    RecebimentosFilterSituacao, 
    RecebimentosFilterTipo
)
from src.automation.pages.inicial.segundo_plano_page import SegundoPlanoPage
from src.core.use_cases.download_recebimentos import DownloadRecebimentos
from src.core.use_cases.processador_recebimentos import ProcessadorRecebimentos
from src.automation.tasks.extrator_recebimentos import ExtratorRecebimentos

def setup_options():
    # Criar um perfil temporário
    temp_profile = tempfile.mkdtemp()

    options = Options()
    options.use_chromium = True
    options.add_argument(f"user-data-dir={temp_profile}")
    options.add_argument("--incognito")
    options.add_argument("--kiosk")
    # options.add_argument("headless")
    # options.add_argument("disable-gpu")
    options.add_experimental_option("prefs", {
        "download.default_directory": rf"{config.DOWNLOAD_PATH}",  # Define o local de download
        "download.prompt_for_download": False,       # Desativa a confirmação
        "download.directory_upgrade": True,          # Permite alterar o diretório
        "savefile.default_directory": config.DOWNLOAD_PATH,
        "safebrowsing.enabled": True                # Desativa avisos de segurança
    })
    return options

def main():
    
    edger_driver = config.Drivers().edge

    options = setup_options()
    service = Service(executable_path=edger_driver["path"])
    driver = webdriver.Edge(service=service, options=options)

    username = os.getenv("EDOCS_USERNAME")
    password = os.getenv("EDOCS_PASSWORD")
    
    logingPage = LoginPage(driver, username, password)
    time.sleep(2)

    recebimentos_filters = RecebimentosFilter(
        situacao=RecebimentosFilterSituacao.AUTORIZO_USO,
        data_entrada="06/07/2025",
        data_saida="07/07/2025",
        tipo=RecebimentosFilterTipo.DESTINATARIO
    )

    recebimentos_page = RecebimentosPage(driver, recebimentos_filters)

    coletor_recebimentos = ColetorRecebimentos(recebimentos_page)

    segundo_plano_page = SegundoPlanoPage(driver)

    download_recebimentos = DownloadRecebimentos(segundo_plano_page)

    processador_recebimentos = ProcessadorRecebimentos()

    extrator_recebimentos = ExtratorRecebimentos(logingPage, coletor_recebimentos, download_recebimentos, processador_recebimentos)
    extrator_recebimentos.execute()
    time.sleep(20)
    
if __name__ == "__main__":
    main()