import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from src.logger_instance import logger
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import tempfile
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from src.automation.pages.login_page import LoginPage
from src.automation.pages.nfe.recebimentos_page import RecebimentosPage, RecebimentosFilter, RecebimentosFilterSituacao, RecebimentosFilterTipo

def main():
    load_dotenv()
    # Criar um perfil temporário
    temp_profile = tempfile.mkdtemp()

    options = Options()
    options.add_argument(f"user-data-dir={temp_profile}")
    options.add_argument("--incognito")

    edge_driver_path = './drivers/msedgedriver.exe'
    service = Service(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service, options=options)

    username = os.getenv("EDOCS_USERNAME")
    password = os.getenv("EDOCS_PASSWORD")
    
    logingPage = LoginPage(driver, username, password)
    logingPage.navigate()
    logingPage.logar()
    time.sleep(2)

    recebimentosFilter = RecebimentosFilter(
        situacao=RecebimentosFilterSituacao.RECEBIDA_FORNECEDOR,
        data_entrada="01/07/2025",
        data_saida="02/07/2025",
        tipo = RecebimentosFilterTipo.DESTINATARIO
    )

    recebimentosPage = RecebimentosPage(driver, recebimentosFilter)

    recebimentosPage.navigate()
    time.sleep(10)
    recebimentosPage.toggleFilterMenu()
    time.sleep(5)
    recebimentosPage.preencherFiltros()

    time.sleep(5)
    driver.quit()
    
if __name__ == "__main__":
    main()