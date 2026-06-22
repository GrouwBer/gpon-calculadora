"""Painel de equipamentos (OLT/ONU) da interface."""

import customtkinter as ctk


class PainelEquipamentos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._criar_widgets()

    def _criar_widgets(self):
        ctk.CTkLabel(self, text="Equipamentos", font=("", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        self.classe_var = ctk.StringVar(value="Personalizado")
        ctk.CTkLabel(self, text="Classe de Potencia:").grid(row=1, column=0, sticky="w", padx=5)
        self.classe_combo = ctk.CTkComboBox(self, values=["Personalizado", "B+", "C+", "C++"], variable=self.classe_var, width=120)
        self.classe_combo.grid(row=1, column=1, sticky="w", padx=5)

        ctk.CTkLabel(self, text="Ptx (dBm):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.ptx_entry = ctk.CTkEntry(self, width=100)
        self.ptx_entry.grid(row=2, column=1, sticky="w", padx=5)

        ctk.CTkLabel(self, text="Sensibilidade (dBm):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.s_entry = ctk.CTkEntry(self, width=100)
        self.s_entry.grid(row=3, column=1, sticky="w", padx=5)

        self.grid_columnconfigure(1, weight=1)

    def get_valores(self) -> dict:
        return {"ptx": self.ptx_entry.get(), "s": self.s_entry.get(), "classe": self.classe_var.get()}

    def set_valor(self, campo: str, valor: str):
        if campo == "ptx":
            self.ptx_entry.delete(0, "end")
            self.ptx_entry.insert(0, valor)
        elif campo == "s":
            self.s_entry.delete(0, "end")
            self.s_entry.insert(0, valor)

    def limpar(self):
        self.ptx_entry.delete(0, "end")
        self.s_entry.delete(0, "end")
        self.classe_var.set("Personalizado")
