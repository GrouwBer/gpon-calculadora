"""Solver para identificacao e resolucao da variavel faltante."""

import math
from .link_budget import LinkBudget
from .equipamento import Equipamento
from .fibra import Fibra
from .splitter import Splitter
from .exceptions import DadosInsuficientesError, NenhumaIncognitaError
from .constantes import SPLITTER_RATIOS_VALIDAS, PERDA_CONECTOR_PADRAO, PERDA_FUSAO_PADRAO, MARGEM_PADRAO


def _arredondar_splitter(N: float) -> int:
    for ratio in SPLITTER_RATIOS_VALIDAS:
        if ratio >= N:
            return ratio
    return SPLITTER_RATIOS_VALIDAS[-1]


def resolver(campos: dict, sentido: str = "downstream") -> dict:
    # Ignorar splitter2 opcionais na contagem de vazios
    campos_essenciais = {k: v for k, v in campos.items() if k not in ("splitter2_razao", "splitter2_excesso")}
    vazios = [k for k, v in campos_essenciais.items() if v is None]
    if len(vazios) > 1:
        raise DadosInsuficientesError(vazios)
    if len(vazios) == 0:
        raise NenhumaIncognitaError()
    campo_faltante = vazios[0]

    ptx = campos.get("ptx")
    s = campos.get("s")
    distancia = campos.get("distancia")
    atenuacao = campos.get("atenuacao_fibra", 0.25 if sentido == "downstream" else 0.35)
    splitter_razao = campos.get("splitter_razao")
    splitter_excesso = campos.get("splitter_excesso", 1.0)
    splitter2_razao = campos.get("splitter2_razao")
    splitter2_excesso = campos.get("splitter2_excesso", 1.0)
    conectores_qtd = campos.get("conectores_qtd", 0)
    perda_conector = campos.get("perda_conector", PERDA_CONECTOR_PADRAO)
    fusoes_qtd = campos.get("fusoes_qtd", 0)
    perda_fusao = campos.get("perda_fusao", PERDA_FUSAO_PADRAO)
    margem = campos.get("margem", MARGEM_PADRAO)
    classe = campos.get("classe")

    def _perda_splitter_known() -> float:
        total = 0.0
        if splitter_razao is not None and splitter_razao > 0:
            total += 10.0 * math.log10(splitter_razao) + splitter_excesso
        if splitter2_razao is not None and splitter2_razao > 0:
            total += 10.0 * math.log10(splitter2_razao) + splitter2_excesso
        return total

    perda_splitters = _perda_splitter_known()
    perda_conectores_known = (conectores_qtd if conectores_qtd is not None else 0) * perda_conector
    perda_fusoes_known = (fusoes_qtd if fusoes_qtd is not None else 0) * perda_fusao

    if campo_faltante == "ptx":
        if distancia is None or s is None:
            raise ValueError("Distancia e sensibilidade sao necessarias")
        perda_dist = distancia * atenuacao
        a_total = perda_dist + perda_splitters + perda_conectores_known + perda_fusoes_known + margem
        valor_calculado = s + a_total

    elif campo_faltante == "s":
        if ptx is None or distancia is None:
            raise ValueError("Ptx e distancia sao necessarias")
        perda_dist = distancia * atenuacao
        a_total = perda_dist + perda_splitters + perda_conectores_known + perda_fusoes_known + margem
        valor_calculado = ptx - a_total

    elif campo_faltante == "distancia":
        if ptx is None or s is None:
            raise ValueError("Ptx e sensibilidade sao necessarias")
        perdas_outras = perda_splitters + perda_conectores_known + perda_fusoes_known + margem
        if atenuacao <= 0:
            raise ValueError("Atenuacao da fibra deve ser maior que zero")
        valor_calculado = (ptx - s - perdas_outras) / atenuacao
        if valor_calculado < 0:
            raise ValueError(f"Distancia negativa ({valor_calculado:.2f} km)")

    elif campo_faltante == "margem":
        if ptx is None or s is None or distancia is None:
            raise ValueError("Ptx, sensibilidade e distancia sao necessarias")
        perda_dist = distancia * atenuacao
        a_sem_margem = perda_dist + perda_splitters + perda_conectores_known + perda_fusoes_known
        valor_calculado = ptx - s - a_sem_margem

    elif campo_faltante == "splitter_razao":
        if ptx is None or s is None or distancia is None:
            raise ValueError("Ptx, sensibilidade e distancia sao necessarias")
        perda_dist = distancia * atenuacao
        splitter2_perda = (
            10.0 * math.log10(splitter2_razao) + splitter2_excesso
            if splitter2_razao is not None and splitter2_razao > 0 else 0.0
        )
        perdas_sem_splitter1 = perda_dist + splitter2_perda + perda_conectores_known + perda_fusoes_known + margem
        resto = ptx - s - perdas_sem_splitter1
        if resto <= 0:
            raise ValueError(f"Orcamento insuficiente: {resto:.2f} dB")
        N_frac = 10.0 ** (resto / 10.0)
        valor_calculado = _arredondar_splitter(N_frac)

    else:
        raise ValueError(f"Campo '{campo_faltante}' nao suportado")

    ptx_v = ptx if ptx is not None else (s + s + margem) if campo_faltante != "ptx" and s else valor_calculado
    s_v = s if s is not None else (ptx - (distancia * atenuacao + perda_splitters + perda_conectores_known + perda_fusoes_known + margem)) if ptx and distancia else valor_calculado

    # Reconstruir campos resolvidos
    campos_resolvidos = {k: v for k, v in campos.items()}
    campos_resolvidos[campo_faltante] = valor_calculado

    # Valores definitivos
    ptx_f = campos_resolvidos.get("ptx") or 0.0
    s_f = campos_resolvidos.get("s") or 0.0
    dist_f = campos_resolvidos.get("distancia") or 0.0
    at_f = campos_resolvidos.get("atenuacao_fibra", atenuacao) or atenuacao
    con_q = int(campos_resolvidos.get("conectores_qtd", 0) or 0)
    pc_f = campos_resolvidos.get("perda_conector", PERDA_CONECTOR_PADRAO)
    fus_q = int(campos_resolvidos.get("fusoes_qtd", 0) or 0)
    pf_f = campos_resolvidos.get("perda_fusao", PERDA_FUSAO_PADRAO)
    marg_f = campos_resolvidos.get("margem", MARGEM_PADRAO)

    eq = Equipamento(ptx_down=ptx_f if sentido == "downstream" else ptx_f,
                     ptx_up=ptx_f if sentido == "upstream" else ptx_f,
                     s_down=s_f if sentido == "downstream" else s_f,
                     s_up=s_f if sentido == "upstream" else s_f,
                     classe=classe)
    fibra = Fibra(distancia=dist_f if dist_f > 0 else None)
    spl = []
    sr1 = campos_resolvidos.get("splitter_razao")
    se1 = campos_resolvidos.get("splitter_excesso", 1.0)
    sr2 = campos_resolvidos.get("splitter2_razao")
    se2 = campos_resolvidos.get("splitter2_excesso", 1.0)
    if sr1 is not None and sr1 > 0:
        spl.append(Splitter(razao=int(sr1), excesso_perda=se1))
    if sr2 is not None and sr2 > 0:
        spl.append(Splitter(razao=int(sr2), excesso_perda=se2))

    lb = LinkBudget(eq, fibra, spl, con_q, pc_f, fus_q, pf_f, marg_f, sentido)

    unidades = {"ptx": "dBm", "s": "dBm", "distancia": "km", "margem": "dB", "splitter_razao": ":1"}

    return {
        "campo_calculado": campo_faltante,
        "valor_calculado": valor_calculado,
        "unidade": unidades.get(campo_faltante, ""),
        "potencia_recebida": lb.calcular_potencia_recebida(),
        "breakdown": lb.breakdown(),
        "veredito": lb.veredito(),
        "link_budget": lb,
    }
