"""Janela principal da Calculadora de Link Budget GPON."""
import customtkinter as ctk
from src.views.painel_equipamentos import PainelEquipamentos
from src.views.painel_fibra import PainelFibra
from src.views.painel_componentes import PainelComponentes
from src.views.painel_seguranca import PainelSeguranca
from src.views.painel_resultado import PainelResultado


class TelaPrincipal(ctk.CTk):
    def __init__(self, presenter=None):
        super().__init__()
        self.title("Calculadora de Link Budget GPON")
        self.geometry("900x700")
        self.minsize(800, 600)
        self.presenter = presenter
        self._criar_layout()
        if presenter:
            self._conectar_presenter()

    def set_presenter(self, presenter):
        self.presenter = presenter
        self._conectar_presenter()

    def _conectar_presenter(self):
        self.btn_calcular.configure(command=self.presenter.on_calcular)
        self.btn_limpar.configure(command=self.presenter.on_limpar)
        self.btn_demo.configure(command=self.presenter.on_demonstracao)
        self.btn_exportar_txt.configure(command=self.presenter.on_exportar_txt)
        self.btn_exportar_pdf.configure(command=self.presenter.on_exportar_pdf)
        self.bind("<Return>", lambda e: self.presenter.on_calcular())
        self.bind("<Escape>", lambda e: self.presenter.on_limpar())

        self.painel_equip.classe_combo.configure(
            command=self.presenter.on_classe_selecionada)

        for child in self.painel_fibra.sentido_frame.winfo_children():
            if isinstance(child, ctk.CTkRadioButton):
                child.configure(command=lambda: self.presenter.on_sentido_alterado(
                    self.painel_fibra.sentido_var.get()))

        self._vincular_focusout()

    def _vincular_focusout(self):
        entries = [
            ("ptx", self.painel_equip.ptx_entry),
            ("s", self.painel_equip.s_entry),
            ("distancia", self.painel_fibra.distancia_entry),
            ("margem", self.painel_seguranca.margem_entry),
            ("conectores_qtd", self.painel_componentes.con_qtd_entry),
            ("perda_conector", self.painel_componentes.con_perda_entry),
            ("fusoes_qtd", self.painel_componentes.fus_qtd_entry),
            ("perda_fusao", self.painel_componentes.fus_perda_entry),
        ]
        for nome, entry in entries:
            entry.bind("<FocusOut>", lambda e, n=nome: self._validar_campo_ao_sair(n))

    def _validar_campo_ao_sair(self, nome: str):
        if not self.presenter:
            return
        try:
            campos_raw = self.presenter._coletar_campos()
            campos_sanitizados = self.presenter.controller._converter_campos(campos_raw)
            alertas = self.presenter.controller.validador.validar_campos(campos_sanitizados)
            alertas_campo = [a for a in alertas if a.campo == nome]
            self._destacar_campo(nome, alertas_campo)
        except Exception:
            pass  # Silenciosamente ignora erros de validacao inline

    def _destacar_campo(self, nome: str, alertas: list):
        entry_map = {
            "ptx": self.painel_equip.ptx_entry,
            "s": self.painel_equip.s_entry,
            "distancia": self.painel_fibra.distancia_entry,
            "margem": self.painel_seguranca.margem_entry,
            "conectores_qtd": self.painel_componentes.con_qtd_entry,
            "perda_conector": self.painel_componentes.con_perda_entry,
            "fusoes_qtd": self.painel_componentes.fus_qtd_entry,
            "perda_fusao": self.painel_componentes.fus_perda_entry,
        }
        entry = entry_map.get(nome)
        if not entry:
            return
        if any(a.nivel == "error" for a in alertas):
            entry.configure(border_color="red")
        elif any(a.nivel == "warning" for a in alertas):
            entry.configure(border_color="orange")
        else:
            entry.configure(border_color="gray")

    def _criar_layout(self):
        self.frame_esq = ctk.CTkScrollableFrame(self, width=420)
        self.frame_esq.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.painel_equip = PainelEquipamentos(self.frame_esq)
        self.painel_equip.pack(fill="x", padx=5, pady=5)

        self.painel_fibra = PainelFibra(self.frame_esq)
        self.painel_fibra.pack(fill="x", padx=5, pady=5)

        self.painel_componentes = PainelComponentes(self.frame_esq)
        self.painel_componentes.pack(fill="x", padx=5, pady=5)

        self.painel_seguranca = PainelSeguranca(self.frame_esq)
        self.painel_seguranca.pack(fill="x", padx=5, pady=5)

        self.frame_botoes = ctk.CTkFrame(self.frame_esq)
        self.frame_botoes.pack(fill="x", padx=5, pady=5)

        self.btn_limpar = ctk.CTkButton(self.frame_botoes, text="Limpar", fg_color="gray")
        self.btn_limpar.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_calcular = ctk.CTkButton(self.frame_botoes, text="Calcular")
        self.btn_calcular.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_demo = ctk.CTkButton(self.frame_botoes, text="Demonstracao", fg_color="green")
        self.btn_demo.pack(side="left", padx=5, expand=True, fill="x")

        # Export buttons
        self.frame_export = ctk.CTkFrame(self.frame_esq)
        self.frame_export.pack(fill="x", padx=5, pady=5)

        self.btn_exportar_txt = ctk.CTkButton(self.frame_export, text="Exportar TXT", fg_color="darkblue")
        self.btn_exportar_txt.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_exportar_pdf = ctk.CTkButton(self.frame_export, text="Exportar PDF", fg_color="darkblue")
        self.btn_exportar_pdf.pack(side="left", padx=5, expand=True, fill="x")

        self.painel_resultado = PainelResultado(self)
        self.painel_resultado.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    def _limpar(self):
        self.painel_equip.limpar()
        self.painel_fibra.limpar()
        self.painel_componentes.limpar()
        self.painel_seguranca.limpar()
        self.painel_resultado.limpar()

    def _demonstracao(self):
        self._limpar()
        self.painel_equip.classe_combo.set("C+")
        self.painel_equip.set_valor("ptx", "5.0")
        self.painel_equip.set_valor("s", "-30.0")
        self.painel_fibra.set_valor("distancia", "12.0")
        self.painel_fibra.set_valor("atenuacao_fibra", "0.25")
        self.painel_componentes.splitter1_combo.set("1:32")
        self.painel_componentes.con_qtd_entry.delete(0, "end")
        self.painel_componentes.con_qtd_entry.insert(0, "4")
        self.painel_componentes.con_perda_entry.delete(0, "end")
        self.painel_componentes.con_perda_entry.insert(0, "0.3")
        self.painel_componentes.fus_qtd_entry.delete(0, "end")
        self.painel_componentes.fus_qtd_entry.insert(0, "3")
        self.painel_componentes.fus_perda_entry.delete(0, "end")
        self.painel_componentes.fus_perda_entry.insert(0, "0.05")
        self.painel_seguranca.margem_entry.delete(0, "end")
        self.painel_seguranca.margem_entry.insert(0, "3.0")
