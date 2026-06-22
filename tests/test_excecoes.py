"""Testes de tratamento de excecoes e robustez."""
import pytest
from src.models.exceptions import (
    DadosInsuficientesError,
    NenhumaIncognitaError,
    ValorFisicamenteImpossivelError,
)
from src.controllers.calculator_controller import CalculatorController


class TestExcecoes:
    def test_dados_insuficientes_error_mensagem(self):
        err = DadosInsuficientesError(["distancia", "margem"])
        assert "2" in str(err)
        assert "distancia" in str(err)

    def test_nenhuma_incognita_error_mensagem(self):
        err = NenhumaIncognitaError()
        assert "preenchidos" in str(err)

    def test_valor_impossivel_error_mensagem(self):
        err = ValorFisicamenteImpossivelError(
            "distancia", -5.0, "> 0 km")
        assert "distancia" in str(err)
        assert "-5.0" in str(err)

    def test_controller_nao_crasha_texto_aleatorio(self):
        ctrl = CalculatorController()
        campos = {
            "ptx": "!@#$%", "s": "-30.0", "distancia": "10.0",
            "margem": "3.0",
        }
        r = ctrl.calcular(campos)
        assert "sucesso" in r  # Deve retornar dict, nao exception

    def test_controller_nao_crasha_caracteres_especiais(self):
        ctrl = CalculatorController()
        campos = {
            "ptx": "5.0", "s": "-30.0", "distancia": "10.0\n\'\"",
            "margem": "3.0",
        }
        r = ctrl.calcular(campos)
        assert "sucesso" in r

    def test_mensagem_erro_indica_campo(self):
        ctrl = CalculatorController()
        campos = {
            "ptx": "abc123", "s": "-30.0", "distancia": "10.0",
            "margem": "3.0",
        }
        r = ctrl.calcular(campos)
        assert r["sucesso"] is False
        assert "ptx" in r["erro"] or "abc" in r["erro"]
