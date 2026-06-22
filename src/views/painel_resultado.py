"""Painel de resultado do calculo."""
import customtkinter as ctk

class PainelResultado(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._criar_widgets()

    def _criar_widgets(self):
        ctk.CTkLabel(self, text="Resultado", font=("", 16, "bold")).pack(anchor="w", pady=(0,10))
        self.text_area = ctk.CTkTextbox(self, height=250, wrap="word")
        self.text_area.pack(fill="both", expand=True)
        self.text_area.insert("1.0", "Pressione 'Calcular' para obter o resultado.\n")
        self.text_area.configure(state="disabled")

    def exibir_resultado(self, resultado: dict):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", "end")

        if not resultado.get("sucesso", False):
            self.text_area.insert("end", f"ERRO: {resultado.get('erro', 'Erro desconhecido')}\n")
            self.text_area.configure(state="disabled")
            return

        mensagem = resultado.get("mensagem", "")
        if mensagem:
            self.text_area.insert("end", f"{mensagem}\n\n")

        cc = resultado.get("campo_calculado")
        vc = resultado.get("valor_calculado")
        uni = resultado.get("unidade", "")
        if cc and vc is not None:
            self.text_area.insert("end", f"Campo calculado: {cc} = {vc:.2f} {uni}\n\n")

        # Breakdown
        bd = resultado.get("breakdown", {})
        self.text_area.insert("end", "=== BREAKDOWN ===\n")
        for comp in ["fibra", "splitters", "conectores", "fusoes", "margem"]:
            if comp in bd:
                v = bd[comp]["valor"]
                pct = bd[comp]["percentual"]
                self.text_area.insert("end", f"  {comp.capitalize()}: {v:.2f} dB ({pct:.1f}%)\n")
        if "atenuacao_total" in bd:
            self.text_area.insert("end", f"  ---\n  ATENUACAO TOTAL: {bd['atenuacao_total']['valor']:.2f} dB\n\n")

        # Potencia recebida
        pr = resultado.get("potencia_recebida")
        if pr is not None:
            self.text_area.insert("end", f"Potencia recebida: {pr:.2f} dBm\n")

        # Veredito
        v = resultado.get("veredito", {})
        self.text_area.insert("end", f"\n=== VEREDITO ===\n")
        self.text_area.insert("end", f"{v.get('viabilidade', '')}\n")
        self.text_area.insert("end", f"{v.get('mensagem', '')}\n")
        if "folga" in v:
            folga = v["folga"]
            sinal = "+" if folga >= 0 else ""
            self.text_area.insert("end", f"Folga: {sinal}{folga:.2f} dB\n")

        # Alertas
        alertas = resultado.get("alertas", [])
        if alertas:
            self.text_area.insert("end", f"\n=== ALERTAS ({len(alertas)}) ===\n")
            for a in alertas:
                nivel = a.nivel if hasattr(a, 'nivel') else a.get('nivel', 'info')
                msg = a.mensagem if hasattr(a, 'mensagem') else a.get('mensagem', '')
                self.text_area.insert("end", f"  [{nivel.upper()}] {msg}\n")

        self.text_area.configure(state="disabled")

    def limpar(self):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", "Pressione 'Calcular' para obter o resultado.\n")
        self.text_area.configure(state="disabled")
