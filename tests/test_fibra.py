"""Testes para a classe Fibra."""

import pytest
from src.models.fibra import Fibra


class TestFibra:
    def test_atributos_padrao(self):
        """Fibra instanciada sem argumentos tem valores G.652.D."""
        fibra = Fibra()
        assert fibra.atenuacao_1310 == 0.35
        assert fibra.atenuacao_1490 == 0.25
        assert fibra.distancia is None

    def test_atenuacao_para_1490(self):
        """Coeficiente correto para downstream (1490 nm)."""
        fibra = Fibra()
        assert fibra.atenuacao_para(1490) == 0.25

    def test_atenuacao_para_1310(self):
        """Coeficiente correto para upstream (1310 nm)."""
        fibra = Fibra()
        assert fibra.atenuacao_para(1310) == 0.35

    def test_atenuacao_com_distancia_definida(self):
        """Fibra com distancia definida."""
        fibra = Fibra(distancia=10.0)
        assert fibra.distancia == 10.0

    def test_atenuacao_para_comprimento_invalido(self):
        """Comprimento de onda nao suportado lanca ValueError."""
        fibra = Fibra()
        with pytest.raises(ValueError):
            fibra.atenuacao_para(850)

    def test_distancia_opcional(self):
        """Distancia pode ser None (variavel faltante)."""
        fibra = Fibra()
        assert fibra.distancia is None
        # Deve ser possivel definir depois
        fibra.distancia = 20.0
        assert fibra.distancia == 20.0
