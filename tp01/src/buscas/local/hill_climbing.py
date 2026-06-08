"""
Hill-Climbing para otimização da ordem de visitação dos pontos de coleta.

Representação: permutação de índices [0..k-1] dos pontos de coleta.
Vizinhança:    troca de dois elementos (swap) — gera k*(k-1)/2 vizinhos.

Justificativa da vizinhança por swap:
  · Cada swap altera exatamente dois segmentos do caminho, tornando
    o delta de custo calculável em O(1) se as distâncias estiverem pré-computadas.
  · É a menor perturbação que gera uma permutação distinta.
  · O espaço de vizinhança cobre todo o conjunto de permutações (conexo),
    garantindo que qualquer ótimo global é atingível por uma sequência de swaps.

Executa n_execucoes vezes com permutações iniciais aleatórias distintas
(reinicialização aleatória) para estimar métricas estatísticas.
"""
import time, random, math, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from labirinto import LabirintoBusca
from buscas.local.distancias import (
    calcular_distancias, custo_solucao, custo_otimo_bruteforce
)
from buscas.local.resultado_local import ResultadoBuscaLocal


# ── Vizinhança ────────────────────────────────────────────────────────────────

def _vizinhos_swap(s: list) -> list[list]:
    """Todos os vizinhos por troca de dois elementos."""
    vizinhos = []
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            v = s.copy()
            v[i], v[j] = v[j], v[i]
            vizinhos.append(v)
    return vizinhos


# ── Uma execução ──────────────────────────────────────────────────────────────

def _executar(s0: list, lab: LabirintoBusca, dist: dict):
    """
    Uma corrida de Hill-Climbing steepest-ascent a partir de s0.
    Retorna (solucao_final, custo_final, convergencia).
    convergencia: lista de custos a cada iteração (passo de melhora).
    """
    s = s0.copy()
    c = custo_solucao(s, lab, dist)
    convergencia = [c]

    while True:
        melhor_v = None
        melhor_c = c

        for v in _vizinhos_swap(s):
            cv = custo_solucao(v, lab, dist)
            if cv < melhor_c:
                melhor_c = cv
                melhor_v = v

        if melhor_v is None:
            break   # ótimo local — nenhum swap melhora

        s = melhor_v
        c = melhor_c
        convergencia.append(c)

    return s, c, convergencia


# ── Interface pública ─────────────────────────────────────────────────────────

def hill_climbing(lab: LabirintoBusca,
                  dist: dict | None = None,
                  n_execucoes: int = 30,
                  semente: int | None = None) -> ResultadoBuscaLocal:
    """
    Executa HC n_execucoes vezes com inícios aleatórios e coleta métricas.

    dist: dicionário de distâncias pré-computado (opcional — calcula se None).
    """
    if not lab.coletas:
        raise ValueError('Hill-Climbing local requer pelo menos um ponto de coleta.')

    if dist is None:
        dist = calcular_distancias(lab)

    rng  = random.Random(semente)
    k    = len(lab.coletas)
    base = list(range(k))

    if k < 2:
        s0 = base.copy()
        c0 = custo_solucao(s0, lab, dist)
        c_otimo = custo_otimo_bruteforce(lab, dist)
        return ResultadoBuscaLocal(
            algoritmo='Hill-Climbing',
            melhor_custo=c0, pior_custo=c0, custo_medio=c0,
            tempo_medio_ms=0.0, iteracoes_media=0,
            n_execucoes=1, taxa_sucesso=1.0,
            melhor_permutacao=s0, custo_otimo=c_otimo,
            convergencia=[c0],
        )

    custos:    list[float] = []
    tempos:    list[float] = []
    iteracoes: list[int]   = []

    melhor_perm:  list  = []
    melhor_custo: float = math.inf
    melhor_conv:  list  = []

    for _ in range(n_execucoes):
        s0 = base.copy()
        rng.shuffle(s0)

        t0 = time.perf_counter()
        s, c, conv = _executar(s0, lab, dist)
        t_ms = (time.perf_counter() - t0) * 1000

        custos.append(c)
        tempos.append(t_ms)
        iteracoes.append(len(conv) - 1)

        if c < melhor_custo:
            melhor_custo = c
            melhor_perm  = s
            melhor_conv  = conv

    # Ótimo por brute-force (k ≤ 8)
    c_otimo = custo_otimo_bruteforce(lab, dist) if k <= 8 else math.inf

    # Taxa de sucesso: execuções dentro de 10% do melhor encontrado
    limiar = melhor_custo * 1.10
    taxa   = sum(1 for c in custos if c <= limiar) / n_execucoes

    return ResultadoBuscaLocal(
        algoritmo        = 'Hill-Climbing',
        melhor_custo     = melhor_custo,
        pior_custo       = max(custos),
        custo_medio      = sum(custos) / len(custos),
        tempo_medio_ms   = sum(tempos) / len(tempos),
        iteracoes_media  = sum(iteracoes) / len(iteracoes),
        n_execucoes      = n_execucoes,
        taxa_sucesso     = taxa,
        melhor_permutacao= melhor_perm,
        custo_otimo      = c_otimo,
        convergencia     = melhor_conv,
    )
