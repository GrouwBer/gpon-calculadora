"""Constantes e dados de referencia ITU-T para calculo de Link Budget GPON.

Fontes: ITU-T G.984.2, G.652, FS.com, APNIC, FOA
"""

from typing import Dict, Final

# ---------------------------------------------------------------------------
# Classes de potencia GPON (ITU-T G.984.2)
# ---------------------------------------------------------------------------
# Valores padrao (tipicos/minimos conservadores) para preenchimento automatico.
# Usados por Equipamento.from_classe().
GPON_CLASSES_DEFAULT: Final[Dict[str, Dict[str, float]]] = {
    "B+":  {"ptx_down": 1.5, "ptx_up": 0.5, "s_down": -27.0, "s_up": -28.0, "budget": 28.0},
    "C+":  {"ptx_down": 5.0, "ptx_up": 3.0, "s_down": -30.0, "s_up": -32.0, "budget": 32.0},
    "C++": {"ptx_down": 7.0, "ptx_up": 4.0, "s_down": -32.0, "s_up": -35.0, "budget": 35.0},
}

CLASSES_VALIDAS: Final[list[str]] = ["B+", "C+", "C++"]

# ---------------------------------------------------------------------------
# Atenuacao da fibra G.652.D por comprimento de onda (dB/km)
# ---------------------------------------------------------------------------
FIBER_ATTENUATION: Final[Dict[int, float]] = {
    1310: 0.35,  # Upstream (ONU -> OLT)
    1490: 0.25,  # Downstream (OLT -> ONU)
    1550: 0.20,  # RF Video (CATV) overlay
}

# ---------------------------------------------------------------------------
# Perdas por splitter (PLC) - valores conservadores (maximos)
# ---------------------------------------------------------------------------
SPLITTER_LOSS_TABLE: Final[Dict[int, Dict[str, float]]] = {
    2:  {"teorica": 3.01, "tipica_max": 3.8,  "excesso_tipico": 0.8},
    4:  {"teorica": 6.02, "tipica_max": 7.3,  "excesso_tipico": 1.3},
    8:  {"teorica": 9.03, "tipica_max": 10.7, "excesso_tipico": 1.7},
    16: {"teorica": 12.04, "tipica_max": 14.0, "excesso_tipico": 2.0},
    32: {"teorica": 15.05, "tipica_max": 17.5, "excesso_tipico": 2.5},
    64: {"teorica": 18.06, "tipica_max": 21.0, "excesso_tipico": 3.0},
}

SPLITTER_RATIOS_VALIDAS: Final[list[int]] = [2, 4, 8, 16, 32, 64]

# ---------------------------------------------------------------------------
# Perdas por conector e fusao (valores conservadores)
# ---------------------------------------------------------------------------
PERDA_CONECTOR_PADRAO: Final[float] = 0.3    # SC/APC tipico
PERDA_FUSAO_PADRAO: Final[float] = 0.05      # fusion splice tipico

# ---------------------------------------------------------------------------
# Margem de seguranca
# ---------------------------------------------------------------------------
MARGEM_PADRAO: Final[float] = 3.0

# ---------------------------------------------------------------------------
# Comprimentos de onda GPON
# ---------------------------------------------------------------------------
COMPRIMENTOS_ONDA: Final[Dict[str, int]] = {
    "downstream": 1490,
    "upstream": 1310,
}

# ---------------------------------------------------------------------------
# Limites de validacao ITU-T
# ---------------------------------------------------------------------------
GPON_LIMITS: Final[Dict[str, tuple[float, float, str]]] = {
    "ptx_down": (1.0, 9.0, "dBm"),
    "ptx_up": (0.0, 7.0, "dBm"),
    "s_down": (-32.0, -27.0, "dBm"),
    "s_up": (-35.0, -28.0, "dBm"),
    "distancia": (0.1, 60.0, "km"),
    "atenuacao_fibra": (0.15, 0.50, "dB/km"),
    "conectores_qtd": (0, 10, "un"),
    "perda_conector": (0.1, 1.0, "dB"),
    "fusoes_qtd": (0, 20, "un"),
    "perda_fusao": (0.01, 0.30, "dB"),
    "margem": (0.0, 6.0, "dB"),
}
