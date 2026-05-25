#!/usr/bin/env python3
"""Gera visualizacao.html — animação web dos algoritmos de busca."""

import sys, os, json, math, heapq, itertools, time
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labirinto import LabirintoBusca, LabirintoComColetas, No

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, 'visualizacao.html')

MAPAS = {
    '1': (os.path.join(BASE, 'mapas', 'lab1.txt'), 'Lab 1 — simples'),
    '2': (os.path.join(BASE, 'mapas', 'lab2.txt'), 'Lab 2 — coletas'),
    '3': (os.path.join(BASE, 'mapas', 'lab3.txt'), 'Lab 3 — serpentino'),
    '4': (os.path.join(BASE, 'mapas', 'lab4.txt'), 'Lab 4 — complexo'),
}


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


def ucs_gen(lab):      return _prio_gen(lab, lambda n: n.g)
def gulosa_gen(lab):   return _prio_gen(lab, lambda n: lab.h(n.estado))
def a_estrela_gen(lab):return _prio_gen(lab, lambda n: n.g + lab.h(n.estado))


def run_gen(gen):
    """Coleta frames com delta encoding e mede o tempo de execução."""
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


def collect_all():
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
            'h': lab_base.altura,
            'w': lab_base.largura,
            'walls': lab_base.paredes,
            'start': list(lab_base.inicio),
            'goal':  list(lab_base.objetivo),
            'coletas': [list(c) for c in lab_base.coletas],
            'label': label,
        }

        print(f'  lab{map_id}:', end='', flush=True)
        algos = {}
        for name, make in [
            ('BFS',    lambda: bfs_gen(lab)),
            ('DFS',    lambda: dfs_gen(lab)),
            ('UCS',    lambda: ucs_gen(lab)),
            ('Gulosa', lambda: gulosa_gen(lab)),
            ('A*',     lambda: a_estrela_gen(lab)),
        ]:
            algos[name] = run_gen(make())
            print(f' {name}', end='', flush=True)
        print()
        all_data[map_id] = {'grid': grid, 'algorithms': algos}
    return all_data


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
}
body { background:var(--bg); color:var(--text); font-family:'Courier New',monospace; min-height:100vh; padding:14px 10px; }

.header { text-align:center; margin-bottom:12px; }
.header h1 { font-size:1.25rem; font-weight:bold; letter-spacing:.04em; }
.header p  { font-size:.77rem; color:var(--subtext); margin-top:3px; }

.map-bar { display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin-bottom:12px; }
.map-btn { background:var(--surface0); color:var(--subtext); border:1px solid var(--surface1);
           border-radius:6px; padding:5px 14px; cursor:pointer; font-family:inherit; font-size:.82rem; }
