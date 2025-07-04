import time
from src.core.use_cases.coletor_recebimentos import ColetorRecebimentos
from src.automation.pages.login_page import LoginPage


class ExtratorRecebimentos:
    def __init__(self, login_page: LoginPage, coletor_recebimentos: ColetorRecebimentos):
        self.login_page = login_page
        self.coletor_recebimentos = coletor_recebimentos
    
    def execute(self):
        self.login_page.logar()
        time.sleep(2)
        self.coletor_recebimentos.execute()
