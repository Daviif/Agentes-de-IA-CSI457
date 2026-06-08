"""
Algoritmo Genético para otimização da ordem de visitação dos pontos de coleta.

Representação: permutação de índices [0..k-1] dos pontos de coleta.
Operadores:
  · Seleção:  torneio de tamanho k (padrão 3)
  · Crossover: Order Crossover (OX) — preserva permutações válidas
  · Mutação:  swap de dois elementos com probabilidade mut_rate
  · Elitismo: melhor indivíduo preservado a cada geração

Justificativa do OX:
  Copiar um segmento de p1 e preencher o restante na ordem relativa de p2
  garante que o filho é sempre uma permutação válida e herda estrutura
  de ambos os pais — propriedade essencial em problemas de roteamento.
"""
import time, random, math, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from labirinto import LabirintoBusca
from buscas.local.distancias import (
    calcular_distancias, custo_solucao, custo_otimo_bruteforce
)
from buscas.local.resultado_local import ResultadoBuscaLocal


# ── Operadores genéticos ──────────────────────────────────────────────────────

def _torneio(pop: list, custos: list, k: int, rng: random.Random) -> list:
    candidatos = rng.sample(range(len(pop)), k)
    return pop[min(candidatos, key=lambda i: custos[i])].copy()


def _ox(p1: list, p2: list, rng: random.Random) -> list:
    """Order Crossover: copia segmento de p1, preenche com ordem relativa de p2."""
    n = len(p1)
    a, b = sorted(rng.sample(range(n), 2))
    filho = [None] * n
    filho[a:b+1] = p1[a:b+1]
    segmento = set(filho[a:b+1])
    pos = (b + 1) % n
    for gene in p2[b+1:] + p2[:b+1]:
        if gene not in segmento:
            filho[pos] = gene
            pos = (pos + 1) % n
    return filho


def _mutar(s: list, rng: random.Random) -> list:
    v = s.copy()
    i, j = rng.sample(range(len(v)), 2)
    v[i], v[j] = v[j], v[i]
    return v


# ── Interface pública ─────────────────────────────────────────────────────────

def genetic_algorithm(lab: LabirintoBusca,
                      dist: dict | None = None,
                      pop_size: int = 50,
                      n_geracoes: int = 200,
                      mut_rate: float = 0.15,
                      torneio_k: int = 3,
                      semente: int | None = None) -> ResultadoBuscaLocal:
    """
    Executa o GA e retorna métricas compatíveis com ResultadoBuscaLocal.
    n_execucoes=1 pois o GA já mantém diversidade via população.
    """
    if not lab.coletas:
        raise ValueError('GA requer pelo menos um ponto de coleta.')

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
            algoritmo='Algoritmo Genético',
            melhor_custo=c0, pior_custo=c0, custo_medio=c0,
            tempo_medio_ms=0.0, iteracoes_media=0,
            n_execucoes=1, taxa_sucesso=1.0,
            melhor_permutacao=s0, custo_otimo=c_otimo,
            convergencia=[c0],
        )

    t0 = time.perf_counter()

    pop    = [rng.sample(base, k) for _ in range(pop_size)]
    custos = [custo_solucao(ind, lab, dist) for ind in pop]

    melhor_idx  = min(range(pop_size), key=lambda i: custos[i])
    melhor_perm = pop[melhor_idx].copy()
    melhor_custo = custos[melhor_idx]
    convergencia = [melhor_custo]

    for _ in range(n_geracoes):
        nova_pop    = [melhor_perm.copy()]   # elitismo
        novos_custos = [melhor_custo]

        while len(nova_pop) < pop_size:
            p1   = _torneio(pop, custos, torneio_k, rng)
            p2   = _torneio(pop, custos, torneio_k, rng)
            filho = _ox(p1, p2, rng)
            if rng.random() < mut_rate:
                filho = _mutar(filho, rng)
            c = custo_solucao(filho, lab, dist)
            nova_pop.append(filho)
            novos_custos.append(c)

        pop    = nova_pop
        custos = novos_custos

        gen_idx = min(range(pop_size), key=lambda i: custos[i])
        if custos[gen_idx] < melhor_custo:
            melhor_custo = custos[gen_idx]
            melhor_perm  = pop[gen_idx].copy()

        convergencia.append(melhor_custo)

    t_ms    = (time.perf_counter() - t0) * 1000
    c_otimo = custo_otimo_bruteforce(lab, dist) if k <= 8 else math.inf
    limiar  = melhor_custo * 1.10
    taxa    = sum(1 for c in custos if c <= limiar) / pop_size

    return ResultadoBuscaLocal(
        algoritmo        = 'Algoritmo Genético',
        melhor_custo     = melhor_custo,
        pior_custo       = max(custos),
        custo_medio      = sum(custos) / len(custos),
        tempo_medio_ms   = t_ms,
        iteracoes_media  = n_geracoes,
        n_execucoes      = 1,
        taxa_sucesso     = taxa,
        melhor_permutacao= melhor_perm,
        custo_otimo      = c_otimo,
        convergencia     = convergencia,
    )
