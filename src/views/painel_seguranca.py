"""Painel de margem de seguranca."""
import customtkinter as ctk

class PainelSeguranca(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Margem de Seguranca", font=("", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,5))
        ctk.CTkLabel(self, text="Margem (dB):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.margem_entry = ctk.CTkEntry(self, width=100)
        self.margem_entry.grid(row=1, column=1, sticky="w", padx=5)
        self.margem_entry.insert(0, "3.0")
        self.grid_columnconfigure(1, weight=1)

    def get_valores(self) -> dict:
        return {"margem": self.margem_entry.get()}

    def limpar(self):
        self.margem_entry.delete(0, "end"); self.margem_entry.insert(0, "3.0")
