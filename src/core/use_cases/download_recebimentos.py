import time
from src.automation.pages.inicial.segundo_plano_page import SegundoPlanoPage


class DownloadRecebimentos:
    def __init__(self, segundo_plano_page: SegundoPlanoPage):
        self.segundo_plano_page = segundo_plano_page
    
    def execute(self):
        self.segundo_plano_page.navigate()
        time.sleep(5)
        self.segundo_plano_page.download_all_results()
        time.sleep(30)
        self.segundo_plano_page.clearTable()
    
    def quit(self):
        self.segundo_plano_page.quit()