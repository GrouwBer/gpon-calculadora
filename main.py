#!/usr/bin/env python3
"""Calculadora de Link Budget GPON.

Ponto de entrada da aplicacao desktop para calculo, validacao e simulacao
de orcamento de potencia optica em redes GPON (ITU-T G.984.x).
"""

import sys
import customtkinter as ctk


def main() -> None:
    """Inicializa e executa a interface grafica da calculadora."""
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    # Importacao tardia para evitar loops de importacao
    from src.views.tela_principal import TelaPrincipal

    app = TelaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()
