import pytest
from unittest.mock import create_autospec
from src.automation.tasks.extrator_recebimentos import ExtratorRecebimentos
from src.automation.pages.login_page import LoginPage
from src.automation.pages.nfe.recebimentos_page import RecebimentosPage
from src.automation.pages.inicial.segundo_plano_page import SegundoPlanoPage
from src.core.use_cases.coletor_recebimentos import ColetorRecebimentos
from src.core.use_cases.download_recebimentos import DownloadRecebimentos
from src.core.use_cases.processador_recebimentos import ProcessadorRecebimentos
from src.core.use_cases.send_to_ts import SendToTs
from src.core.entities.terminal_server import TerminalServer
import src.config.config as config

@pytest.fixture
def login_page():
    return create_autospec(LoginPage)

@pytest.fixture
def recebimentos_page():
    return create_autospec(RecebimentosPage)

@pytest.fixture
def segundo_plano_page():
    return create_autospec(SegundoPlanoPage)

@pytest.fixture
def terminal_server():
    return create_autospec(TerminalServer)

@pytest.mark.integration
class TestExtratorRecebimentosIntegration:
    def test_execute(self, login_page, recebimentos_page, segundo_plano_page, terminal_server):
        # Inicializa os use cases com dependências mockadas
        coletor = ColetorRecebimentos(recebimentos_page)
        download = DownloadRecebimentos(segundo_plano_page)
        processador = ProcessadorRecebimentos()

        # Mocka SendToTs
        send_to_ts = SendToTs(files=[], terminal_server=terminal_server, destination="/destination")

        # Inicializa o extrator
        extrator = ExtratorRecebimentos(
            login_page=login_page,
            coletor_recebimentos=coletor,
            download_recebimentos=download,
            processador_recebimentos=processador,
            send_to_ts=send_to_ts
        )

        # Executa
        extrator.execute()

        # Verifica se os métodos principais foram chamados
        login_page.logar.assert_called_once()
        recebimentos_page.some_method.assert_called()
        segundo_plano_page.some_other_method.assert_called()
        send_to_ts.execute.assert_called_once()
