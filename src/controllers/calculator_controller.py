"""Controlador que orquestra Model + Validador para o calculo de Link Budget."""

from typing import Optional
from src.models.equipamento import Equipamento
from src.models.fibra import Fibra
from src.models.splitter import Splitter
from src.models.link_budget import LinkBudget
from src.models.solver import resolver
from src.models.validador import Validador
from src.models.exceptions import DadosInsuficientesError, NenhumaIncognitaError


class CalculatorController:
    def __init__(self) -> None:
        self.validador = Validador()
        self.ultimo_resultado: Optional[dict] = None

    def sanitizar(self, valor: str) -> Optional[float]:
        if valor is None:
            return None
        if isinstance(valor, (int, float)):
            return float(valor)
        v = str(valor).strip()
        if v == "":
            return None
        v = v.replace(",", ".")
        try:
            return float(v)
        except (ValueError, TypeError):
            raise ValueError(f"Valor invalido: '{valor}' nao e um numero valido.")

    def sanitizar_int(self, valor: str) -> Optional[int]:
        if valor is None:
            return None
        if isinstance(valor, int):
            return valor
        v = self.sanitizar(valor)
        if v is None:
            return None
        return int(v)

    def _construir_link_budget(self, campos: dict, sentido: str, classe: Optional[str]) -> tuple[LinkBudget, list]:
        eq = Equipamento.from_classe(classe) if classe in ("B+", "C+", "C++") else Equipamento(
            ptx_down=campos.get("ptx", 0.0) or 0.0,
            ptx_up=campos.get("ptx", 0.0) or 0.0,
            s_down=campos.get("s", 0.0) or 0.0,
            s_up=campos.get("s", 0.0) or 0.0,
            classe=classe,
        )
        fibra = Fibra(distancia=campos.get("distancia") or None)
        spl = []
        sr1 = campos.get("splitter_razao")
        se1 = campos.get("splitter_excesso", 1.0) or 1.0
        sr2 = campos.get("splitter2_razao")
        se2 = campos.get("splitter2_excesso", 1.0) or 1.0
        if sr1 is not None and sr1 > 0:
            spl.append(Splitter(razao=int(sr1), excesso_perda=se1))
        if sr2 is not None and sr2 > 0:
            spl.append(Splitter(razao=int(sr2), excesso_perda=se2))
        lb = LinkBudget(
            equipamento=eq, fibra=fibra, splitters=spl,
            conectores_qtd=int(campos.get("conectores_qtd", 0) or 0),
            perda_conector=campos.get("perda_conector", 0.3) or 0.3,
            fusoes_qtd=int(campos.get("fusoes_qtd", 0) or 0),
            perda_fusao=campos.get("perda_fusao", 0.05) or 0.05,
            margem=campos.get("margem", 3.0) or 3.0,
            sentido=sentido,
        )
        alertas = self.validador.validar_campos(campos, classe)
        return lb, alertas

    def _montar_resultado(self, lb: LinkBudget, campo_calc: Optional[str],
                           valor_calc: Optional[float], unidade: str,
                           alertas: list, erro: Optional[str] = None,
                           mensagem: Optional[str] = None) -> dict:
        return {
            "sucesso": erro is None,
            "campo_calculado": campo_calc,
            "valor_calculado": valor_calc,
            "unidade": unidade,
            "potencia_recebida": lb.calcular_potencia_recebida(),
            "breakdown": lb.breakdown(),
            "veredito": lb.veredito(),
            "alertas": alertas,
            "erro": erro,
            "mensagem": mensagem,
        }

    def calcular(self, campos_raw: dict, sentido: str = "downstream",
                 classe: Optional[str] = None) -> dict:
        try:
            campos = self._converter_campos(campos_raw)
        except ValueError as e:
            return {"sucesso": False, "erro": str(e)}

        # Verificar quantos campos estao vazios (ignorar splitter2 opcionais)
        campos_essenciais = {k: v for k, v in campos.items() if k not in ("classe", "splitter2_razao", "splitter2_excesso")}
        vazios = sum(1 for v in campos_essenciais.values() if v is None)
        campos_calc = {k: v for k, v in campos_essenciais.items()}

        try:
            if vazios == 0:
                # Nenhum campo vazio — apenas veredito
                lb, alertas = self._construir_link_budget(campos, sentido, classe)
                a_total = lb.calcular_atenuacao_total()
                alertas.extend(self.validador.validar_atenuacao_total(a_total, classe or ""))
                return self._montar_resultado(lb, None, None, "", alertas,
                    mensagem="Nenhum campo para calcular - exibindo veredito do enlace.")

            if vazios == 1:
                resultado_solver = resolver(campos, sentido)
                lb = resultado_solver["link_budget"]
                lb2, alertas = self._construir_link_budget(campos, sentido, classe)
                a_total = lb.calcular_atenuacao_total()
                alertas.extend(self.validador.validar_atenuacao_total(a_total, classe or ""))
                return self._montar_resultado(lb,
                    resultado_solver["campo_calculado"],
                    resultado_solver["valor_calculado"],
                    resultado_solver.get("unidade", ""), alertas)

            # Mais de 1 vazio
            return {"sucesso": False, "erro": f"Preencha exatamente 1 campo em branco. {vazios} campos vazios encontrados."}

        except (DadosInsuficientesError, ValueError) as e:
            return {"sucesso": False, "erro": str(e)}

    def _converter_campos(self, raw: dict) -> dict:
        mapa_float = ["ptx", "s", "distancia", "atenuacao_fibra",
                      "splitter_excesso", "splitter2_excesso",
                      "perda_conector", "perda_fusao", "margem"]
        mapa_int = ["splitter_razao", "splitter2_razao",
                     "conectores_qtd", "fusoes_qtd"]
        result = {}
        for chave in mapa_float:
            if chave in raw:
                result[chave] = self.sanitizar(raw[chave])
        for chave in mapa_int:
            if chave in raw:
                result[chave] = self.sanitizar_int(raw[chave])
        if "classe" in raw:
            result["classe"] = raw["classe"] if raw["classe"] else None
        return result
