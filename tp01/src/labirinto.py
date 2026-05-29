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


@dataclass
class ResultadoBuscaOnline:
    algoritmo: str
    encontrado: bool
    movimentos_totais: int
    custo_real: float
    celulas_reveladas: int
    celulas_revisitadas: int
    replanejamentos: int
    custo_otimo_offline: float
    caminho_percorrido: List[Estado]
    tempo_ms: float = 0.0

    @property
    def razao_online_offline(self) -> Optional[float]:
        if self.custo_otimo_offline > 0 and self.encontrado:
            return round(self.custo_real / self.custo_otimo_offline, 3)
        return None


class LabirintoOnline:
    """
    Simula um agente em labirinto desconhecido.
    O mapa real é oculto; o agente constrói mapa interno via percepção.
    mapa interno: None=desconhecido, False=livre, True=parede.
    """

    def __init__(self, lab_real: 'LabirintoBusca', raio: int = 1):
        self._real = lab_real
        self.raio = raio
        self.altura = lab_real.altura
        self.largura = lab_real.largura
        self.inicio = lab_real.inicio
        self.objetivo = lab_real.objetivo
        self.mapa: List[List[Optional[bool]]] = [
            [None] * self.largura for _ in range(self.altura)
        ]
        r, c = self.inicio
        self.mapa[r][c] = False

    def perceber(self, pos: Estado):
        """Revela células dentro do raio (distância de Manhattan).
        Retorna (novos_livres, novas_paredes) como listas de Estado."""
        r, c = pos
        novos_livres: List[Estado] = []
        novas_paredes: List[Estado] = []
        for dr in range(-self.raio, self.raio + 1):
            for dc in range(-self.raio, self.raio + 1):
                if abs(dr) + abs(dc) <= self.raio:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.altura and 0 <= nc < self.largura:
                        if self.mapa[nr][nc] is None:
                            eh_parede = self._real.paredes[nr][nc]
                            self.mapa[nr][nc] = eh_parede
                            if eh_parede:
                                novas_paredes.append((nr, nc))
                            else:
                                novos_livres.append((nr, nc))
        return novos_livres, novas_paredes

    def mover(self, pos: Estado, acao: str) -> Optional[Estado]:
        """Move no mapa real. Retorna nova posição ou None se bloqueado."""
        r, c = pos
        d = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}[acao]
        nr, nc = r + d[0], c + d[1]
        if 0 <= nr < self.altura and 0 <= nc < self.largura and not self._real.paredes[nr][nc]:
            return (nr, nc)
        return None

    def vizinhos_livres_internos(self, pos: Estado):
        """Vizinhos que não são paredes conhecidas (livres ou desconhecidos)."""
        r, c = pos
        for acao, (nr, nc) in [('up', (r-1, c)), ('down', (r+1, c)),
                                ('left', (r, c-1)), ('right', (r, c+1))]:
            if 0 <= nr < self.altura and 0 <= nc < self.largura:
                if self.mapa[nr][nc] is not True:
                    yield acao, (nr, nc), 1.0

    def h_interna(self, pos: Estado) -> float:
        return abs(pos[0] - self.objetivo[0]) + abs(pos[1] - self.objetivo[1])


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