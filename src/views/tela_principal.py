"""Janela principal da Calculadora de Link Budget GPON."""
import customtkinter as ctk
from src.views.painel_equipamentos import PainelEquipamentos
from src.views.painel_fibra import PainelFibra
from src.views.painel_componentes import PainelComponentes
from src.views.painel_seguranca import PainelSeguranca
from src.views.painel_resultado import PainelResultado

class TelaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Link Budget GPON")
        self.geometry("900x700")
        self.minsize(800, 600)
        self._criar_layout()

    def _criar_layout(self):
        # Frame esquerdo (parametros)
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

        # Botoes
        self.frame_botoes = ctk.CTkFrame(self.frame_esq)
        self.frame_botoes.pack(fill="x", padx=5, pady=5)

        self.btn_limpar = ctk.CTkButton(self.frame_botoes, text="Limpar", command=self._limpar, fg_color="gray")
        self.btn_limpar.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_calcular = ctk.CTkButton(self.frame_botoes, text="Calcular", command=self._calcular)
        self.btn_calcular.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_demo = ctk.CTkButton(self.frame_botoes, text="Demonstracao", command=self._demonstracao, fg_color="green")
        self.btn_demo.pack(side="left", padx=5, expand=True, fill="x")

        # Frame direito (resultado)
        self.painel_resultado = PainelResultado(self)
        self.painel_resultado.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Atalhos
        self.bind("<Return>", lambda e: self._calcular())
        self.bind("<Escape>", lambda e: self._limpar())

    # Placeholder methods (serao conectados ao Presenter na ISSUE-008)
    def _calcular(self):
        self.painel_resultado.text_area.configure(state="normal")
        self.painel_resultado.text_area.delete("1.0", "end")
        self.painel_resultado.text_area.insert("end", "Presenter nao conectado ainda (ISSUE-008).\n")
        self.painel_resultado.text_area.configure(state="disabled")

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
        self.painel_componentes.con_qtd_entry.delete(0, "end"); self.painel_componentes.con_qtd_entry.insert(0, "4")
        self.painel_componentes.con_perda_entry.delete(0, "end"); self.painel_componentes.con_perda_entry.insert(0, "0.3")
        self.painel_componentes.fus_qtd_entry.delete(0, "end"); self.painel_componentes.fus_qtd_entry.insert(0, "3")
        self.painel_componentes.fus_perda_entry.delete(0, "end"); self.painel_componentes.fus_perda_entry.insert(0, "0.05")
        self.painel_seguranca.margem_entry.delete(0, "end"); self.painel_seguranca.margem_entry.insert(0, "3.0")
