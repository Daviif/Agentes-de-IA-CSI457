from labirinto import LabirintoBusca, ResultadoBusca
from typing import Optional


def _pos(estado):
    """Extrai (row, col) de estado simples ou estendido ((row,col), frozenset)."""
    return estado[0] if isinstance(estado[0], tuple) else estado


def imprimir_labirinto(lab: LabirintoBusca, resultado: Optional[ResultadoBusca] = None, mostrar_explorados: bool = True):
    caminho = {_pos(e) for e in resultado.caminho} if resultado and resultado.encontrado else set()
    explorados = {_pos(e) for e in resultado.estados_explorados} if resultado and mostrar_explorados else set()

    inicio_pos = _pos(lab.inicio)
    objetivo_pos = _pos(lab.objetivo)

    print()
    for i in range(lab.altura):
        for j in range(lab.largura):
            estado = (i, j)
            if lab.paredes[i][j]:
                print('█', end='')
            elif estado == inicio_pos:
                print('A', end='')
            elif estado == objetivo_pos:
                print('B', end='')
            elif estado in lab.coletas:
                print('C', end='')
            elif estado in caminho:
                print('*', end='')
            elif estado in explorados:
                print('.', end='')
            else:
                print(' ', end='')
        print()
    print()


def imprimir_metricas(resultado: ResultadoBusca):
    print(f'Algoritmo: {resultado.algoritmo}')
    print(f'Sucesso: {"sim" if resultado.encontrado else "não"}')
    print(f'Custo total: {resultado.custo_total}')
    print(f'Nós explorados: {resultado.nos_explorados}')
    print(f'Nós expandidos: {resultado.nos_expandidos}')
    print(f'Tamanho do caminho: {resultado.tamanho_caminho}')
    print(f'Tempo (ms): {resultado.tempo_ms:.4f}')
    print(f'Fronteira máx.: {resultado.fronteira_max}')
