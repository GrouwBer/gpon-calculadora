# Documento de Requisitos — Calculadora de Link Budget GPON

> **Versão:** 1.0  
> **Data:** 2026-06-23  
> **Projeto Interdisciplinar** — IFSULDEMINAS Campus Poços de Caldas  
> **Disciplinas:** Propagação de Ondas Eletromagnéticas + Engenharia de Software  
> **Autor do projeto:** Guilherme (GrouwBer)

---

## 1. Introdução

### 1.1 Propósito

Este documento descreve os requisitos funcionais e não-funcionais da **Calculadora de Link Budget GPON**, uma aplicação desktop com interface gráfica que permite calcular, validar e simular o orçamento de potência óptica de redes GPON (Gigabit Passive Optical Network).

O diferencial arquitetural é que o sistema **identifica a variável faltante** dentre os parâmetros do enlace e resolve a equação para ela — o usuário não precisa saber previamente qual fórmula usar.

### 1.2 Escopo

O sistema abrange:
- Cálculo de atenuação em fibra óptica (dB/km) para diferentes comprimentos de onda (1310 nm, 1490 nm)
- Perdas por inserção em splitters ópticos (1 ou 2 estágios)
- Perdas em conectores e fusões
- Balanço de potência (Ptx − Atenuação = Prec)
- Validação contra limites normativos (ITU-T G.984.x, G.652)
- Interface gráfica com feedback visual de alertas
- Exportação de resultados (TXT / PDF)

### 1.3 Referências Normativas

| Norma | Descrição |
|-------|-----------|
| ITU-T G.984.1 | GPON — General characteristics |
| ITU-T G.984.2 | GPON — PMD layer specification (classes B+, C+, C++) |
| ITU-T G.652 | Single-mode optical fibre characteristics |
| Ato Anatel nº 7869 | Referenda ITU-T G.984.2 para equipamentos GPON no Brasil |

---

## 2. Requisitos Funcionais

| ID | Requisito | Prioridade | Status |
|----|-----------|------------|--------|
| **RF01** | Entrada numérica para Ptx, S, distância, atenuação, splitter, conectores, fusões, margem | **Alta** | ✅ |
| **RF02** | Identificar campo vazio e calcular automaticamente | **Alta** | ✅ |
| **RF03** | Selecionar classe de potência (B+, C+, C++) com preenchimento automático | **Alta** | ✅ |
| **RF04** | Coeficientes de atenuação distintos: 1490 nm (0.25 dB/km) e 1310 nm (0.35 dB/km) | **Alta** | ✅ |
| **RF05** | Exibir breakdown: perda_por_distancia, splitter, conectores, fusões, total, P_rec | **Alta** | ✅ |
| **RF06** | Veredito visual: "ENLACE VIÁVEL" (verde) ou "ENLACE INVIÁVEL" (vermelho) | **Alta** | ✅ |
| **RF07** | Validar campos contra limites e exibir alertas (warning/error) | **Média** | ✅ |
| **RF08** | Tratar dados insuficientes com mensagem de erro clara | **Alta** | ✅ |
| **RF09** | Suportar splitter de 1 ou 2 estágios em cascata | **Média** | ✅ |
| **RF10** | Botões Calcular/Limpar, atalhos Enter/Escape | **Alta** | ✅ |
| **RF11** | Modo de demonstração com cenário típico | **Baixa** | ✅ |
| **RF12** | Interface organizada por seções lógicas | **Média** | ✅ |
| **RF13** | Tratar entradas não numéricas sem crash | **Alta** | ✅ |
| **RF14** | Exibir resultado com unidade correta | **Alta** | ✅ |
| **RF15** | Impedir valores negativos para quantidades | **Alta** | ✅ |
| **RF16** | Exportação TXT e PDF | **Média** | ✅ |

---

## 3. Requisitos Não-Funcionais

### 3.1 Performance

| Requisito | Meta | Status |
|-----------|------|--------|
| Tempo de cálculo | ≤ 10 ms | ✅ |
| Tempo de inicialização | ≤ 2 s | ✅ |
| Responsividade da UI | ≤ 100 ms | ✅ |

### 3.2 Confiabilidade

| Requisito | Meta | Status |
|-----------|------|--------|
| Crashes por entrada inválida | 0 | ✅ (109 testes) |
| Cobertura de testes (models) | ≥ 80% | ✅ (92%) |
| Mensagens de erro em português | Sim | ✅ |

### 3.3 Portabilidade

- **Linguagem:** Python 3.10+
- **Plataformas:** Windows, Linux, macOS
- **Interface:** CustomTkinter
- **Empacotamento:** PyInstaller (build.bat / build.sh)

