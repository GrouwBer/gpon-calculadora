"""Testes para a classe Splitter."""

import math
import pytest
from src.models.splitter import Splitter


class TestSplitter:
    def test_perda_teorica_1_32(self):
        """Splitter 1:32 tem perda teorica de 15.05 dB."""
        s = Splitter(razao=32)
        esperado = 10.0 * math.log10(32)
        assert abs(s.perda_teorica - esperado) < 1e-10

    def test_perda_teorica_1_2(self):
        """Splitter 1:2 tem perda teorica de 3.01 dB."""
        s = Splitter(razao=2)
        esperado = 10.0 * math.log10(2)
        assert abs(s.perda_teorica - esperado) < 1e-10

    def test_perda_teorica_1_4(self):
        """Splitter 1:4 tem perda teorica de 6.02 dB."""
        s = Splitter(razao=4)
        assert abs(s.perda_teorica - 6.02) < 0.01

    def test_perda_total_com_excesso(self):
        """Perda total = teorica + excesso."""
        s = Splitter(razao=32, excesso_perda=1.0)
        esperado = 10.0 * math.log10(32) + 1.0
        assert abs(s.perda_total - esperado) < 1e-10

    def test_excesso_padrao(self):
        """Excesso de perda padrao e 1.0 dB."""
        s = Splitter(razao=16)
        assert s.excesso_perda == 1.0

    def test_todas_razoes_validas(self):
        """Todas as razoes validas funcionam."""
        for razao in [2, 4, 8, 16, 32, 64]:
            s = Splitter(razao=razao)
            assert s.razao == razao
            assert abs(s.perda_teorica - 10.0 * math.log10(razao)) < 1e-10

    def test_razao_invalida_lanca_excecao(self):
        """Razao que nao e potencia de 2 lanca ValueError."""
        with pytest.raises(ValueError) as exc:
            Splitter(razao=3)
        assert "2" in str(exc.value)

    def test_excesso_negativo_lanca_excecao(self):
        """Excesso de perda negativo lanca ValueError."""
        with pytest.raises(ValueError):
            Splitter(razao=8, excesso_perda=-0.5)

    def test_razao_zero_lanca_excecao(self):
        """Razao zero lanca ValueError."""
        with pytest.raises(ValueError):
            Splitter(razao=0)
