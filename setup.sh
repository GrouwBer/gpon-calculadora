#!/usr/bin/env bash
# Script de setup para Linux/macOS - Calculadora GPON
set -e
echo "Criando ambiente virtual..."
python3 -m venv .venv
echo "Ativando ambiente virtual..."
source .venv/bin/activate
echo "Instalando dependencias..."
pip install -r requirements.txt
echo ""
echo "Setup concluido! Para executar:"
echo "  source .venv/bin/activate"
echo "  python main.py"
