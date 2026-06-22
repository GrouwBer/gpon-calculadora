"""Painel de splitters, conectores e fusoes."""
import customtkinter as ctk

class PainelComponentes(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._criar_widgets()

    def _criar_widgets(self):
        ctk.CTkLabel(self, text="Splitters, Conectores e Fusoes", font=("", 14, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0,5))

        ctk.CTkLabel(self, text="Splitter 1:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.splitter1_combo = ctk.CTkComboBox(self, values=["1:2", "1:4", "1:8", "1:16", "1:32", "1:64"], width=80)
        self.splitter1_combo.grid(row=1, column=1, sticky="w", padx=5)
        self.splitter1_combo.set("1:32")
        ctk.CTkLabel(self, text="Excesso (dB):").grid(row=1, column=2, sticky="w", padx=5)
        self.splitter1_exc_entry = ctk.CTkEntry(self, width=60)
        self.splitter1_exc_entry.grid(row=1, column=3, sticky="w", padx=5)
        self.splitter1_exc_entry.insert(0, "2.5")

        self.splitter2_check = ctk.CTkCheckBox(self, text="Splitter 2", command=self._toggle_splitter2)
        self.splitter2_check.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        self.splitter2_combo = ctk.CTkComboBox(self, values=["1:2", "1:4", "1:8", "1:16", "1:32", "1:64"], width=80, state="disabled")
        self.splitter2_combo.grid(row=2, column=1, sticky="w", padx=5)
        self.splitter2_combo.set("1:16")
        ctk.CTkLabel(self, text="Excesso (dB):").grid(row=2, column=2, sticky="w", padx=5)
        self.splitter2_exc_entry = ctk.CTkEntry(self, width=60, state="disabled")
        self.splitter2_exc_entry.grid(row=2, column=3, sticky="w", padx=5)
        self.splitter2_exc_entry.insert(0, "1.5")

        ctk.CTkLabel(self, text="Conectores (qtd):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.con_qtd_entry = ctk.CTkEntry(self, width=60)
        self.con_qtd_entry.grid(row=3, column=1, sticky="w", padx=5)
        self.con_qtd_entry.insert(0, "4")
        ctk.CTkLabel(self, text="Perda/un (dB):").grid(row=3, column=2, sticky="w", padx=5)
        self.con_perda_entry = ctk.CTkEntry(self, width=60)
        self.con_perda_entry.grid(row=3, column=3, sticky="w", padx=5)
        self.con_perda_entry.insert(0, "0.3")

        ctk.CTkLabel(self, text="Fusoes (qtd):").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.fus_qtd_entry = ctk.CTkEntry(self, width=60)
        self.fus_qtd_entry.grid(row=4, column=1, sticky="w", padx=5)
        self.fus_qtd_entry.insert(0, "3")
        ctk.CTkLabel(self, text="Perda/un (dB):").grid(row=4, column=2, sticky="w", padx=5)
        self.fus_perda_entry = ctk.CTkEntry(self, width=60)
        self.fus_perda_entry.grid(row=4, column=3, sticky="w", padx=5)
        self.fus_perda_entry.insert(0, "0.05")

        self.grid_columnconfigure(3, weight=1)

    def _toggle_splitter2(self):
        state = "normal" if self.splitter2_check.get() else "disabled"
        self.splitter2_combo.configure(state=state)
        self.splitter2_exc_entry.configure(state=state)

    def get_valores(self) -> dict:
        return {
            "splitter_razao": self.splitter1_combo.get().split(":")[1],
            "splitter_excesso": self.splitter1_exc_entry.get(),
            "splitter2_razao": self.splitter2_combo.get().split(":")[1] if self.splitter2_check.get() else "",
            "splitter2_excesso": self.splitter2_exc_entry.get() if self.splitter2_check.get() else "",
            "conectores_qtd": self.con_qtd_entry.get(),
            "perda_conector": self.con_perda_entry.get(),
            "fusoes_qtd": self.fus_qtd_entry.get(),
            "perda_fusao": self.fus_perda_entry.get(),
        }

    def limpar(self):
        self.splitter1_combo.set("1:32")
        self.splitter1_exc_entry.delete(0, "end"); self.splitter1_exc_entry.insert(0, "2.5")
        self.splitter2_check.deselect(); self._toggle_splitter2()
        self.con_qtd_entry.delete(0, "end"); self.con_qtd_entry.insert(0, "4")
        self.con_perda_entry.delete(0, "end"); self.con_perda_entry.insert(0, "0.3")
        self.fus_qtd_entry.delete(0, "end"); self.fus_qtd_entry.insert(0, "3")
        self.fus_perda_entry.delete(0, "end"); self.fus_perda_entry.insert(0, "0.05")
