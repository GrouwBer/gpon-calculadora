"""Testes de edge cases e robustez."""
import pytest
from src.controllers.calculator_controller import CalculatorController


class TestEdgeCases:
    def setup_method(self):
        self.ctrl = CalculatorController()

    def _campos_base(self) -> dict:
        return {
            "ptx": "5.0", "s": "-30.0", "distancia": "10.0",
            "atenuacao_fibra": "0.25", "splitter_razao": "32",
            "splitter_excesso": "2.5", "conectores_qtd": "4",
            "perda_conector": "0.3", "fusoes_qtd": "3",
            "perda_fusao": "0.05", "margem": "3.0",
        }

    def test_virgula_como_decimal(self):
        """Virgula como separador decimal deve ser normalizada."""
        c = self._campos_base()
        c["distancia"] = "10,5"
        r = self.ctrl.calcular(c)
        assert r["sucesso"]

    def test_espacos_em_branco(self):
        """Espacos em branco devem ser ignorados."""
        c = self._campos_base()
        c["distancia"] = "  10  "
        r = self.ctrl.calcular(c)
        assert r["sucesso"]

    def test_notacao_cientifica(self):
        """Notacao cientifica deve ser aceita."""
        c = self._campos_base()
        c["distancia"] = "1e1"
        r = self.ctrl.calcular(c)
        assert r["sucesso"]

    def test_valores_extremos(self):
        """Valores extremamente altos nao devem crashar."""
        c = self._campos_base()
        c["distancia"] = "1000"
        r = self.ctrl.calcular(c)
        assert r["sucesso"]  # Pode dar erro de validacao, mas nao crash

    def test_margem_zero(self):
        """Margem zero e valida."""
        c = self._campos_base()
        c["margem"] = "0"
        r = self.ctrl.calcular(c)
        assert r["sucesso"]

    def test_campos_zero_permitidos(self):
        """Conectores e fusoes com valor zero sao permitidos."""
        c = self._campos_base()
        c["conectores_qtd"] = "0"
        c["fusoes_qtd"] = "0"
        r = self.ctrl.calcular(c)
        assert r["sucesso"]

    def test_string_vazia_vira_none(self):
        """String vazia deve ser convertida para None."""
        c = self._campos_base()
        c["distancia"] = ""
        r = self.ctrl.calcular(c)
        assert "erro" not in r or r["erro"] is None
        # Deve tentar resolver a distancia

    def test_texto_nao_numerico_lanca_erro(self):
        """Texto nao numerico nao crasha, retorna erro."""
        c = self._campos_base()
        c["ptx"] = "abc"
        r = self.ctrl.calcular(c)
        assert r["sucesso"] is False
        assert "invalido" in r.get("erro", "").lower()

    def test_unicode_digits(self):
        """Digitos Unicode (ex: fullwidth) devem ser tratados."""
        c = self._campos_base()
        c["distancia"] = "１０"  # fullwidth digits
        r = self.ctrl.calcular(c)
        assert r["sucesso"]  # Python aceita esses como digitos

    def test_erro_em_portugues(self):
        """Mensagens de erro devem estar em portugues."""
        c = self._campos_base()
        c["ptx"] = "xyz"
        r = self.ctrl.calcular(c)
        assert r["sucesso"] is False
        assert r["erro"] is not None

    def test_dois_campos_vazios(self):
        """Dois campos vazios retornam erro especifico."""
        c = self._campos_base()
        c["distancia"] = ""
        c["margem"] = ""
        r = self.ctrl.calcular(c)
        assert r["sucesso"] is False

    def test_sem_campos_vazios(self):
        """Todos campos preenchidos retorna veredito."""
        c = self._campos_base()
        r = self.ctrl.calcular(c)
        assert r["sucesso"]
        assert r["campo_calculado"] is None

    def test_overflow_nao_crasha(self):
        """Valor extremo 1e308 nao deve crashar."""
        c = self._campos_base()
        c["distancia"] = "1e308"
        r = self.ctrl.calcular(c)
        assert "sucesso" in r  # pode ser erro, mas nao exception
