"""Presenter que liga a View ao Controller."""
from typing import Optional
from src.controllers.calculator_controller import CalculatorController
from src.views.tela_principal import TelaPrincipal
from src.models.equipamento import Equipamento
from src.models.constantes import FIBER_ATTENUATION


class CalculatorPresenter:
    def __init__(self, view: TelaPrincipal,
                 controller: Optional[CalculatorController] = None):
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

    def on_classe_selecionada(self, nome_classe: str) -> None:
        """Preenche Ptx e S quando uma classe e selecionada."""
        if nome_classe == "Personalizado":
            return
        eq = Equipamento.from_classe(nome_classe)
        sentido = self.view.painel_fibra.sentido_var.get()
        if sentido == "downstream":
            self.view.painel_equip.set_valor("ptx", str(eq.ptx_down))
            self.view.painel_equip.set_valor("s", str(eq.s_down))
        else:
            self.view.painel_equip.set_valor("ptx", str(eq.ptx_up))
            self.view.painel_equip.set_valor("s", str(eq.s_up))

    def on_sentido_alterado(self, sentido: str) -> None:
        """Atualiza atenuacao e valores Ptx/S quando o sentido muda."""
        if sentido == "downstream":
            coef = FIBER_ATTENUATION[1490]
        else:
            coef = FIBER_ATTENUATION[1310]
        self.view.painel_fibra.set_valor("atenuacao_fibra", str(coef))
        # Atualizar Ptx/S se uma classe estiver selecionada
        classe = self.view.painel_equip.classe_var.get()
        if classe != "Personalizado":
            self.on_classe_selecionada(classe)

    def _coletar_campos(self) -> dict:
        campos = {}
        campos.update(self.view.painel_equip.get_valores())
        campos.update(self.view.painel_fibra.get_valores())
        campos.update(self.view.painel_componentes.get_valores())
        campos.update(self.view.painel_seguranca.get_valores())
        if "sentido" in campos:
            del campos["sentido"]
        return campos
