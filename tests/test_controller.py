"""Testes para o CalculatorController."""

import pytest
from src.controllers.calculator_controller import CalculatorController


class TestCalculatorController:
    def setup_method(self):
        self.ctrl = CalculatorController()

    def test_sanitizar_numero(self):
        assert self.ctrl.sanitizar("5.0") == 5.0

    def test_sanitizar_virgula(self):
        assert self.ctrl.sanitizar("5,5") == 5.5

    def test_sanitizar_vazio(self):
        assert self.ctrl.sanitizar("") is None

    def test_sanitizar_espacos(self):
        assert self.ctrl.sanitizar("  10  ") == 10.0

    def test_sanitizar_texto_lanca_erro(self):
        with pytest.raises(ValueError, match="invalido"):
            self.ctrl.sanitizar("abc")

    def test_calcular_distancia_completo(self):
        campos = {
            "ptx": "5.0",
            "s": "-30.0",
            "distancia": "",
            "atenuacao_fibra": "0.25",
            "splitter_razao": "32",
            "splitter_excesso": "2.5",
            "conectores_qtd": "4",
            "perda_conector": "0.3",
            "fusoes_qtd": "3",
            "perda_fusao": "0.05",
            "margem": "3.0",
        }
        resultado = self.ctrl.calcular(campos, sentido="downstream", classe="C+")
        assert resultado["sucesso"] is True
        assert resultado["campo_calculado"] == "distancia"
        assert resultado["valor_calculado"] > 0
        assert "breakdown" in resultado
        assert "veredito" in resultado

    def test_calcular_todos_preenchidos(self):
        campos = {
            "ptx": "5.0",
            "s": "-30.0",
            "distancia": "10.0",
            "atenuacao_fibra": "0.25",
            "splitter_razao": "32",
            "splitter_excesso": "2.5",
            "conectores_qtd": "4",
            "perda_conector": "0.3",
            "fusoes_qtd": "3",
            "perda_fusao": "0.05",
            "margem": "3.0",
        }
        resultado = self.ctrl.calcular(campos, sentido="downstream")
        assert resultado["sucesso"] is True
        assert resultado["campo_calculado"] is None  # nenhum campo calculado

    def test_erro_texto_nao_numerico(self):
        campos = {
            "ptx": "abc",
            "s": "-30.0",
            "distancia": "10.0",
            "margem": "3.0",
        }
        resultado = self.ctrl.calcular(campos)
        assert resultado["sucesso"] is False
        assert "invalido" in resultado["erro"]

    def test_erro_mais_de_um_campo_vazio(self):
        campos = {
            "ptx": "",
            "s": "",
            "distancia": "10.0",
            "margem": "3.0",
        }
        resultado = self.ctrl.calcular(campos)
        assert resultado["sucesso"] is False

    def test_breakdown_contem_componentes(self):
        campos = {
            "ptx": "5.0",
            "s": "-30.0",
            "distancia": "10.0",
            "atenuacao_fibra": "0.25",
            "splitter_razao": "32",
            "splitter_excesso": "2.5",
            "conectores_qtd": "4",
            "perda_conector": "0.3",
            "fusoes_qtd": "3",
            "perda_fusao": "0.05",
            "margem": "3.0",
        }
        resultado = self.ctrl.calcular(campos)
        bd = resultado["breakdown"]
        assert "fibra" in bd
        assert "splitters" in bd
        assert "conectores" in bd
        assert "atenuacao_total" in bd

    def test_alertas_incluidos(self):
        campos = {
            "ptx": "12.0",
            "s": "-30.0",
            "distancia": "10.0",
            "margem": "3.0",
        }
        resultado = self.ctrl.calcular(campos)
        assert "alertas" in resultado
        assert len(resultado["alertas"]) > 0
