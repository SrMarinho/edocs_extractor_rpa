import os
import time
from datetime import datetime, timedelta
from enum import Enum, unique
from typing import Optional
import toml
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.logger_instance import logger



@unique
class RecebimentosFilterSituacao(Enum):
    ALL = "ALL"
    RECEBIDA_FORNECEDOR = "RECEBIDA_FORNECEDOR"
    AUTORIZO_USO = "AUTORIZO_USO"
    CRITICA_VALIDACAO = "CRITICA_VALIDACAO"
    CANCELADA = "CANCELADA"
    DENEGADA = "DENEGADA"
    
    def __str__(self):
        return self.name

@unique
class RecebimentosFilterRetorno(Enum):
    ALL = "ALL"
    RETORNADO = "RETORNADO"
    CONSULTA_PENDENTE = "CONSULTA_PENDENTE"
    NAO_RETORNADO = "NAO_RETORNADO"
    DESATIVADO = "DESATIVADO"
    ERRO_RETORNO = "ERRO_RETORNO"
    
    def __str__(self):
        return self.name

@unique
class RecebimentosFilterTipoNota(Enum):
    ALL = "ALL"
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    
    def __str__(self):
        return self.name

@unique
class RecebimentosFilterUfEmissao(Enum):
    ALL = "ALL"
    PI = "PI"
    MA = "MA"
    
    def __str__(self):
        return self.name

@unique
class RecebimentosFilterTipo(Enum):
    ALL = "ALL"
    DESTINATARIO = "DESTINATARIO"
    TERCEIRO = "TERCEIRO"
    TRANSPORTADOR = "TRANSPORTADOR"
    
    def __str__(self):
        return self.name

@unique
class RecebimentosFilterManifestacaoDestinatario(Enum):
    ALL = "ALL"
    CIENCIA_OPERACAO = "CIENCIA_OPERACAO"
    CONFIRMACAO_OPERACAO = "CONFIRMACAO_OPERACAO"
    OPERACAO_NAO_REALIZADA = "OPERACAO_NAO_REALIZADA"
    DESCONHECIMENTO_OPERACAO = "DESCONHECIMENTO_OPERACAO"
    
    def __str__(self):
        return self.name

