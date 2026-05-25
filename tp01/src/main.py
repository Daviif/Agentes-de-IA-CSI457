import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from labirinto import LabirintoBusca, LabirintoComColetas, Labirinto
from exibir import imprimir_labirinto
from buscas.classicas.bfs import bfs
from buscas.classicas.dfs import dfs
from buscas.classicas.ucs import ucs
from buscas.classicas.gulosa import gulosa
from buscas.classicas.a_estrela import a_estrela

BASE = os.path.dirname(os.path.abspath(__file__))

MAPAS_PRONTOS = {
    '1': os.path.join(BASE, 'mapas', 'lab1.txt'),
    '2': os.path.join(BASE, 'mapas', 'lab2.txt'),
    '3': os.path.join(BASE, 'mapas', 'lab3.txt'),
    '4': os.path.join(BASE, 'mapas', 'lab4.txt'),
}

ALGORITMOS_CLASSICOS = [
    ('BFS',    bfs),
    ('DFS',    dfs),
    ('UCS',    ucs),
    ('Gulosa', gulosa),
    ('A*',     a_estrela),
]


def escolher_mapa() -> str:
    print('\nEscolha o labirinto:')
    print('  1 - lab1 (simples, sem coletas)')
    print('  2 - lab2 (com pontos de coleta)')
    print('  3 - lab3 (serpentino, maior)')
    print('  4 - lab4 (muito complexo, para teste de performance)')
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


def main():
    caminho = escolher_mapa()
    lab = LabirintoBusca(caminho)
    nome_arquivo = os.path.basename(caminho)

    print('\nLabirinto carregado:')
    imprimir_labirinto(lab)

    print('\nTipo de busca:')
    print('  1 - Busca Clássica (BFS, DFS, UCS, Gulosa, A*)')
    print('  2 - Busca Local    (em breve)')
    print('  3 - Busca Online   (em breve)')
    tipo = input('Opção: ').strip()

    if tipo == '1':
        busca_classica(lab, nome_arquivo)
    elif tipo == '2':
        print('\nBusca Local ainda não implementada (Semana 2).')
    elif tipo == '3':
        print('\nBusca Online ainda não implementada (Semana 3).')
    else:
        print('Opção inválida.')


if __name__ == '__main__':
    main()
