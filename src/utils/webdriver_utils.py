import os
import tempfile
from selenium.webdriver.edge.options import Options


def setup_edge_options(
        download_path: str,
        headless: bool = True,
        kiosk: bool = True,  # Kiosk não costuma ser usado com headless
        incognito: bool = True,  # Corrigido o erro de sintaxe
    ) -> Options:
    """
    Configura as opções do Edge WebDriver com um perfil temporário.
    
    Args:
        download_path: Caminho onde os arquivos serão baixados.
        headless: Executar sem interface gráfica (padrão: True).
        kiosk: Modo tela cheia (padrão: False).
        incognito: Modo privado (padrão: False).
    
    Returns:
        Options: Opções configuradas para o WebDriver.
    """
    temp_profile = tempfile.mkdtemp()

    options = Options()
    options.add_argument(f"user-data-dir={temp_profile}")
    
    if headless:
        options.add_argument("--headless=new")  # Formato atualizado
        options.add_argument("--disable-gpu")  # Prefixo corrigido
    
    if kiosk:
        options.add_argument("--kiosk")  # Só faz sentido em modo GUI
    
    if incognito:
        options.add_argument("--inprivate")  # Edge usa "--inprivate" (não "--incognito")
    
    options.add_experimental_option("prefs", {
        "download.default_directory": download_path.replace("/", "\\"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
    return options