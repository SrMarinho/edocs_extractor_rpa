import os
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.logger_instance import logger


class LoginPage:
    URL = os.getenv("URL_EDOCS")
    PAGE_NAME = "Página de login"
    def __init__(self, driver: WebDriver, username: str, password: str):
        self.driver = driver
        self.username = username
        self.password = password

    def navigate(self) -> None:
        logger.info(f"{self.PAGE_NAME} - Navegando para pagina de login")
        self.driver.get(self.URL)
    
    def logar(self):
        try:
            self.navigate()

            textfield_username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "txbLogin"))
            )

            textfield_username.click()
            textfield_username.send_keys(self.username)
            logger.info(f"{self.PAGE_NAME} - Digitando usuário")

            textfield_password = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "txbSenha"))
            )
            textfield_password.click()
            textfield_password.send_keys(self.password)
            logger.info(f"{self.PAGE_NAME} - Digitando senha")

            btn_entrar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "btnLogin"))
            )
            btn_entrar.click()
            logger.info(f"{self.PAGE_NAME} - Logando")
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Erro ao fazer login - Parando execução - {str(e)}")
            exit()