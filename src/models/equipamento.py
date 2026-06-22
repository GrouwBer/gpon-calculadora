"""Classe de dominio Equipamento (OLT/ONU).

Representa as especificacoes de potencia e sensibilidade dos equipamentos
GPON conforme as classes definidas na ITU-T G.984.2.
"""

from dataclasses import dataclass
from typing import Optional

from .constantes import GPON_CLASSES_DEFAULT, CLASSES_VALIDAS


@dataclass
class Equipamento:
    """Especificacoes de potência e sensibilidade de um equipamento GPON.

    Attributes:
        ptx_down: Potencia de transmissao downstream (OLT->ONU) em dBm.
        ptx_up: Potencia de transmissao upstream (ONU->OLT) em dBm.
        s_down: Sensibilidade do receptor downstream em dBm.
        s_up: Sensibilidade do receptor upstream em dBm.
        classe: Nome da classe de potencia (B+, C+, C++, ou None para personalizado).
    """

    ptx_down: float
    ptx_up: float
    s_down: float
    s_up: float
    classe: Optional[str] = None

    @classmethod
    def from_classe(cls, nome: str) -> "Equipamento":
        """Cria um Equipamento com os valores padrao de uma classe GPON.

        Args:
            nome: Nome da classe ('B+', 'C+' ou 'C++').

        Returns:
            Equipamento com valores preenchidos conforme a classe.

        Raises:
            ValueError: Se a classe nao for reconhecida.
        """
        if nome not in CLASSES_VALIDAS:
            validas = ", ".join(CLASSES_VALIDAS)
            raise ValueError(
                f"Classe de potencia '{nome}' invalida. "
                f"Classes validas: {validas}"
            )

        vals = GPON_CLASSES_DEFAULT[nome]
        return cls(
            ptx_down=vals["ptx_down"],
            ptx_up=vals["ptx_up"],
            s_down=vals["s_down"],
            s_up=vals["s_up"],
            classe=nome,
        )
