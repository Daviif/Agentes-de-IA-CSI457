#!/usr/bin/env python3
"""Gera visualizacao.html — animação web dos algoritmos de busca (clássica + local + online)."""

import sys, os, json, math, heapq, itertools, time, random, csv
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labirinto import LabirintoBusca, LabirintoComColetas, LabirintoOnline, No
from buscas.classicas.bfs       import bfs
from buscas.classicas.dfs       import dfs
from buscas.classicas.ucs       import ucs
from buscas.classicas.gulosa    import gulosa
from buscas.classicas.a_estrela import a_estrela
from buscas.local.distancias    import calcular_distancias, custo_solucao

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, 'visualizacao.html')

MAPAS = {
    '1': (os.path.join(BASE, 'mapas', 'lab1.txt'), 'Lab 1 — simples'),
    '2': (os.path.join(BASE, 'mapas', 'lab2.txt'), 'Lab 2 — coletas'),
    '3': (os.path.join(BASE, 'mapas', 'lab3.txt'), 'Lab 3 — serpentino'),
    '4': (os.path.join(BASE, 'mapas', 'lab4.txt'), 'Lab 4 — complexo'),
    '5': (os.path.join(BASE, 'mapas', 'lab5.txt'), 'Lab 5 — sem coleta'),
    '6': (os.path.join(BASE, 'mapas', 'lab6.txt'), 'Lab 6 — busca local'),
    '7': (os.path.join(BASE, 'mapas', 'lab7.txt'), 'Lab 7 — 7 coletas'),
}

CLASSICOS = [('BFS', bfs), ('DFS', dfs), ('UCS', ucs), ('Gulosa', gulosa), ('A*', a_estrela)]


# ── Geradores de frames (busca clássica, delta encoding) ──────────────────────

# ──────────────────────────────────────────────────────────────
# Geradores para busca clássica (existentes)
# ──────────────────────────────────────────────────────────────

def _pos(estado):
    return list(estado[0]) if isinstance(estado[0], tuple) else list(estado)


def bfs_gen(lab):
    inicio = No(lab.inicio)
    fronteira = deque([inicio])
    em_fronteira = {lab.inicio}
    explorados = set()
    while fronteira:
        yield [_pos(e) for e in explorados], [_pos(n.estado) for n in fronteira], None
        no = fronteira.popleft()
        em_fronteira.discard(no.estado)
        if no.estado == lab.objetivo:
            caminho, _ = lab.reconstruir(no)
            yield [_pos(e) for e in explorados], [], [_pos(p) for p in caminho]
            return
        explorados.add(no.estado)
        for acao, estado, custo in lab.vizinhos(no.estado):
            if estado not in explorados and estado not in em_fronteira:
                fronteira.append(No(estado=estado, pai=no, acao=acao, g=no.g + custo))
                em_fronteira.add(estado)
    yield [_pos(e) for e in explorados], [], None


def dfs_gen(lab):
    inicio = No(lab.inicio)
    fronteira = [inicio]
    em_fronteira = {lab.inicio}
    explorados = set()
    while fronteira:
        yield [_pos(e) for e in explorados], [_pos(n.estado) for n in fronteira], None
        no = fronteira.pop()
        em_fronteira.discard(no.estado)
        if no.estado == lab.objetivo:
            caminho, _ = lab.reconstruir(no)
            yield [_pos(e) for e in explorados], [], [_pos(p) for p in caminho]
            return
        explorados.add(no.estado)
        for acao, estado, custo in lab.vizinhos(no.estado):
            if estado not in explorados and estado not in em_fronteira:
                fronteira.append(No(estado=estado, pai=no, acao=acao, g=no.g + custo))
                em_fronteira.add(estado)
    yield [_pos(e) for e in explorados], [], None


def _prio_gen(lab, fn_prio):
    contador = itertools.count()
    inicio = No(lab.inicio, g=0.0)
    fila = [(fn_prio(inicio), next(contador), inicio)]
    melhor_g = {lab.inicio: 0.0}
    fechados = set()
    while fila:
        yield [_pos(e) for e in fechados], [_pos(item[2].estado) for item in fila], None
        _, _, no = heapq.heappop(fila)
        if no.estado in fechados:
            continue
        fechados.add(no.estado)
        if no.estado == lab.objetivo:
            caminho, _ = lab.reconstruir(no)
            yield [_pos(e) for e in fechados], [], [_pos(p) for p in caminho]
            return
        for acao, estado, custo in lab.vizinhos(no.estado):
            novo_g = no.g + custo
            if estado in fechados:
                continue
            if novo_g < melhor_g.get(estado, math.inf):
                filho = No(estado=estado, pai=no, acao=acao, g=novo_g)
                melhor_g[estado] = novo_g
                heapq.heappush(fila, (fn_prio(filho), next(contador), filho))
    yield [_pos(e) for e in fechados], [], None


def ucs_gen(lab):       return _prio_gen(lab, lambda n: n.g)
def gulosa_gen(lab):    return _prio_gen(lab, lambda n: lab.h(n.estado))
def a_estrela_gen(lab): return _prio_gen(lab, lambda n: n.g + lab.h(n.estado))


def run_gen(gen):
    """Coleta frames com delta encoding e mede o tempo total."""
    t0 = time.perf_counter()
    prev_e: frozenset = frozenset()
    prev_f: frozenset = frozenset()
    out = []
    for e, f, p in gen:
        curr_e = frozenset(tuple(x) for x in e)
        curr_f = frozenset(tuple(x) for x in f)
        out.append({
            'ea': [list(x) for x in curr_e - prev_e],
            'fa': [list(x) for x in curr_f - prev_f],
            'fr': [list(x) for x in prev_f - curr_f],
            'p':  p,
        })
        prev_e = curr_e
        prev_f = curr_f
    return {'frames': out, 't': round((time.perf_counter() - t0) * 1000, 2)}


# ──────────────────────────────────────────────────────────────
# Geradores para busca online
# ──────────────────────────────────────────────────────────────

_INVERSA = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
_DELTA   = {'up': (-1,0), 'down': (1,0), 'left': (0,-1), 'right': (0,1)}


def _a_estrela_interno(lab: LabirintoOnline, inicio):
    """A* otimista no mapa interno. Retorna lista de posições ou None."""
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


def _acao_para(pos, prox):
    dr, dc = prox[0]-pos[0], prox[1]-pos[1]
    return {(-1,0):'up',(1,0):'down',(0,-1):'left',(0,1):'right'}[(dr,dc)]


def online_replanning_gen(lab_real: LabirintoBusca, stats: dict):
    """
    Gerador passo-a-passo do Replanning A*.
    Yields (pos, novos_livres, novas_paredes) a cada movimento.
    Preenche `stats` ao final.
    """
    lab = LabirintoOnline(lab_real)
    pos = lab.inicio
    new_free, new_walls = lab.perceber(pos)
    yield list(pos), [list(p) for p in new_free], [list(p) for p in new_walls]

    caminho = [pos]
    visitadas = {pos}
    movimentos = 0
    revisitadas = 0
    replanejamentos = 0
    limite = lab.altura * lab.largura * 4
    plano = None
    plano_idx = 0

    for _ in range(limite):
        if pos == lab.objetivo:
            break

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
            lab.mapa[prox[0]][prox[1]] = True
            plano = None
            yield list(pos), [], [list(prox)]
            continue

        pos = nova
        plano_idx += 1
        movimentos += 1
        if pos in visitadas:
            revisitadas += 1
        visitadas.add(pos)
        caminho.append(pos)
        new_free, new_walls = lab.perceber(pos)
        yield list(pos), [list(p) for p in new_free], [list(p) for p in new_walls]

    stats['encontrado'] = pos == lab.objetivo
    stats['movimentos'] = movimentos
    stats['revisitadas'] = revisitadas
    stats['replanejamentos'] = replanejamentos
    stats['reveladas'] = sum(
        1 for r in range(lab.altura) for c in range(lab.largura)
        if lab.mapa[r][c] is not None
    )


