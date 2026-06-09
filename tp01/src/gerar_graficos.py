"""
Gera todos os gráficos de desempenho do TP01.

Saída: pasta graficos/ com os arquivos PNG abaixo:
  classica_nos_expandidos.png   — nós expandidos por algoritmo/mapa
  classica_custo_caminho.png    — custo do caminho por algoritmo/mapa
  classica_tempo.png            — tempo de execução por algoritmo/mapa
  local_convergencia_lab_2_coletas.png      — curva de convergência HC vs SA (lab2)
  local_convergencia_lab_6_busca_local.png  — curva de convergência HC vs SA (lab6)
  local_convergencia_lab_7_7_coletas.png    — curva de convergência HC vs SA (lab7)
  local_comparacao.png                      — melhor/médio/pior custo HC vs SA vs AG
  online_razao.png                          — razão online/offline por mapa e estratégia
  online_movimentos_revisitadas.png         — movimentos totais e células revisitadas
"""

import os
import sys
import csv
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from labirinto import LabirintoBusca, LabirintoOnline
from buscas.local.distancias import calcular_distancias
from buscas.local.hill_climbing import hill_climbing
from buscas.local.simulated_annealing import simulated_annealing
from buscas.local.genetic_algorithm import genetic_algorithm
from buscas.online.replanning_a_estrela import replanning_a_estrela
from buscas.online.online_dfs import online_dfs
from buscas.classicas.a_estrela import a_estrela

BASE    = os.path.dirname(os.path.abspath(__file__))
GRAFICOS = os.path.join(BASE, '..', 'graficos')
os.makedirs(GRAFICOS, exist_ok=True)

MAPAS_DIR = os.path.join(BASE, 'mapas')

CORES = {
    'BFS':    '#2196F3',
    'DFS':    '#F44336',
    'UCS':    '#4CAF50',
    'Gulosa': '#FF9800',
    'A*':     '#9C27B0',
}

CORES_LOCAL = {
    'Hill-Climbing':      '#E53935',
    'Simulated Annealing': '#1E88E5',
    'Algoritmo Genético': '#43A047',
}

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _salvar(fig, nome: str):
    path = os.path.join(GRAFICOS, nome)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Salvo: {path}')


def _ler_csv(nome: str):
    path = os.path.join(BASE, nome)
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


# ─────────────────────────────────────────────────────────────────────────────
# 1. Gráficos de Busca Clássica
# ─────────────────────────────────────────────────────────────────────────────

def graficos_classica():
    print('\n[1/3] Gráficos de busca clássica...')
    rows = _ler_csv('resultados_semana1.csv')
    mapas      = sorted(set(r['mapa'] for r in rows))
    algoritmos = ['BFS', 'DFS', 'UCS', 'Gulosa', 'A*']
    x = np.arange(len(mapas))
    w = 0.15

    # — Nós expandidos —
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, alg in enumerate(algoritmos):
        vals = [
            float(next(r['nos_expandidos'] for r in rows if r['mapa']==m and r['algoritmo']==alg))
            for m in mapas
        ]
        ax.bar(x + i*w, vals, w, label=alg, color=CORES[alg])
    ax.set_xticks(x + w*2)
    ax.set_xticklabels(mapas)
    ax.set_ylabel('Nós Expandidos')
    ax.set_title('Busca Clássica — Nós Expandidos por Algoritmo e Mapa')
    ax.legend()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'{int(v):,}'))
    _salvar(fig, 'classica_nos_expandidos.png')

    # — Custo do caminho —
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, alg in enumerate(algoritmos):
        vals = [
            float(next(r['custo_total'] for r in rows if r['mapa']==m and r['algoritmo']==alg))
            for m in mapas
        ]
        ax.bar(x + i*w, vals, w, label=alg, color=CORES[alg])
    ax.set_xticks(x + w*2)
    ax.set_xticklabels(mapas)
    ax.set_ylabel('Custo do Caminho')
    ax.set_title('Busca Clássica — Custo do Caminho por Algoritmo e Mapa')
    ax.legend()
    _salvar(fig, 'classica_custo_caminho.png')

    # — Tempo de execução —
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, alg in enumerate(algoritmos):
        vals = [
            float(next(r['tempo_ms'] for r in rows if r['mapa']==m and r['algoritmo']==alg))
            for m in mapas
        ]
        ax.bar(x + i*w, vals, w, label=alg, color=CORES[alg])
    ax.set_xticks(x + w*2)
    ax.set_xticklabels(mapas)
    ax.set_ylabel('Tempo (ms)')
    ax.set_title('Busca Clássica — Tempo de Execução por Algoritmo e Mapa')
    ax.legend()
    _salvar(fig, 'classica_tempo.png')


