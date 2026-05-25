import heapq
import itertools
import math
import time
import sys
import os
from typing import List, Set, Dict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from labirinto import LabirintoBusca, ResultadoBusca, No, Estado


def ucs(lab: LabirintoBusca) -> ResultadoBusca:
    t0 = time.perf_counter()
    contador = itertools.count()
    inicio = No(lab.inicio, g=0.0)
    fronteira: list = []
    heapq.heappush(fronteira, (0.0, next(contador), inicio))
    melhor_g: Dict[Estado, float] = {lab.inicio: 0.0}
    fechados: Set[Estado] = set()
    ordem_explorados: List[Estado] = []
    nos_explorados = 0
    nos_expandidos = 0
    fronteira_max = 1

    while fronteira:
        fronteira_max = max(fronteira_max, len(fronteira))
        _, _, no = heapq.heappop(fronteira)

        if no.estado in fechados:
            continue

        nos_explorados += 1
        ordem_explorados.append(no.estado)

        if no.estado == lab.objetivo:
            caminho, acoes = LabirintoBusca.reconstruir(no)
            return ResultadoBusca(
                'Busca de Custo Uniforme (UCS)', True,
                caminho, acoes, nos_explorados, nos_expandidos,
                ordem_explorados,
                custo_total=no.g,
                tempo_ms=(time.perf_counter() - t0) * 1000,
                fronteira_max=fronteira_max,
            )

        fechados.add(no.estado)
        nos_expandidos += 1

        for acao, estado, custo in lab.vizinhos(no.estado):
            novo_g = no.g + custo
            if estado in fechados:
                continue
            if novo_g < melhor_g.get(estado, math.inf):
                filho = No(estado=estado, pai=no, acao=acao, g=novo_g)
                melhor_g[estado] = novo_g
                heapq.heappush(fronteira, (novo_g, next(contador), filho))

    return ResultadoBusca(
        'Busca de Custo Uniforme (UCS)', False, [], [], nos_explorados, nos_expandidos,
        ordem_explorados,
        custo_total=0.0,
        tempo_ms=(time.perf_counter() - t0) * 1000,
        fronteira_max=fronteira_max,
    )
