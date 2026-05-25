import time
import sys
import os
from collections import deque
from typing import List, Set

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from labirinto import LabirintoBusca, ResultadoBusca, No, Estado


def bfs(lab: LabirintoBusca) -> ResultadoBusca:
    t0 = time.perf_counter()
    inicio = No(lab.inicio)
    fronteira = deque([inicio])
    em_fronteira = {lab.inicio}
    explorados: Set[Estado] = set()
    ordem_explorados: List[Estado] = []
    nos_explorados = 0
    nos_expandidos = 0
    fronteira_max = 1

    while fronteira:
        fronteira_max = max(fronteira_max, len(fronteira))
        no = fronteira.popleft()
        em_fronteira.discard(no.estado)
        nos_explorados += 1
        ordem_explorados.append(no.estado)

        if no.estado == lab.objetivo:
            caminho, acoes = LabirintoBusca.reconstruir(no)
            return ResultadoBusca(
                'Busca em Largura (BFS)', True,
                caminho, acoes, nos_explorados, nos_expandidos,
                ordem_explorados,
                custo_total=no.g,
                tempo_ms=(time.perf_counter() - t0) * 1000,
                fronteira_max=fronteira_max,
            )

        explorados.add(no.estado)
        nos_expandidos += 1

        for acao, estado, custo in lab.vizinhos(no.estado):
            if estado not in explorados and estado not in em_fronteira:
                filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                fronteira.append(filho)
                em_fronteira.add(estado)

    return ResultadoBusca(
        'Busca em Largura (BFS)', False, [], [], nos_explorados, nos_expandidos,
        ordem_explorados,
        custo_total=0.0,
        tempo_ms=(time.perf_counter() - t0) * 1000,
        fronteira_max=fronteira_max,
    )