.map-btn:hover { background:var(--surface1); color:var(--text); }
.map-btn.active { background:#89b4fa; color:#1e1e2e; border-color:#89b4fa; font-weight:bold; }

.grids-area { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:12px; }
@media(max-width:800px){ .grids-area{ grid-template-columns:repeat(2,1fr); } }
@media(max-width:520px){ .grids-area{ grid-template-columns:1fr; } }

.algo-box { background:var(--mantle); border-radius:8px; padding:10px 8px 12px;
            display:flex; flex-direction:column; align-items:center; gap:8px; }
.algo-title { font-size:.8rem; font-weight:bold; color:var(--subtext); text-align:center;
              min-height:1.1em; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:100%; }
.algo-title.running { color:var(--text); }
.algo-title.done    { color:#a6e3a1; }
.algo-title.no-path { color:#f38ba8; }

.maze-wrap { display:flex; justify-content:center; }
.maze { display:grid; gap:2px; background:var(--bg); padding:3px; border-radius:4px; }
.cell { border-radius:2px; }

.legend-box { background:var(--mantle); border-radius:8px; padding:12px 16px;
              display:flex; flex-direction:column; justify-content:center; gap:6px; }
.legend-box h3 { font-size:.78rem; color:var(--overlay); text-align:center; margin-bottom:2px;
                 letter-spacing:.08em; text-transform:uppercase; }
.legend-item { display:flex; align-items:center; gap:8px; font-size:.76rem; color:var(--subtext); }
.swatch { width:14px; height:14px; border-radius:3px; flex-shrink:0; }

.controls { display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:12px;
            background:var(--mantle); border-radius:8px; padding:10px 20px; }
.ctrl-btn { background:var(--surface0); color:var(--text); border:1px solid var(--surface1);
            border-radius:6px; padding:6px 18px; cursor:pointer; font-family:inherit;
            font-size:.88rem; min-width:96px; text-align:center; }
.ctrl-btn:hover { background:var(--surface1); }
.ctrl-btn.is-play  { border-color:#a6e3a1; color:#a6e3a1; }
.ctrl-btn.is-pause { border-color:#f38ba8; color:#f38ba8; }
.speed-group { display:flex; align-items:center; gap:8px; font-size:.82rem; color:var(--subtext); }
input[type=range] { accent-color:#89b4fa; width:130px; cursor:pointer; }
#speed-val { min-width:2ch; color:#89b4fa; font-weight:bold; }
</style>
</head>
<body>

<div class="header">
  <h1>Busca em Labirinto — CSI457</h1>
  <p>BFS · DFS · UCS · Gulosa · A* — expansão em tempo real</p>
</div>

<div class="map-bar" id="map-bar"></div>

<div class="grids-area">
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
    <div class="legend-item"><div class="swatch" style="background:var(--coleta)"></div>Coleta obrigatória (C)</div>
    <div class="legend-item"><div class="swatch" style="background:var(--explored)"></div>Nó explorado</div>
    <div class="legend-item"><div class="swatch" style="background:var(--frontier)"></div>Fronteira (aberta)</div>
    <div class="legend-item"><div class="swatch" style="background:var(--path)"></div>Caminho encontrado</div>
    <div class="legend-item"><div class="swatch" style="background:var(--wall)"></div>Parede</div>
    <div class="legend-item"><div class="swatch" style="background:var(--free);border:1px solid #aaa"></div>Livre</div>
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

<script>
const DATA = __DATA__;
const ALGOS = ['BFS','DFS','UCS','Gulosa','A*'];

// currentMap, per-algo frame index, done flags, animation timer
let currentMap=null, frameIdx={}, doneAlgo={}, playing=false, timer=null;
// cells[algo] = [{div, key, r, c}]
let cells={};
// algoState[algo] = {exp: Set<"r,c">, frt: Set<"r,c">, expCount:int, path:null|array}
let algoState={};

function initMapBar(){
  const bar=document.getElementById('map-bar');
  for(const [id,{grid}] of Object.entries(DATA)){
    const btn=document.createElement('button');
    btn.className='map-btn'; btn.textContent=grid.label; btn.dataset.id=id;
    btn.onclick=()=>loadMap(id); bar.appendChild(btn);
  }
}

function loadMap(id){
  currentMap=id;
  document.querySelectorAll('.map-btn').forEach(b=>b.classList.toggle('active',b.dataset.id===id));
  buildGrids(); restart();
}

function buildGrids(){
  const {grid}=DATA[currentMap];
  const {h,w,walls,start,goal,coletas}=grid;
  const coletaSet=new Set(coletas.map(([r,c])=>r+','+c));
  const startKey=start[0]+','+start[1], goalKey=goal[0]+','+goal[1];
  const sz=Math.min(36,Math.floor(300/w));
  for(const algo of ALGOS){
    const mazeEl=document.getElementById('maze-'+algo);
    mazeEl.innerHTML='';
    mazeEl.style.gridTemplateColumns=`repeat(${w},${sz}px)`;
    const alCells=[];
    for(let r=0;r<h;r++) for(let c=0;c<w;c++){
      const div=document.createElement('div');
      div.className='cell'; div.style.width=sz+'px'; div.style.height=sz+'px';
      const key=r+','+c;
      div.style.backgroundColor=walls[r][c]?'var(--wall)':key===startKey?'var(--start)':key===goalKey?'var(--goal)':coletaSet.has(key)?'var(--coleta)':'var(--free)';
      mazeEl.appendChild(div); alCells.push({div,key,r,c});
    }
    cells[algo]=alCells;
  }
}

// Apply one delta to algoState[algo] (delta = {ea, fa, fr, p})
function applyDelta(algo, delta){
  const st=algoState[algo];
  for(const [r,c] of delta.ea){ st.exp.add(r+','+c); st.expCount++; }
  for(const [r,c] of delta.fa) st.frt.add(r+','+c);
  for(const [r,c] of delta.fr) st.frt.delete(r+','+c);
  if(delta.p!==null) st.path=delta.p;
}

function renderCurrent(algo){
  const {grid}=DATA[currentMap];
  const {walls,start,goal,coletas}=grid;
  const coletaSet=new Set(coletas.map(([r,c])=>r+','+c));
  const startKey=start[0]+','+start[1], goalKey=goal[0]+','+goal[1];
  const {exp,frt,path}=algoState[algo];
  const pathSet=path?new Set(path.map(([r,c])=>r+','+c)):null;
  for(const {div,key,r,c} of cells[algo]){
    let color;
    if(walls[r][c])            color='var(--wall)';
    else if(key===startKey)    color='var(--start)';
    else if(key===goalKey)     color='var(--goal)';
    else if(pathSet?.has(key)) color='var(--path)';
    else if(frt.has(key))      color='var(--frontier)';
    else if(exp.has(key))      color='var(--explored)';
    else if(coletaSet.has(key))color='var(--coleta)';
    else                       color='var(--free)';
    div.style.backgroundColor=color;
  }
}

function resetAlgoState(){
  for(const algo of ALGOS)
    algoState[algo]={exp:new Set(),frt:new Set(),expCount:0,path:null};
}

function restart(){
  stopTimer(); resetAlgoState();
  for(const algo of ALGOS){
    frameIdx[algo]=0; doneAlgo[algo]=false;
    const el=document.getElementById('title-'+algo);
    el.textContent=algo; el.className='algo-title';
    // apply frame 0
    const frames=DATA[currentMap].algorithms[algo].frames;
    if(frames.length){ applyDelta(algo,frames[0]); renderCurrent(algo); }
  }
  playing=true; updatePlayBtn(); startTimer();
}

function startTimer(){ timer=setInterval(tick,50); }
function stopTimer(){ if(timer){clearInterval(timer);timer=null;} }

function tick(){
  const speed=+document.getElementById('speed-slider').value;
  let anyActive=false;
  for(const algo of ALGOS){
    if(doneAlgo[algo]) continue;
    anyActive=true;
    const frames=DATA[currentMap].algorithms[algo].frames;
    let idx=frameIdx[algo];
    for(let s=0;s<speed&&idx<frames.length-1;s++){
      idx++;
      applyDelta(algo,frames[idx]);
    }
    frameIdx[algo]=idx;
    renderCurrent(algo);
    const finished=idx>=frames.length-1;
    updateTitle(algo,finished);
    if(finished) doneAlgo[algo]=true;
  }
  if(!anyActive){ stopTimer(); playing=false; updatePlayBtn(); }
}

function updateTitle(algo,finished){
  const el=document.getElementById('title-'+algo);
  const st=algoState[algo];
  if(finished){
    const t=DATA[currentMap].algorithms[algo].t;
    if(st.path){ el.textContent=`${algo}  ✓  custo=${st.path.length}  exp=${st.expCount}  ${t}ms`; el.className='algo-title done'; }
    else        { el.textContent=`${algo}  ✗  sem solução  ${t}ms`; el.className='algo-title no-path'; }
  } else {
    el.textContent=`${algo}  (${st.expCount} exp.)`; el.className='algo-title running';
  }
}

function togglePlay(){
  if(playing){ stopTimer(); playing=false; }
  else{
    if(Object.values(doneAlgo).every(Boolean)){ restart(); return; }
    playing=true; startTimer();
  }
  updatePlayBtn();
}

function updatePlayBtn(){
  const btn=document.getElementById('btn-play');
  if(playing){ btn.textContent='⏸  Pausar'; btn.className='ctrl-btn is-pause'; }
  else        { btn.textContent='▶  Play';   btn.className='ctrl-btn is-play';  }
}

initMapBar();
const firstMap=Object.keys(DATA)[0];
if(firstMap) loadMap(firstMap);
</script>
</body>
</html>"""


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

    size_kb = len(html.encode()) / 1024
    print(f'\nGerado: {OUT}  ({size_kb:.0f} KB)')
    print(f'Abra no navegador:  xdg-open {OUT}')


if __name__ == '__main__':
    main()