def online_dfs_gen(lab_real: LabirintoBusca, stats: dict):
    """
    Gerador passo-a-passo do Online DFS.
    Yields (pos, novos_livres, novas_paredes) a cada movimento.
    Preenche `stats` ao final.
    """
    lab = LabirintoOnline(lab_real)
    pos = lab.inicio
    new_free, new_walls = lab.perceber(pos)
    yield list(pos), [list(p) for p in new_free], [list(p) for p in new_walls]

    nao_tentadas = {}
    pilha = []
    visitadas = {pos}
    movimentos = 0
    revisitadas = 0
    limite = lab.altura * lab.largura * 4

    def _acoes(p):
        return [a for a, _, _ in lab.vizinhos_livres_internos(p)]

    for _ in range(limite):
        if pos == lab.objetivo:
            break

        if pos not in nao_tentadas:
            nao_tentadas[pos] = _acoes(pos)

        moveu = False
        while nao_tentadas[pos]:
            acao = nao_tentadas[pos].pop(0)
            nova = lab.mover(pos, acao)
            if nova is None:
                dr, dc = _DELTA[acao]
                r2, c2 = pos[0]+dr, pos[1]+dc
                if 0 <= r2 < lab.altura and 0 <= c2 < lab.largura:
                    lab.mapa[r2][c2] = True
                    yield list(pos), [], [[r2, c2]]
                continue

            pilha.append((pos, _INVERSA[acao]))
            pos = nova
            movimentos += 1
            if pos in visitadas:
                revisitadas += 1
            visitadas.add(pos)
            new_free, new_walls = lab.perceber(pos)
            if pos not in nao_tentadas:
                nao_tentadas[pos] = _acoes(pos)
            yield list(pos), [list(p) for p in new_free], [list(p) for p in new_walls]
            moveu = True
            break

        if not moveu:
            if not pilha:
                break
            _, back_acao = pilha.pop()
            nova = lab.mover(pos, back_acao)
            if nova is None:
                break
            pos = nova
            movimentos += 1
            revisitadas += 1
            new_free, new_walls = lab.perceber(pos)
            yield list(pos), [list(p) for p in new_free], [list(p) for p in new_walls]

    stats['encontrado'] = pos == lab.objetivo
    stats['movimentos'] = movimentos
    stats['revisitadas'] = revisitadas
    stats['replanejamentos'] = 0
    stats['reveladas'] = sum(
        1 for r in range(lab.altura) for c in range(lab.largura)
        if lab.mapa[r][c] is not None
    )


def run_online_gen(gen_func, lab_real):
    """Executa gerador online e coleta frames + estatísticas."""
    t0 = time.perf_counter()
    stats = {}
    frames = []
    for pos, new_free, new_walls in gen_func(lab_real, stats):
        frames.append({'pos': pos, 'rf': new_free, 'rw': new_walls})
    elapsed = round((time.perf_counter() - t0) * 1000, 2)
    return {'frames': frames, 't': elapsed, **stats}


def _custo_offline(lab_real: LabirintoBusca) -> float:
    """A* offline para obter custo ótimo de referência."""
    lab_p = LabirintoComColetas(lab_real) if lab_real.coletas else lab_real
    contador = itertools.count()
    inicio = No(lab_p.inicio, g=0.0)
    h0 = lab_p.h(lab_p.inicio)
    fronteira = [(h0, next(contador), inicio)]
    melhor_g = {lab_p.inicio: 0.0}
    fechados = set()
    while fronteira:
        _, _, no = heapq.heappop(fronteira)
        if no.estado in fechados:
            continue
        if no.estado == lab_p.objetivo:
            return no.g
        fechados.add(no.estado)
        for acao, estado, custo in lab_p.vizinhos(no.estado):
            novo_g = no.g + custo
            if estado not in fechados and novo_g < melhor_g.get(estado, math.inf):
                filho = No(estado=estado, pai=no, acao=acao, g=novo_g)
                melhor_g[estado] = novo_g
                h = lab_p.h(estado)
                heapq.heappush(fronteira, (novo_g + h, next(contador), filho))
    return 0.0


# ──────────────────────────────────────────────────────────────
# Geradores de frames (busca local)
# ──────────────────────────────────────────────────────────────

def _a_estrela_caminho(lab: LabirintoBusca, origem: tuple, destino: tuple) -> list:
    """Menor caminho entre dois pontos (retorna lista de células)."""
    if origem == destino:
        return [origem]
    def h(p): return abs(p[0]-destino[0]) + abs(p[1]-destino[1])
    cnt = itertools.count()
    fila = [(h(origem), next(cnt), origem, 0.0)]
    melhor_g: dict = {origem: 0.0}
    parent: dict   = {origem: None}
    fechados: set  = set()
    while fila:
        _, _, pos, g = heapq.heappop(fila)
        if pos in fechados: continue
        if pos == destino:
            path = []
            cur = pos
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return list(reversed(path))
        fechados.add(pos)
        for di, dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni, nj = pos[0]+di, pos[1]+dj
            np_ = (ni, nj)
            if 0<=ni<lab.altura and 0<=nj<lab.largura and not lab.paredes[ni][nj]:
                ng = g + 1.0
                if np_ not in fechados and ng < melhor_g.get(np_, math.inf):
                    melhor_g[np_] = ng
                    parent[np_] = pos
                    heapq.heappush(fila, (ng+h(np_), next(cnt), np_, ng))
    return []


def _calcular_caminhos(lab: LabirintoBusca) -> dict:
    """Pré-computa a sequência de células do menor caminho entre todos os pares relevantes."""
    pontos = [lab.inicio] + list(lab.coletas) + [lab.objetivo]
    caminhos: dict = {}
    for i in range(len(pontos)):
        for j in range(len(pontos)):
            if i != j:
                caminhos[(pontos[i], pontos[j])] = _a_estrela_caminho(lab, pontos[i], pontos[j])
    return caminhos


def _perm_celulas(perm: list, lab: LabirintoBusca, caminhos: dict) -> list:
    """Sequência plana de células [r,c] para a rota A→C_π(1)→…→B."""
    coletas = lab.coletas
    seq = [lab.inicio] + [coletas[i] for i in perm] + [lab.objetivo]
    cells: list = []
    for i in range(len(seq)-1):
        trecho = caminhos[(seq[i], seq[i+1])]
        if cells and trecho and cells[-1] == list(trecho[0]):
            cells.extend(list(c) for c in trecho[1:])
        else:
            cells.extend(list(c) for c in trecho)
    return cells


def _swap_all(s: list):
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            v = s.copy()
            v[i], v[j] = v[j], v[i]
            yield v


def hc_frames_gen(lab: LabirintoBusca, dist: dict, caminhos: dict,
                  n_execucoes: int = 30, semente: int = 42):
    """
    Gera frames para animação do Hill-Climbing.
    Cada frame = ótimo local de uma execução.
    Frame: {path, custo, best_custo, run, done}
    """
    k = len(lab.coletas)
    if k < 2:
        s = list(range(k))
        c = custo_solucao(s, lab, dist)
        f = {'path': _perm_celulas(s, lab, caminhos), 'custo': c, 'best_custo': c, 'run': 1, 'done': False}
        yield f
        yield {**f, 'done': True}
        return

    rng = random.Random(semente)
    base = list(range(k))
    best_global_c = math.inf
    best_global_s: list = []

    for run_i in range(n_execucoes):
        s = base.copy()
        rng.shuffle(s)
        c = custo_solucao(s, lab, dist)

        while True:
            best_v = None
            best_c = c
            for v in _swap_all(s):
                cv = custo_solucao(v, lab, dist)
                if cv < best_c:
                    best_c = cv
                    best_v = v
            if best_v is None:
                break
            s, c = best_v, best_c

        if c < best_global_c:
            best_global_c = c
            best_global_s = s.copy()

        yield {
            'path':       _perm_celulas(s, lab, caminhos),
            'custo':      c,
            'best_custo': best_global_c,
            'run':        run_i + 1,
            'done':       False,
        }

    yield {
        'path':       _perm_celulas(best_global_s, lab, caminhos),
        'custo':      best_global_c,
        'best_custo': best_global_c,
        'run':        n_execucoes,
        'done':       True,
    }


_SA_SAMPLE = 500   # frames de SA a cada N iterações
_GA_SAMPLE = 1    # frames de GA a cada N gerações (1 = toda geração)