# ─────────────────────────────────────────────────────────────────────────────
# 2. Gráficos de Busca Local — convergência + comparação
# ─────────────────────────────────────────────────────────────────────────────

_MAPAS_LOCAL = {
    'Lab 2 — coletas':    os.path.join(MAPAS_DIR, 'lab2.txt'),
    'Lab 6 — busca local': os.path.join(MAPAS_DIR, 'lab6.txt'),
    'Lab 7 — 7 coletas':  os.path.join(MAPAS_DIR, 'lab7.txt'),
}

def _nome_arquivo(label: str) -> str:
    return label.lower().replace(' ', '_').replace('—', '').replace('__', '_').strip('_')


def graficos_local():
    print('\n[2/3] Gráficos de busca local...')
    rows = _ler_csv('resultados_semana2.csv')

    # — Curvas de convergência por mapa —
    for label, caminho in _MAPAS_LOCAL.items():
        lab  = LabirintoBusca(caminho)
        dist = calcular_distancias(lab)

        res_hc = hill_climbing(lab, dist, n_execucoes=30, semente=42)
        res_sa = simulated_annealing(lab, dist, n_execucoes=20, semente=42)

        fig, ax = plt.subplots(figsize=(10, 5))

        # HC: poucos pontos (iterações são melhoras)
        ax.plot(range(len(res_hc.convergencia)), res_hc.convergencia,
                color=CORES_LOCAL['Hill-Climbing'], lw=2,
                marker='o', markersize=4, label='Hill-Climbing')

        # SA: muitos pontos — reamostrar a cada 50 para legibilidade
        conv_sa = res_sa.convergencia
        step = max(1, len(conv_sa) // 200)
        xs   = list(range(0, len(conv_sa), step))
        ys   = [conv_sa[i] for i in xs]
        ax.plot(xs, ys, color=CORES_LOCAL['Simulated Annealing'], lw=2,
                label='Simulated Annealing')

        # Linha do ótimo
        c_otimo = res_hc.custo_otimo if math.isfinite(res_hc.custo_otimo) else None
        if c_otimo:
            ax.axhline(c_otimo, color='gray', lw=1.2, ls='--', label=f'Ótimo ({c_otimo:.0f})')

        ax.set_xlabel('Iteração')
        ax.set_ylabel('Melhor Custo')
        ax.set_title(f'Convergência — {label}')
        ax.legend()
        _salvar(fig, f'local_convergencia_{_nome_arquivo(label)}.png')

    # — Comparação melhor/médio/pior por algoritmo e mapa —
    algoritmos = ['Hill-Climbing', 'Simulated Annealing', 'Algoritmo Genético']
    mapas      = sorted(set(r['mapa'] for r in rows))
    x = np.arange(len(mapas))
    w = 0.22

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=False)
    metricas = [
        ('melhor_custo', 'Melhor Custo'),
        ('custo_medio',  'Custo Médio'),
        ('pior_custo',   'Pior Custo'),
    ]

    for ax, (col, titulo) in zip(axes, metricas):
        for i, alg in enumerate(algoritmos):
            vals = []
            for m in mapas:
                match = next((r for r in rows if r['mapa']==m and r['algoritmo']==alg), None)
                vals.append(float(match[col]) if match else 0)
            bars = ax.bar(x + i*w, vals, w, label=alg, color=CORES_LOCAL[alg])
            for bar, v in zip(bars, vals):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        f'{v:.0f}', ha='center', va='bottom', fontsize=7)
        ax.set_xticks(x + w)
        ax.set_xticklabels([m.split('—')[-1].strip() for m in mapas], fontsize=8)
        ax.set_ylabel('Custo')
        ax.set_title(titulo)
        ax.legend(fontsize=8)

    fig.suptitle('Busca Local — Comparação de Custos por Algoritmo e Mapa', fontsize=13)
    plt.tight_layout()
    _salvar(fig, 'local_comparacao.png')


