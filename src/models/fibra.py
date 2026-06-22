"""Classe de dominio Fibra Optica.

Representa o enlace de fibra optica G.652.D com coeficientes de atenuacao
diferenciados por comprimento de onda.
"""

from dataclasses import dataclass
from typing import Optional

from .constantes import FIBER_ATTENUATION


@dataclass
class Fibra:
    """Enlace de fibra optica com parametros de propagacao.

    Attributes:
        distancia: Distancia total do enlace em km (None se nao definida).
        atenuacao_1310: Coeficiente de atenuacao em 1310 nm (dB/km).
        atenuacao_1490: Coeficiente de atenuacao em 1490 nm (dB/km).
    """

    distancia: Optional[float] = None
    atenuacao_1310: float = FIBER_ATTENUATION[1310]
    atenuacao_1490: float = FIBER_ATTENUATION[1490]

    def atenuacao_para(self, comprimento_onda: int) -> float:
        """Retorna o coeficiente de atenuacao para um comprimento de onda.

        Args:
            comprimento_onda: Comprimento de onda em nm (1310, 1490 ou 1550).

        Returns:
            Coeficiente de atenuacao em dB/km.

        Raises:
            ValueError: Se o comprimento de onda nao for suportado.
        """
        if comprimento_onda == 1310:
            return self.atenuacao_1310
        elif comprimento_onda == 1490:
            return self.atenuacao_1490
        elif comprimento_onda in (1330, 1550):
            return FIBER_ATTENUATION.get(comprimento_onda, 0.20)
        raise ValueError(
            f"Comprimento de onda {comprimento_onda} nm nao suportado. "
            f"Valores validos: 1310, 1490, 1550"
        )
