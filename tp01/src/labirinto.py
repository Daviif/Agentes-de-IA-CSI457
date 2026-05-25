from dataclasses import dataclass
from typing import Any, Optional, Tuple, List, Dict, Set, Protocol, runtime_checkable
from collections import deque
import heapq
import itertools
import math

Estado = Tuple[int, int]


@runtime_checkable
class Labirinto(Protocol):
    """
    Interface mínima usada pelos algoritmos de busca.
    Satisfeita por LabirintoBusca e LabirintoComColetas.
    """
    inicio: Any
    objetivo: Any

    def vizinhos(self, estado: Any) -> List[Tuple]: ...
    def h(self, estado: Any) -> float: ...
    def reconstruir(self, no: 'No') -> Tuple[List, List]: ...

@dataclass
class No:
    estado: Estado
    pai: Optional['No'] = None
    acao: Optional[str] = None
    g: float = 0.0

@dataclass
class ResultadoBusca:
    algoritmo: str
    encontrado: bool
    caminho: List[Estado]
    acoes: List[str]
    nos_explorados: int
    nos_expandidos: int
    estados_explorados: List[Estado]
    custo_total: float = 0.0
    tempo_ms: float = 0.0
    fronteira_max: int = 0

    @property
    def tamanho_caminho(self) -> Optional[int]:
        return len(self.acoes) if self.encontrado else None

class LabirintoBusca:
    inicio: Tuple[int, int]
    objetivo: Tuple[int, int]
    coletas: List[Tuple[int, int]]
    
    def __init__(self, filename: str):
        with open(filename, encoding='utf-8') as f:
            contents = f.read()

        if contents.count('A') != 1:
            raise ValueError('O labirinto deve ter exatamente um ponto inicial A.')
        if contents.count('B') != 1:
            raise ValueError('O labirinto deve ter exatamente um objetivo B.')

        linhas = contents.splitlines()
        self.altura = len(linhas)
        self.largura = max(len(linha) for linha in linhas)
        self.paredes = []
        self.coletas = []

        for i in range(self.altura):
            row = []
            for j in range(self.largura):
                char = linhas[i][j] if j < len(linhas[i]) else ' '
                if char == 'A':
                    self.inicio = (i, j)
                    row.append(False)
                elif char == 'B':
                    self.objetivo = (i, j)
                    row.append(False)
                elif char == 'C':  # Ponto de coleta (célula livre)
                    self.coletas.append((i, j))
                    row.append(False)
                elif char == ' ':
                    row.append(False)
                else:
                    row.append(True)
            self.paredes.append(row)

    def vizinhos(self, estado: Estado):
        linha, coluna = estado
        candidatos = [
            ('up',    (linha - 1, coluna)),
            ('down',  (linha + 1, coluna)),
            ('left',  (linha, coluna - 1)),
            ('right', (linha, coluna + 1)),
        ]
        resultado = []
        for acao, (l, c) in candidatos:
            if 0 <= l < self.altura and 0 <= c < self.largura and not self.paredes[l][c]:
                resultado.append((acao, (l, c), 1.0))
        return resultado

    def h(self, estado: Estado) -> float:
        """Heurística de Manhattan para movimentos ortogonais com custo unitário."""
        return abs(estado[0] - self.objetivo[0]) + abs(estado[1] - self.objetivo[1])

    def reconstruir(self, no: No):
        estados = []
        acoes = []
        atual = no
        while atual.pai is not None:
            estados.append(atual.estado)
            acoes.append(atual.acao)
            atual = atual.pai
        estados.reverse()
        acoes.reverse()
        return estados, acoes


class LabirintoComColetas:
    """
    Adapta LabirintoBusca para busca com coletas obrigatórias.

    Estado = (posição, frozenset_coletas_restantes).
    O objetivo só é atingido quando o agente está em B e todas as coletas
    foram visitadas (frozenset vazio).
    """

    def __init__(self, lab: LabirintoBusca):
        self._lab = lab
        self.altura = lab.altura
        self.largura = lab.largura
        self.coletas = lab.coletas
        self._objetivo_pos = lab.objetivo
        self.inicio = (lab.inicio, frozenset(lab.coletas))
        self.objetivo = (lab.objetivo, frozenset())

    def vizinhos(self, estado):
        pos, coletas = estado
        resultado = []
        for acao, nova_pos, custo in self._lab.vizinhos(pos):
            novas_coletas = coletas - {nova_pos}
            resultado.append((acao, (nova_pos, novas_coletas), custo))
        return resultado

    def h(self, estado) -> float:
        """
        Heurística admissível: maior distância de Manhattan entre a posição atual
        e qualquer destino obrigatório restante (coletas + objetivo).
        Nunca superestima o custo real.
        """
        pos, coletas = estado
        destinos = coletas | {self._objetivo_pos}
        return max(abs(pos[0] - d[0]) + abs(pos[1] - d[1]) for d in destinos)

    def reconstruir(self, no: No):
        """Reconstrói caminho retornando apenas posições (sem o frozenset)."""
        estados = []
        acoes = []
        atual = no
        while atual.pai is not None:
            estados.append(atual.estado[0])
            acoes.append(atual.acao)
            atual = atual.pai
        estados.reverse()
        acoes.reverse()
        return estados, acoes