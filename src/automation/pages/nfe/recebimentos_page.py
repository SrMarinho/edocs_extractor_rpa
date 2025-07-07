import os
from enum import Enum
import time
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.logger_instance import logger


class RecebimentosFilterSituacao(Enum):
    ALL = "Todos"
    RECEBIDA_FORNECEDOR = "Recebida Fornecedor"
    AUTORIZO_USO = "Autorizo Uso"
    CRITICA_VALIDACAO = "Critica Validacao"
    CANCELADA = "Cancelada"
    DENEGADA = "Denegada"

class RecebimentosFilterRetorno(Enum):
    ALL = "Todos"
    RETORNADO = "Retornado"
    CONSULTA_PENDENTE = "Consulta pendente"
    NAO_RETORNADO = "Não retornado"
    DESATIVADO = "Desativado"
    ERRO_RETORNO = "Erro Retorno"

class RecebimentosFilterTipoNota(Enum):
    ALL = "Todos"
    ENTRADA = "Entrada"
    SAIDA = "Saída"

class RecebimentosFilterUfEmissao(Enum):
    ALL = "Todas"
    PI = "Piauí"
    MA = "Maranhão"

class RecebimentosFilterTipo(Enum):
    ALL = "Todos"
    DESTINATARIO = "Destinatario"
    TERCEIRO = "Terceiro"
    TRANSPORTADOR = "Transportador"
    
class RecebimentosFilterManifestacaoDestinatario(Enum):
    ALL = "Todos"
    CIENCIA_OPERACAO = "Ciência da Operação"
    CONFIRMACAO_OPERACAO = "Confirmação da Operação"
    OPERACAO_NAO_REALIZADA = "Operação não Realizada"
    DESCONHECIMENTO_OPERACAO = "Desconhecimento da Operação"

class RecebimentosFilter:
    def __init__(
        self,
        situacao: RecebimentosFilterSituacao = RecebimentosFilterSituacao.ALL, 
        numero: str = "",
        retorno: RecebimentosFilterRetorno = RecebimentosFilterRetorno.ALL,
        data_entrada: str = "",
        data_saida: str = "",
        tipo_nota: RecebimentosFilterTipoNota = RecebimentosFilterTipoNota.ALL,
        cnpj_cpf_emitente: str = "",
        uf_emissao: RecebimentosFilterUfEmissao = RecebimentosFilterUfEmissao.ALL,
        nome_destinatario: str = "",
        serie: str = "",
        chave: str = "",
        total_inicial: str = "",
        total_final: str = "",
        tipo: RecebimentosFilterTipo = RecebimentosFilterTipo.ALL,
        nome_emitente: str = "",
        data_emissao_inicial: str = "",
        data_emissao_final: str = "",
        inscricao_estadual_destinatario: str = "",
        manifestacao_destinatario: RecebimentosFilterManifestacaoDestinatario = RecebimentosFilterManifestacaoDestinatario.ALL
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