def sa_frames_gen(lab: LabirintoBusca, dist: dict, caminhos: dict,
                  T0: float | None = None, alpha: float = 0.995,
                  max_iter: int = 5000, n_execucoes: int = 20, semente: int = 42):
    """
    Gera frames para animação do Simulated Annealing.
    Mostra o caminho aceito atualmente a cada _SA_SAMPLE iterações + melhoras globais.
    Frame: {path, custo, best_custo, run, iter, done}
    """
    k = len(lab.coletas)
    if k < 2:
        s = list(range(k))
        c = custo_solucao(s, lab, dist)
        f = {'path': _perm_celulas(s, lab, caminhos), 'custo': c, 'best_custo': c,
             'run': 1, 'iter': 0, 'done': False}
        yield f
        yield {**f, 'done': True}
        return

    rng = random.Random(semente)
    base = list(range(k))
    best_global_c = math.inf
    best_global_s: list = []

    for run_i in range(n_execucoes):
        s0 = base.copy()
        rng.shuffle(s0)
        c0 = custo_solucao(s0, lab, dist)
        T  = T0 if T0 is not None else max(5.0 * c0, 1.0)

        s, c = s0.copy(), c0

        if c < best_global_c:
            best_global_c = c
            best_global_s = s.copy()

        for it in range(max_iter):
            i, j = rng.sample(range(k), 2)
            v = s.copy()
            v[i], v[j] = v[j], v[i]
            cv = custo_solucao(v, lab, dist)

            delta = cv - c
            if delta < 0 or (T > 1e-10 and rng.random() < math.exp(-delta / T)):
                s, c = v, cv
                if c < best_global_c:
                    best_global_c = c
                    best_global_s = s.copy()

            T *= alpha

            if (it + 1) % _SA_SAMPLE == 0:
                yield {
                    'path':       _perm_celulas(s, lab, caminhos),
                    'custo':      c,
                    'best_custo': best_global_c,
                    'run':        run_i + 1,
                    'iter':       it + 1,
                    'done':       False,
                }

    yield {
        'path':       _perm_celulas(best_global_s, lab, caminhos),
        'custo':      best_global_c,
        'best_custo': best_global_c,
        'run':        n_execucoes,
        'iter':       max_iter,
        'done':       True,
    }


def ga_frames_gen(lab: LabirintoBusca, dist: dict, caminhos: dict,
                  pop_size: int = 50, n_geracoes: int = 200,
                  mut_rate: float = 0.15, torneio_k: int = 3,
                  semente: int = 42):
    """
    Gera frames para animação do Algoritmo Genético.
    1 frame por geração mostrando o melhor indivíduo da população.
    Frame: {path, custo, best_custo, gen, done}
    """
    k = len(lab.coletas)
    if k < 2:
        s = list(range(k))
        c = custo_solucao(s, lab, dist)
        f = {'path': _perm_celulas(s, lab, caminhos), 'custo': c, 'best_custo': c, 'gen': 0, 'done': False}
        yield f
        yield {**f, 'done': True}
        return

    rng  = random.Random(semente)
    base = list(range(k))

    pop    = [rng.sample(base, k) for _ in range(pop_size)]
    custos = [custo_solucao(ind, lab, dist) for ind in pop]

    melhor_idx   = min(range(pop_size), key=lambda i: custos[i])
    melhor_perm  = pop[melhor_idx].copy()
    melhor_custo = custos[melhor_idx]

    yield {
        'path':       _perm_celulas(melhor_perm, lab, caminhos),
        'custo':      melhor_custo,
        'best_custo': melhor_custo,
        'gen':        0,
        'done':       False,
    }

    for gen in range(1, n_geracoes + 1):
        nova_pop     = [melhor_perm.copy()]
        novos_custos = [melhor_custo]

        while len(nova_pop) < pop_size:
            cands1 = rng.sample(range(pop_size), torneio_k)
            cands2 = rng.sample(range(pop_size), torneio_k)
            p1 = pop[min(cands1, key=lambda i: custos[i])].copy()
            p2 = pop[min(cands2, key=lambda i: custos[i])].copy()

            a, b = sorted(rng.sample(range(k), 2))
            filho = [None] * k
            filho[a:b+1] = p1[a:b+1]
            segmento = set(filho[a:b+1])
            pos = (b + 1) % k
            for gene in p2[b+1:] + p2[:b+1]:
                if gene not in segmento:
                    filho[pos] = gene
                    pos = (pos + 1) % k

            if rng.random() < mut_rate:
                i, j = rng.sample(range(k), 2)
                filho[i], filho[j] = filho[j], filho[i]

            c = custo_solucao(filho, lab, dist)
            nova_pop.append(filho)
            novos_custos.append(c)

        pop    = nova_pop
        custos = novos_custos

        gen_idx = min(range(pop_size), key=lambda i: custos[i])
        if custos[gen_idx] < melhor_custo:
            melhor_custo = custos[gen_idx]
            melhor_perm  = pop[gen_idx].copy()

        yield {
            'path':       _perm_celulas(melhor_perm, lab, caminhos),
            'custo':      melhor_custo,
            'best_custo': melhor_custo,
            'gen':        gen,
            'done':       gen == n_geracoes,
        }


# ── Coleta de métricas ────────────────────────────────────────────────────────

def _downsample(arr: list, max_pts: int = 300) -> list:
    if len(arr) <= max_pts:
        return arr
    step = (len(arr) - 1) / (max_pts - 1)
    return [arr[round(i * step)] for i in range(max_pts)]


def _metrica_classica(res, short_name: str) -> dict:
    return {
        'nome':          short_name,
        'encontrado':    res.encontrado,
        'custo':         round(res.custo_total, 1),
        'passos':        res.tamanho_caminho if res.tamanho_caminho is not None else None,
        'expandidos':    res.nos_expandidos,
        'explorados':    res.nos_explorados,
        'tempo_ms':      round(res.tempo_ms, 4),
        'fronteira_max': res.fronteira_max,
    }


def _metrica_local(res, lab: LabirintoBusca) -> dict:
    perm = res.melhor_permutacao
    seq  = ['A'] + [f'C{i+1}' for i in perm] + ['B']
    return {
        'algoritmo':    res.algoritmo,
        'melhor_ordem': ' → '.join(seq),
        'melhor_custo': round(res.melhor_custo, 1),
        'pior_custo':   round(res.pior_custo, 1),
        'custo_medio':  round(res.custo_medio, 2),
        'tempo_ms':     round(res.tempo_medio_ms, 3),
        'iteracoes':    round(res.iteracoes_media, 1),
        'n_execucoes':  res.n_execucoes,
        'taxa_sucesso': round(res.taxa_sucesso * 100, 1),
        'conv_ini':     round(res.convergencia[0])  if res.convergencia else None,
        'conv_fim':     round(res.convergencia[-1]) if res.convergencia else None,
        'conv_passos':  len(res.convergencia) - 1,
        'convergencia': _downsample(res.convergencia, 300),
        'custo_otimo':  round(res.custo_otimo, 1) if res.custo_otimo < math.inf else None,
        'gap':          round((res.melhor_custo / res.custo_otimo - 1) * 100, 1)
                        if res.custo_otimo < math.inf else None,
    }


# ──────────────────────────────────────────────────────────────
# Coleta de dados para todos os mapas
# ──────────────────────────────────────────────────────────────

