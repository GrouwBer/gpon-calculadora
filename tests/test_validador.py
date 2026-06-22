"""Testes para o Validador."""

import pytest
from src.models.validador import Validador
from src.models.alerta import Alerta


class TestValidador:
    def setup_method(self):
        self.val = Validador()

    def test_ptx_dentro_do_range(self):
        alertas = self.val.validar_ptx(3.0)
        assert len(alertas) == 0

    def test_ptx_muito_alto_error(self):
        alertas = self.val.validar_ptx(12.0)
        assert len(alertas) == 1
        assert alertas[0].nivel == "error"

    def test_ptx_fora_tipico_warning(self):
        alertas = self.val.validar_ptx(8.0)
        assert len(alertas) == 1
        assert alertas[0].nivel == "warning"

    def test_distancia_acima_60km_error(self):
        alertas = self.val.validar_distancia(80.0)
        assert len(alertas) == 1
        assert alertas[0].nivel == "error"

    def test_distancia_zero_error(self):
        alertas = self.val.validar_distancia(0)
        assert len(alertas) == 1
        assert alertas[0].nivel == "error"

    def test_distancia_negativa_error(self):
        alertas = self.val.validar_distancia(-5.0)
        assert len(alertas) == 1
        assert alertas[0].nivel == "error"

    def test_margem_alta_warning(self):
        alertas = self.val.validar_margem(8.0)
        assert len(alertas) == 1
        assert alertas[0].nivel == "warning"

    def test_margem_zero_valida(self):
        alertas = self.val.validar_margem(0.0)
        assert len(alertas) == 0  # dentro do limite (>= 0)

    def test_margem_negativa_error(self):
        alertas = self.val.validar_margem(-1.0)
        assert len(alertas) == 1
        assert alertas[0].nivel == "error"

    def test_conectores_negativo_error(self):
        alertas = self.val.validar_conectores(-2, None)
        assert len(alertas) == 1

    def test_perda_conector_fora_range(self):
        alertas = self.val.validar_conectores(4, 2.0)
        tem_erro = any(a.nivel == "error" for a in alertas)
        assert tem_erro

    def test_atenuacao_total_excede_budget(self):
        alertas = self.val.validar_atenuacao_total(35.0, "B+")
        assert len(alertas) == 1
        assert alertas[0].nivel == "error"

    def test_atenuacao_total_dentro_budget(self):
        alertas = self.val.validar_atenuacao_total(20.0, "C+")
        assert len(alertas) == 0

    def test_validar_campos_multiplos(self):
        campos = {
            "ptx": 12.0,
            "s": -30.0,
            "distancia": 80.0,
            "margem": 3.0,
            "conectores_qtd": 4,
            "perda_conector": 0.3,
            "fusoes_qtd": 3,
            "perda_fusao": 0.05,
        }
        alertas = self.val.validar_campos(campos)
        assert len(alertas) >= 2  # ptx error + distancia error

    def test_nenhum_alerta_cenario_valido(self):
        campos = {
            "ptx": 3.0,
            "s": -28.0,
            "distancia": 10.0,
            "margem": 3.0,
            "conectores_qtd": 4,
            "perda_conector": 0.3,
            "fusoes_qtd": 3,
            "perda_fusao": 0.05,
        }
        alertas = self.val.validar_campos(campos)
        assert len(alertas) == 0
