import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from labirinto import LabirintoBusca
from exibir import imprimir_labirinto
from buscas.classicas.bfs import bfs
from buscas.classicas.dfs import dfs
from buscas.classicas.ucs import ucs
from buscas.classicas.gulosa import gulosa
from buscas.classicas.a_estrela import a_estrela

BASE = os.path.dirname(os.path.abspath(__file__))

MAPAS = {
    'lab1': os.path.join(BASE, 'mapas', 'lab1.txt'),
    'lab2': os.path.join(BASE, 'mapas', 'lab2.txt'),
    'lab3': os.path.join(BASE, 'mapas', 'lab3.txt'),
}

ALGORITMOS = [
    ('BFS',    bfs),
    ('DFS',    dfs),
    ('UCS',    ucs),
    ('Gulosa', gulosa),
    ('A*',     a_estrela),
]

CABECALHO = ['mapa', 'algoritmo', 'sucesso', 'custo_total', 'tamanho_caminho',
             'nos_expandidos', 'nos_explorados', 'tempo_ms', 'fronteira_max']


def executar():
    resultados = []

    for nome_mapa, caminho_mapa in MAPAS.items():
        lab = LabirintoBusca(caminho_mapa)
        print(f'\n{"="*60}')
        print(f'Mapa: {nome_mapa}  ({lab.altura}L x {lab.largura}C)')
        print(f'Início: {lab.inicio}   Objetivo: {lab.objetivo}   Coletas: {lab.coletas}')
        print(f'{"="*60}')

        fmt = '{:<10} {:<8} {:<8} {:<8} {:<12} {:<12} {:<12} {:<10}'
        print(fmt.format('Algoritmo', 'Sucesso', 'Custo', 'Passos',
                         'Expandidos', 'Explorados', 'Tempo(ms)', 'Fronteira'))
        print('-' * 80)

        melhor = None
        for nome, func in ALGORITMOS:
            res = func(lab)
            print(fmt.format(
                nome,
                str(res.encontrado),
                f'{res.custo_total:.0f}',
                str(res.tamanho_caminho),
                res.nos_expandidos,
                res.nos_explorados,
                f'{res.tempo_ms:.4f}',
                res.fronteira_max,
            ))
            resultados.append({
                'mapa': nome_mapa,
                'algoritmo': nome,
                'sucesso': res.encontrado,
                'custo_total': res.custo_total,
                'tamanho_caminho': res.tamanho_caminho,
                'nos_expandidos': res.nos_expandidos,
                'nos_explorados': res.nos_explorados,
                'tempo_ms': round(res.tempo_ms, 4),
                'fronteira_max': res.fronteira_max,
            })
            if nome == 'A*' and res.encontrado:
                melhor = res

        if melhor:
            imprimir_labirinto(lab, resultado=melhor, mostrar_explorados=False)

    saida = os.path.join(BASE, 'resultados_semana1.csv')
    with open(saida, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO)
        writer.writeheader()
        writer.writerows(resultados)
    print(f'\nResultados salvos em: {saida}')


if __name__ == '__main__':
    executar()