def collect_all():
    # Importar aqui para evitar ciclo no nível de módulo
    from buscas.local.hill_climbing       import hill_climbing
    from buscas.local.simulated_annealing import simulated_annealing
    from buscas.local.genetic_algorithm   import genetic_algorithm

    all_data = {}
    for map_id, (path, label) in MAPAS.items():
        if not os.path.exists(path):
            continue
        try:
            lab_base = LabirintoBusca(path)
        except Exception as ex:
            print(f'  lab{map_id}: erro — {ex}')
            continue

        lab = LabirintoComColetas(lab_base) if lab_base.coletas else lab_base
        grid = {
            'h':       lab_base.altura,
            'w':       lab_base.largura,
            'walls':   lab_base.paredes,
            'start':   list(lab_base.inicio),
            'goal':    list(lab_base.objetivo),
            'coletas': [list(c) for c in lab_base.coletas],
            'label':   label,
        }

        print(f'  lab{map_id}:', end='', flush=True)

        # Animação clássica
        GEN_MAP = [
            ('BFS', bfs_gen), ('DFS', dfs_gen), ('UCS', ucs_gen),
            ('Gulosa', gulosa_gen), ('A*', a_estrela_gen),
        ]
        algos = {}
        for name, gen_fn in GEN_MAP:
            algos[name] = run_gen(gen_fn(lab))
            print(f' {name}', end='', flush=True)

        # Métricas clássicas
        metricas = [_metrica_classica(func(lab), short) for short, func in CLASSICOS]

        # Busca local (só quando há ≥2 coletas)
        local      = None
        local_anim = None
        if len(lab_base.coletas) >= 2:
            print(' [HC SA GA]', end='', flush=True)
            dist     = calcular_distancias(lab_base)
            res_hc   = hill_climbing(lab_base, dist=dist, n_execucoes=30, semente=42)
            res_sa   = simulated_annealing(lab_base, dist=dist, n_execucoes=20, semente=42)
            res_ga   = genetic_algorithm(lab_base, dist=dist, n_geracoes=200, semente=42)
            local    = {'hc': _metrica_local(res_hc, lab_base),
                        'sa': _metrica_local(res_sa, lab_base),
                        'ga': _metrica_local(res_ga, lab_base)}

            print(' [anim HC SA GA]', end='', flush=True)
            caminhos   = _calcular_caminhos(lab_base)
            local_anim = {
                'hc': list(hc_frames_gen(lab_base, dist, caminhos, n_execucoes=30, semente=42)),
                'sa': list(sa_frames_gen(lab_base, dist, caminhos, n_execucoes=20, semente=42)),
                'ga': list(ga_frames_gen(lab_base, dist, caminhos, n_geracoes=200, semente=42)),
            }

        # Busca online
        print(f'  |  online:', end='', flush=True)
        custo_offline = _custo_offline(lab_base)
        online_algos = {}
        for name, gen_func in [
            ('Replanning A*', online_replanning_gen),
            ('Online DFS',    online_dfs_gen),
        ]:
            data = run_online_gen(gen_func, lab_base)
            data['custo_offline'] = custo_offline
            custo_real = data.get('movimentos', 0)
            data['razao'] = (
                round(custo_real / custo_offline, 3)
                if data.get('encontrado') and custo_offline > 0
                else None
            )
            online_algos[name] = data
            print(f' {name}', end='', flush=True)

        print()
        all_data[map_id] = {
            'grid':       grid,
            'algorithms': algos,
            'metricas':   metricas,
            'local':      local,
            'local_anim': local_anim,
            'online':     online_algos,
        }
    return all_data


# ──────────────────────────────────────────────────────────────
# Template HTML
# ──────────────────────────────────────────────────────────────

HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Busca em Labirinto — CSI457</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg:       #1e1e2e; --mantle:  #181825;
  --surface0: #313244; --surface1:#45475a;
  --overlay:  #6c7086; --subtext: #a6adc8; --text: #cdd6f4;
  --wall:     #45475a; --free:    #e5e7ef;
  --start:    #40a02b; --goal:    #d20f39; --coleta: #df8e1d;
  --explored: #89b4fa; --frontier:#f9e2af; --path:   #fab387;
  --unknown:  #11111b; --agent:   #cba6f7; --trail:  #89dceb;
  --green:    #a6e3a1; --red:     #f38ba8; --yellow: #f9e2af;
  --blue:     #89b4fa; --peach:   #fab387; --mauve:  #cba6f7;
  --lavender: #b4befe;
}
body { background:var(--bg); color:var(--text); font-family:'Courier New',monospace;
       min-height:100vh; padding:14px 10px; }

.header { text-align:center; margin-bottom:10px; }
.header h1 { font-size:1.25rem; font-weight:bold; letter-spacing:.04em; }
.header p  { font-size:.77rem; color:var(--subtext); margin-top:3px; }

.mode-bar { display:flex; gap:8px; justify-content:center; margin-bottom:8px; }
.mode-btn { background:var(--surface0); color:var(--subtext); border:1px solid var(--surface1);
            border-radius:6px; padding:5px 20px; cursor:pointer; font-family:inherit; font-size:.84rem; }
