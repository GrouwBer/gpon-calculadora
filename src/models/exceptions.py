"""Excecoes personalizadas do dominio de Link Budget GPON."""


class DadosInsuficientesError(ValueError):
    """Mais de um campo em branco — nao e possivel determinar qual resolver."""

    def __init__(self, campos_vazios: list[str]):
        self.campos_vazios = campos_vazios
        n = len(campos_vazios)
        msg = (
            f"Preencha exatamente 1 campo em branco para o calculo automatico. "
            f"Campos em branco encontrados ({n}): {', '.join(campos_vazios)}"
        )
        super().__init__(msg)


class NenhumaIncognitaError(ValueError):
    """Todos os campos estao preenchidos — nao ha variavel a calcular."""

    def __init__(self) -> None:
        super().__init__(
            "Todos os campos estao preenchidos. "
            "Nao ha variavel a calcular — exibindo veredito do enlace."
        )


class ValorFisicamenteImpossivelError(ValueError):
    """Valor calculado esta fora dos limites fisicos possiveis."""

    def __init__(self, campo: str, valor: float, limite: str):
        self.campo = campo
        self.valor = valor
        super().__init__(
            f"Valor calculado para '{campo}' = {valor:.2f} "
            f"esta fora dos limites fisicos ({limite}). "
            f"Verifique os parametros de entrada."
        )
