@echo off
REM Script de setup para Windows - Calculadora GPON
echo Criando ambiente virtual...
python -m venv .venv
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat
echo Instalando dependencias...
pip install -r requirements.txt
echo.
echo Setup concluido! Para executar:
echo   .venv\Scripts\activate.bat
echo   python main.py
