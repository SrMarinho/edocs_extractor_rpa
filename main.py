import os
import time
from dotenv import load_dotenv
from selenium import webdriver
import tempfile
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from src.automation.tasks.extrator_recebimentos import ExtratorRecebimentos
from src.core.use_cases.coletor_recebimentos import ColetorRecebimentos
from src.automation.pages.login_page import LoginPage
from src.automation.pages.nfe.recebimentos_page import (
    RecebimentosPage, 
    RecebimentosFilter, 
    RecebimentosFilterSituacao, 
    RecebimentosFilterTipo
)
from src.automation.pages.inicial.segundo_plano_page import SegundoPlanoPage
import src.config.config as config

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
        "download.default_directory": config.get_download_directory(),  # Define o local de download
        "download.prompt_for_download": False,       # Desativa a confirmação
        "download.directory_upgrade": True,          # Permite alterar o diretório
        "safebrowsing.enabled": True                # Desativa avisos de segurança
    })
    return options

def main():
    load_dotenv()

    edger_driver = config.Drivers().edge

    options = setup_options()
    service = Service(executable_path=edger_driver["path"])
    driver = webdriver.Edge(service=service, options=options)

    username = os.getenv("EDOCS_USERNAME")
    password = os.getenv("EDOCS_PASSWORD")
    
    logingPage = LoginPage(driver, username, password)
    logingPage.logar()
    time.sleep(2)
    segundo_plano_page = SegundoPlanoPage(driver)
    segundo_plano_page.navigate()
    time.sleep(2)
    segundo_plano_page.download_all_results()

    time.sleep(30)
    driver.quit()
    return

    recebimentosFilter = RecebimentosFilter(
        situacao=RecebimentosFilterSituacao.AUTORIZO_USO,
        data_entrada="03/07/2025",
        data_saida="04/07/2025",
        tipo = RecebimentosFilterTipo.DESTINATARIO
    )

    recebimentosPage = RecebimentosPage(driver, recebimentosFilter)

    coletorRecebimentos = ColetorRecebimentos(recebimentosPage)

    extratorRecebimentos = ExtratorRecebimentos(logingPage, coletorRecebimentos)
    extratorRecebimentos.execute()

    time.sleep(5)
    driver.quit()
    
if __name__ == "__main__":
    main()