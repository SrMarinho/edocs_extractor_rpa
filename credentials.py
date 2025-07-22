import os
import keyring
from typing import Tuple
from dotenv import load_dotenv
from src.logger_instance import logger
from getpass import getpass
from cryptography.fernet import Fernet

def input_credentials(secret_key: str) -> Tuple[str, str, str]:
    """
    Obtém as credenciais do usuário e a chave do gerenciador de credenciais.
    
    Returns:
        Tuple[str, str, str]: (wcm_key, username, password)
    
    Raises:
        ValueError: Se as credenciais não puderem ser obtidas
    """
    try:
        wcm_key = os.getenv("WINDOWS_CREDENTIAL_MANAGER_EDOCS_KEY")
        if not wcm_key:
            logger.error("Chave WCM não encontrada no .env")
            raise ValueError("Chave para credenciais do Windows não encontrada")

        
        username = input("Username: ").strip()
        if not username:
            raise ValueError("Username não pode ser vazio")

            
        password = getpass("Password: ")
        if not password:
            raise ValueError("Password não pode ser vazio")

        cipher = Fernet(secret_key)

        crypted_password = cipher.encrypt(password.encode("utf-8"))

        return wcm_key, username, crypted_password.decode("utf-8")
        
    except Exception as e:
        logger.error(f"Falha na configuração: {str(e)}")
        raise

def save_auth(wcm_key: str, username: str, password: str) -> None:
    """
    Salva as credenciais no Windows Credential Manager.
    
    Args:
        wcm_key: Chave de identificação
        username: Nome de usuário
        password: Senha
    
    Raises:
        Exception: Se falhar ao salvar as credenciais
    """
    try:
        keyring.set_password(wcm_key, username, password)
        logger.info("Credenciais salvas com sucesso")
    except Exception as e:
        logger.error(f"Erro ao salvar credenciais: {str(e)}")
        raise

def main():
    """Função principal que carrega configurações e salva credenciais."""
    try:
        if not load_dotenv():
            logger.warning(".env não encontrado ou não carregado")
        
        secret_key = os.getenv("SECRET_KEY", "")
        wcm_key, username, password = input_credentials(secret_key)
        save_auth(wcm_key, username, password)
        
        # Limpeza de segurança
        del password
    except Exception as e:
        logger.critical(f"Falha crítica: {str(e)}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()