.mode-btn:hover { background:var(--surface1); color:var(--text); }
.mode-btn.active { background:#cba6f7; color:#1e1e2e; border-color:#cba6f7; font-weight:bold; }

.map-bar { display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin-bottom:12px; }
.map-btn { background:var(--surface0); color:var(--subtext); border:1px solid var(--surface1);
           border-radius:6px; padding:5px 14px; cursor:pointer; font-family:inherit; font-size:.82rem; }
.map-btn:hover { background:var(--surface1); color:var(--text); }
.map-btn.active { background:var(--blue); color:#1e1e2e; border-color:var(--blue); font-weight:bold; }

/* Grids */
.grids-area { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:10px; }
.local-grids-area { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:10px; }
@media(max-width:800px){ .grids-area{ grid-template-columns:repeat(2,1fr); } }
@media(max-width:900px){ .local-grids-area{ grid-template-columns:repeat(2,1fr); } }
@media(max-width:600px){ .local-grids-area{ grid-template-columns:1fr; } }
@media(max-width:520px){ .grids-area{ grid-template-columns:1fr; } }

.online-area { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:12px; }
@media(max-width:800px){ .online-area{ grid-template-columns:repeat(2,1fr); } }
@media(max-width:520px){ .online-area{ grid-template-columns:1fr; } }

.algo-box { background:var(--mantle); border-radius:8px; padding:10px 8px 12px;
            display:flex; flex-direction:column; align-items:center; gap:8px; }
.algo-title { font-size:.8rem; font-weight:bold; color:var(--subtext); text-align:center;
              min-height:1.1em; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:100%; }
.algo-title.running { color:var(--text); }
.algo-title.done    { color:var(--green); }
.algo-title.no-path { color:var(--red); }

.maze-wrap { display:flex; justify-content:center; }
.maze { display:grid; gap:2px; background:var(--bg); padding:3px; border-radius:4px; }
.cell { border-radius:2px; }

/* Legend */
.legend-box { background:var(--mantle); border-radius:8px; padding:12px 16px;
              display:flex; flex-direction:column; justify-content:center; gap:6px; }
.legend-box h3 { font-size:.78rem; color:var(--overlay); text-align:center; margin-bottom:2px;
                 letter-spacing:.08em; text-transform:uppercase; }
.legend-item { display:flex; align-items:center; gap:8px; font-size:.76rem; color:var(--subtext); }
.swatch { width:14px; height:14px; border-radius:3px; flex-shrink:0; }

/* Controls */
.controls { display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:12px;
            background:var(--mantle); border-radius:8px; padding:10px 20px; margin-bottom:16px; }
.ctrl-btn { background:var(--surface0); color:var(--text); border:1px solid var(--surface1);
            border-radius:6px; padding:6px 18px; cursor:pointer; font-family:inherit;
            font-size:.88rem; min-width:96px; text-align:center; }
.ctrl-btn:hover { background:var(--surface1); }
.ctrl-btn.is-play  { border-color:var(--green); color:var(--green); }
.ctrl-btn.is-pause { border-color:var(--red);   color:var(--red); }
.speed-group { display:flex; align-items:center; gap:8px; font-size:.82rem; color:var(--subtext); }
input[type=range] { accent-color:var(--blue); width:130px; cursor:pointer; }
#speed-val { min-width:2ch; color:var(--blue); font-weight:bold; }

/* Section titles */
.section-title { font-size:.82rem; letter-spacing:.1em; text-transform:uppercase;
                 color:var(--overlay); margin-bottom:8px; padding-left:4px; }

/* Classical results table */
.results-area { margin-bottom:16px; }
.table-wrap { overflow-x:auto; }
.results-table { width:100%; border-collapse:collapse; font-size:.8rem;
                 background:var(--mantle); border-radius:8px; overflow:hidden; }
.results-table th { background:var(--surface0); color:var(--subtext); font-weight:bold;
                    padding:8px 12px; text-align:right; white-space:nowrap; letter-spacing:.04em; }
.results-table th:first-child { text-align:left; }
.results-table td { padding:7px 12px; text-align:right; color:var(--text);
                    border-top:1px solid var(--surface0); }
.results-table td:first-child { text-align:left; color:var(--blue); font-weight:bold; }
.results-table tr:hover td { background:var(--surface0); }
.ok   { color:var(--green) !important; }
.fail { color:var(--red)   !important; }

/* Local search result cards */
.local-area { margin-bottom:16px; }
.local-cards { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }
@media(max-width:900px){ .local-cards{ grid-template-columns:1fr 1fr; } }
@media(max-width:600px){ .local-cards{ grid-template-columns:1fr; } }

.local-card { background:var(--mantle); border-radius:8px; padding:14px 16px;
              display:flex; flex-direction:column; gap:5px; }
.local-card-title { font-size:.88rem; font-weight:bold; color:var(--mauve);
                    border-bottom:1px solid var(--surface1); padding-bottom:6px; margin-bottom:4px; }
.lrow { display:flex; justify-content:space-between; align-items:baseline;
        font-size:.78rem; gap:12px; }
.lrow > span:first-child { color:var(--subtext); white-space:nowrap; }
.lrow > span:last-child  { color:var(--text); text-align:right; }
.lrow.ordem > span:last-child { color:var(--peach); font-weight:bold; }
.gap-tag     { color:var(--green); font-size:.72rem; margin-left:6px; }
.gap-tag.bad { color:var(--yellow); }

/* Gráficos de convergência */
.conv-section { margin-bottom:16px; }
.conv-charts  { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }
@media(max-width:900px){ .conv-charts{ grid-template-columns:1fr 1fr; } }
@media(max-width:600px){ .conv-charts{ grid-template-columns:1fr; } }
.conv-box { background:var(--mantle); border-radius:8px; padding:10px 10px 6px; }
.conv-box-title { font-size:.78rem; font-weight:bold; color:var(--subtext); text-align:center; margin-bottom:6px; }
.conv-box canvas { display:block; width:100%; height:auto; border-radius:4px; }
</style>
</head>
<body>

<div class="header">
  <h1>Busca em Labirinto — CSI457</h1>
  <p id="mode-subtitle">BFS · DFS · UCS · Gulosa · A* — expansão em tempo real</p>
</div>

<div class="mode-bar">
  <button class="mode-btn active" id="mode-classic" onclick="setMode('classic')">Busca Clássica</button>
  <button class="mode-btn" id="mode-local"  onclick="setMode('local')">Busca Local</button>
  <button class="mode-btn" id="mode-online" onclick="setMode('online')">Busca Online</button>
</div>

<div class="map-bar" id="map-bar"></div>

<!-- Animação busca clássica -->
<div class="grids-area" id="classic-area">
  <div class="algo-box"><div class="algo-title" id="title-BFS">BFS</div>
    <div class="maze-wrap"><div class="maze" id="maze-BFS"></div></div></div>
  <div class="algo-box"><div class="algo-title" id="title-DFS">DFS</div>
    <div class="maze-wrap"><div class="maze" id="maze-DFS"></div></div></div>
  <div class="algo-box"><div class="algo-title" id="title-UCS">UCS</div>
    <div class="maze-wrap"><div class="maze" id="maze-UCS"></div></div></div>
  <div class="algo-box"><div class="algo-title" id="title-Gulosa">Gulosa</div>
    <div class="maze-wrap"><div class="maze" id="maze-Gulosa"></div></div></div>
  <div class="algo-box"><div class="algo-title" id="title-A*">A*</div>
    <div class="maze-wrap"><div class="maze" id="maze-A*"></div></div></div>
  <div class="legend-box">
    <h3>Legenda</h3>
    <div class="legend-item"><div class="swatch" style="background:var(--start)"></div>Início (A)</div>
    <div class="legend-item"><div class="swatch" style="background:var(--goal)"></div>Objetivo (B)</div>
    <div class="legend-item"><div class="swatch" style="background:var(--coleta)"></div>Coleta (C)</div>
    <div class="legend-item"><div class="swatch" style="background:var(--explored)"></div>Explorado</div>
    <div class="legend-item"><div class="swatch" style="background:var(--frontier)"></div>Fronteira</div>
    <div class="legend-item"><div class="swatch" style="background:var(--path)"></div>Caminho</div>
    <div class="legend-item"><div class="swatch" style="background:var(--wall)"></div>Parede</div>
    <div class="legend-item"><div class="swatch" style="background:var(--free);border:1px solid #888"></div>Livre</div>
  </div>
</div>

<!-- Animação busca local (oculto quando não há coletas) -->
<div id="local-grids-section" style="display:none; margin-bottom:10px;">
  <div class="section-title">Animação — Busca Local (ordem de visitação dos pontos de coleta)</div>
  <div class="local-grids-area">
    <div class="algo-box">
      <div class="algo-title" id="title-HC">Hill-Climbing</div>
      <div class="maze-wrap"><div class="maze" id="maze-HC"></div></div>
    </div>
    <div class="algo-box">
      <div class="algo-title" id="title-SA">Simulated Annealing</div>
      <div class="maze-wrap"><div class="maze" id="maze-SA"></div></div>
    </div>
    <div class="algo-box">
      <div class="algo-title" id="title-GA">Algoritmo Genético</div>
      <div class="maze-wrap"><div class="maze" id="maze-GA"></div></div>
    </div>
  </div>
</div>

<!-- Grade busca online -->
<div class="online-area" id="online-area" style="display:none">
  <div class="algo-box"><div class="algo-title" id="title-Replanning A*">Replanning A*</div>
    <div class="maze-wrap"><div class="maze" id="maze-Replanning A*"></div></div></div>
  <div class="algo-box"><div class="algo-title" id="title-Online DFS">Online DFS</div>
    <div class="maze-wrap"><div class="maze" id="maze-Online DFS"></div></div></div>
  <div class="legend-box">
    <h3>Legenda Online</h3>
    <div class="legend-item"><div class="swatch" style="background:var(--agent)"></div>Agente (pos. atual)</div>
    <div class="legend-item"><div class="swatch" style="background:var(--trail)"></div>Trilha percorrida</div>
    <div class="legend-item"><div class="swatch" style="background:var(--free);border:1px solid #aaa"></div>Livre (revelado)</div>
    <div class="legend-item"><div class="swatch" style="background:var(--wall)"></div>Parede (revelada)</div>
    <div class="legend-item"><div class="swatch" style="background:var(--unknown)"></div>Desconhecido</div>
    <div class="legend-item"><div class="swatch" style="background:var(--start)"></div>Início (A)</div>
    <div class="legend-item"><div class="swatch" style="background:var(--goal)"></div>Objetivo (B)</div>
  </div>
</div>

<div class="controls">
  <button class="ctrl-btn is-play" id="btn-play" onclick="togglePlay()">▶  Play</button>
  <button class="ctrl-btn" onclick="restart()">↺  Reiniciar</button>
  <div class="speed-group">
    <span>Velocidade</span>
    <input type="range" id="speed-slider" min="1" max="30" value="8"
           oninput="document.getElementById('speed-val').textContent=this.value">
    <span id="speed-val">8</span>
  </div>
</div>

<!-- Tabela resultados clássicos -->
<div class="results-area">
  <div class="section-title">Resultados — Busca Clássica</div>
  <div class="table-wrap">
    <table class="results-table">
      <thead>
        <tr>
          <th>Algoritmo</th><th>Sucesso</th><th>Custo</th><th>Passos</th>
          <th>Expandidos</th><th>Explorados</th><th>Tempo (ms)</th><th>Front. Máx</th>
        </tr>
      </thead>
      <tbody id="results-tbody"></tbody>
    </table>
  </div>
</div>

<!-- Cards busca local (oculto quando não há coletas) -->
<div class="local-area" id="local-area" style="display:none">
  <div class="section-title">Resultados — Busca Local</div>
  <div class="local-cards" id="local-cards"></div>
</div>

<!-- Gráficos de convergência (oculto quando não há coletas) -->
<div class="conv-section" id="conv-section" style="display:none">
  <div class="section-title">Convergência — iteração × melhor custo</div>
  <div class="conv-charts">
    <div class="conv-box">
      <div class="conv-box-title">Hill-Climbing</div>
      <canvas id="conv-hc" width="380" height="200"></canvas>
    </div>
    <div class="conv-box">
      <div class="conv-box-title">Simulated Annealing</div>
      <canvas id="conv-sa" width="380" height="200"></canvas>
    </div>
    <div class="conv-box">
      <div class="conv-box-title">Algoritmo Genético</div>
      <canvas id="conv-ga" width="380" height="200"></canvas>
    </div>
  </div>
</div>

<!-- Tabela resultados online -->
<div class="results-area" id="online-results-area">
  <div class="section-title">Resultados — Busca Online</div>
  <div class="table-wrap">
    <table class="results-table">
      <thead>
        <tr>
          <th>Algoritmo</th><th>Sucesso</th><th>Movimentos</th><th>Custo Offline</th>
          <th>Reveladas</th><th>Revisitadas</th><th>Replanejamentos</th><th>Tempo (ms)</th><th>Razão</th>
        </tr>
      </thead>
      <tbody id="online-results-tbody"></tbody>
    </table>
  </div>
</div>

<script>
const DATA         = __DATA__;
const ALGOS        = ['BFS','DFS','UCS','Gulosa','A*'];
const LOCAL_ALGOS  = ['HC','SA','GA'];
const ONLINE_ALGOS = ['Replanning A*','Online DFS'];

let currentMap = null, currentMode = 'classic';
let frameIdx = {}, doneAlgo = {}, playing = false, timer = null;
let cells = {}, algoState = {};
let localCells = {}, localFrameIdx = {}, localDone = {};
let onlineFrameIdx = {}, onlineDone = {};
let onlineCells = {}, onlineState = {};

// ── Modo ─────────────────────────────────────────────────────────────────────
function setMode(mode) {
  currentMode = mode;
  document.getElementById('mode-classic').classList.toggle('active', mode==='classic');
  document.getElementById('mode-local').classList.toggle('active',   mode==='local');
  document.getElementById('mode-online').classList.toggle('active',  mode==='online');
  document.getElementById('classic-area').style.display        = mode==='classic' ? '' : 'none';
  const hasLocal = currentMap && DATA[currentMap]?.local_anim;
  document.getElementById('local-grids-section').style.display = mode==='local' && hasLocal ? '' : 'none';
  document.getElementById('online-area').style.display         = mode==='online'  ? '' : 'none';
  document.getElementById('mode-subtitle').textContent =
    mode==='classic' ? 'BFS · DFS · UCS · Gulosa · A* — expansão em tempo real' :
    mode==='local'   ? 'Hill-Climbing · Simulated Annealing · Algoritmo Genético' :
                       'Replanning A* · Online DFS — mapa desconhecido';
  restart();
}

// ── Mapa bar ─────────────────────────────────────────────────────────────────
function initMapBar() {
  const bar = document.getElementById('map-bar');
  for(const [id, {grid}] of Object.entries(DATA)) {
    const btn = document.createElement('button');
    btn.className = 'map-btn'; btn.textContent = grid.label; btn.dataset.id = id;
    btn.onclick = () => loadMap(id); bar.appendChild(btn);
  }
}

function loadMap(id) {
  currentMap = id;
  document.querySelectorAll('.map-btn').forEach(b => b.classList.toggle('active', b.dataset.id===id));
  buildGrids();
  buildLocalGrids();
  buildOnlineGrids();
  renderTable(id);
  renderLocalCards(id);
  renderConvCharts(id);
  renderOnlineTable(id);
  restart();
}

// ── Grade clássica ────────────────────────────────────────────────────────────
function buildGrids() {
  const {grid} = DATA[currentMap];
  const {h, w, walls, start, goal, coletas} = grid;
  const coletaSet = new Set(coletas.map(([r,c]) => r+','+c));
  const startKey = start[0]+','+start[1], goalKey = goal[0]+','+goal[1];
  const sz = Math.min(36, Math.floor(300/w));
  for(const algo of ALGOS) {
    const mazeEl = document.getElementById('maze-'+algo);
    mazeEl.innerHTML = '';
    mazeEl.style.gridTemplateColumns = `repeat(${w},${sz}px)`;
    const alCells = [];
    for(let r=0; r<h; r++) for(let c=0; c<w; c++) {
      const div = document.createElement('div');
      div.className = 'cell'; div.style.width = sz+'px'; div.style.height = sz+'px';
      const key = r+','+c;
      div.style.backgroundColor = walls[r][c] ? 'var(--wall)' : key===startKey ? 'var(--start)'
        : key===goalKey ? 'var(--goal)' : coletaSet.has(key) ? 'var(--coleta)' : 'var(--free)';
      mazeEl.appendChild(div); alCells.push({div, key, r, c});
    }
    cells[algo] = alCells;
  }
}

// ── Grade local ───────────────────────────────────────────────────────────────
function buildLocalGrids() {
  const hasLocal = DATA[currentMap].local_anim !== null;
  if(!hasLocal) return;
  const {grid} = DATA[currentMap];
  const {h, w, walls, start, goal, coletas} = grid;
  const coletaSet = new Set(coletas.map(([r,c]) => r+','+c));
  const startKey = start[0]+','+start[1], goalKey = goal[0]+','+goal[1];
  const sz = Math.min(36, Math.floor(300/w));
  for(const algo of LOCAL_ALGOS) {
    const mazeEl = document.getElementById('maze-'+algo);
    mazeEl.innerHTML = '';
    mazeEl.style.gridTemplateColumns = `repeat(${w},${sz}px)`;
    const alCells = [];
    for(let r=0; r<h; r++) for(let c=0; c<w; c++) {
      const div = document.createElement('div');
      div.className = 'cell'; div.style.width = sz+'px'; div.style.height = sz+'px';
      const key = r+','+c;
      div.style.backgroundColor = walls[r][c] ? 'var(--wall)' : key===startKey ? 'var(--start)'
        : key===goalKey ? 'var(--goal)' : coletaSet.has(key) ? 'var(--coleta)' : 'var(--free)';
      mazeEl.appendChild(div); alCells.push({div, key, r, c});
    }
    localCells[algo] = alCells;
  }
}

// ── Rendering clássico ────────────────────────────────────────────────────────
function applyDelta(algo, delta) {
  const st = algoState[algo];
  for(const [r,c] of delta.ea) { st.exp.add(r+','+c); st.expCount++; }
  for(const [r,c] of delta.fa)  st.frt.add(r+','+c);
  for(const [r,c] of delta.fr)  st.frt.delete(r+','+c);
  if(delta.p !== null) st.path = delta.p;
}

function renderCurrent(algo) {
  const {grid} = DATA[currentMap];
  const {walls, start, goal, coletas} = grid;
  const coletaSet = new Set(coletas.map(([r,c]) => r+','+c));
  const startKey = start[0]+','+start[1], goalKey = goal[0]+','+goal[1];
  const {exp, frt, path} = algoState[algo];
  const pathSet = path ? new Set(path.map(([r,c]) => r+','+c)) : null;
  for(const {div, key, r, c} of cells[algo]) {
    let color;
    if(walls[r][c])             color = 'var(--wall)';
    else if(key === startKey)   color = 'var(--start)';
    else if(key === goalKey)    color = 'var(--goal)';
    else if(pathSet?.has(key))  color = 'var(--path)';
    else if(frt.has(key))       color = 'var(--frontier)';
    else if(exp.has(key))       color = 'var(--explored)';
    else if(coletaSet.has(key)) color = 'var(--coleta)';
    else                        color = 'var(--free)';
    div.style.backgroundColor = color;
  }
}

// ── Rendering local ───────────────────────────────────────────────────────────
function renderLocalMaze(algo, frame) {
  if(!localCells[algo]) return;
  const {grid} = DATA[currentMap];
  const {walls, start, goal, coletas} = grid;
  const coletaSet = new Set(coletas.map(([r,c]) => r+','+c));
  const startKey = start[0]+','+start[1], goalKey = goal[0]+','+goal[1];
  const pathSet = new Set(frame.path.map(([r,c]) => r+','+c));
  for(const {div, key, r, c} of localCells[algo]) {
    let color;
    if(walls[r][c])             color = 'var(--wall)';
    else if(key===startKey)     color = 'var(--start)';
    else if(key===goalKey)      color = 'var(--goal)';
    else if(coletaSet.has(key)) color = 'var(--coleta)';
    else if(pathSet.has(key))   color = 'var(--path)';
    else                        color = 'var(--free)';
    div.style.backgroundColor = color;
  }
}

function updateLocalTitle(algo, frame) {
  const el = document.getElementById('title-'+algo);
  if(!el) return;
  const name = algo==='HC' ? 'Hill-Climbing' : algo==='SA' ? 'Simulated Annealing' : 'Algoritmo Genético';
  const nRuns = DATA[currentMap].local[algo.toLowerCase()].n_execucoes;
  if(frame.done) {
    el.textContent = `${name}  ✓  melhor=${frame.best_custo}`; el.className = 'algo-title done';
  } else if(algo==='GA') {
    el.textContent = `${name}  gen ${frame.gen}/200  melhor=${frame.best_custo}`; el.className = 'algo-title running';
  } else if(algo==='SA') {
    el.textContent = `${name}  run ${frame.run}/${nRuns}  iter ${frame.iter}  custo=${frame.custo}`; el.className = 'algo-title running';
  } else {
    el.textContent = `${name}  run ${frame.run}/${nRuns}  custo=${frame.custo}  best=${frame.best_custo}`; el.className = 'algo-title running';
  }
}

// ── Loop de animação ──────────────────────────────────────────────────────────
function resetAlgoState() {
  for(const algo of ALGOS)
    algoState[algo] = {exp: new Set(), frt: new Set(), expCount: 0, path: null};
}

function restart() {
  stopTimer(); resetAlgoState();
  for(const algo of ALGOS) {
    frameIdx[algo] = 0; doneAlgo[algo] = false;
    const el = document.getElementById('title-'+algo);
    el.textContent = algo; el.className = 'algo-title';
    const frames = DATA[currentMap].algorithms[algo].frames;
    if(frames.length) { applyDelta(algo, frames[0]); renderCurrent(algo); }
  }
  if(DATA[currentMap].local_anim) {
    for(const algo of LOCAL_ALGOS) {
      localFrameIdx[algo] = 0; localDone[algo] = false;
      const el = document.getElementById('title-'+algo);
      if(el) { el.textContent = algo==='HC' ? 'Hill-Climbing' : algo==='SA' ? 'Simulated Annealing' : 'Algoritmo Genético'; el.className = 'algo-title'; }
      const frames = DATA[currentMap].local_anim[algo.toLowerCase()];
      if(frames && frames.length) { renderLocalMaze(algo, frames[0]); updateLocalTitle(algo, frames[0]); }
    }
  }
  resetOnlineState(); buildOnlineGrids();
  for(const algo of ONLINE_ALGOS) {
    onlineFrameIdx[algo] = 0; onlineDone[algo] = false;
    const el = document.getElementById('title-'+algo);
    if(el) { el.textContent = algo; el.className = 'algo-title'; }
    const frames = DATA[currentMap].online[algo]?.frames || [];
    if(frames.length) { applyOnlineDelta(algo, frames[0]); renderOnline(algo); }
  }
  playing = true; updatePlayBtn(); startTimer();
}

function startTimer() { timer = setInterval(tick, 50); }
function stopTimer()  { if(timer) { clearInterval(timer); timer = null; } }

function tick() {
  const speed = +document.getElementById('speed-slider').value;
  let anyActive = false;

  for(const algo of ALGOS) {
    if(doneAlgo[algo]) continue;
    anyActive = true;
    const frames = DATA[currentMap].algorithms[algo].frames;
    let idx = frameIdx[algo];
    for(let s=0; s<speed && idx<frames.length-1; s++) { idx++; applyDelta(algo, frames[idx]); }
    frameIdx[algo] = idx;
    renderCurrent(algo);
    const finished = idx >= frames.length-1;
    updateTitle(algo, finished);
    if(finished) doneAlgo[algo] = true;
  }

  if(DATA[currentMap].local_anim) {
    for(const algo of LOCAL_ALGOS) {
      if(localDone[algo]) continue;
      anyActive = true;
      const frames = DATA[currentMap].local_anim[algo.toLowerCase()];
      let idx = localFrameIdx[algo];
      if(idx < frames.length-1) idx++;
      localFrameIdx[algo] = idx;
      const frame = frames[idx];
      renderLocalMaze(algo, frame);
      updateLocalTitle(algo, frame);
      if(frame.done || idx >= frames.length-1) localDone[algo] = true;
    }
  }

  for(const algo of ONLINE_ALGOS) {
    if(onlineDone[algo]) continue;
    anyActive = true;
    const frames = DATA[currentMap].online[algo]?.frames || [];
    let idx = onlineFrameIdx[algo];
    for(let s=0; s<speed && idx<frames.length-1; s++) { idx++; applyOnlineDelta(algo, frames[idx]); }
    onlineFrameIdx[algo] = idx;
    renderOnline(algo);
    const finished = idx >= frames.length-1;
    updateOnlineTitle(algo, finished);
    if(finished) onlineDone[algo] = true;
  }

  if(!anyActive) { stopTimer(); playing = false; updatePlayBtn(); }
}

function updateTitle(algo, finished) {
  const el = document.getElementById('title-'+algo);
  const st = algoState[algo];
  const t  = DATA[currentMap].algorithms[algo].t;
  if(finished) {
    if(st.path) { el.textContent = `${algo}  ✓  custo=${st.path.length}  exp=${st.expCount}  ${t}ms`; el.className = 'algo-title done'; }
    else        { el.textContent = `${algo}  ✗  sem solução  ${t}ms`; el.className = 'algo-title no-path'; }
  } else {
    el.textContent = `${algo}  (${st.expCount} exp.)`; el.className = 'algo-title running';
  }
}

// ── Grade online ──────────────────────────────────────────────────────────────
function buildOnlineGrids() {
  const {grid} = DATA[currentMap];
  const {h, w} = grid;
  const sz = Math.min(36, Math.floor(300/w));
  for(const algo of ONLINE_ALGOS) {
    const mazeEl = document.getElementById('maze-'+algo);
    mazeEl.innerHTML = '';
    mazeEl.style.gridTemplateColumns = `repeat(${w},${sz}px)`;
    const alCells = [];
    for(let r=0; r<h; r++) for(let c=0; c<w; c++) {
      const div = document.createElement('div');
      div.className = 'cell'; div.style.width = sz+'px'; div.style.height = sz+'px';
      div.style.backgroundColor = 'var(--unknown)';
      mazeEl.appendChild(div); alCells.push({div, key: r+','+c, r, c});
    }
    onlineCells[algo] = alCells;
  }
}

function resetOnlineState() {
  for(const algo of ONLINE_ALGOS)
    onlineState[algo] = {rf: new Set(), rw: new Set(), trail: [], pos: null};
}

function applyOnlineDelta(algo, frame) {
  const st = onlineState[algo];
  for(const [r,c] of (frame.rf || [])) st.rf.add(r+','+c);
  for(const [r,c] of (frame.rw || [])) st.rw.add(r+','+c);
  if(frame.pos) { st.trail.push(frame.pos); st.pos = frame.pos; }
}

function renderOnline(algo) {
  const {grid} = DATA[currentMap];
  const {start, goal} = grid;
  const startKey = start[0]+','+start[1], goalKey = goal[0]+','+goal[1];
  const st = onlineState[algo];
  const posKey = st.pos ? st.pos[0]+','+st.pos[1] : null;
  const trailSet = new Set(st.trail.slice(0, -1).map(([r,c]) => r+','+c));
  for(const {div, key} of onlineCells[algo]) {
    let color;
    if(key === posKey)         color = 'var(--agent)';
    else if(key === goalKey)   color = 'var(--goal)';
    else if(key === startKey)  color = 'var(--start)';
    else if(st.rw.has(key))   color = 'var(--wall)';
    else if(trailSet.has(key)) color = 'var(--trail)';
    else if(st.rf.has(key))   color = 'var(--free)';
    else                       color = 'var(--unknown)';
    div.style.backgroundColor = color;
  }
}

function updateOnlineTitle(algo, finished) {
  const el = document.getElementById('title-'+algo);
  const st = onlineState[algo];
  if(finished) {
    const d = DATA[currentMap].online[algo];
    if(d.encontrado) {
      const razao = d.razao != null ? `  razão=${d.razao}` : '';
      el.textContent = `${algo}  ✓  mov=${d.movimentos}  rev=${d.reveladas}${razao}  ${d.t}ms`;
      el.className = 'algo-title done';
    } else {
      el.textContent = `${algo}  ✗  sem solução  ${d.t}ms`; el.className = 'algo-title no-path';
    }
  } else {
    el.textContent = `${algo}  (${st.trail.length} mov.)`; el.className = 'algo-title running';
  }
}

function togglePlay() {
  if(playing) { stopTimer(); playing = false; }
  else {
    const classicDone  = Object.values(doneAlgo).every(Boolean);
    const localDoneAll = !DATA[currentMap].local_anim || LOCAL_ALGOS.every(a => localDone[a]);
    const onlineDoneAll = Object.values(onlineDone).every(Boolean);
    const allDone = currentMode==='classic' ? classicDone :
                    currentMode==='local'   ? localDoneAll :
                                              onlineDoneAll;
    if(allDone) { restart(); return; }
    playing = true; startTimer();
  }
  updatePlayBtn();
}

function updatePlayBtn() {
  const btn = document.getElementById('btn-play');
  if(playing) { btn.textContent = '⏸  Pausar'; btn.className = 'ctrl-btn is-pause'; }
  else        { btn.textContent = '▶  Play';   btn.className = 'ctrl-btn is-play'; }
}

// ── Tabela resultados clássicos ───────────────────────────────────────────────
function renderTable(mapId){
  const metricas=DATA[mapId].metricas;
  const tbody=document.getElementById('results-tbody');
  tbody.innerHTML='';
  for(const m of metricas){
    const ok=m.encontrado;
    const tr=document.createElement('tr');
    tr.innerHTML=
      `<td>${m.nome}</td>`+
      `<td class="${ok?'ok':'fail'}">${ok?'✓':'✗'}</td>`+
      `<td>${ok?m.custo:'—'}</td>`+
      `<td>${m.passos!=null?m.passos:'—'}</td>`+
      `<td>${m.expandidos}</td>`+
      `<td>${m.explorados}</td>`+
      `<td>${m.tempo_ms}</td>`+
      `<td>${m.fronteira_max}</td>`;
    tbody.appendChild(tr);
  }
}

// ── Cards busca local ─────────────────────────────────────────────────────────
function renderLocalCards(mapId){
  const local=DATA[mapId].local;
  const area=document.getElementById('local-area');
  if(!local){ area.style.display='none'; return; }
  area.style.display='';
  const cards=document.getElementById('local-cards');
  cards.innerHTML='';
  for(const res of [local.hc, local.sa, local.ga]){
    let optLine='';
    if(res.custo_otimo!==null){
      const gapClass=res.gap===0?'gap-tag':'gap-tag bad';
      optLine=`<div class="lrow"><span>Ótimo (brute-force)</span>`+
              `<span>${res.custo_otimo} <em class="${gapClass}">(gap ${res.gap}%)</em></span></div>`;
    }
    const convLine=res.conv_ini!==null
      ?`${res.conv_ini} → ${res.conv_fim}  (${res.conv_passos} passos)`:'—';
    cards.innerHTML+=`
      <div class="local-card">
        <div class="local-card-title">${res.algoritmo}</div>
        <div class="lrow ordem"><span>Melhor ordem</span><span>${res.melhor_ordem}</span></div>
        <div class="lrow"><span>Melhor custo</span><span>${res.melhor_custo}</span></div>
        ${optLine}
        <div class="lrow"><span>Pior custo</span><span>${res.pior_custo}</span></div>
        <div class="lrow"><span>Custo médio</span><span>${res.custo_medio}</span></div>
        <div class="lrow"><span>Tempo médio</span><span>${res.tempo_ms} ms</span></div>
        <div class="lrow"><span>Iterações médias</span><span>${res.iteracoes}</span></div>
        <div class="lrow"><span>Execuções</span><span>${res.n_execucoes}</span></div>
        <div class="lrow"><span>Taxa de sucesso</span><span>${res.taxa_sucesso}%</span></div>
        <div class="lrow"><span>Convergência</span><span>${convLine}</span></div>
      </div>`;
  }
}

// ── Gráficos de convergência ──────────────────────────────────────────────────
function drawConvChart(canvasId, data, color){
  const canvas=document.getElementById(canvasId);
  if(!canvas||!data||data.length<1) return;
  const ctx=canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  const pad={t:18,r:14,b:32,l:54};
  const cW=W-pad.l-pad.r, cH=H-pad.t-pad.b;
  const n=data.length;

  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#181825'; ctx.fillRect(0,0,W,H);

  const minY=Math.min(...data), maxY=Math.max(...data);
  const rangeY=maxY-minY||1;

  // Linhas de grade e rótulos Y
  for(let i=0;i<=4;i++){
    const val=minY+rangeY*i/4;
    const y=pad.t+cH-cH*i/4;
    ctx.fillStyle='#6c7086'; ctx.font='10px Courier New'; ctx.textAlign='right';
    ctx.fillText(Math.round(val),pad.l-5,y+3);
    ctx.strokeStyle=i===0?'#45475a':'#31324455'; ctx.lineWidth=i===0?1:0.5;
    ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(pad.l+cW,y); ctx.stroke();
  }

  // Eixo vertical
  ctx.strokeStyle='#45475a'; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(pad.l,pad.t); ctx.lineTo(pad.l,pad.t+cH); ctx.stroke();

  // Curva de convergência
  ctx.strokeStyle=color; ctx.lineWidth=1.8; ctx.lineJoin='round';
  ctx.beginPath();
  for(let i=0;i<n;i++){
    const x=pad.l+(n>1?i/(n-1):0.5)*cW;
    const y=pad.t+cH-(data[i]-minY)/rangeY*cH;
    i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
  }
  ctx.stroke();

  // Rótulo do custo final (canto superior direito da linha)
  const lastY=pad.t+cH-(data[n-1]-minY)/rangeY*cH;
  ctx.fillStyle=color; ctx.font='bold 10px Courier New'; ctx.textAlign='right';
  ctx.fillText(Math.round(data[n-1]),pad.l+cW-2,Math.max(lastY-4,pad.t+10));

  // Rótulo eixo X
  ctx.fillStyle='#6c7086'; ctx.font='10px Courier New';
  ctx.textAlign='center'; ctx.fillText('iteração',pad.l+cW/2,H-3);
  ctx.textAlign='left';  ctx.fillText('0',pad.l,H-3);
  ctx.textAlign='right'; ctx.fillText(n-1,pad.l+cW,H-3);
}

function renderConvCharts(mapId){
  const local=DATA[mapId]&&DATA[mapId].local;
  const section=document.getElementById('conv-section');
  if(!local){section.style.display='none';return;}
  section.style.display='';
  drawConvChart('conv-hc',local.hc.convergencia,'#89b4fa');
  drawConvChart('conv-sa',local.sa.convergencia,'#a6e3a1');
  drawConvChart('conv-ga',local.ga.convergencia,'#cba6f7');
}

// ── Tabela resultados online ──────────────────────────────────────────────────
function renderOnlineTable(mapId){
  const online=DATA[mapId].online;
  const tbody=document.getElementById('online-results-tbody');
  tbody.innerHTML='';
  for(const [nome,d] of Object.entries(online)){
    const ok=d.encontrado;
    const tr=document.createElement('tr');
    tr.innerHTML=
      `<td>${nome}</td>`+
      `<td class="${ok?'ok':'fail'}">${ok?'✓':'✗'}</td>`+
      `<td>${d.movimentos}</td>`+
      `<td>${d.custo_offline}</td>`+
      `<td>${d.reveladas}</td>`+
      `<td>${d.revisitadas}</td>`+
      `<td>${d.replanejamentos}</td>`+
      `<td>${d.t}</td>`+
      `<td>${d.razao!=null?d.razao:'—'}</td>`;
    tbody.appendChild(tr);
  }
}

// ── Boot ──────────────────────────────────────────────────────────────────────
initMapBar();
const firstMap = Object.keys(DATA)[0];
if(firstMap) loadMap(firstMap);
</script>
</body>
</html>"""


def gerar_csv_local(all_data: dict, outdir: str) -> str:
    """Gera resultados_semana2.csv com métricas da busca local por mapa e algoritmo."""
    caminho = os.path.join(outdir, 'resultados_semana2.csv')
    campos = [
        'mapa', 'algoritmo',
        'melhor_custo', 'pior_custo', 'custo_medio',
        'tempo_medio_ms', 'iteracoes_media', 'n_execucoes',
        'taxa_sucesso_%', 'custo_otimo', 'gap_%',
    ]
    with open(caminho, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for data in all_data.values():
            if data['local'] is None:
                continue
            label = data['grid']['label']
            for key in ('hc', 'sa', 'ga'):
                m = data['local'][key]
                w.writerow({
                    'mapa':           label,
                    'algoritmo':      m['algoritmo'],
                    'melhor_custo':   m['melhor_custo'],
                    'pior_custo':     m['pior_custo'],
                    'custo_medio':    m['custo_medio'],
                    'tempo_medio_ms': m['tempo_ms'],
                    'iteracoes_media':m['iteracoes'],
                    'n_execucoes':    m['n_execucoes'],
                    'taxa_sucesso_%': m['taxa_sucesso'],
                    'custo_otimo':    m['custo_otimo'] if m['custo_otimo'] is not None else '',
                    'gap_%':          m['gap']         if m['gap']         is not None else '',
                })
    return caminho


def main():
    print('Gerando dados dos algoritmos...')
    all_data = collect_all()
    if not all_data:
        print('Nenhum mapa carregado.')
        sys.exit(1)

    data_json = json.dumps(all_data, ensure_ascii=False, separators=(',', ':'))
    html = HTML.replace('__DATA__', data_json)

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)

    csv_path = gerar_csv_local(all_data, BASE)

    size_kb = len(html.encode()) / 1024
    print(f'\nGerado: {OUT}  ({size_kb:.0f} KB)')
    print(f'CSV:    {csv_path}')
    print(f'Abra no navegador:  xdg-open {OUT}')


if __name__ == '__main__':
    main()
