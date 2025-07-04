import os
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.logger_instance import logger


class SegundoPlanoPage:
    URL = os.getenv("URL_EDOCS") + "/Sistema/SegundoPlano/ProcessamentoSegundoPlano.aspx"
    PAGE_NAME = "SegundoPlano"

    def __init__(self, driver: WebDriver):
        self.driver = driver
    
    def refresh_list(self):
        ...
    
    def delete_register_msg_handler(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "btnBarraMensagemSim"))
            )
            element.click()

            logger.info(f"{self.PAGE_NAME} - Confirmando exclusão de registro")
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Erro ao tentar confirmar exclusão de registro: {str(e)}")