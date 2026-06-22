"""Classe Alerta — representa um alerta de validacao."""

from dataclasses import dataclass
from typing import Literal, Optional


TipoSeveridade = Literal["info", "warning", "error"]


@dataclass
class Alerta:
    """Alerta de validacao para um campo do link budget."""

    campo: str
    nivel: TipoSeveridade
    mensagem: str
    valor_referencia: Optional[float] = None

    @property
    def icone(self) -> str:
        if self.nivel == "info":
            return "[i]"
        elif self.nivel == "warning":
            return "[!]"
        elif self.nivel == "error":
            return "[X]"
        return "[?]"
