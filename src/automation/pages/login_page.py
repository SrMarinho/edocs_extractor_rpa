import os
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class LoginPage:
    URL = os.getenv("URL_EDOCS")
    def __init__(self, driver: WebDriver, username: str, password: str):
        self.driver = driver
        self.username = username
        self.password = password
    
    def navigate(self) -> None:
        self.driver.get(self.URL)
    
    def logar(self):
        textfield_username = self.driver.find_element(By.ID, "txbLogin")
        textfield_username.click()
        textfield_username.send_keys(self.username)

        textfield_password = self.driver.find_element(By.ID, "txbSenha")
        textfield_password.click()
        textfield_password.send_keys(self.password)

        
        btn_entrar = self.driver.find_element(By.ID, "btnLogin")
        btn_entrar.click()