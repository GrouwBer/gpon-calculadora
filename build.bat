@echo off
REM Script de build para Windows - Calculadora GPON
echo Instalando PyInstaller...
pip install pyinstaller
echo Gerando executavel...
pyinstaller --onefile --windowed --name CalculadoraGPON ^
    --add-data "resources;resources" ^
    --collect-data customtkinter ^
    main.py
echo.
echo Executavel gerado: dist\CalculadoraGPON.exe
