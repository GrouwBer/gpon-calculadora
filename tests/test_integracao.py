"""Testes de integracao completos — cenarios do PRD §14.4."""
import pytest
from src.controllers.calculator_controller import CalculatorController


class TestIntegracao:
    def setup_method(self):
        self.ctrl = CalculatorController()

    def _build_campos(self, overrides: dict) -> dict:
        campos = {
            "ptx": "5.0", "s": "-30.0", "distancia": "10.0",
            "atenuacao_fibra": "0.25", "splitter_razao": "32",
            "splitter_excesso": "2.5", "conectores_qtd": "4",
            "perda_conector": "0.3", "fusoes_qtd": "3",
            "perda_fusao": "0.05", "margem": "3.0",
        }
        campos.update(overrides)
        return campos

    def test_cenario_urbano_tipico(self):
        """PRD §14.4.1: 5km, 1:32, classe B+ -> viavel."""
        campos = self._build_campos({
            "ptx": "1.5", "s": "-27.0", "distancia": "5.0",
            "classe": "B+",
        })
        r = self.ctrl.calcular(campos, sentido="downstream", classe="B+")
        assert r["sucesso"]
        assert r["veredito"]["status"] is True

    def test_cenario_limite(self):
        """PRD §14.4.2: 20km, 1:64, classe C+ -> viavel (proximo do limite)."""
        campos = self._build_campos({
            "ptx": "5.0", "s": "-30.0", "distancia": "20.0",
            "splitter_razao": "64", "splitter_excesso": "3.0",
            "conectores_qtd": "2", "fusoes_qtd": "2",
            "classe": "C+",
        })
        r = self.ctrl.calcular(campos, sentido="downstream", classe="C+")
        assert r["sucesso"]
        folga = r["veredito"]["folga"]
        assert folga <= 3.0  # Proximo do limite

    def test_cenario_inviavel(self):
        """PRD §14.4.3: 40km, 1:64, classe B+ -> inviavel."""
        campos = self._build_campos({
            "ptx": "1.5", "s": "-27.0", "distancia": "40.0",
            "splitter_razao": "64", "splitter_excesso": "3.0",
            "conectores_qtd": "6",
            "classe": "B+",
        })
        r = self.ctrl.calcular(campos, sentido="downstream", classe="B+")
        assert r["sucesso"]
        assert r["veredito"]["status"] is False

    def test_cenario_distancia_maxima(self):
        """PRD §14.4.4: Calcular distancia maxima."""
        campos = self._build_campos({
            "ptx": "5.0", "s": "-30.0", "distancia": "",
            "splitter_razao": "16", "splitter_excesso": "1.5",
        })
        r = self.ctrl.calcular(campos, sentido="downstream")
        assert r["sucesso"]
        assert r["campo_calculado"] == "distancia"
        assert r["valor_calculado"] > 0
