import heapq
import itertools
import math
import time
import sys
import os
from typing import List, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from labirinto import LabirintoOnline, ResultadoBuscaOnline, No, Estado


def _a_estrela_interno(lab: LabirintoOnline, inicio: Estado) -> Optional[List[Estado]]:
    """A* no mapa interno (desconhecido = livre). Retorna lista de posições ou None."""
    contador = itertools.count()
    no_ini = No(inicio, g=0.0)
    fronteira = [(lab.h_interna(inicio), next(contador), no_ini)]
    melhor_g = {inicio: 0.0}
    fechados = set()

    while fronteira:
        _, _, no = heapq.heappop(fronteira)
        if no.estado in fechados:
            continue
        if no.estado == lab.objetivo:
            estados = []
            atual = no
            while atual.pai is not None:
                estados.append(atual.estado)
                atual = atual.pai
            estados.reverse()
            return estados
        fechados.add(no.estado)
        for acao, prox, custo in lab.vizinhos_livres_internos(no.estado):
            novo_g = no.g + custo
            if prox in fechados or novo_g >= melhor_g.get(prox, math.inf):
                continue
            filho = No(estado=prox, pai=no, acao=acao, g=novo_g)
            melhor_g[prox] = novo_g
            heapq.heappush(fronteira, (novo_g + lab.h_interna(prox), next(contador), filho))
    return None


def _acao_para(pos: Estado, prox: Estado) -> str:
    dr, dc = prox[0] - pos[0], prox[1] - pos[1]
    return {(-1, 0): 'up', (1, 0): 'down', (0, -1): 'left', (0, 1): 'right'}[(dr, dc)]


def replanning_a_estrela(lab: LabirintoOnline) -> ResultadoBuscaOnline:
    t0 = time.perf_counter()
    pos = lab.inicio
    lab.perceber(pos)

    caminho = [pos]
    visitadas = {pos}
    movimentos = 0
    custo_real = 0.0
    revisitadas = 0
    replanejamentos = 0
    limite = lab.altura * lab.largura * 4

    plano: Optional[List[Estado]] = None
    plano_idx = 0

    for _ in range(limite):
        if pos == lab.objetivo:
            break

        # Replaneja se necessário
        replanear = plano is None or plano_idx >= len(plano)
        if not replanear and plano:
            prox = plano[plano_idx]
            if lab.mapa[prox[0]][prox[1]] is True:
                replanear = True

        if replanear:
            replanejamentos += 1
            plano = _a_estrela_interno(lab, pos)
            plano_idx = 0
            if not plano:
                break

        if plano_idx >= len(plano):
            break

        prox = plano[plano_idx]
        acao = _acao_para(pos, prox)
        nova = lab.mover(pos, acao)

        if nova is None:
            # Parede não mapeada — revela e replaneja
            lab.mapa[prox[0]][prox[1]] = True
            plano = None
            continue

        pos = nova
        plano_idx += 1
        movimentos += 1
        custo_real += 1.0
        if pos in visitadas:
            revisitadas += 1
        visitadas.add(pos)
        caminho.append(pos)
        lab.perceber(pos)

    encontrado = pos == lab.objetivo
    celulas_reveladas = sum(
        1 for r in range(lab.altura) for c in range(lab.largura)
        if lab.mapa[r][c] is not None
    )

    return ResultadoBuscaOnline(
        algoritmo='Replanning A*',
        encontrado=encontrado,
        movimentos_totais=movimentos,
        custo_real=custo_real,
        celulas_reveladas=celulas_reveladas,
        celulas_revisitadas=revisitadas,
        replanejamentos=replanejamentos,
        custo_otimo_offline=0.0,
        caminho_percorrido=caminho,
        tempo_ms=(time.perf_counter() - t0) * 1000,
    )