# ─────────────────────────────────────────────────────────────────────────────
# 3. Gráficos de Busca Online — razão online/offline
# ─────────────────────────────────────────────────────────────────────────────

_MAPAS_ONLINE = {
    'lab1': os.path.join(MAPAS_DIR, 'lab1.txt'),
    'lab3': os.path.join(MAPAS_DIR, 'lab3.txt'),
    'lab6': os.path.join(MAPAS_DIR, 'lab6.txt'),
}

def _custo_otimo(lab: LabirintoBusca) -> float:
    from labirinto import LabirintoComColetas
    problema = LabirintoComColetas(lab) if lab.coletas else lab
    res = a_estrela(problema)
    return res.custo_total if res.custo_total else math.inf


def graficos_online():
    print('\n[3/3] Gráficos de busca online...')
    estrategias = ['Replanning A*', 'Online DFS']
    mapas       = list(_MAPAS_ONLINE.keys())

    razoes      = {e: [] for e in estrategias}
    movimentos  = {e: [] for e in estrategias}
    revisitadas = {e: [] for e in estrategias}

    for nome, caminho in _MAPAS_ONLINE.items():
        lab_real  = LabirintoBusca(caminho)
        c_otimo   = _custo_otimo(lab_real)

        # Replanning A*
        lab_on = LabirintoOnline(lab_real)
        res    = replanning_a_estrela(lab_on)
        res.custo_otimo_offline = c_otimo
        razoes['Replanning A*'].append(res.razao_online_offline or 0)
        movimentos['Replanning A*'].append(res.movimentos_totais)
        revisitadas['Replanning A*'].append(res.celulas_revisitadas)

        # Online DFS
        lab_on2 = LabirintoOnline(lab_real)
        res2    = online_dfs(lab_on2)
        res2.custo_otimo_offline = c_otimo
        razoes['Online DFS'].append(res2.razao_online_offline or 0)
        movimentos['Online DFS'].append(res2.movimentos_totais)
        revisitadas['Online DFS'].append(res2.celulas_revisitadas)

    x = np.arange(len(mapas))
    w = 0.35
    cores_on = {'Replanning A*': '#1565C0', 'Online DFS': '#B71C1C'}

    # — Razão online/offline —
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, est in enumerate(estrategias):
        bars = ax.bar(x + i*w, razoes[est], w, label=est, color=cores_on[est])
        for bar, v in zip(bars, razoes[est]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{v:.2f}', ha='center', va='bottom', fontsize=9)
    ax.axhline(1.0, color='green', lw=1.5, ls='--', label='Razão ideal (1.0)')
    ax.set_xticks(x + w/2)
    ax.set_xticklabels(mapas)
    ax.set_ylabel('Razão Online / Offline')
    ax.set_title('Busca Online — Razão Custo Online vs. Ótimo Offline')
    ax.legend()
    _salvar(fig, 'online_razao.png')

    # — Movimentos totais e células revisitadas —
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    for i, est in enumerate(estrategias):
        ax1.bar(x + i*w, movimentos[est], w, label=est, color=cores_on[est])
        ax2.bar(x + i*w, revisitadas[est], w, label=est, color=cores_on[est])

    for ax, titulo, ylabel in [
        (ax1, 'Movimentos Totais', 'Movimentos'),
        (ax2, 'Células Revisitadas', 'Células'),
    ]:
        ax.set_xticks(x + w/2)
        ax.set_xticklabels(mapas)
        ax.set_ylabel(ylabel)
        ax.set_title(f'Busca Online — {titulo}')
        ax.legend()

    plt.tight_layout()
    _salvar(fig, 'online_movimentos_revisitadas.png')


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Gerando gráficos de desempenho do TP01...')
    graficos_classica()
    graficos_local()
    graficos_online()
    print(f'\nTodos os gráficos salvos em: {os.path.abspath(GRAFICOS)}')
