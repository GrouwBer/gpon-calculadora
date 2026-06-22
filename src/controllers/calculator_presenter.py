"""Presenter que liga a View ao Controller."""
from typing import Optional
from src.controllers.calculator_controller import CalculatorController
from src.views.tela_principal import TelaPrincipal

class CalculatorPresenter:
    def __init__(self, view: TelaPrincipal, controller: Optional[CalculatorController] = None):
        self.view = view
        self.controller = controller or CalculatorController()

    def on_calcular(self) -> None:
        campos = self._coletar_campos()
        sentido = self.view.painel_fibra.sentido_var.get()
        classe = self.view.painel_equip.classe_var.get()
        if classe == "Personalizado":
            classe = None

        resultado = self.controller.calcular(campos, sentido=sentido, classe=classe)
        self.view.painel_resultado.exibir_resultado(resultado)

    def on_limpar(self) -> None:
        self.view._limpar()

    def on_demonstracao(self) -> None:
        self.view._demonstracao()

    def _coletar_campos(self) -> dict:
        campos = {}
        campos.update(self.view.painel_equip.get_valores())
        campos.update(self.view.painel_fibra.get_valores())
        campos.update(self.view.painel_componentes.get_valores())
        campos.update(self.view.painel_seguranca.get_valores())
        if "sentido" in campos:
            del campos["sentido"]
        return campos
