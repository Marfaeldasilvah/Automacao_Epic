@echo off
echo ===================================================
echo   Instalando dependencias do Garo RefreshShop...
echo ===================================================

:: 1. Criar o ambiente virtual se nao existir
if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
)

:: 2. Ativar o ambiente virtual e instalar as bibliotecas
echo Instalando bibliotecas do requirements.txt...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ===================================================
echo   Tudo pronto! Todas as dependencias foram instaladas.
echo ===================================================
pause