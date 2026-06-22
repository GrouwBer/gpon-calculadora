"""Validador de parametros de Link Budget GPON."""

from typing import Optional
from .alerta import Alerta
from .constantes import CLASSES_VALIDAS, GPON_CLASSES_DEFAULT


class Validador:
    LIMITES = {
        "ptx":        (0.0, 10.0, "dBm", "Potencia de transmissao"),
        "s":          (-40.0, -25.0, "dBm", "Sensibilidade do receptor"),
        "distancia":  (0.1, 60.0, "km", "Distancia da fibra"),
        "atenuacao":  (0.15, 0.50, "dB/km", "Atenuacao da fibra"),
        "conectores": (0, 10, "un", "Quantidade de conectores"),
        "perda_con":  (0.1, 1.0, "dB", "Perda por conector"),
        "fusoes":     (0, 20, "un", "Quantidade de fusoes"),
        "perda_fus":  (0.01, 0.30, "dB", "Perda por fusao"),
        "margem":     (0.0, 6.0, "dB", "Margem de seguranca"),
    }
    TIPICOS = {
        "ptx":        (1.0, 7.0),
        "s":          (-32.0, -27.0),
        "distancia":  (1.0, 20.0),
        "margem":     (1.0, 3.0),
    }

    def validar_ptx(self, valor: Optional[float]) -> list[Alerta]:
        alertas = []
        if valor is None:
            return alertas
        mn, mx, _, desc = self.LIMITES["ptx"]
        if valor < mn or valor > mx:
            alertas.append(Alerta("ptx", "error", f"{desc} fora do limite: {valor:.1f} dBm (range: {mn} a {mx} dBm)", valor))
        elif self._fora_tipico("ptx", valor):
            tmin, tmax = self.TIPICOS["ptx"]
            alertas.append(Alerta("ptx", "warning", f"{desc} fora do tipico: {valor:.1f} dBm (tipico: {tmin} a {tmax} dBm)", valor))
        return alertas

    def validar_s(self, valor: Optional[float]) -> list[Alerta]:
        alertas = []
        if valor is None:
            return alertas
        mn, mx, _, desc = self.LIMITES["s"]
        if valor < mn or valor > mx:
            alertas.append(Alerta("s", "error", f"{desc} fora do limite: {valor:.1f} dBm (range: {mn} a {mx} dBm)", valor))
        elif self._fora_tipico("s", valor):
            tmin, tmax = self.TIPICOS["s"]
            alertas.append(Alerta("s", "warning", f"{desc} fora do tipico: {valor:.1f} dBm (tipico: {tmin} a {tmax} dBm)", valor))
        return alertas

    def validar_distancia(self, valor: Optional[float]) -> list[Alerta]:
        alertas = []
        if valor is None:
            return alertas
        if valor <= 0:
            alertas.append(Alerta("distancia", "error", "Distancia deve ser maior que zero.", valor))
            return alertas
        mn, mx, _, desc = self.LIMITES["distancia"]
        if valor > mx:
            alertas.append(Alerta("distancia", "error", f"{desc} maxima: {mx} km. Valor: {valor:.1f} km.", valor))
        elif self._fora_tipico("distancia", valor):
            tmin, tmax = self.TIPICOS["distancia"]
            alertas.append(Alerta("distancia", "warning", f"{desc} fora do tipico: {valor:.1f} km (tipico: {tmin} a {tmax} km)", valor))
        return alertas

    def validar_margem(self, valor: Optional[float]) -> list[Alerta]:
        alertas = []
        if valor is None:
            return alertas
        mn, mx, _, desc = self.LIMITES["margem"]
        if valor < mn:
            alertas.append(Alerta("margem", "error", f"{desc} nao pode ser negativa: {valor:.1f} dB.", valor))
        elif valor > mx:
            alertas.append(Alerta("margem", "warning", f"{desc} acima do tipico: {valor:.1f} dB (tipico: {mn} a {mx} dB)", valor))
        return alertas

    def validar_conectores(self, qtd: Optional[int], perda: Optional[float]) -> list[Alerta]:
        alertas = []
        if qtd is not None:
            if qtd < 0:
                alertas.append(Alerta("conectores_qtd", "error", "Quantidade negativa.", float(qtd)))
        if perda is not None:
            mn, mx, _, desc = self.LIMITES["perda_con"]
            if perda < mn or perda > mx:
                alertas.append(Alerta("perda_conector", "error", f"{desc} fora do limite: {perda:.2f} dB (range: {mn} a {mx} dB)", perda))
        return alertas

    def validar_fusoes(self, qtd: Optional[int], perda: Optional[float]) -> list[Alerta]:
        alertas = []
        if qtd is not None and qtd < 0:
            alertas.append(Alerta("fusoes_qtd", "error", "Quantidade negativa.", float(qtd)))
        if perda is not None:
            mn, mx, _, desc = self.LIMITES["perda_fus"]
            if perda < mn or perda > mx:
                alertas.append(Alerta("perda_fusao", "error", f"{desc} fora do limite: {perda:.3f} dB (range: {mn} a {mx} dB)", perda))
        return alertas

    def validar_atenuacao_total(self, a_total: float, classe: Optional[str]) -> list[Alerta]:
        alertas = []
        if classe and classe in CLASSES_VALIDAS:
            budget = GPON_CLASSES_DEFAULT[classe]["budget"]
            if a_total > budget:
                alertas.append(Alerta("atenuacao_total", "error", f"Atenuacao ({a_total:.1f} dB) excede orcamento {classe} ({budget:.0f} dB).", a_total))
        return alertas

    def validar_campos(self, campos: dict, classe: Optional[str] = None) -> list[Alerta]:
        alertas: list[Alerta] = []
        alertas.extend(self.validar_ptx(campos.get("ptx")))
        alertas.extend(self.validar_s(campos.get("s")))
        alertas.extend(self.validar_distancia(campos.get("distancia")))
        alertas.extend(self.validar_margem(campos.get("margem")))
        alertas.extend(self.validar_conectores(campos.get("conectores_qtd"), campos.get("perda_conector")))
        alertas.extend(self.validar_fusoes(campos.get("fusoes_qtd"), campos.get("perda_fusao")))
        a_total = campos.get("atenuacao_total")
        if a_total is not None:
            alertas.extend(self.validar_atenuacao_total(a_total, classe))
        return alertas

    def _fora_tipico(self, campo: str, valor: float) -> bool:
        if campo not in self.TIPICOS:
            return False
        tmin, tmax = self.TIPICOS[campo]
        return valor < tmin or valor > tmax
