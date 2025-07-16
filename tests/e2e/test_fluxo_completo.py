import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from pathlib import Path
import os
import time

from src.automation.tasks.extrator_recebimentos import ExtratorRecebimentos
from src.automation.pages.login_page import LoginPage
from src.automation.pages.nfe.recebimentos_page import RecebimentosPage, RecebimentosFilter
from src.automation.pages.inicial.segundo_plano_page import SegundoPlanoPage
from src.core.use_cases.coletor_recebimentos import ColetorRecebimentos
from src.core.use_cases.download_recebimentos import DownloadRecebimentos
from src.core.use_cases.processador_recebimentos import ProcessadorRecebimentos
from src.core.use_cases.send_to_ts import SendToTs
from src.core.entities.terminal_server import TerminalServer
from src.utils.webdriver_utils import setup_edge_options
import src.config.config as config

@pytest.fixture(scope="module")
def driver():
    options = setup_edge_options(config.DOWNLOAD_PATH)
    service = Service(executable_path=config.Drivers().edge["path"])
    driver = webdriver.Edge(service=service, options=options)
    yield driver
    driver.quit()

@pytest.fixture
def xml_dir(tmp_path):
    xml_dir = tmp_path / "xml"
    xml_dir.mkdir()
    return xml_dir

@pytest.fixture
def env_vars(monkeypatch, xml_dir):
    # Setup environment variables
    monkeypatch.setenv("EDOCS_USERNAME", "test_user")
    monkeypatch.setenv("EDOCS_PASSWORD", "test_pass")
    monkeypatch.setenv("TERMINAL_SERVER_HOST", "test_host")
    monkeypatch.setenv("TERMINAL_SERVER_XML_FOLDER", str(xml_dir))
    monkeypatch.setenv("XML_FILE_FINAL_DESTINATION", str(xml_dir))

@pytest.mark.e2e
@pytest.mark.slow
def test_fluxo_completo(driver, env_vars, xml_dir):
    try:
        # Inicialização das páginas/services
        login_page = LoginPage(
            driver, 
            os.getenv("EDOCS_USERNAME"), 
            os.getenv("EDOCS_PASSWORD")
        )
        
        recebimentos_page = RecebimentosPage(
            driver, 
            RecebimentosFilter(**RecebimentosFilter.get_params()["filtros"])
        )

        # Configura e executa o extrator
        extrator = ExtratorRecebimentos(
            login_page=login_page,
            coletor_recebimentos=ColetorRecebimentos(recebimentos_page),
            download_recebimentos=DownloadRecebimentos(SegundoPlanoPage(driver)),
            processador_recebimentos=ProcessadorRecebimentos(),
            send_to_ts=SendToTs(
                files=[],  # Será preenchido após a extração
                terminal_server=TerminalServer(os.getenv("TERMINAL_SERVER_HOST")),
                destination=os.getenv("TERMINAL_SERVER_XML_FOLDER")
            )
        )

        # Executa o fluxo completo
        extrator.execute()

        # Verificações
        assert xml_dir.exists()
        xml_files = list(xml_dir.glob("*.xml"))
        assert len(xml_files) > 0

    except Exception as e:
        driver.save_screenshot("erro_e2e.png")
        raise
