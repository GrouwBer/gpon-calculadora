"""Testes para o solver de variavel faltante."""

import pytest
from src.models.solver import resolver, _arredondar_splitter
from src.models.exceptions import DadosInsuficientesError, NenhumaIncognitaError


class TestSolver:
    def test_resolver_distancia(self):
        """Resolver distancia quando e o unico campo vazio."""
        campos = {
            "ptx": 5.0,
            "s": -30.0,
            "distancia": None,
            "atenuacao_fibra": 0.25,
            "splitter_razao": 32,
            "splitter_excesso": 2.5,
            "conectores_qtd": 4,
            "perda_conector": 0.3,
            "fusoes_qtd": 3,
            "perda_fusao": 0.05,
            "margem": 3.0,
        }
        resultado = resolver(campos, sentido="downstream")
        assert resultado["campo_calculado"] == "distancia"
        assert resultado["valor_calculado"] > 0

    def test_resolver_potencia_tx(self):
        campos = {
            "ptx": None,
            "s": -30.0,
            "distancia": 10.0,
            "atenuacao_fibra": 0.25,
            "splitter_razao": 32,
            "splitter_excesso": 2.5,
            "conectores_qtd": 4,
            "perda_conector": 0.3,
            "fusoes_qtd": 3,
            "perda_fusao": 0.05,
            "margem": 3.0,
        }
        resultado = resolver(campos, sentido="downstream")
        assert resultado["campo_calculado"] == "ptx"
        assert resultado["valor_calculado"] is not None

    def test_resolver_sensibilidade(self):
        campos = {
            "ptx": 5.0,
            "s": None,
            "distancia": 10.0,
            "atenuacao_fibra": 0.25,
            "splitter_razao": 32,
            "splitter_excesso": 2.5,
            "conectores_qtd": 4,
            "perda_conector": 0.3,
            "fusoes_qtd": 3,
            "perda_fusao": 0.05,
            "margem": 3.0,
        }
        resultado = resolver(campos, sentido="downstream")
        assert resultado["campo_calculado"] == "s"
        assert resultado["valor_calculado"] is not None

    def test_resolver_margem(self):
        campos = {
            "ptx": 5.0,
            "s": -30.0,
            "distancia": 10.0,
            "atenuacao_fibra": 0.25,
            "splitter_razao": 32,
            "splitter_excesso": 2.5,
            "conectores_qtd": 4,
            "perda_conector": 0.3,
            "fusoes_qtd": 3,
            "perda_fusao": 0.05,
            "margem": None,
        }
        resultado = resolver(campos, sentido="downstream")
        assert resultado["campo_calculado"] == "margem"
        assert resultado["valor_calculado"] is not None

    def test_resolver_razao_splitter(self):
        campos = {
            "ptx": 5.0,
            "s": -30.0,
            "distancia": 10.0,
            "atenuacao_fibra": 0.25,
            "splitter_razao": None,
            "splitter_excesso": 2.5,
            "conectores_qtd": 4,
            "perda_conector": 0.3,
            "fusoes_qtd": 3,
            "perda_fusao": 0.05,
            "margem": 3.0,
        }
        resultado = resolver(campos, sentido="downstream")
        assert resultado["campo_calculado"] == "splitter_razao"
        assert isinstance(resultado["valor_calculado"], int)

    def test_dados_insuficientes(self):
        campos = {
            "ptx": None,
            "s": None,
            "distancia": 10.0,
            "atenuacao_fibra": 0.25,
            "splitter_razao": 32,
            "splitter_excesso": 2.5,
            "conectores_qtd": 4,
            "perda_conector": 0.3,
            "fusoes_qtd": 3,
            "perda_fusao": 0.05,
            "margem": 3.0,
        }
        with pytest.raises(DadosInsuficientesError):
            resolver(campos)

    def test_nenhuma_incognita(self):
        campos = {
            "ptx": 5.0,
            "s": -30.0,
            "distancia": 10.0,
            "atenuacao_fibra": 0.25,
            "splitter_razao": 32,
            "splitter_excesso": 2.5,
            "conectores_qtd": 4,
            "perda_conector": 0.3,
            "fusoes_qtd": 3,
            "perda_fusao": 0.05,
            "margem": 3.0,
        }
        with pytest.raises(NenhumaIncognitaError):
            resolver(campos)


class TestArredondarSplitter:
    def test_arredondar_para_32(self):
        assert _arredondar_splitter(27.3) == 32

    def test_arredondar_para_64(self):
        assert _arredondar_splitter(50.0) == 64

    def test_valor_exato_2(self):
        assert _arredondar_splitter(2.0) == 2

    def test_menor_que_2(self):
        assert _arredondar_splitter(1.0) == 2

    def test_maior_que_64(self):
        assert _arredondar_splitter(100.0) == 64
