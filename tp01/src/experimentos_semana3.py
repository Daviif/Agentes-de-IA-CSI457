"""
Experimentos da Semana 3 — Busca Online no Labirinto Desconhecido.

Executa Replanning A* e Online DFS em múltiplos mapas e salva
resultados_semana3.csv com as métricas obrigatórias do enunciado.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from labirinto import LabirintoBusca, LabirintoOnline, LabirintoComColetas
from buscas.classicas.a_estrela import a_estrela
from buscas.online.replanning_a_estrela import replanning_a_estrela
from buscas.online.online_dfs import online_dfs

BASE = os.path.dirname(os.path.abspath(__file__))

MAPAS = [
    ('lab1', os.path.join(BASE, 'mapas', 'lab1.txt')),
    ('lab2', os.path.join(BASE, 'mapas', 'lab2.txt')),
    ('lab3', os.path.join(BASE, 'mapas', 'lab3.txt')),
    ('lab6', os.path.join(BASE, 'mapas', 'lab6.txt')),
]

ALGORITMOS = [
    ('Replanning A*', replanning_a_estrela),
    ('Online DFS',    online_dfs),
]

CABECALHO = [
    'mapa',
    'algoritmo',
    'sucesso',
    'movimentos_totais',
    'custo_real',
    'celulas_reveladas',
    'celulas_revisitadas',
    'replanejamentos',
    'custo_otimo_offline',
    'razao_online_offline',
    'tempo_ms',
]


def custo_otimo(lab: LabirintoBusca) -> float:
    problema = LabirintoComColetas(lab) if lab.coletas else lab
    res = a_estrela(problema)
    return res.custo_total if res.encontrado and res.custo_total else 0.0


def main():
    linhas = []

    fmt = '{:<16} {:<18} {:<8} {:<6} {:<8} {:<10} {:<12} {:<10} {:<8} {:<6}'
    print(fmt.format(
        'Mapa', 'Algoritmo', 'Sucesso', 'Mov.', 'Custo',
        'Reveladas', 'Revisitadas', 'Replan.', 'Ótimo', 'Razão'
    ))
    print('-' * 100)

    for nome_mapa, caminho in MAPAS:
        lab = LabirintoBusca(caminho)
        c_otimo = custo_otimo(lab)

        for nome_alg, func in ALGORITMOS:
            lab_online = LabirintoOnline(lab)
            res = func(lab_online)
            res.custo_otimo_offline = c_otimo

            razao = res.razao_online_offline
            razao_str = f'{razao:.3f}' if razao is not None else 'N/A'

            print(fmt.format(
                nome_mapa,
                nome_alg,
                str(res.encontrado),
                res.movimentos_totais,
                f'{res.custo_real:.0f}',
                res.celulas_reveladas,
                res.celulas_revisitadas,
                res.replanejamentos,
                f'{c_otimo:.0f}',
                razao_str,
            ))

            linhas.append({
                'mapa':                nome_mapa,
                'algoritmo':           nome_alg,
                'sucesso':             res.encontrado,
                'movimentos_totais':   res.movimentos_totais,
                'custo_real':          round(res.custo_real, 1),
                'celulas_reveladas':   res.celulas_reveladas,
                'celulas_revisitadas': res.celulas_revisitadas,
                'replanejamentos':     res.replanejamentos,
                'custo_otimo_offline': round(c_otimo, 1),
                'razao_online_offline': razao_str,
                'tempo_ms':            round(res.tempo_ms, 4),
            })

    saida = os.path.join(BASE, 'resultados_semana3.csv')
    with open(saida, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO)
        writer.writeheader()
        writer.writerows(linhas)

    print(f'\nResultados salvos em: {saida}')


if __name__ == '__main__':
    main()