### 3.4 Manutenibilidade

- Arquitetura MVP (Model-View-Presenter)
- Separação clara: `models/` (domínio), `controllers/` (orquestração), `views/` (UI)
- Model não importa nenhum módulo de UI
- Docstrings em todas as classes e funções públicas

---

## 4. Arquitetura

### 4.1 Padrão: MVP (Model-View-Presenter)

```
View (CustomTkinter)  ←→  Presenter  →  Controller  →  Model (Domínio)
```

| Camada | Diretório | Responsabilidade |
|--------|-----------|-----------------|
| **Model** | `src/models/` | Lógica de negócio pura |
| **Controller** | `src/controllers/` | Sanitização + orquestração |
| **Presenter** | `src/controllers/` | Mediação View ↔ Controller |
| **View** | `src/views/` | Renderização CustomTkinter |

### 4.2 Estrutura de Diretórios

```
gpon-calculadora/
├── main.py                    # Entry point
├── requirements.txt           # Dependências
├── pytest.ini                 # Config testes
├── build.bat / build.sh       # Empacotamento
├── README.md
├── docs/                      # Documentação
│   ├── diagrama-caso-de-uso.puml
│   ├── diagrama-classes.puml
│   └── documento-de-requisitos.md
├── src/
│   ├── models/                # 9 módulos
│   │   ├── link_budget.py     # Cálculo principal
│   │   ├── equipamento.py     # Equipamento OLT/ONU
│   │   ├── fibra.py           # Fibra G.652.D
│   │   ├── splitter.py        # Splitter PLC
│   │   ├── validador.py       # Validação
│   │   ├── alerta.py          # Objeto Alerta
│   │   ├── solver.py          # Resolução da variável
│   │   ├── constantes.py      # Constantes ITU-T
│   │   └── exceptions.py      # Exceções
│   ├── controllers/           # 3 módulos
│   │   ├── calculator_controller.py
│   │   ├── calculator_presenter.py
│   │   └── exportador.py
│   └── views/                 # 6 módulos
│       ├── tela_principal.py
│       ├── painel_equipamentos.py
│       ├── painel_fibra.py
│       ├── painel_componentes.py
│       ├── painel_seguranca.py
│       └── painel_resultado.py
└── tests/                     # 12 módulos, 109 testes
```

---

## 5. Fórmulas

```
P_rec = P_tx − A_total

A_total = α×d + 10×log₁₀(N) + A_excesso + qtd_con×pc + qtd_fus×pf + Margem

VIÁVEL:    P_rec ≥ S + Margem
INVIÁVEL:  P_rec < S + Margem
```

---

## 6. Classes de Potência (ITU-T G.984.2)

| Classe | Ptx Down | Ptx Up | S Down | S Up | Budget |
|--------|----------|--------|--------|------|--------|
| **B+** | +1.5 dBm | +0.5 dBm | −27.0 dBm | −28.0 dBm | 28 dB |
| **C+** | +5.0 dBm | +3.0 dBm | −30.0 dBm | −32.0 dBm | 32 dB |
| **C++** | +7.0 dBm | +4.0 dBm | −32.0 dBm | −35.0 dBm | 35 dB |

---

## 7. Cobertura de Testes

- **Total:** 109 testes
- **Cobertura (models):** 92%
- **Framework:** pytest + pytest-cov
- **Cenários de integração:** 4 cenários reais (urbano típico, limite, inviável, distância máxima)

---

## 8. Tecnologias

| Componente | Tecnologia |
|-----------|-----------|
| Linguagem | Python 3.10+ |
| Interface | CustomTkinter 5.2+ |
| Resolução | SymPy 1.12+ |
| Testes | pytest 7.4+, pytest-cov 4.1+ |
| PDF | fpdf2 2.7+ |
| Empacotamento | PyInstaller |

---

## 9. Critérios de Aceite

### Propagação de Ondas
- [x] Cálculo correto de atenuação com 2 comprimentos de onda
- [x] Cálculo correto de perda por splitter (10×log₁₀(N))
- [x] Resultados conferem com cálculo manual
- [x] Diferenciação downstream vs upstream
- [x] Breakdown completo com valor e unidade

### Engenharia de Software
- [x] Classes de domínio sem import de UI
- [x] Controller como única camada de mediação
- [x] 92% de cobertura em models/
- [x] Zero crashes com entradas inválidas
- [x] Mensagens de erro em português
- [x] Código documentado com docstrings

---

> **Fim do documento.**  
> *Diagramas UML complementares em `docs/diagrama-caso-de-uso.puml` e `docs/diagrama-classes.puml`.*
