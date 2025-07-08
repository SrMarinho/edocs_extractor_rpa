import time
from selenium.webdriver.remote.webdriver import WebDriver
from src.automation.pages.nfe.recebimentos_page import RecebimentosPage
from src.logger_instance import logger

class ColetorRecebimentos:
    def __init__(self, recebimentos_page: RecebimentosPage):
        self.recebimentos_page = recebimentos_page

    def execute(self) -> bool:
        try:
            logger.info("Iniciando coleta de recebimentos para XML")
            
            self.recebimentos_page.navigate()
            self.recebimentos_page.toggleFilterMenu()
            time.sleep(2)

            self._aplicar_filtros()
            
            self.recebimentos_page.applyFilters()
                
            time.sleep(2)
            
            if self.recebimentos_page.hasReceipt():
                self.recebimentos_page.saveAllXML()
                time.sleep(2)
                self.recebimentos_page.handleXMLDownloadMessage()
            
            logger.info("Coleta de recebimentos feita com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro durante a coleta: {str(e)}")
            return False

    def _aplicar_filtros(self):
        """Aplica todos os filtros configurados"""
        try:
            self.recebimentos_page.setSituacao()
            self.recebimentos_page.setNumero()
            self.recebimentos_page.setRetorno()
            self.recebimentos_page.setDataEntrada()
            time.sleep(1)
            self.recebimentos_page.setDataSaida()
            time.sleep(1)
            self.recebimentos_page.setTipo()
            self.recebimentos_page.setTipoNota()
            self.recebimentos_page.setCpnjCpfEmitente()
            self.recebimentos_page.setUfEmitente()
            self.recebimentos_page.setNomeDestinatario()
        except Exception as e:
            logger.warning(f"Erro ao aplicar filtro: {str(e)}")