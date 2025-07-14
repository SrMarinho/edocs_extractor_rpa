<#
.SYNOPSIS
    Configura um ambiente Python no Windows e executa um script.
.DESCRIPTION
    Este script verifica se o Python está instalado, instala se necessário,
    cria um ambiente virtual (opcional) e executa um script Python.
#>

# Função para verificar e instalar o Python
function Install-Python {
    Write-Host "Verificando a instalação do Python..." -ForegroundColor Cyan
    
    # Verifica se o Python está no PATH
    $pythonInstalled = $false
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -like "Python *") {
            Write-Host "Python já instalado: $pythonVersion" -ForegroundColor Green
            $pythonInstalled = $true
        }
    } catch {
        # Python não encontrado
    }

    if (-not $pythonInstalled) {
        Write-Host "Python não encontrado. Instalando..." -ForegroundColor Yellow
        
        # Baixar o instalador do Python
        $pythonUrl = "https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe"
        $installerPath = "$env:TEMP\python-installer.exe"
        
        Write-Host "Baixando instalador do Python..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
        
        # Instalar Python silenciosamente com PATH
        Write-Host "Instalando Python..." -ForegroundColor Cyan
        Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
        
        # Verificar instalação novamente
        try {
            $pythonVersion = python --version 2>&1
            if ($pythonVersion -like "Python *") {
                Write-Host "Python instalado com sucesso: $pythonVersion" -ForegroundColor Green
                
                # Atualizar pip após instalação
                Write-Host "Atualizando pip..." -ForegroundColor Cyan
                python -m pip install --upgrade pip
            } else {
                Write-Host "A instalação do Python pode ter falhado." -ForegroundColor Red
                exit 1
            }
        } catch {
            Write-Host "Falha ao verificar a instalação do Python." -ForegroundColor Red
            exit 1
        }
    }
}

# Função para configurar ambiente virtual (opcional)
function Setup-VirtualEnv {
    param (
        [string]$envName = "venv"
    )
    
    Write-Host "Configurando ambiente virtual Python..." -ForegroundColor Cyan
    
    # Verificar se o módulo venv está disponível
    try {
        python -m venv --help | Out-Null
    } catch {
        Write-Host "O módulo venv não está disponível. Instalando..." -ForegroundColor Yellow
        python -m pip install virtualenv
    }
    
    # Criar ambiente virtual
    if (-not (Test-Path $envName)) {
        python -m venv $envName
        Write-Host "Ambiente virtual criado em: $envName" -ForegroundColor Green
    } else {
        Write-Host "Ambiente virtual já existe em: $envName" -ForegroundColor Yellow
    }
    
    # Ativar ambiente virtual
    $activatePath = "$envName\Scripts\Activate.ps1"
    if (Test-Path $activatePath) {
        . $activatePath
        Write-Host "Ambiente virtual ativado." -ForegroundColor Green
    } else {
        Write-Host "Não foi possível ativar o ambiente virtual." -ForegroundColor Red
    }
}

# Função para instalar dependências
function Install-Dependencies {
    param (
        [string]$requirementsFile = "requirements.txt"
    )
    
    if (Test-Path $requirementsFile) {
        Write-Host "Instalando dependências do $requirementsFile..." -ForegroundColor Cyan
        pip install -r $requirementsFile
    } else {
        Write-Host "Arquivo $requirementsFile não encontrado. Pulando instalação de dependências." -ForegroundColor Yellow
    }
}

# Função principal
function Main {
    # 1. Verificar e instalar Python se necessário
    Install-Python
    
    # 2. Configurar ambiente virtual (opcional - descomente se quiser usar)
    # Setup-VirtualEnv -envName "venv"
    
    # 3. Instalar dependências (se houver requirements.txt)
    Install-Dependencies
    
    # 4. Executar o script Python
    $scriptPath = ".\meu_script.py"  # Altere para o caminho do seu script
    
    if (Test-Path $scriptPath) {
        Write-Host "Executando script Python: $scriptPath" -ForegroundColor Cyan
        python $scriptPath
    } else {
        Write-Host "Script Python não encontrado em: $scriptPath" -ForegroundColor Red
        Write-Host "Crie um arquivo 'meu_script.py' ou ajuste a variável `$scriptPath no código." -ForegroundColor Yellow
    }
}

# Executar função principal
Main