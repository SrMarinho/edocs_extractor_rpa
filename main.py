import os
from pathlib import Path
from typing import List, Optional

import keyring
from selenium import webdriver
from selenium.webdriver.edge.service import Service

from src.automation.pages.login_page import LoginPage
from src.automation.pages.nfe.recebimentos_page import RecebimentosPage, RecebimentosFilter
from src.automation.pages.inicial.segundo_plano_page import SegundoPlanoPage
from src.automation.tasks.extrator_recebimentos import ExtratorRecebimentos

from src.core.use_cases.coletor_recebimentos import ColetorRecebimentos
from src.core.use_cases.download_recebimentos import DownloadRecebimentos
from src.core.use_cases.processador_recebimentos import ProcessadorRecebimentos
from src.core.use_cases.send_to_ts import SendToTs
from src.core.entities.terminal_server import TerminalServer

from src.utils.webdriver_utils import setup_edge_options
from src.logger_instance import logger
import src.config.config as config


def setup_environment() -> tuple[Path, str, str]:
    """Configura e valida as variáveis de ambiente necessárias."""
    xml_dir = Path(os.getenv("XML_FILE_FINAL_DESTINATION"))
    host = os.getenv("TERMINAL_SERVER_HOST")
    destination = str(Path(os.getenv("TERMINAL_SERVER_XML_FOLDER")))

    if not all([host, destination]):
        raise ValueError("Variáveis de ambiente não configuradas corretamente")

    # Garante que a pasta XML existe
    xml_dir.mkdir(parents=True, exist_ok=True)
    
    return xml_dir, host, destination


def setup_webdriver() -> webdriver.Edge:
    """Configura e inicializa o WebDriver do Edge."""
    headless = False if os.getenv('HEADLESS_MODE', False) == True else True
    options = setup_edge_options(config.DOWNLOAD_PATH, headless=headless)
    service = Service(executable_path=config.Drivers().edge["path"])
    return webdriver.Edge(service=service, options=options)

def initialize_pages(driver: webdriver.Edge) -> tuple[LoginPage, RecebimentosPage]:
    """Inicializa as páginas necessárias para o processo."""
    credential_key = os.getenv("WINDOWS_CREDENTIAL_MANAGER_EDOCS_KEY")
    if not credential_key:
        logger.warning("Erro ao tentar buscar usuário e senha no Windows Credential Manager, por favor, coloque suas credenciais lá, parando execução")
        exit()

    try:
        creds = keyring.get_credential(credential_key, None)
    except Exception as e:
        logger.error("Erro ao tentar buscar usuário e senha no Windows Credential Manager, por favor, coloque suas credenciais lá")
        raise e

    if not creds:
        logger.error("Cadastre usuário e senha no Windows Credential Manager")
        raise ValueError("Cadastre usuário e senha no Windows Credential Manager")

    username = creds.username
    password = creds.password

    login_page = LoginPage(
        driver, 
        username,
        password
    )
    
    recebimentos_page = RecebimentosPage(
        driver, 
        RecebimentosFilter(**RecebimentosFilter.get_params()["filtros"])
    )
    
    return login_page, recebimentos_page


def get_xml_files(xml_dir: Path) -> List[str]:
    """Retorna a lista de arquivos XML no diretório especificado."""
    return [str(Path(xml_dir / f)) for f in os.listdir(xml_dir) if f.endswith('.xml')]


def process_xml_files(driver: webdriver.Edge, xml_dir: Path, host: str, destination: str) -> None:
    """Processa os arquivos XML e envia para o Terminal Server se houver arquivos."""
    try:
        # Inicializa páginas e componentes
        login_page, recebimentos_page = initialize_pages(driver)
        
        send_to_ts = SendToTs(
            terminal_server=TerminalServer(host),
            destination=destination,
        )
        # Configura e executa o extrator
        extrator = ExtratorRecebimentos(
            login_page=login_page,
            coletor_recebimentos=ColetorRecebimentos(recebimentos_page),
            download_recebimentos=DownloadRecebimentos(SegundoPlanoPage(driver)),
            processador_recebimentos=ProcessadorRecebimentos(),
            send_to_ts=send_to_ts
        )
        
        extrator.execute()
        
    except Exception as e:
        logger.critical(f"Erro crítico durante o processamento: {e}", exc_info=True)
        driver.save_screenshot("erro_critico.png")
        raise


def main() -> None:
    """Função principal que coordena o processo de extração e envio de XMLs."""
    try:
        # Configura ambiente e webdriver
        xml_dir, host, destination = setup_environment()
        
        with setup_webdriver() as driver:
            process_xml_files(driver, xml_dir, host, destination)
            
    except Exception as e:
        logger.critical(f"Erro crítico na execução principal: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
