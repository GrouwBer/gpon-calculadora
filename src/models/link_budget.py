"""Classe principal de calculo de Link Budget GPON.

Implementa as formulas de propagacao optica conforme ITU-T G.984.x e G.652.
Nao importa nenhum modulo de UI — e puro dominio.
"""

from dataclasses import dataclass, field
from typing import Optional
import math

from .equipamento import Equipamento
from .fibra import Fibra
from .splitter import Splitter
from .constantes import COMPRIMENTOS_ONDA


@dataclass
class LinkBudget:
    """Calculadora de orcamento de potencia optica para redes GPON.

    Encapsula todos os parametros do enlace e fornece metodos para
    calcular perdas, potencia recebida e veredito de viabilidade.

    Attributes:
        equipamento: Especificacoes do equipamento (OLT/ONU).
        fibra: Enlace de fibra optica.
        splitters: Lista de splitters no enlace (1 ou 2 estagios).
        conectores_qtd: Numero de pares de conectores.
        perda_conector: Perda por conector (dB).
        fusoes_qtd: Numero de fusoes.
        perda_fusao: Perda por fusao (dB).
        margem: Margem de seguranca (dB).
        sentido: Sentido do enlace ('downstream' ou 'upstream').
    """

    equipamento: Equipamento
    fibra: Fibra
    splitters: list[Splitter] = field(default_factory=list)
    conectores_qtd: int = 0
    perda_conector: float = 0.3
    fusoes_qtd: int = 0
    perda_fusao: float = 0.05
    margem: float = 3.0
    sentido: str = "downstream"

    def __post_init__(self) -> None:
        """Valida o sentido apos inicializacao."""
        if self.sentido not in ("downstream", "upstream"):
            raise ValueError(
                f"Sentido invalido: '{self.sentido}'. "
                f"Use 'downstream' ou 'upstream'."
            )

    @property
    def comprimento_onda(self) -> int:
        """Comprimento de onda (nm) conforme o sentido do enlace."""
        return COMPRIMENTOS_ONDA[self.sentido]

    @property
    def ptx(self) -> float:
        """Potencia de transmissao (dBm) conforme o sentido."""
        return (self.equipamento.ptx_down if self.sentido == "downstream"
                else self.equipamento.ptx_up)

    @property
    def sensibilidade(self) -> float:
        """Sensibilidade do receptor (dBm) conforme o sentido."""
        return (self.equipamento.s_down if self.sentido == "downstream"
                else self.equipamento.s_up)

    @property
    def atenuacao_fibra_coeficiente(self) -> float:
        """Coeficiente de atenuacao da fibra (dB/km) para o comprimento de onda atual."""
        return self.fibra.atenuacao_para(self.comprimento_onda)

    def calcular_perda_distancia(self) -> float:
        """Calcula a perda por atenuacao na fibra.

        Returns:
            Perda em dB (distancia x coeficiente).

        Raises:
            ValueError: Se distancia for None ou <= 0.
        """
        if self.fibra.distancia is None:
            raise ValueError("Distancia nao definida. Defina a distancia da fibra.")
        if self.fibra.distancia <= 0:
            raise ValueError(
                f"Distancia deve ser maior que zero: {self.fibra.distancia} km"
            )
        return self.fibra.distancia * self.atenuacao_fibra_coeficiente

    def calcular_perda_splitters(self) -> float:
        """Calcula a perda total dos splitters no enlace.

        Returns:
            Perda total em dB (soma de 1 ou 2 estagios).
        """
        return sum(s.perda_total for s in self.splitters)

    def calcular_perda_conectores(self) -> float:
        """Calcula a perda total dos conectores.

        Returns:
            Perda em dB (quantidade x perda unitaria).
        """
        return self.conectores_qtd * self.perda_conector

    def calcular_perda_fusoes(self) -> float:
        """Calcula a perda total das fusoes.

        Returns:
            Perda em dB (quantidade x perda unitaria).
        """
        return self.fusoes_qtd * self.perda_fusao

    def calcular_atenuacao_total(self) -> float:
        """Calcula a atenuacao total do enlace.

        Soma todas as contribuicoes de perda.

        Returns:
            Atenuacao total em dB.
        """
        return (self.calcular_perda_distancia()
                + self.calcular_perda_splitters()
                + self.calcular_perda_conectores()
                + self.calcular_perda_fusoes()
                + self.margem)

    def calcular_potencia_recebida(self) -> float:
        """Calcula a potencia optica recebida na ponta do enlace.

        Formula: P_rec = Ptx - A_total

        Returns:
            Potencia recebida em dBm.
        """
        return self.ptx - self.calcular_atenuacao_total()

    def veredito(self) -> dict:
        """Avalia se o enlace e viavel.

        Um enlace e viavel se P_rec >= S + margem.

        Returns:
            Dicionario com status, folga (dB) e mensagem.
        """
        p_rec = self.calcular_potencia_recebida()
        s = self.sensibilidade
        limiar = s + self.margem
        folga = p_rec - limiar

        if folga >= 0:
            return {
                "status": True,
                "viabilidade": "ENLACE VIAVEL",
                "folga": folga,
                "mensagem": (
                    f"P_rec ({p_rec:.2f} dBm) >= S ({s:.1f} dBm) + "
                    f"Margem ({self.margem:.1f} dB)"
                ),
            }
        else:
            return {
                "status": False,
                "viabilidade": "ENLACE INVIAVEL",
                "folga": folga,
                "mensagem": (
                    f"P_rec ({p_rec:.2f} dBm) < S ({s:.1f} dBm) + "
                    f"Margem ({self.margem:.1f} dB)"
                ),
            }

    def breakdown(self) -> dict:
        """Retorna discriminacao detalhada de todas as perdas.

        Returns:
            Dicionario com cada componente, valor em dB e percentual.
        """
        perda_dist = self.calcular_perda_distancia()
        perda_spl = self.calcular_perda_splitters()
        perda_con = self.calcular_perda_conectores()
        perda_fus = self.calcular_perda_fusoes()
        a_total = perda_dist + perda_spl + perda_con + perda_fus + self.margem

        def pct(valor: float) -> float:
            return (valor / a_total * 100) if a_total > 0 else 0.0

        return {
            "fibra": {"valor": perda_dist, "unidade": "dB", "percentual": pct(perda_dist)},
            "splitters": {"valor": perda_spl, "unidade": "dB", "percentual": pct(perda_spl)},
            "conectores": {"valor": perda_con, "unidade": "dB", "percentual": pct(perda_con)},
            "fusoes": {"valor": perda_fus, "unidade": "dB", "percentual": pct(perda_fus)},
            "margem": {"valor": self.margem, "unidade": "dB", "percentual": pct(self.margem)},
            "atenuacao_total": {"valor": a_total, "unidade": "dB", "percentual": 100.0},
        }
