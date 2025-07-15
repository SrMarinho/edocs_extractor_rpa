import os
import time
import subprocess
from src.automation.pages.system.explorer_page import ExplorerPage
from src.core.entities.terminal_server import TerminalServer
from src.logger_instance import logger

class SendToTs:
    def __init__(
            self,
            files: list[str], 
            terminal_server: TerminalServer,
            destination: str, 
        ):
        self.files = files
        self.terminal_server = terminal_server
        self.destination = destination
        self.explorer_page = ExplorerPage()

    def copy_files_to_clipboard(self):
        """Copia os arquivos para a área de transferência usando PowerShell"""
        try:
            # Formata os caminhos dos arquivos para o formato Windows
            formatted_files = [f"\"{str(f).replace('/', '\\')}\"".strip() for f in self.files]
            files_str = ','.join(formatted_files)
            
            # Comando PowerShell simplificado para copiar os arquivos
            ps_command = f"$files = @({files_str}); Set-Clipboard -Path $files"
            
            # Executa o comando PowerShell
            subprocess.run(['powershell', '-Command', ps_command], check=True)
            
            logger.info(f"Arquivos copiados para a área de transferência: {self.files}")
            
        except Exception as e:
            logger.error(f"Falha ao copiar arquivos para área de transferência: {str(e)}")
            raise Exception(f"Falha ao copiar arquivos para área de transferência: {str(e)}")

    def execute(self):
        # Conecta ao Terminal Server
        if not self.terminal_server.connect():
            raise Exception("Falha ao conectar ao Terminal Server")
        time.sleep(30)

        # Copia os arquivos para a área de transferência
        self.copy_files_to_clipboard()
        
        # Abre nova janela do Explorer no destino
        self.explorer_page.open_new_window()
        time.sleep(3)
        self.explorer_page.locate(self.destination)
        time.sleep(3)
        self.explorer_page.paste_files()
        time.sleep(len(self.files) * 2)  # Aguarda a cópia ser concluída
        
        # Fecha a janela do Explorer
        self.explorer_page.close_current_window()
        
        # Desconecta
        if not self.terminal_server.disconnect():
            raise Exception("Falha ao desconectar do Terminal Server")
