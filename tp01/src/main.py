import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from labirinto import LabirintoBusca, LabirintoComColetas, LabirintoOnline, Labirinto
from exibir import imprimir_labirinto
from buscas.classicas.bfs import bfs
from buscas.classicas.dfs import dfs
from buscas.classicas.ucs import ucs
from buscas.classicas.gulosa import gulosa
from buscas.classicas.a_estrela import a_estrela
from buscas.online.replanning_a_estrela import replanning_a_estrela
from buscas.online.online_dfs import online_dfs
from buscas.local.distancias import calcular_distancias, custo_solucao
from buscas.local.hill_climbing import hill_climbing
from buscas.local.simulated_annealing import simulated_annealing
from buscas.local.genetic_algorithm import genetic_algorithm
from buscas.local.resultado_local import _exibir_resultado_local

BASE = os.path.dirname(os.path.abspath(__file__))

MAPAS_PRONTOS = {
    '1': os.path.join(BASE, 'mapas', 'lab1.txt'),
    '2': os.path.join(BASE, 'mapas', 'lab2.txt'),
    '3': os.path.join(BASE, 'mapas', 'lab3.txt'),
    '4': os.path.join(BASE, 'mapas', 'lab4.txt'),
    '6': os.path.join(BASE, 'mapas', 'lab6.txt'),
    '7': os.path.join(BASE, 'mapas', 'lab7.txt'),
}

ALGORITMOS_CLASSICOS = [
    ('BFS',    bfs),
    ('DFS',    dfs),
    ('UCS',    ucs),
    ('Gulosa', gulosa),
    ('A*',     a_estrela),
]

ALGORITMOS_ONLINE = [
    ('Replanning A*', replanning_a_estrela),
    ('Online DFS',    online_dfs),
]


def escolher_mapa() -> str:
    print('\nEscolha o labirinto:')
    print('  1 - lab1 (simples, sem coletas)')
    print('  2 - lab2 (com pontos de coleta)')
    print('  3 - lab3 (serpentino, maior)')
    print('  4 - lab4 (muito complexo, para teste de performance)')
    print('  5 - lab5 (teste de performance)')
    print('  6 - lab6 ')
    print('  7 - lab7 ')
    print('  0 - Inserir caminho manualmente')
    opcao = input('Opção: ').strip()
    if opcao in MAPAS_PRONTOS:
        return MAPAS_PRONTOS[opcao]
    if opcao == '0':
        caminho = input('Caminho do arquivo .txt: ').strip()
        return os.path.expanduser(caminho)
    print('Opção inválida, usando lab1.')
    return MAPAS_PRONTOS['1']


def busca_classica(lab: LabirintoBusca, nome_arquivo: str = 'labirinto'):
    lab_problema: Labirinto = LabirintoComColetas(lab) if lab.coletas else lab

    print(f'\n{"="*60}')
    print(f'Mapa: {nome_arquivo}  ({lab.altura}L x {lab.largura}C)')
    print(f'Início: {lab.inicio}   Objetivo: {lab.objetivo}   Coletas: {lab.coletas}')
    print(f'{"="*60}')

    fmt = '{:<10} {:<8} {:<8} {:<8} {:<12} {:<12} {:<12} {:<10}'
    print(fmt.format('Algoritmo', 'Sucesso', 'Custo', 'Passos',
                     'Expandidos', 'Explorados', 'Tempo(ms)', 'Fronteira'))
    print('-' * 80)

    resultados = []
    for nome, func in ALGORITMOS_CLASSICOS:
        res = func(lab_problema)
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
        resultados.append((nome, res))

    for nome, res in resultados:
        print(f'\nSolução {nome} (custo={res.custo_total:.0f}):')
        imprimir_labirinto(lab, resultado=res, mostrar_explorados=True)


def busca_online(lab: LabirintoBusca, nome_arquivo: str = 'labirinto'):
    lab_problema: Labirinto = LabirintoComColetas(lab) if lab.coletas else lab
    res_offline = a_estrela(lab_problema)
    custo_otimo = res_offline.custo_total if res_offline.encontrado else 0.0

    print(f'\n{"="*60}')
    print(f'Mapa: {nome_arquivo}  ({lab.altura}L x {lab.largura}C)')
    print(f'Início: {lab.inicio}   Objetivo: {lab.objetivo}')
    print(f'Custo ótimo offline (A*): {custo_otimo:.0f}')
    print(f'{"="*60}')

    fmt = '{:<16} {:<8} {:<8} {:<10} {:<10} {:<12} {:<12} {:<8}'
    print(fmt.format('Algoritmo', 'Sucesso', 'Mov.', 'Custo', 'Reveladas',
                     'Revisitadas', 'Tempo(ms)', 'Razão'))
    print('-' * 90)

    for nome, func in ALGORITMOS_ONLINE:
        lab_online = LabirintoOnline(lab)
        res = func(lab_online)
        res.custo_otimo_offline = custo_otimo
        razao = f'{res.razao_online_offline:.3f}' if res.razao_online_offline else 'N/A'
        print(fmt.format(
            nome,
            str(res.encontrado),
            res.movimentos_totais,
            f'{res.custo_real:.0f}',
            res.celulas_reveladas,
            res.celulas_revisitadas,
            f'{res.tempo_ms:.4f}',
            razao,
        ))

    print(f'\n  Razão online/offline = custo percorrido / custo ótimo offline')
    print(f'  Razão = 1.0 → agente igualou o desempenho offline')
    print(f'  Razão > 1.0 → custo extra por desconhecer o ambiente')


def busca_local(lab: LabirintoBusca, nome_arquivo: str = 'labirinto'):
    if len(lab.coletas) < 2:
        print('\nBusca local requer ≥2 pontos de coleta para otimizar a ordem de visitação.')
        print('Use um mapa com pelo menos 2 marcadores C (ex: lab2).')
        return

    print(f'\n{"="*60}')
    print(f'Mapa: {nome_arquivo}  ({lab.altura}L x {lab.largura}C)')
    print(f'Início: {lab.inicio}   Objetivo: {lab.objetivo}')
    print(f'Coletas ({len(lab.coletas)}): {lab.coletas}')
    print(f'{"="*60}')

    print('\nPré-computando distâncias (A*)...', end='', flush=True)
    dist = calcular_distancias(lab)
    print(' OK')

    res_hc = hill_climbing(lab, dist=dist, n_execucoes=30, semente=42)
    res_sa = simulated_annealing(lab, dist=dist, n_execucoes=20, semente=42)
    res_ga = genetic_algorithm(lab, dist=dist, n_geracoes=200, semente=42)

    _exibir_resultado_local(res_hc, lab, dist)
    _exibir_resultado_local(res_sa, lab, dist)
    _exibir_resultado_local(res_ga, lab, dist)


def main():
    caminho = escolher_mapa()
    lab = LabirintoBusca(caminho)
    nome_arquivo = os.path.basename(caminho)

    print('\nLabirinto carregado:')
    imprimir_labirinto(lab)

    print('\nTipo de busca:')
    print('  1 - Busca Clássica (BFS, DFS, UCS, Gulosa, A*)')
    print('  2 - Busca Local    (Hill-Climbing, Simulated Annealing, Algoritmo Genético)')
    print('  3 - Busca Online   (Replanning A*, Online DFS)')
    tipo = input('Opção: ').strip()

    if tipo == '1':
        busca_classica(lab, nome_arquivo)
    elif tipo == '2':
        busca_local(lab, nome_arquivo)
    elif tipo == '3':
        busca_online(lab, nome_arquivo)
    else:
        print('Opção inválida.')


if __name__ == '__main__':
    main()
