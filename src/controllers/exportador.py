"""Exportacao de resultados para TXT e PDF."""
import os
from datetime import datetime
from typing import Optional


class Exportador:
    def exportar_txt(self, resultado: dict, filepath: str) -> None:
        linhas = []
        linhas.append("=" * 60)
        linhas.append("RELATORIO DE LINK BUDGET GPON")
        linhas.append("=" * 60)
        linhas.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        linhas.append("")

        if not resultado.get("sucesso", False):
            linhas.append(f"ERRO: {resultado.get('erro', 'Erro desconhecido')}")
        else:
            cc = resultado.get("campo_calculado")
            vc = resultado.get("valor_calculado")
            uni = resultado.get("unidade", "")
            if cc and vc is not None:
                linhas.append(f"Campo calculado: {cc} = {vc:.2f} {uni}")
                linhas.append("")

            bd = resultado.get("breakdown", {})
            linhas.append("--- BREAKDOWN ---")
            for comp in ["fibra", "splitters", "conectores", "fusoes", "margem"]:
                if comp in bd:
                    v = bd[comp]["valor"]
                    pct = bd[comp]["percentual"]
                    linhas.append(f"  {comp.capitalize():12s}: {v:7.2f} dB ({pct:5.1f}%)")
            if "atenuacao_total" in bd:
                linhas.append(f"  {'---':12s}")
                linhas.append(f"  {'ATENUACAO TOTAL':12s}: {bd['atenuacao_total']['valor']:7.2f} dB")
            linhas.append("")

            pr = resultado.get("potencia_recebida")
            if pr is not None:
                linhas.append(f"Potencia recebida: {pr:.2f} dBm")
                linhas.append("")

            v = resultado.get("veredito", {})
            linhas.append("--- VEREDITO ---")
            linhas.append(f"{v.get('viabilidade', '')}")
            linhas.append(f"{v.get('mensagem', '')}")
            if "folga" in v:
                sinal = "+" if v["folga"] >= 0 else ""
                linhas.append(f"Folga: {sinal}{v['folga']:.2f} dB")

            alertas = resultado.get("alertas", [])
            if alertas:
                linhas.append("")
                linhas.append(f"--- ALERTAS ({len(alertas)}) ---")
                for a in alertas:
                    nivel = a.nivel if hasattr(a, 'nivel') else a.get('nivel', 'info')
                    msg = a.mensagem if hasattr(a, 'mensagem') else a.get('mensagem', '')
                    linhas.append(f"  [{nivel.upper()}] {msg}")

        linhas.append("")
        linhas.append("=" * 60)
        linhas.append("Fim do relatorio.")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas))

    def exportar_pdf(self, resultado: dict, filepath: str) -> None:
        try:
            from fpdf import FPDF
        except ImportError:
            pdf = SimplePDFFallback()
            pdf.exportar(resultado, filepath)
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Relatorio de Link Budget GPON", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        if not resultado.get("sucesso", False):
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, f"ERRO: {resultado.get('erro', '')}", new_x="LMARGIN", new_y="NEXT")
        else:
            cc = resultado.get("campo_calculado")
            vc = resultado.get("valor_calculado")
            uni = resultado.get("unidade", "")
            if cc and vc is not None:
                pdf.set_font("Helvetica", "", 11)
                pdf.cell(0, 7, f"Campo calculado: {cc} = {vc:.2f} {uni}", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(3)

            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "Breakdown:", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            bd = resultado.get("breakdown", {})
            for comp in ["fibra", "splitters", "conectores", "fusoes", "margem"]:
                if comp in bd:
                    v = bd[comp]["valor"]
                    pct = bd[comp]["percentual"]
                    pdf.cell(0, 6, f"  {comp.capitalize()}: {v:.2f} dB ({pct:.1f}%)", new_x="LMARGIN", new_y="NEXT")
            if "atenuacao_total" in bd:
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 6, f"  ATENUACAO TOTAL: {bd['atenuacao_total']['valor']:.2f} dB", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

            pr = resultado.get("potencia_recebida")
            if pr is not None:
                pdf.set_font("Helvetica", "", 10)
                pdf.cell(0, 6, f"Potencia recebida: {pr:.2f} dBm", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(3)

            v = resultado.get("veredito", {})
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, v.get("viabilidade", ""), new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, v.get("mensagem", ""), new_x="LMARGIN", new_y="NEXT")
            if "folga" in v:
                sinal = "+" if v["folga"] >= 0 else ""
                pdf.cell(0, 6, f"Folga: {sinal}{v['folga']:.2f} dB", new_x="LMARGIN", new_y="NEXT")

            alertas = resultado.get("alertas", [])
            if alertas:
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 6, f"Alertas ({len(alertas)}):", new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", "", 9)
                for a in alertas:
                    nivel = a.nivel if hasattr(a, 'nivel') else a.get('nivel', 'info')
                    msg = a.mensagem if hasattr(a, 'mensagem') else a.get('mensagem', '')
                    pdf.cell(0, 5, f"  [{nivel.upper()}] {msg}", new_x="LMARGIN", new_y="NEXT")

        pdf.output(filepath)


class SimplePDFFallback:
    """Fallback simples quando fpdf2 nao esta disponivel."""
    def exportar(self, resultado: dict, filepath: str) -> None:
        txt_path = filepath.replace(".pdf", ".txt")
        Exportador().exportar_txt(resultado, txt_path)
        with open(txt_path, "r", encoding="utf-8") as f:
            conteudo = f.read()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("PDF export not available. Install fpdf2.\n\n")
            f.write(conteudo)
