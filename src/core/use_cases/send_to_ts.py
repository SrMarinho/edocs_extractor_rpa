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
        """Copia os arquivos para a área de transferência usando PowerShell com suporte a caminhos longos"""
        try:
            # Cria um arquivo temporário com a lista de arquivos
            temp_list_path = os.path.join(os.path.dirname(self.files[0]), 'temp_file_list.txt')
            with open(temp_list_path, 'w', encoding='utf-8') as f:
                for file_path in self.files:
                    abs_path = os.path.abspath(str(file_path))
                    f.write(f"{abs_path}\n")
            
            # Comando PowerShell otimizado usando o arquivo temporário
            ps_command = f"""
                $files = Get-Content -Path "{temp_list_path}" -Encoding UTF8
                try {{
                    Set-Clipboard -Path $files -ErrorAction Stop
                    Write-Output "Arquivos copiados para a área de transferência"
                }} catch {{
                    Write-Error "Falha ao copiar arquivos: $_"
                    exit 1
                }} finally {{
                    Remove-Item -Path "{temp_list_path}" -Force
                }}
            """
            
            # Executa o comando PowerShell com timeout
            result = subprocess.run(['powershell', '-Command', ps_command], 
                                check=True,
                                capture_output=True,
                                text=True,
                                timeout=30)
            
            logger.info(f"Arquivos copiados com sucesso: {result.stdout}")
            return True
        except subprocess.TimeoutExpired:
            logger.error("Timeout ao tentar copiar arquivos para área de transferência")
            raise Exception("Operação demorou muito tempo")
        except subprocess.CalledProcessError as e:
            error_msg = f"Erro no PowerShell: {e.stderr}" if e.stderr else "Erro desconhecido no PowerShell"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            raise Exception(f"Falha ao copiar arquivos: {str(e)}")

    def execute(self):
        # Conecta ao Terminal Server
        if not self.terminal_server.connect():
            raise Exception("Falha ao conectar ao Terminal Server")
        time.sleep(30)

        try:
            # Copia os arquivos para a área de transferência
            self.copy_files_to_clipboard()
            
            # Abre nova janela do Explorer no destino
            self.explorer_page.open_new_window()
            time.sleep(3)
            self.explorer_page.locate(self.destination)
            time.sleep(3)
            self.explorer_page.paste_files()
            time.sleep(len(self.files) * 0.1)  # Aguarda a cópia ser concluída
            time.sleep(3)
            # Fecha a janela do Explorer
            self.explorer_page.close_current_window()
            time.sleep(1)

            # Desconecta
            if not self.terminal_server.disconnect():
                raise Exception("Falha ao desconectar do Terminal Server")
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            if not self.terminal_server.disconnect():
                raise Exception("Falha ao desconectar do Terminal Server")
            raise Exception(f"Falha ao copiar arquivos: {str(e)}")

