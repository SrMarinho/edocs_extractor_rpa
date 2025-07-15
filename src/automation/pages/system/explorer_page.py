import pyautogui
import time
from src.logger_instance import logger

class ExplorerPage:
    PAGE_NAME = "Windows Explorer"

    def locate(self, location: str):
        """Foca no campo de endereço do Explorer"""
        try:
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(2)
            pyautogui.write(str(location))
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(1)
            logger.info(f"{self.PAGE_NAME} - Campo de endereço focado")
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Não foi possível pressionar tecla de atalho para 'localizar': {str(e)}")

    def open_new_window(self):
        """Abre uma nova janela do Explorer"""
        try:
            pyautogui.hotkey('win', 'e')
            logger.info(f"{self.PAGE_NAME} - Nova janela aberta")
            time.sleep(1)  # Espera a janela abrir
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao abrir nova janela: {str(e)}")

    def navigate_to_path(self, path):
        """Navega para um caminho específico no Explorer"""
        try:
            self.locate()  # Foca no campo de endereço
            pyautogui.write(path)
            pyautogui.press('enter')
            logger.info(f"{self.PAGE_NAME} - Navegado para: {path}")
            time.sleep(1)  # Espera a navegação completar
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao navegar para o caminho {path}: {str(e)}")

    def create_new_folder(self, folder_name):
        """Cria uma nova pasta no local atual"""
        try:
            pyautogui.hotkey('ctrl', 'shift', 'n')
            time.sleep(0.5)
            pyautogui.write(folder_name)
            pyautogui.press('enter')
            logger.info(f"{self.PAGE_NAME} - Pasta '{folder_name}' criada com sucesso")
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao criar nova pasta: {str(e)}")

    def refresh(self):
        """Atualiza a janela atual do Explorer"""
        try:
            pyautogui.hotkey('f5')
            logger.info(f"{self.PAGE_NAME} - Janela atualizada")
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao atualizar janela: {str(e)}")

    def close_current_window(self):
        """Fecha a janela atual do Explorer"""
        try:
            pyautogui.hotkey('alt', 'f4')
            logger.info(f"{self.PAGE_NAME} - Janela fechada")
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao fechar janela: {str(e)}")

    def search_file(self, filename):
        """Realiza uma busca por um arquivo na pasta atual"""
        try:
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            pyautogui.write(filename)
            logger.info(f"{self.PAGE_NAME} - Buscando por arquivo: {filename}")
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao buscar arquivo: {str(e)}")

    def select_all(self):
        """Seleciona todos os itens na pasta atual"""
        try:
            pyautogui.hotkey('ctrl', 'a')
            logger.info(f"{self.PAGE_NAME} - Todos os itens selecionados")
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao selecionar todos os itens: {str(e)}")

    def view_details(self):
        """Altera a visualização para detalhes"""
        try:
            pyautogui.hotkey('ctrl', 'shift', '6')
            logger.info(f"{self.PAGE_NAME} - Visualização alterada para detalhes")
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao alterar visualização: {str(e)}")

    def open_properties(self):
        """Abre as propriedades do item selecionado"""
        try:
            pyautogui.hotkey('alt', 'enter')
            logger.info(f"{self.PAGE_NAME} - Propriedades abertas")
            time.sleep(1)  # Espera a janela de propriedades abrir
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao abrir propriedades: {str(e)}")

    def paste_files(self):
        """Cola arquivos copiados/recortados no local atual do Explorer"""
        try:
            pyautogui.hotkey('ctrl', 'v')
            logger.info(f"{self.PAGE_NAME} - Comando de colar executado")
            time.sleep(1)  # Pequena pausa para garantir que a ação seja completada
            return True
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao colar arquivos: {str(e)}")
            return False