class RecebimentosFilter:
    PARAMS_FILE = "files/parametros/recebimentos_filters.toml"
    def __init__(
        self,
        situacao: str =  "", 
        numero: str = "",
        retorno: str = "",
        data_entrada: str = "",
        data_saida: str = "",
        tipo_nota: str = "",
        cnpj_cpf_emitente: str = "",
        uf_emissao: str = "",
        nome_destinatario: str = "",
        serie: str = "",
        chave: str = "",
        total_inicial: str = "",
        total_final: str = "",
        tipo: str = "",
        nome_emitente: str = "",
        data_emissao_inicial: str = "",
        data_emissao_final: str = "",
        inscricao_estadual_destinatario: str = "",
        manifestacao_destinatario: str = ""
    ):
        self.situacao = situacao
        self.numero = numero
        self.retorno = retorno
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.tipo_nota = tipo_nota
        self.cnpj_cpf_emitente = cnpj_cpf_emitente
        self.uf_emissao = uf_emissao
        self.nome_destinatario = nome_destinatario
        self.serie = serie
        self.chave = chave
        self.total_inicial = total_inicial
        self.total_final = total_final
        self.tipo = tipo
        self.nome_emitente = nome_emitente
        self.data_emissao_inicial = data_emissao_inicial
        self.data_emissao_final = data_emissao_final
        self.inscricao_estadual_destinatario = inscricao_estadual_destinatario
        self.manifestacao_destinatario = manifestacao_destinatario
        self._post_init()
    
    def _post_init(self):
        enum_fields = {
            'situacao': RecebimentosFilterSituacao,
            'retorno': RecebimentosFilterRetorno,
            'tipo_nota': RecebimentosFilterTipoNota,
            'uf_emissao': RecebimentosFilterUfEmissao,
            'tipo': RecebimentosFilterTipo,
            'manifestacao_destinatario': RecebimentosFilterManifestacaoDestinatario
        }
        
        for field_name, enum_class in enum_fields.items():
            current_value = getattr(self, field_name)
            try:
                if not isinstance(current_value, enum_class):
                    setattr(self, field_name, enum_class(current_value))
            except ValueError as e:
                logger.info(f"Recebimentos Filter - Valor inválido para {field_name}: {current_value}. Usando valor padrão. Erro: {str(e)}")
                setattr(self, field_name, enum_class.ALL)
        
        
        if not self.data_entrada:
            self._post_init_data_entrada()

        if not self.data_saida:
            self._post_init_data_saida()

    def _post_init_data_entrada(self):
        current_datetime = datetime.now()
        aux_date = current_datetime - timedelta(days=1)
        yesterday_date_formated = aux_date.strftime("%d/%m/%Y")
        self.data_entrada = yesterday_date_formated
        logger.debug(f"Recebimentos Filtros - Data entrada vazia, mundando o valor para ontem: {yesterday_date_formated}")

    def _post_init_data_saida(self):
        current_datetime = datetime.now()
        current_date_formated = current_datetime.strftime("%d/%m/%Y")
        self.data_saida = current_date_formated
        logger.debug(f"Recebimentos Filtros - Data saida vazia, mundando o valor para hoje: {current_date_formated}")
    
        
    
    @staticmethod
    def get_params():
        if RecebimentosFilter.PARAMS_FILE.endswith(".toml"):
            return RecebimentosFilter._get_params_from_toml()
        else:
            raise NotImplementedError("Ainda não foi implementado para aceitar esse tipo de formato de arquivo para os paramêtros")
    
    @staticmethod
    def _get_params_from_toml():
        logger.info(f"Lendo paramêtros no arquivo {RecebimentosFilter.PARAMS_FILE}")
        try:
            with open(RecebimentosFilter.PARAMS_FILE, 'r') as f:
                return toml.load(f)
        except FileNotFoundError:
            logger.info(f"Arquivo não encontrado!")
        except toml.TomlDecodeError:
            logger.info(f"Erro na formatação do TOML!")

