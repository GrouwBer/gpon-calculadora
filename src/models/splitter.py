"""Classe de dominio Splitter Optico.

Representa um divisor optico passivo (PLC splitter) com razao de divisao
e perda por insercao (excesso de perda).
"""

from dataclasses import dataclass
import math

from .constantes import SPLITTER_RATIOS_VALIDAS


@dataclass
class Splitter:
    """Divisor optico passivo (PLC splitter).

    Attributes:
        razao: Razao de divisao (N saidas). Deve ser potencia de 2.
        excesso_perda: Perda por insercao adicional (excess loss) em dB.
    """

    razao: int
    excesso_perda: float = 1.0

    def __post_init__(self) -> None:
        """Valida a razao apos a inicializacao."""
        if self.razao not in SPLITTER_RATIOS_VALIDAS:
            validas = ", ".join(str(r) for r in SPLITTER_RATIOS_VALIDAS)
            raise ValueError(
                f"Razao de splitter {self.razao}:{self.razao} invalida. "
                f"A razao deve ser uma potencia de 2 entre "
                f"as seguintes: {validas}"
            )
        if self.excesso_perda < 0:
            raise ValueError(
                f"Excesso de perda nao pode ser negativo: {self.excesso_perda}"
            )

    @property
    def perda_teorica(self) -> float:
        """Perda teorica do splitter: 10 * log10(N) dB."""
        return 10.0 * math.log10(self.razao)

    @property
    def perda_total(self) -> float:
        """Perda total do splitter: perda teorica + excesso."""
        return self.perda_teorica + self.excesso_perda

    def __repr__(self) -> str:
        return (f"Splitter(1:{self.razao}, "
                f"perda_teorica={self.perda_teorica:.2f} dB, "
                f"excesso={self.excesso_perda:.1f} dB, "
                f"total={self.perda_total:.2f} dB)")
