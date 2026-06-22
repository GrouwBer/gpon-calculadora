"""Testes para o Exportador."""
import os
import tempfile
import pytest
from src.controllers.exportador import Exportador


class TestExportador:
    def setup_method(self):
        self.exp = Exportador()
        self.resultado_teste = {
            "sucesso": True,
            "campo_calculado": "distancia",
            "valor_calculado": 12.0,
            "unidade": "km",
            "potencia_recebida": -18.85,
            "breakdown": {
                "fibra": {"valor": 3.0, "unidade": "dB", "percentual": 12.6},
                "splitters": {"valor": 16.5, "unidade": "dB", "percentual": 69.2},
                "conectores": {"valor": 1.2, "unidade": "dB", "percentual": 5.0},
                "fusoes": {"valor": 0.15, "unidade": "dB", "percentual": 0.6},
                "margem": {"valor": 3.0, "unidade": "dB", "percentual": 12.6},
                "atenuacao_total": {"valor": 23.85, "unidade": "dB", "percentual": 100.0},
            },
            "veredito": {
                "status": True,
                "viabilidade": "ENLACE VIAVEL",
                "folga": 8.15,
                "mensagem": "P_rec (-18.85 dBm) >= S (-30.0 dBm) + Margem (3.0 dB)",
            },
            "alertas": [],
        }

    def test_exportar_txt_cria_arquivo(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            self.exp.exportar_txt(self.resultado_teste, path)
            assert os.path.exists(path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "RELATORIO DE LINK BUDGET GPON" in content
            assert "ENLACE VIAVEL" in content
            assert "23.85" in content
        finally:
            os.unlink(path)

    def test_exportar_txt_contem_campo_calculado(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            self.exp.exportar_txt(self.resultado_teste, path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "distancia = 12.00 km" in content
        finally:
            os.unlink(path)

    def test_exportar_txt_contem_breakdown(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            self.exp.exportar_txt(self.resultado_teste, path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "Fibra" in content
            assert "Splitters" in content
        finally:
            os.unlink(path)

    def test_exportar_txt_contem_veredito(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            self.exp.exportar_txt(self.resultado_teste, path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "VIAVEL" in content
        finally:
            os.unlink(path)

    def test_exportar_txt_com_erro(self):
        resultado_erro = {"sucesso": False, "erro": "Teste de erro"}
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            self.exp.exportar_txt(resultado_erro, path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "ERRO" in content
            assert "Teste de erro" in content
        finally:
            os.unlink(path)

    def test_exportar_pdf_cria_arquivo(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            self.exp.exportar_pdf(self.resultado_teste, path)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)

    def test_exportar_txt_sem_calculo(self):
        """Exportador nao deve falhar se chamado sem resultado previo."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            self.exp.exportar_txt({"sucesso": False, "erro": "Nenhum calculo"}, path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "ERRO" in content
        finally:
            os.unlink(path)
