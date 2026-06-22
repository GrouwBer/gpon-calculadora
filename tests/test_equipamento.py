"""Testes para a classe Equipamento."""

import pytest
from src.models.equipamento import Equipamento
from src.models.constantes import GPON_CLASSES_DEFAULT


class TestEquipamento:
    def test_from_classe_bplus(self):
        """Criacao de equipamento B+ preenche valores corretos."""
        eq = Equipamento.from_classe("B+")
        dados = GPON_CLASSES_DEFAULT["B+"]
        assert eq.ptx_down == dados["ptx_down"]
        assert eq.ptx_up == dados["ptx_up"]
        assert eq.s_down == dados["s_down"]
        assert eq.s_up == dados["s_up"]
        assert eq.classe == "B+"

    def test_from_classe_cplus(self):
        """Criacao de equipamento C+ preenche valores corretos."""
        eq = Equipamento.from_classe("C+")
        dados = GPON_CLASSES_DEFAULT["C+"]
        assert eq.ptx_down == dados["ptx_down"]
        assert eq.s_down == dados["s_down"]
        assert eq.classe == "C+"

    def test_from_classe_cpp(self):
        """Criacao de equipamento C++ preenche valores corretos."""
        eq = Equipamento.from_classe("C++")
        dados = GPON_CLASSES_DEFAULT["C++"]
        assert eq.ptx_down == dados["ptx_down"]
        assert eq.s_down == dados["s_down"]
        assert eq.classe == "C++"

    def test_classe_invalida_lanca_excecao(self):
        """Classe de potencia invalida lanca ValueError."""
        with pytest.raises(ValueError) as exc:
            Equipamento.from_classe("X+")
        assert "B+" in str(exc.value)
        assert "C+" in str(exc.value)
        assert "C++" in str(exc.value)

    def test_criacao_manual(self):
        """Criacao manual de equipamento sem classe."""
        eq = Equipamento(ptx_down=4.0, ptx_up=2.0, s_down=-28.0, s_up=-30.0)
        assert eq.ptx_down == 4.0
        assert eq.s_up == -30.0
        assert eq.classe is None

    def test_todas_as_classes_disponiveis(self):
        """Todas as classes validas podem ser instanciadas."""
        for classe in ["B+", "C+", "C++"]:
            eq = Equipamento.from_classe(classe)
            assert eq.classe == classe
            assert eq.ptx_down > 0
            assert eq.s_down < 0
