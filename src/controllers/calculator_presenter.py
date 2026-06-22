"""Presenter que liga a View ao Controller."""
import os
from tkinter import filedialog, messagebox
from typing import Optional
from src.controllers.calculator_controller import CalculatorController
from src.controllers.exportador import Exportador
from src.views.tela_principal import TelaPrincipal
from src.models.equipamento import Equipamento
from src.models.constantes import FIBER_ATTENUATION


class CalculatorPresenter:
    def __init__(self, view: TelaPrincipal,
                 controller: Optional[CalculatorController] = None):
        self.view = view
        self.controller = controller or CalculatorController()
        self.exportador = Exportador()
        self.ultimo_resultado: Optional[dict] = None

    def on_calcular(self) -> None:
        campos = self._coletar_campos()
        sentido = self.view.painel_fibra.sentido_var.get()
        classe = self.view.painel_equip.classe_var.get()
        if classe == "Personalizado":
            classe = None
        resultado = self.controller.calcular(campos, sentido=sentido, classe=classe)
        self.ultimo_resultado = resultado
        self.view.painel_resultado.exibir_resultado(resultado)

    def on_limpar(self) -> None:
        self.view._limpar()
        self.ultimo_resultado = None

    def on_demonstracao(self) -> None:
        self.view._demonstracao()
        self.ultimo_resultado = None

    def on_classe_selecionada(self, nome_classe: str) -> None:
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
        if sentido == "downstream":
            coef = FIBER_ATTENUATION[1490]
        else:
            coef = FIBER_ATTENUATION[1310]
        self.view.painel_fibra.set_valor("atenuacao_fibra", str(coef))
        classe = self.view.painel_equip.classe_var.get()
        if classe != "Personalizado":
            self.on_classe_selecionada(classe)

    def on_exportar_txt(self) -> None:
        if not self.ultimo_resultado:
            messagebox.showinfo("Exportar", "Execute um calculo antes de exportar.")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt")],
            title="Exportar como TXT",
        )
        if not filepath:
            return
        try:
            self.exportador.exportar_txt(self.ultimo_resultado, filepath)
            messagebox.showinfo("Exportar", f"Relatorio exportado com sucesso:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro", f"Nao foi possivel exportar:\n{e}")

    def on_exportar_pdf(self) -> None:
        if not self.ultimo_resultado:
            messagebox.showinfo("Exportar", "Execute um calculo antes de exportar.")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Exportar como PDF",
        )
        if not filepath:
            return
        try:
            self.exportador.exportar_pdf(self.ultimo_resultado, filepath)
            messagebox.showinfo("Exportar", f"Relatorio exportado com sucesso:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro", f"Nao foi possivel exportar:\n{e}")

    def _coletar_campos(self) -> dict:
        campos = {}
        campos.update(self.view.painel_equip.get_valores())
        campos.update(self.view.painel_fibra.get_valores())
        campos.update(self.view.painel_componentes.get_valores())
        campos.update(self.view.painel_seguranca.get_valores())
        if "sentido" in campos:
            del campos["sentido"]
        return campos
