"""Testes de coverage para caminhos nao testados."""

import pytest
from src.models.exceptions import ValorFisicamenteImpossivelError
from src.models.solver import resolver
from src.models.exceptions import DadosInsuficientesError, NenhumaIncognitaError


class TestCoverageGaps:
    def test_valor_fisicamente_impossivel_error(self):
        """Testa a excecao ValorFisicamenteImpossivelError."""
        err = ValorFisicamenteImpossivelError("distancia", -5.0, "> 0 km")
        assert "distancia" in str(err)
        assert "-5.0" in str(err)

    def test_resolver_distancia_negativa(self):
        """Resolver distancia com parametros que resultam em distancia negativa."""
        campos = {
            "ptx": 1.5,
            "s": -27.0,
            "distancia": None,
            "atenuacao_fibra": 0.25,
            "splitter_razao": 64,
            "splitter_excesso": 3.0,
            "conectores_qtd": 10,
            "perda_conector": 0.5,
            "fusoes_qtd": 5,
            "perda_fusao": 0.1,
            "margem": 5.0,
        }
        with pytest.raises(ValueError, match="negativa"):
            resolver(campos, sentido="downstream")

    def test_resolver_ptx_sem_distancia(self):
        """Resolver Ptx sem distancia deve lancar erro."""
        campos = {
            "ptx": None,
            "s": -30.0,
            "distancia": None,
            "atenuacao_fibra": 0.25,
            "splitter_razao": 32,
            "splitter_excesso": 1.0,
            "conectores_qtd": 0,
            "margem": 3.0,
        }
        with pytest.raises(ValueError):
            resolver(campos)

    def test_resolver_sem_ptx_e_sem_distancia(self):
        """Resolver sensibilidade sem Ptx e distancia."""
        campos = {
            "ptx": None,
            "s": None,
            "distancia": None,
            "atenuacao_fibra": 0.25,
            "splitter_razao": 32,
            "splitter_excesso": 1.0,
        }
        with pytest.raises(DadosInsuficientesError):
            resolver(campos)

    def test_resolver_margem_sem_ptx(self):
        """Resolver margem sem Ptx deve lancar erro."""
        campos = {
            "ptx": None,
            "s": -30.0,
            "distancia": 10.0,
            "atenuacao_fibra": 0.25,
            "splitter_razao": 32,
            "splitter_excesso": 1.0,
            "conectores_qtd": 0,
            "margem": None,
        }
        with pytest.raises(ValueError):
            resolver(campos)

    def test_resolver_splitter_sem_ptx(self):
        """Resolver splitter sem Ptx deve lancar erro."""
        campos = {
            "ptx": None,
            "s": -30.0,
            "distancia": 10.0,
            "atenuacao_fibra": 0.25,
            "splitter_razao": None,
            "splitter_excesso": 1.0,
            "conectores_qtd": 0,
            "margem": 3.0,
        }
        with pytest.raises(ValueError):
            resolver(campos)
