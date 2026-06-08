"""
Pré-computação de distâncias entre pontos do labirinto via A*.

d(X, Y) = custo do menor caminho de X a Y (BFS/A* no grid).
Usado pela busca local para avaliar o custo de uma permutação.
"""
import heapq, itertools, math, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from labirinto import LabirintoBusca


def _vizinhos(lab: LabirintoBusca, pos: tuple):
    i, j = pos
    for di, dj in ((-1,0),(1,0),(0,-1),(0,1)):
        ni, nj = i+di, j+dj
        if 0 <= ni < lab.altura and 0 <= nj < lab.largura and not lab.paredes[ni][nj]:
            yield (ni, nj)


def a_estrela_entre(lab: LabirintoBusca, origem: tuple, destino: tuple) -> float:
    """Custo do menor caminho entre dois pontos quaisquer do labirinto."""
    if origem == destino:
        return 0.0

    def h(p): return abs(p[0] - destino[0]) + abs(p[1] - destino[1])

    cnt  = itertools.count()
    fila = [(h(origem), next(cnt), origem, 0.0)]
    melhor_g: dict = {origem: 0.0}
    fechados: set  = set()

    while fila:
        _, _, pos, g = heapq.heappop(fila)
        if pos in fechados:
            continue
        if pos == destino:
            return g
        fechados.add(pos)
        for np in _vizinhos(lab, pos):
            ng = g + 1.0
            if np not in fechados and ng < melhor_g.get(np, math.inf):
                melhor_g[np] = ng
                heapq.heappush(fila, (ng + h(np), next(cnt), np, ng))

    return math.inf   # sem caminho (labirinto desconexo)


def calcular_distancias(lab: LabirintoBusca) -> dict:
    """
    Pré-computa d(X,Y) para todos os pares entre {A, C1…Ck, B}.
    Retorna dict[(pos1, pos2)] = float (simétrico).
    """
    pontos = [lab.inicio] + list(lab.coletas) + [lab.objetivo]
    dist: dict = {}
    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            c = a_estrela_entre(lab, pontos[i], pontos[j])
            dist[(pontos[i], pontos[j])] = c
            dist[(pontos[j], pontos[i])] = c
    return dist


def custo_solucao(permutacao: list, lab: LabirintoBusca, dist: dict) -> float:
    """
    C(s) = d(A, C_π(1)) + Σ d(C_π(i), C_π(i+1)) + d(C_π(k), B)

    permutacao: lista de índices em lab.coletas
    """
    coletas = lab.coletas
    seq = [lab.inicio] + [coletas[i] for i in permutacao] + [lab.objetivo]
    return sum(dist[(seq[i], seq[i+1])] for i in range(len(seq) - 1))


def custo_otimo_bruteforce(lab: LabirintoBusca, dist: dict) -> float:
    """Custo ótimo por força bruta — viável apenas para k ≤ 8."""
    k = len(lab.coletas)
    if k == 0:
        return dist.get((lab.inicio, lab.objetivo), math.inf)
    melhor = math.inf
    for perm in itertools.permutations(range(k)):
        c = custo_solucao(list(perm), lab, dist)
        if c < melhor:
            melhor = c
    return melhor
