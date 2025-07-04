import os
import time
from dotenv import load_dotenv
from selenium import webdriver
import tempfile
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from src.automation.pages.login_page import LoginPage
from src.automation.pages.nfe.recebimentos_page import (
    RecebimentosPage, 
    RecebimentosFilter, 
    RecebimentosFilterSituacao, 
    RecebimentosFilterTipo
)
from src.automation.tasks.extrator_recebimentos import ExtratorRecebimentos
from src.core.use_cases.coletor_recebimentos import ColetorRecebimentos
from src.config.config import download_directory

def main():
    load_dotenv()
    # Criar um perfil temporário
    temp_profile = tempfile.mkdtemp()

    options = Options()
    options.add_argument(f"user-data-dir={temp_profile}")
    options.add_argument("--incognito")
    options.add_experimental_option("prefs", {
        "download.default_directory": download_directory,  # Define o local de download
        "download.prompt_for_download": False,       # Desativa a confirmação
        "download.directory_upgrade": True,          # Permite alterar o diretório
        "safebrowsing.enabled": True                # Desativa avisos de segurança
    })

    edge_driver_path = './drivers/msedgedriver.exe'
    service = Service(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service, options=options)

    username = os.getenv("EDOCS_USERNAME")
    password = os.getenv("EDOCS_PASSWORD")
    
    logingPage = LoginPage(driver, username, password)

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