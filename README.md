# Edocs Extractor RPA

Este é um projeto de automação (RPA - Robotic Process Automation) que extrai arquivos XML do sistema E-Docs. O robô faz login no sistema, navega até a área de recebimentos, aplica filtros e faz o download dos arquivos XML necessários.

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

1. Python 3.12 ou superior
2. Microsoft Edge (navegador)
3. Microsoft Edge WebDriver (driver do navegador)
4. Git (para clonar o repositório)

## 🚀 Instalação

### 1. Clone o repositório

```powershell
git clone https://github.com/SrMarinho/edocs_extractor_rpa
cd edocs_extractor_rpa
```

### 2. Crie um ambiente virtual Python

```powershell
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
.\venv\Scripts\activate
```

### 3. Instale as dependências

```powershell
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Crie um arquivo .env

Crie um arquivo chamado `.env` na raiz do projeto com as seguintes variáveis:

```env
# Credenciais do E-Docs
EDOCS_USERNAME=seu_usuario
EDOCS_PASSWORD=sua_senha

# Caminhos
EDGE_DRIVER_PATH=C:\caminho\para\msedgedriver.exe
DOWNLOAD_PATH=C:\caminho\para\pasta\de\downloads\zip
XML_FILE_FINAL_DESTINATION=C:\caminho\para\pasta\destino\xml
XML_COMPRESSED_FILES_DESTINATION=C:\caminho\para\pasta\arquivos\compactados

# Configurações do Logger
APP_NAME=XML_EXTRACTOR
LOG_LEVEL=INFO
LOG_DIR=logs
```

### 2. Crie as pastas necessárias

O projeto precisa das seguintes pastas:
- `files/temp` - para arquivos temporários
- `files/zip` - para arquivos ZIP baixados
- `files/xml` - para os arquivos XML extraídos
- `logs` - para os arquivos de log

Você pode criar todas as pastas com o seguinte comando:

```powershell
mkdir files\temp, files\zip, files\xml, logs
```

## 🎮 Como Executar

1. Certifique-se de que o ambiente virtual está ativado:
```powershell
.\venv\Scripts\activate
```

2. Execute o script principal:
```powershell
python main.py
```

## 📌 Observações Importantes

- O script utiliza o navegador Microsoft Edge. Certifique-se de que ele está instalado e atualizado.
- O Edge WebDriver deve ser compatível com a versão do seu navegador Edge.
- Mantenha suas credenciais seguras e nunca as compartilhe ou as envie para o controle de versão.
- O script criará screenshots em caso de erros críticos para ajudar na depuração.

## 📁 Estrutura do Projeto

```
edocs_extractor_rpa/
├── assets/
├── files/
│   ├── temp/
│   ├── zip/
│   └── xml/
├── src/
│   ├── automation/
│   │   ├── pages/
│   │   └── tasks/
│   ├── config/
│   ├── core/
│   └── utils/
├── .env
├── main.py
└── requirements.txt
```

## 🚨 Solução de Problemas

1. **Erro de WebDriver**: Verifique se o caminho do Edge WebDriver está correto no arquivo `.env`
2. **Erro de Login**: Confirme se as credenciais no arquivo `.env` estão corretas
3. **Erro de Permissão**: Verifique se você tem permissão para escrever nas pastas de destino
4. **Screenshots de Erro**: Em caso de erro crítico, procure por `erro_critico.png` na pasta do projeto

## 📫 Suporte

Em caso de dúvidas ou problemas, consulte os logs gerados na pasta `logs` ou abra uma issue no repositório.

---

## 🧪 Testes Automatizados

O projeto possui testes unitários, de integração e end-to-end localizados na pasta `tests/`.

### Instalação das dependências de teste

```powershell
pip install -r requirements-test.txt
```

### Executando os testes

```powershell
python -m pytest
```

Você pode rodar testes específicos usando as marcações:
- `unit`: Testes unitários
- `integration`: Testes de integração
- `e2e`: Testes end-to-end

Exemplo:
```powershell
pytest -m unit
```

## 🛠️ Scripts Utilitários

- `setup.ps1`: Automatiza a instalação do Python, criação do ambiente virtual e instalação das dependências.
- `run.ps1`: Ativa o ambiente virtual e executa o projeto.

## 📁 Drivers

Coloque o `msedgedriver.exe` na pasta `drivers/` e configure o caminho no arquivo `.env`:
```
EDGE_DRIVER_PATH=C:\caminho\para\drivers\msedgedriver.exe
```

## ⚙️ Filtros de Recebimentos

O arquivo `files/parametros/recebimentos_filters.toml` permite customizar filtros usados na extração de recebimentos. Edite conforme necessário para ajustar os critérios de busca no E-Docs.


