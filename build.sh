#!/usr/bin/env bash
# Script de build para Linux/macOS - Calculadora GPON
set -e
echo "Instalando PyInstaller..."
pip install pyinstaller
echo "Gerando executavel..."
pyinstaller --onefile --windowed --name CalculadoraGPON \
    --add-data "resources:resources" \
    --collect-data customtkinter \
    main.py
echo ""
echo "Executavel gerado: dist/CalculadoraGPON"
