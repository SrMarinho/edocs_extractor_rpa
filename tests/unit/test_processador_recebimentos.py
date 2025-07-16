import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from src.core.use_cases.processador_recebimentos import ProcessadorRecebimentos

@pytest.fixture
def processador():
    return ProcessadorRecebimentos()

@pytest.fixture
def mock_zip_file(tmp_path):
    # Cria um arquivo ZIP de teste
    zip_path = tmp_path / "test.zip"
    zip_path.write_bytes(b"test data")
    return zip_path

@pytest.mark.unit
class TestProcessadorRecebimentos:
    def test_init(self, processador):
        assert processador.zip_file is None
        assert isinstance(processador.zip_path, Path)
        assert isinstance(processador.temp_dir, Path)

    def test_execute_without_zip_file(self, processador):
        with pytest.raises(ValueError, match="É necessário indicar o um arquivo"):
            processador.execute()

    @patch("src.core.use_cases.processador_recebimentos.zipfile.ZipFile")
    def test_extrair_zip(self, mock_zipfile, processador, mock_zip_file):
        processador.zip_file = "test.zip"
        processador._extrair_zip()
        mock_zipfile.assert_called_once()

    def test_filtrar_arquivos(self, processador, tmp_path):
        # Setup
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        
        # Criar alguns arquivos de teste
        (test_dir / "valid.xml").write_text("test")
        (test_dir / "NFe-OPCIEN.xml").write_text("test")
        
        processador.temp_dir = tmp_path
        processador.zip_file = "test_dir"
        
        # Test
        processador._filtrar_arquivos()
        
        # Verify
        assert len(processador.arquivos_validos) == 1
        assert processador.arquivos_validos[0].name == "valid.xml"

    @patch("src.core.use_cases.processador_recebimentos.shutil.move")
    def test_mover_validos(self, mock_move, processador, tmp_path):
        # Setup
        processador.arquivos_validos = [Path(tmp_path / "test.xml")]
        
        # Test
        processador._mover_validos()
        
        # Verify
        mock_move.assert_called_once()

    @patch("src.core.use_cases.processador_recebimentos.shutil.rmtree")
    @patch("pathlib.Path.unlink")
    def test_limpar_temp(self, mock_unlink, mock_rmtree, processador):
        processador.zip_file = "test.zip"
        processador._limpar_temp()
        
        mock_rmtree.assert_called_once()
        mock_unlink.assert_called_once()

    def test_limpar_xml(self, processador, tmp_path):
        # Setup
        xml_dir = tmp_path / "xml"
        xml_dir.mkdir()
        test_file = xml_dir / "test.xml"
        test_file.write_text("test")
        
        with patch("src.core.use_cases.processador_recebimentos.XML_DESTINATION_PATH", str(xml_dir)):
            # Test
            processador.limpar_xml()
            
            # Verify
            assert not test_file.exists()
