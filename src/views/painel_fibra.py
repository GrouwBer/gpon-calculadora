"""Painel de fibra optica."""
import customtkinter as ctk

class PainelFibra(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._criar_widgets()

    def _criar_widgets(self):
        ctk.CTkLabel(self, text="Fibra Otica", font=("", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,5))
        self.sentido_var = ctk.StringVar(value="downstream")
        self.sentido_frame = ctk.CTkFrame(self)
        self.sentido_frame.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        ctk.CTkRadioButton(self.sentido_frame, text="Downstream (1490 nm)", variable=self.sentido_var, value="downstream").pack(side="left", padx=2)
        ctk.CTkRadioButton(self.sentido_frame, text="Upstream (1310 nm)", variable=self.sentido_var, value="upstream").pack(side="left", padx=2)

        ctk.CTkLabel(self, text="Distancia (km):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.distancia_entry = ctk.CTkEntry(self, width=100)
        self.distancia_entry.grid(row=2, column=1, sticky="w", padx=5)

        ctk.CTkLabel(self, text="Atenuacao (dB/km):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.atenuacao_entry = ctk.CTkEntry(self, width=100)
        self.atenuacao_entry.grid(row=3, column=1, sticky="w", padx=5)

        self.grid_columnconfigure(1, weight=1)

    def get_valores(self) -> dict:
        return {"distancia": self.distancia_entry.get(), "atenuacao_fibra": self.atenuacao_entry.get(), "sentido": self.sentido_var.get()}

    def set_valor(self, campo: str, valor: str):
        if campo == "distancia":
            self.distancia_entry.delete(0, "end")
            self.distancia_entry.insert(0, valor)
        elif campo == "atenuacao_fibra" or campo == "atenuacao":
            self.atenuacao_entry.delete(0, "end")
            self.atenuacao_entry.insert(0, valor)
        elif campo == "sentido":
            self.sentido_var.set(valor)

    def limpar(self):
        self.distancia_entry.delete(0, "end")
        self.atenuacao_entry.delete(0, "end")
        self.sentido_var.set("downstream")
