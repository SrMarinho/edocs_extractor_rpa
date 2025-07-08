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
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "btnAtualizarGrid"))
            )
            element.click()
        except Exception as e:
            logger.error(
                f"{self.PAGE_NAME} - Atualizar lista de processamento: {str(e)}")

    def download_result(self, row: WebElement) -> bool:
        logger.info(f"{self.PAGE_NAME} - Baixando registro - {row.text}")
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells[7]:
                try:
                    element = WebDriverWait(cells[7], 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "a"))
                    )
                    # Clicar no link para download do arquivo
                    if element and element.text.endswith(".zip"):
                        element.click()
                        return True
                    else:
                        # Para quando não é algo "baixavel"
                        return True
                except Exception as e:
                    # Caso não ache o link do arquivo
                    return False
        except Exception as e:
            logger.error(
                f"{self.PAGE_NAME} - Falha ao tentar baixar arquivo - {row.text}: {str(e)}")
            return False

    def download_all_results(self):
        logger.info(f"{self.PAGE_NAME} - Baixando registros")
        try:
            # Percorrendo linhas da tabela
            for _ in range(10):  # Número máximo de tentativas de refresh
                table = self.driver.find_element(By.ID, "grdProcessamentos")
                body = table.find_element(By.TAG_NAME, "tbody")
                rows = body.find_elements(By.TAG_NAME, "tr")
                
                for i, row in enumerate(rows):
                    tries = 15

                    # fica atualizando a lista até o link de download ou mensagem aparecer
                    for _ in range(tries):
                        if not self.download_result(row):
                            self.refresh_list()
                            time.sleep(15)
                            # Recarregar TODAS as linhas após refresh
                            table = self.driver.find_element(By.ID, "grdProcessamentos")
                            body = table.find_element(By.TAG_NAME, "tbody")
                            rows = body.find_elements(By.TAG_NAME, "tr")
                            # Reatribuir a row atual usando o índice
                            row = rows[i]
                        else:
                            break
                    # Espera pelo download
                    time.sleep(60)
                break  # Sai do loop se completar todas as linhas
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao tentar baixar arquivos: {str(e)}")

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
            while True:  # Continua até não haver mais registros
                table = self.driver.find_element(By.ID, "grdProcessamentos")
                body = table.find_element(By.TAG_NAME, "tbody")
                rows = body.find_elements(By.TAG_NAME, "tr")
                
                if not rows:
                    break
                    
                row = rows[0]
                row_text = row.text
                
                row.click()
                time.sleep(2)
                self.delete_register(row_text)
                time.sleep(2)
                self.delete_register_msg_handler()
                
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao tentar limpar tabela: {str(e)}")
            return False
        return True

    def quit(self):
        self.driver.quit()