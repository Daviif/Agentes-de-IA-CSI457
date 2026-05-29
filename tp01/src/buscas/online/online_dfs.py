import time
import sys
import os
from typing import List, Dict, Tuple, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from labirinto import LabirintoOnline, ResultadoBuscaOnline, Estado

_INVERSA = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
_DELTA = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}


def online_dfs(lab: LabirintoOnline) -> ResultadoBuscaOnline:
    """
    Online DFS sistemático (AIMA Cap. 4).
    Mantém ações não tentadas por posição e pilha de retorno.
    """
    t0 = time.perf_counter()
    pos = lab.inicio
    lab.perceber(pos)

    # pos -> lista de ações ainda não tentadas
    nao_tentadas: Dict[Estado, List[str]] = {}
    # pilha de (pos_anterior, acao_de_retorno) para backtracking
    pilha: List[Tuple[Estado, str]] = []

    visitadas = {pos}
    caminho = [pos]
    movimentos = 0
    custo_real = 0.0
    revisitadas = 0
    limite = lab.altura * lab.largura * 4

    def _acoes_disponiveis(p: Estado) -> List[str]:
        return [a for a, _, _ in lab.vizinhos_livres_internos(p)]

    for _ in range(limite):
        if pos == lab.objetivo:
            break

        if pos not in nao_tentadas:
            nao_tentadas[pos] = _acoes_disponiveis(pos)

        moveu = False
        while nao_tentadas[pos]:
            acao = nao_tentadas[pos].pop(0)
            nova = lab.mover(pos, acao)
            if nova is None:
                # Parede desconhecida — marca e tenta próxima ação
                dr, dc = _DELTA[acao]
                r2, c2 = pos[0] + dr, pos[1] + dc
                if 0 <= r2 < lab.altura and 0 <= c2 < lab.largura:
                    lab.mapa[r2][c2] = True
                continue

            pilha.append((pos, _INVERSA[acao]))
            pos = nova
            movimentos += 1
            custo_real += 1.0
            if pos in visitadas:
                revisitadas += 1
            visitadas.add(pos)
            caminho.append(pos)
            lab.perceber(pos)
            # Descobre ações disponíveis na nova posição
            if pos not in nao_tentadas:
                nao_tentadas[pos] = _acoes_disponiveis(pos)
            moveu = True
            break

        if not moveu:
            # Sem ações — backtrack
            if not pilha:
                break
            _, back_acao = pilha.pop()
            nova = lab.mover(pos, back_acao)
            if nova is None:
                break
            pos = nova
            movimentos += 1
            custo_real += 1.0
            revisitadas += 1
            caminho.append(pos)
            lab.perceber(pos)

    encontrado = pos == lab.objetivo
    celulas_reveladas = sum(
        1 for r in range(lab.altura) for c in range(lab.largura)
        if lab.mapa[r][c] is not None
    )

    return ResultadoBuscaOnline(
        algoritmo='Online DFS',
        encontrado=encontrado,
        movimentos_totais=movimentos,
        custo_real=custo_real,
        celulas_reveladas=celulas_reveladas,
        celulas_revisitadas=revisitadas,
        replanejamentos=0,
        custo_otimo_offline=0.0,
        caminho_percorrido=caminho,
        tempo_ms=(time.perf_counter() - t0) * 1000,
    )
