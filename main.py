#!/usr/bin/env python3
"""Calculadora de Link Budget GPON."""
import customtkinter as ctk

def main() -> None:
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    from src.views.tela_principal import TelaPrincipal
    from src.controllers.calculator_presenter import CalculatorPresenter

    app = TelaPrincipal()
    presenter = CalculatorPresenter(view=app)
    app.set_presenter(presenter)
    app.mainloop()

if __name__ == "__main__":
    main()
