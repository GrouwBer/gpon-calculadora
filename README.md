# Calculadora de Link Budget GPON

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

Ferramenta desktop para **cálculo, validação e simulação** de orçamento de potência óptica em redes GPON, conforme normas **ITU-T G.984.x** e **G.652**.

## Funcionalidades

- **Cálculo automático**: identifica a variável faltante e resolve o link budget
- **Classes de potência**: B+, C+, C++ (ITU-T G.984.2) com preenchimento automático
- **Downstream/Upstream**: alterna entre 1490 nm e 1310 nm com coeficientes distintos
- **Splitters em cascata**: suporta até 2 estágios de splitter
- **Validação em tempo real**: alertas visuais (bordas coloridas) para valores fora dos limites
- **Breakdown detalhado**: discriminação de cada componente de perda com percentual
- **Veredito**: "ENLACE VIÁVEL" (verde) ou "ENLACE INVIÁVEL" (vermelho) com folga
- **Modo demonstração**: cenário típico pré-preenchido para exploração
- **Exportação**: resultados em TXT e PDF

## Arquitetura

O projeto segue o padrão **MVP (Model-View-Presenter)**:

```
src/
  models/         # Domínio puro (sem referência a UI)
    constantes.py   # Tabelas ITU-T (classes, atenuação, limites)
    equipamento.py  # Equipamento OLT/ONU
    fibra.py        # Fibra óptica G.652.D
    splitter.py     # Splitter PLC
    link_budget.py  # Cálculo de propagação
    solver.py       # Resolução da variável faltante
    validador.py    # Validação contra limites
    alerta.py       # Objeto Alerta
    exceptions.py   # Exceções personalizadas
  controllers/   # Orquestração
    calculator_controller.py  # Sanitização + delegação
    calculator_presenter.py   # Ligação View ↔ Controller
    exportador.py             # Exportação TXT/PDF
  views/         # Interface gráfica (CustomTkinter)
    tela_principal.py         # Janela principal
    painel_*.py               # Painéis de parâmetros e resultado
```

## Pré-requisitos

- Python 3.10 ou superior
- Pip (gerenciador de pacotes)

## Instalação (modo desenvolvedor)

```bash
git clone https://github.com/GrouwBer/gpon-calculadora.git
cd gpon-calculadora

# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução

```bash
python main.py
```

## Testes

```bash
pytest tests/ --cov=src/models --cov-report=term
```

## Empacotamento (executável standalone)

### Windows
```bash
build.bat
```
Gera `dist/CalculadoraGPON.exe`.

### Linux/macOS
```bash
./build.sh
```
Gera `dist/CalculadoraGPON`.

## Guia rápido

1. **Preencha os parâmetros** do enlace (equipamentos, fibra, splitters, conectores)
2. **Deixe 1 campo em branco** — será automaticamente calculado
3. **Clique "Calcular"** e veja o breakdown, veredito e folga

## Referências

- ITU-T G.984.1 — GPON General characteristics
- ITU-T G.984.2 — GPON PMD layer specification (classes B+, C+, C++)
- ITU-T G.652 — Single-mode optical fibre characteristics
- ITU-T G.657 — Bending-loss insensitive single-mode optical fibre

## Licença

MIT License — veja o arquivo [LICENSE](LICENSE).

---

*Projeto interdisciplinar — IFSULDEMINAS Campus Poços de Caldas*
*Disciplinas: Propagação de Ondas Eletromagnéticas + Engenharia de Software*