class RecebimentosPage:

    URL = str(os.getenv("URL_EDOCS")) + "/Nfe/NFeRecebimento.aspx"
    PAGE_NAME = "Nfe/Recebimentos"

    def __init__(self, driver: WebDriver, filter: Optional[RecebimentosFilter] = None):
        self.driver = driver
        self.filter = filter or RecebimentosFilter()
        self.filterMenu = False

    def navigate(self):
        self.driver.get(self.URL)
        logger.info(f"{self.PAGE_NAME} - Navegando para a pagina de Nfe/Recebimentos")
    
    def toggleFilterMenu(self):
        btn_filtrar = self.driver.find_element(By.ID, "btnFiltrarRecebimentosNfe")
        btn_filtrar.click()
        self.filterMenu = True
        logger.debug(f"{self.PAGE_NAME} - Toggle nos filtros de Nfe/Recebimentos, estado atual: {self.filterMenu}")
    
    def setSituacao(self) -> None:
        logger.debug(f"{self.PAGE_NAME} - Selecionando situação: {self.filter.situacao.value}")
        dropdown_situacao = self.driver.find_element(By.ID, "filtrofltRecebimento0")
        dropdown = Select(dropdown_situacao)
        match self.filter.situacao:
            case RecebimentosFilterSituacao.ALL:
                dropdown.select_by_index(0)
            case RecebimentosFilterSituacao.RECEBIDA_FORNECEDOR:
                dropdown.select_by_index(1)
            case RecebimentosFilterSituacao.AUTORIZO_USO:
                dropdown.select_by_index(2)
            case RecebimentosFilterSituacao.CRITICA_VALIDACAO:
                dropdown.select_by_index(3)
            case RecebimentosFilterSituacao.CANCELADA:
                dropdown.select_by_index(4)
            case RecebimentosFilterSituacao.DENEGADA:
                dropdown.select_by_index(5)
            case _:
                dropdown.select_by_index(0)
    
    def setNumero(self) -> None:
        try:
            if not self.filter.numero: return
            logger.debug(f"{self.PAGE_NAME} - Preenchendo numero: {self.filter.numero}")
            text_field_numero = self.wait_for_element(By.ID, "filtrofltRecebimento2")
            text_field_numero.clear()
            text_field_numero.send_keys(self.filter.numero)
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao preencher número: {str(e)}")
            raise

    def setRetorno(self) -> None:
        try:
            if not self.filter.retorno: return
            logger.debug(f"{self.PAGE_NAME} - Selecionando retorno: {self.filter.retorno.value}")
            dropdown_retorno = self.driver.find_element(By.ID, "filtrofltRecebimento4")
            dropdown = Select(dropdown_retorno)
            match self.filter.retorno:
                case RecebimentosFilterRetorno.ALL:
                    dropdown.select_by_index(0)
                case RecebimentosFilterRetorno.RETORNADO:
                    dropdown.select_by_index(1)
                case RecebimentosFilterRetorno.CONSULTA_PENDENTE:
                    dropdown.select_by_index(2)
                case RecebimentosFilterRetorno.NAO_RETORNADO:
                    dropdown.select_by_index(3)
                case RecebimentosFilterRetorno.DESATIVADO:
                    dropdown.select_by_index(4)
                case RecebimentosFilterRetorno.ERRO_RETORNO:
                    dropdown.select_by_index(5)
                case _:
                    dropdown.select_by_index(0)
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao preencher retorno: {str(e)}")
            raise

    def setDataEntrada(self) -> None:
        try:
            if not self.filter.data_entrada: return
            logger.debug(f"{self.PAGE_NAME} - Preenchendo data entrada: {self.filter.data_entrada}")

            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "filtrofltRecebimento6"))
            )
            element.click()
            element.send_keys(self.filter.data_entrada)
            element.send_keys(Keys.ENTER)
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao preencher data entrada: {str(e)}")
            raise


    def setDataSaida(self) -> None:
        try:
            if not self.filter.data_saida: return
            
            logger.debug(f"{self.PAGE_NAME} - Preenchendo data saida: {self.filter.data_saida}")
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "filtrofltRecebimento6_2"))
            )
            element.click()
            element.send_keys(self.filter.data_saida)
            element.send_keys(Keys.ENTER)
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao preencher data saída: {str(e)}")
            raise

    def setTipo(self) -> None:
        try:
            if not self.filter.tipo: return
            logger.debug(f"{self.PAGE_NAME} - Selecionando tipo: {self.filter.tipo.value}")
            dropdown_select = self.driver.find_element(By.ID, "filtrofltRecebimento7")
            dropdown = Select(dropdown_select)
            match self.filter.tipo:
                case RecebimentosFilterTipo.ALL:
                    dropdown.select_by_index(0)
                case RecebimentosFilterTipo.DESTINATARIO:
                    dropdown.select_by_index(1)
                case RecebimentosFilterTipo.TERCEIRO:
                    dropdown.select_by_index(2)
                case RecebimentosFilterTipo.TRANSPORTADOR:
                    dropdown.select_by_index(3)
                case _:
                    dropdown.select_by_index(0)
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao selectionar tipo: {str(e)}")
            raise

    def setTipoNota(self) -> None:
        try:
            if not self.filter.tipo_nota: return
            logger.debug(f"{self.PAGE_NAME} - Selecionando tipo nota: {self.filter.tipo_nota.value}")
            dropdown_tipo_nota = self.driver.find_element(By.ID, "filtrofltRecebimento4")
            dropdown = Select(dropdown_tipo_nota)
            match self.filter.retorno:
                case RecebimentosFilterTipoNota.ALL:
                    dropdown.select_by_index(0)
                case RecebimentosFilterTipoNota.ENTRADA:
                    dropdown.select_by_index(1)
                case RecebimentosFilterTipoNota.SAIDA:
                    dropdown.select_by_index(2)
                case _:
                    dropdown.select_by_index(0)
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao selectionar tipo nota: {str(e)}")
            raise


    def setCpnjCpfEmitente(self) -> None:
        try:
            if not self.filter.cnpj_cpf_emitente: return
            logger.debug(f"{self.PAGE_NAME} - Preenchendo Cnpj/Cpf Emitente: {self.filter.cnpj_cpf_emitente}")
            text_field = self.driver.find_element(By.ID, "filtrofltRecebimento10")
            text_field.click()
            text_field.send_keys(self.filter.cnpj_cpf_emitente)
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao preencher Cnpj/Cpf Emitente: {str(e)}")
            raise

    def setUfEmitente(self) -> None:
        try:
            if not self.filter.uf_emissao: return
            logger.debug(f"{self.PAGE_NAME} - Selecionando UF Emissão: {self.filter.uf_emissao.value}")
            dropdown_selection = self.driver.find_element(By.ID, "filtrofltRecebimento4")
            dropdown = Select(dropdown_selection)
            match self.filter.retorno:
                case RecebimentosFilterUfEmissao.ALL:
                    dropdown.select_by_index(0)
                case _:
                    dropdown.select_by_index(0)
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao selectionar UF Emitente: {str(e)}")
            raise


    def setNomeDestinatario(self) -> None:
        try:
            if not self.filter.nome_destinatario: return
            logger.debug(f"{self.PAGE_NAME} - Preenchendo Cnpj/Cpf Emitente: {self.filter.nome_destinatario}")
            text_field = self.driver.find_element(By.ID, "filtrofltRecebimento14")
            text_field.click()
            text_field.send_keys(self.filter.nome_destinatario)
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao preencher nome destinatário: {str(e)}")
            raise

    def saveAllXML(self) -> bool:
        """
        Salva os recebimentos em formato XML.
        
        Important:
            - Antes de salvar, é necessário focar em alguma linha da tabela
        """
        logger.info(f"{self.PAGE_NAME} - Salvando recebimentos em XML")
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "divXml"))
            )

            btn_save_all = element.find_element(By.TAG_NAME, "a")
            btn_save_all.click()

            btn_confirmation = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "btnXmlAgrupado"))
            )
            btn_confirmation.click()

            return True
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao salvar XML: {str(e)}")
            return False
    
    def applyFilters(self) -> bool:
        logger.info(f"{self.PAGE_NAME} - Aplicando filtros")
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "filtrofltRecebimentook"))
            )
            element.click()
            return False
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao aplicar filtros: {str(e)}")
            return False
    
    def tableFocus(self) -> bool:
        try:
            table = self.driver.find_element(By.ID, "gridNfe")

            first_row = WebDriverWait(table, 10).until(
                EC.element_to_be_clickable((By.TAG_NAME, "tr"))
            )
            first_row.click()
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ao tentar focar na tabela: {str(e)}")
            return False
    
    def hasReceipt(self) -> bool:
        try:
            table = self.driver.find_element(By.ID, "gridNfe")
            first_row = WebDriverWait(table, 10).until(
                EC.element_to_be_clickable((By.TAG_NAME, "tr"))
            )
            if first_row:
                return True
            return False
        except Exception as e:
            logger.error(f"{self.PAGE_NAME} - Falha ver se tem registro na tabela: {str(e)}")
            return False
    
    def handleXMLDownloadMessage(self) -> bool:
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "btnBarraMensagemSim"))
            )
            element.click()
        except Exception as e:
            ...