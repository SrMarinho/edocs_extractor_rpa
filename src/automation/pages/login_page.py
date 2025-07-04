import os
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    URL = os.getenv("URL_EDOCS")
    def __init__(self, driver: WebDriver, username: str, password: str):
        self.driver = driver
        self.username = username
        self.password = password
    
    def navigate(self) -> None:
        self.driver.get(self.URL)
    
    def logar(self):
        self.navigate()

        textfield_username = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "txbLogin"))
        )
        textfield_username.click()
        textfield_username.send_keys(self.username)

        textfield_password = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "txbSenha"))
        )
        textfield_password.click()
        textfield_password.send_keys(self.password)

        btn_entrar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnLogin"))
        )
        btn_entrar.click()