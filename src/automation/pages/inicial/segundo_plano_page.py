import os
import time
from dataclasses import dataclass
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from src.logger_instance import logger


@dataclass
class ProcessamentoTable:
    descricao: str
    tipo: str
    documento: str
    operacao: str
    data: str
    usuario: str
    resultado: str


class SegundoPlanoPage:
    URL = str(os.getenv("URL_EDOCS")) + \
        "/Sistema/SegundoPlano/ProcessamentoSegundoPlano.aspx"
    PAGE_NAME = "SegundoPlano"

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate(self) -> None:
        self.driver.get(self.URL)

    def refresh_list(self):
        logger.info(
                f"{self.PAGE_NAME} - Atualizando lista de processamento")
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "btnAtualizarGrid"))
            )
            element.click()
        except Exception as e:
            logger.error(
                f"{self.PAGE_NAME} - Atualizar lista de processamento: {str(e)}")

    def download_result(self, row: WebElement) -> bool:
        logger.info(f"{self.PAGE_NAME} - Tentando baixar registro")
        try:
            cells = WebDriverWait(row, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
            )
            try:
                element = WebDriverWait(cells[-1], 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "a"))
                )
                if element and element.text.endswith(".zip"):
                    cells[-1].click()
                    return True
                return True
            except Exception as e:
                return False
        except Exception as e:
            return False

    def download_all_results(self):
        logger.info(f"{self.PAGE_NAME} - Iniciando download de registros")
        
        MAX_DOWNLOAD_ATTEMPTS = 50
        REFRESH_WAIT_TIME = 30
        
        try:
            table = self._get_results_table()
            rows = table.find_elements(By.TAG_NAME, "tr")

            for row_index, row in enumerate(rows):
                download_success = self._process_row_download(row, row_index, 
                                                            MAX_DOWNLOAD_ATTEMPTS, 
                                                            REFRESH_WAIT_TIME)
                
                table = self._get_results_table()
                rows = table.find_elements(By.TAG_NAME, "tr")
                if not download_success:
                    logger.warning(f"{self.PAGE_NAME} - Falha ao baixar registro na linha {row_index}")
                
                time.sleep(REFRESH_WAIT_TIME)
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Erro durante o download dos arquivos: {str(e)}")
            raise

    def _get_results_table(self):
        try:
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "grdProcessamentos"))
            )
            
            tbody = WebDriverWait(self.driver, 10).until(
                lambda driver: table.find_element(By.TAG_NAME, "tbody")
            )
            
            return tbody
            
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Elementos da tabela não encontrados: {str(e)}")
            raise

    def _process_row_download(self, row: WebElement, row_index: int, max_attempts: int, wait_time: float) -> bool:
        """Tenta fazer o download para uma linha específica com waits explícitos
        
        Args:
            row: Elemento da linha da tabela
            row_index: Índice da linha sendo processada
            max_attempts: Número máximo de tentativas
            wait_time: Tempo de espera entre tentativas
        
        Returns:
            bool: True se o download foi bem-sucedido, False caso contrário
        """
        for attempt in range(1, max_attempts + 1):
            try:
                # Tenta fazer o download
                if self.download_result(row):
                    logger.info(f"{self.PAGE_NAME} - Download concluído para linha {row_index + 1}")
                    return True
                else:
                    logger.info(f"{self.PAGE_NAME} - Erro ao tentar baixar linha {row_index + 1}")

                logger.debug(f"{self.PAGE_NAME} - Tentativa {attempt}/{max_attempts} para linha {row_index + 1}")
                
                # Atualiza a lista
                self.refresh_list()
                time.sleep(15)
                
                # Atualiza referências
                table = self._get_results_table()
                rows = WebDriverWait(table, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
                )
                row = rows[row_index]
                
            except Exception as e:
                logger.error(f"{self.PAGE_NAME} - Erro inesperado na linha {row_index}: {str(e)}")
                raise

        logger.warning(f"{self.PAGE_NAME} - Máximo de tentativas ({max_attempts}) atingido para linha {row_index}")
        return False

    def delete_register(self, reg_identification: str = "") -> None:
            logger.info(
                f"{self.PAGE_NAME} - Excluir registro - {reg_identification}")
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "btnExcluir"))
                )
                element.click()
            except Exception as e:
                logger.error(
                    f"{self.PAGE_NAME} - Erro ao tentar excluir registro: {str(e)}")

    def delete_register_msg_handler(self):
        logger.info(f"{self.PAGE_NAME} - Confirmando exclusão de registro")
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "btnBarraMensagemSim"))
            )
            element.click()
        except Exception as e:
            logger.error(
                f"{self.PAGE_NAME} - Erro ao tentar confirmar exclusão de registro: {str(e)}")

    def clearTable(self):
        logger.info(f"{self.PAGE_NAME} - Limpando a tabela de registros")
        try:
            # Continua até não haver mais registros
            while True:
                table = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "grdProcessamentos"))
                )
                
                body = WebDriverWait(table, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "tbody"))
                )

                rows = WebDriverWait(body, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
                )

                td = []
                if rows[0]:
                    td = WebDriverWait(rows[0], 10).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
                    )
                
                if len(td) <= 1:
                    logger.warning(f"{self.PAGE_NAME} - Nenhum registro encontrado")
                    return True
                
                row = rows[0]
                row_text = row.text
                
                row.click()
                time.sleep(2)
                self.delete_register(row_text)
                time.sleep(2)
                self.delete_register_msg_handler()
                time.sleep(2)
                
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao tentar limpar tabela: {str(e)}")
            return False

    def quit(self):
        self.driver.quit()