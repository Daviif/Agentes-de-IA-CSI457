"""
Simulated Annealing para otimização da ordem de visitação dos pontos de coleta.

Representação e vizinhança: idênticas ao Hill-Climbing (swap de dois elementos).

Aceita pioras com probabilidade e^(−Δc / T), onde T decresce geometricamente:
    T_{t+1} = α · T_t,    0 < α < 1

Parâmetros padrão calibrados para os labirintos do TP01:
    T0       = 5 × custo_inicial   (temperatura inicial proporcional ao problema)
    alpha    = 0.995               (resfriamento lento)
    max_iter = 5000 por execução
"""
import time, random, math, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from labirinto import LabirintoBusca
from buscas.local.distancias import (
    calcular_distancias, custo_solucao, custo_otimo_bruteforce
)
from buscas.local.resultado_local import ResultadoBuscaLocal


def _executar(s0: list, lab: LabirintoBusca, dist: dict,
              T0: float, alpha: float, max_iter: int,
              rng: random.Random):
    """
    Uma corrida de SA a partir de s0.
    Retorna (melhor_solucao, melhor_custo, convergencia, n_iteracoes).
    convergencia: melhor custo acumulado a cada iteração.
    """
    k = len(s0)
    s = s0.copy()
    c = custo_solucao(s, lab, dist)

    melhor_s = s.copy()
    melhor_c = c
    T = T0
    convergencia = [c]

    for _ in range(max_iter):
        i, j = rng.sample(range(k), 2)
        v = s.copy()
        v[i], v[j] = v[j], v[i]
        cv = custo_solucao(v, lab, dist)

        delta = cv - c
        if delta < 0 or (T > 1e-10 and rng.random() < math.exp(-delta / T)):
            s, c = v, cv
            if c < melhor_c:
                melhor_c = c
                melhor_s = s.copy()

        T *= alpha
        convergencia.append(melhor_c)

    return melhor_s, melhor_c, convergencia, max_iter


def simulated_annealing(lab: LabirintoBusca,
                        dist: dict | None = None,
                        T0: float | None = None,
                        alpha: float = 0.995,
                        max_iter: int = 5000,
                        n_execucoes: int = 20,
                        semente: int | None = None) -> ResultadoBuscaLocal:
    """
    Executa SA n_execucoes vezes e coleta métricas.

    T0: temperatura inicial. Se None, usa 5 × custo da solução inicial.
    """
    if not lab.coletas:
        raise ValueError('Simulated Annealing requer pelo menos um ponto de coleta.')

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
            algoritmo='Simulated Annealing',
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

        c0    = custo_solucao(s0, lab, dist)
        T_ini = T0 if T0 is not None else max(5.0 * c0, 1.0)

        t0 = time.perf_counter()
        s, c, conv, n_it = _executar(s0, lab, dist, T_ini, alpha, max_iter, rng)
        t_ms = (time.perf_counter() - t0) * 1000

        custos.append(c)
        tempos.append(t_ms)
        iteracoes.append(n_it)

        if c < melhor_custo:
            melhor_custo = c
            melhor_perm  = s
            melhor_conv  = conv

    c_otimo = custo_otimo_bruteforce(lab, dist) if k <= 8 else math.inf
    limiar  = melhor_custo * 1.10
    taxa    = sum(1 for c in custos if c <= limiar) / n_execucoes

    return ResultadoBuscaLocal(
        algoritmo        = 'Simulated Annealing',
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
