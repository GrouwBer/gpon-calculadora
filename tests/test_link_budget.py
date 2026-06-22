"""Testes de unidade para a classe LinkBudget."""

import math
import pytest
from src.models.link_budget import LinkBudget
from src.models.equipamento import Equipamento
from src.models.fibra import Fibra
from src.models.splitter import Splitter


class TestLinkBudget:
    @pytest.fixture
    def eq_cplus(self):
        return Equipamento.from_classe("C+")

    @pytest.fixture
    def eq_bplus(self):
        return Equipamento.from_classe("B+")

    @pytest.fixture
    def fibra_10km(self):
        return Fibra(distancia=10.0)

    @pytest.fixture
    def splitter_1_32(self):
        return Splitter(razao=32, excesso_perda=1.0)

    @pytest.fixture
    def lb_downstream(self, eq_cplus, fibra_10km, splitter_1_32):
        return LinkBudget(
            equipamento=eq_cplus,
            fibra=fibra_10km,
            splitters=[splitter_1_32],
            conectores_qtd=4,
            perda_conector=0.3,
            fusoes_qtd=3,
            perda_fusao=0.05,
            margem=3.0,
            sentido="downstream",
        )

    def test_perda_distancia_1490(self):
        fibra = Fibra(distancia=20.0)
        eq = Equipamento.from_classe("C+")
        lb = LinkBudget(eq, fibra, [], sentido="downstream")
        perda = lb.calcular_perda_distancia()
        assert perda == pytest.approx(5.0, rel=1e-3)

    def test_perda_distancia_1310(self):
        fibra = Fibra(distancia=20.0)
        eq = Equipamento.from_classe("C+")
        lb = LinkBudget(eq, fibra, [], sentido="upstream")
        perda = lb.calcular_perda_distancia()
        assert perda == pytest.approx(7.0, rel=1e-3)

    def test_perda_splitter_1_32(self):
        s = Splitter(razao=32, excesso_perda=1.0)
        total = s.perda_total
        teorica = 10.0 * math.log10(32)
        assert total == pytest.approx(teorica + 1.0, rel=1e-3)

    def test_perda_splitter_2_estagios(self, eq_cplus, fibra_10km):
        s1 = Splitter(razao=4, excesso_perda=0.5)
        s2 = Splitter(razao=8, excesso_perda=0.5)
        perda_s1 = s1.perda_total
        perda_s2 = s2.perda_total
        esperado = 10*math.log10(4) + 0.5 + 10*math.log10(8) + 0.5
        assert (perda_s1 + perda_s2) == pytest.approx(esperado, rel=1e-3)

    def test_atenuacao_total_soma_correta(self, lb_downstream):
        lb = lb_downstream
        esperado = (
            lb.calcular_perda_distancia()
            + lb.calcular_perda_splitters()
            + lb.calcular_perda_conectores()
            + lb.calcular_perda_fusoes()
            + lb.margem
        )
        assert lb.calcular_atenuacao_total() == pytest.approx(esperado, rel=1e-3)

    def test_potencia_recepcao(self, lb_downstream):
        lb = lb_downstream
        p_rec = lb.calcular_potencia_recebida()
        esperado = lb.ptx - lb.calcular_atenuacao_total()
        assert p_rec == pytest.approx(esperado, rel=1e-3)

    def test_veredito_viavel(self, lb_downstream):
        lb = lb_downstream
        v = lb.veredito()
        assert v["status"] is True
        assert "VIAVEL" in v["viabilidade"]

    def test_veredito_inviavel(self, eq_bplus):
        fibra = Fibra(distancia=40.0)
        s = Splitter(razao=64, excesso_perda=2.0)
        lb = LinkBudget(eq_bplus, fibra, [s],
                        conectores_qtd=6, perda_conector=0.3,
                        margem=3.0, sentido="downstream")
        v = lb.veredito()
        assert v["status"] is False
        assert "INVIAVEL" in v["viabilidade"]

    def test_breakdown_contem_componentes(self, lb_downstream):
        bd = lb_downstream.breakdown()
        assert "fibra" in bd
        assert "splitters" in bd
        assert "conectores" in bd
        assert "fusoes" in bd
        assert "margem" in bd
        assert "atenuacao_total" in bd

    def test_breakdown_valores_positivos(self, lb_downstream):
        bd = lb_downstream.breakdown()
        for componente in ["fibra", "splitters", "conectores", "fusoes", "margem"]:
            assert bd[componente]["valor"] >= 0

    def test_distancia_zero_lanca_erro(self, eq_cplus):
        fibra = Fibra(distancia=0)
        lb = LinkBudget(eq_cplus, fibra, [], sentido="downstream")
        with pytest.raises(ValueError, match="maior que zero"):
            lb.calcular_perda_distancia()

    def test_sentido_invalido_lanca_erro(self, eq_cplus):
        fibra = Fibra(distancia=10.0)
        with pytest.raises(ValueError):
            LinkBudget(eq_cplus, fibra, [], sentido="invalido")

    def test_cenario_urbano_tipico(self):
        """PRD 14.4.1: cenario urbano tipico."""
        eq = Equipamento.from_classe("B+")
        fibra = Fibra(distancia=5.0)
        s = Splitter(razao=32, excesso_perda=2.5)
        lb = LinkBudget(eq, fibra, [s],
                        conectores_qtd=4, perda_conector=0.3,
                        fusoes_qtd=3, perda_fusao=0.05,
                        margem=3.0, sentido="downstream")
        a_total = lb.calcular_atenuacao_total()
        p_rec = lb.calcular_potencia_recebida()
        v = lb.veredito()
        assert a_total == pytest.approx(22.35, rel=0.1)
        assert p_rec > eq.s_down
        assert v["status"] is True

    def test_cenario_inviavel(self):
        """PRD 14.4.3: cenario inviavel."""
        eq = Equipamento.from_classe("B+")
        fibra = Fibra(distancia=40.0)
        s = Splitter(razao=64, excesso_perda=3.0)
        lb = LinkBudget(eq, fibra, [s],
                        conectores_qtd=6, perda_conector=0.3,
                        margem=3.0, sentido="downstream")
        v = lb.veredito()
        assert v["status"] is False
