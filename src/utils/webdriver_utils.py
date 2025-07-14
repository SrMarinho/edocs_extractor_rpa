import tempfile
from selenium.webdriver.edge.options import Options


def setup_edge_options(download_path: str) -> Options:
    """
    Configura as opções do Edge WebDriver com um perfil temporário.
    
    Args:
        download_path: Caminho onde os arquivos serão baixados.
    
    Returns:
        Options: Opções configuradas para o WebDriver.
    """
    temp_profile = tempfile.mkdtemp()

    options = Options()
    options.use_chromium = True
    options.add_argument(f"user-data-dir={temp_profile}")
    options.add_argument("--incognito")
    options.add_argument("--kiosk")
    options.add_experimental_option("prefs", {
        "download.default_directory": download_path.replace("/", "\\"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    return options