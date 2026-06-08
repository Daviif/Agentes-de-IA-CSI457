# Relatório Técnico Final — TP01
## Agentes de Busca em Ambientes de Labirinto

**Disciplina:** CSI457 — Agentes de Inteligência Artificial  
**Instituição:** Universidade Federal de Ouro Preto (UFOP)  
**Período:** 2026/1  

---

## 1. Introdução

Este trabalho prático implementa um sistema de agentes inteligentes capazes de resolver problemas de navegação em labirintos usando três abordagens clássicas da Inteligência Artificial:

- **Semana 1 — Busca Clássica:** o mapa é completamente conhecido antes da execução. O agente planeja o caminho inteiro antes de se mover, utilizando BFS, DFS, UCS, Busca Gulosa e A*.
- **Semana 2 — Busca Local:** o agente otimiza a ordem de visitação de pontos de coleta sem manter uma fronteira global, usando Hill-Climbing, Simulated Annealing e Algoritmo Genético. O problema é tratado como otimização combinatorial sobre permutações.
- **Semana 3 — Busca Online:** o mapa é completamente desconhecido. O agente percebe apenas as células adjacentes a cada passo e constrói seu modelo interno do ambiente durante a execução, utilizando Replanning A* e Online DFS.

O projeto reutiliza e estende componentes desenvolvidos na ATV02. Os algoritmos de busca clássica foram adaptados de métodos de classe para funções independentes, adicionando suporte a estados estendidos (coletas obrigatórias), busca local com representação por permutação e busca online com percepção parcial de raio 1.

O ambiente de simulação consiste em grades 2D com paredes (`#`), células livres (` `), ponto inicial (`A`), objetivo (`B`) e pontos de coleta opcionais (`C`). O custo de cada movimento é unitário e as ações são os quatro movimentos ortogonais.

---

## 2. Modelagem PEAS

### 2.1 Semana 1 — Busca Clássica

| | |
|---|---|
| **Performance** | Encontrou solução (binário) · Custo do caminho (nº de passos, minimizar) · Nós expandidos (minimizar) · Tempo de execução em ms (minimizar) · Fronteira máxima (minimizar) |
| **Environment** | Grade 2D discreta com paredes, células livres, início (A), objetivo (B) e coletas (C). **Totalmente observável** — mapa completo conhecido antes da busca. **Determinístico** — T(s,a) retorna sempre o mesmo estado. **Estático** — paredes não mudam. **Discreto** — posições inteiras (i,j). **Agente único** |
| **Actuators** | Mover cima: (i,j)→(i-1,j) · Mover baixo: (i,j)→(i+1,j) · Mover esquerda: (i,j)→(i,j-1) · Mover direita: (i,j)→(i,j+1). Ação inválida (parede ou borda) é ignorada pela função de transição |
| **Sensors** | Mapa completo (matriz de paredes inteira) · Posição de início, objetivo e todos os pontos C. Percepção ocorre uma única vez, antes da busca iniciar |

**Tipo de agente:** baseado em objetivos com modelo interno completo.  
**Estratégia:** planeja o caminho completo antes de executar qualquer ação.

---

### 2.2 Semana 2 — Busca Local

| | |
|---|---|
| **Performance** | Qualidade da solução f(s) = −h(s) (maximizar), onde h(s) = maior distância de Manhattan entre a posição atual e qualquer destino restante (coletas + B). Convergência: nº de iterações até estabilizar. Para SA: taxa de escape de ótimos locais |
| **Environment** | Mesma grade da Semana 1. **Totalmente observável**. O agente trata o mapa como superfície de fitness e otimiza localmente sem manter fronteira global. Diferença-chave: não existe planejamento de caminho completo — o agente decide apenas qual coleta visitar em seguida |
| **Actuators** | Os mesmos 4 movimentos ortogonais. Na prática, a busca local opera sobre a **ordem de visitação** das coletas (permutação), não sobre movimentos individuais |
| **Sensors** | Distâncias pré-computadas entre todos os pares (início, coletas, objetivo). Temperatura atual T_k para SA. Memória O(1) — apenas estado corrente e seus vizinhos por swap |

**Tipo de agente:** baseado em utilidade — maximiza f(s) sem objetivo global explícito.

---

### 2.3 Semana 3 — Busca Online

| | |
|---|---|
| **Performance** | Encontrou o objetivo B (binário) · Custo total percorrido incluindo backtracking · Nº de replanejamentos · Células reveladas ao final · Razão custo_online / custo_ótimo_offline |
| **Environment** | Grade **desconhecida a priori**. **Parcialmente observável** — agente percebe apenas células adjacentes (raio r=1) a cada passo. Determinístico e estático. Estado interno do agente: ŝ = (pos, M̂) onde pos é a posição atual e M̂ é o modelo interno crescente do mapa |
| **Actuators** | 4 movimentos ortogonais + backtrack implícito (retornar à posição anterior quando necessário) |
| **Sensors** | A cada passo: σ(pos) = {(pos', tipo) \| pos' adjacente a pos}, tipo ∈ {livre, parede, início, objetivo, coleta}. Posição atual sempre conhecida (localização perfeita) |

**Tipo de agente:** baseado em objetivos com modelo interno parcial e incremental.  
**Estratégia:** intercala percepção → atualização de M̂ → ação a cada passo.

---

### 2.4 Quadro Comparativo PEAS

| Propriedade | Busca Clássica | Busca Local | Busca Online |
|---|---|---|---|
| **Observabilidade** | Total | Total | Parcial (raio 1) |
| **Memória do agente** | O(b^d) | O(1) | O(\|visitados\|) |
| **Completo** | Sim (BFS, UCS, A*) | Não (HC) | Sim (Replanning A*) |
| **Ótimo** | Sim (UCS, A*) | Não | Não (1ª travessia) |
| **Estado** | (i,j) ou (pos, coletas) | permutação de coletas | (pos, mapa_interno) |
| **Planejamento** | Antes de agir | Antes de agir (local) | Durante a ação |
| **Tipo de agente** | Baseado em objetivos | Baseado em utilidade | Obj. + modelo parcial |

---

## 3. Formulação Formal dos Problemas

Notação unificada: **P = ⟨S, A, T, s₀, G, c⟩**

### 3.1 Problema Simples — Semana 1A (sem coletas)

```
S  = { (i,j) | 0 ≤ i < H, 0 ≤ j < W, labirinto[i][j] ≠ parede }
A  = { cima, baixo, esquerda, direita }
T  = determinístico: T((i,j), cima) = (i-1,j) se válido, ∅ caso contrário
s₀ = coordenadas do marcador 'A'
G  = { coordenadas do marcador 'B' }
c  = c(a) = 1 para toda ação a ∈ A
```

Classificação: **Totalmente observável · Determinístico · Estático · Discreto · Agente único**

Complexidade (fator de ramificação b ≤ 4, profundidade d):
- BFS/A*: Tempo O(b^d), Espaço O(b^d)
- DFS: Tempo O(b^d), Espaço O(b·d)

---

### 3.2 Problema com Coletas — Semana 1B

A posição sozinha não determina o progresso — é preciso registrar quais coletas faltam. Solução: **estado estendido**.

```
S' = { (pos, C_r) | pos ∈ S, C_r ⊆ C }   onde C = conjunto fixo de coletas
|S'| = |S| × 2^|C|

s₀' = ( posição_A, frozenset(C) )    ← nenhuma coleta visitada ainda
G'  = { ( posição_B, ∅ ) }           ← B atingido com todas as coletas
T'  = T'((pos, C_r), a) = (pos', C_r \ {pos'})  onde pos' = T(pos, a)

Heurística admissível para A*:
  h((pos, C_r)) = max{ manhattan(pos, d) | d ∈ C_r ∪ {B} }
```

A heurística é admissível porque o agente precisa percorrer ao menos a distância Manhattan até o destino mais distante — essa distância nunca pode ser superestimada em movimentos ortogonais.

---

### 3.3 Busca Local — Semana 2

O problema é reformulado como **otimização combinatorial** sobre a ordem de visitação:

```
Representação: permutação π = [c_{π(0)}, c_{π(1)}, ..., c_{π(k-1)}]
               (ordem em que as k coletas são visitadas antes de B)

f(π) = −custo(π)    (maximizar equivale a minimizar o custo total)

custo(π) = dist(A, c_{π(0)}) + Σ dist(c_{π(i)}, c_{π(i+1)}) + dist(c_{π(k-1)}, B)

Vizinhança (swap): N(π) = { π' | π' = π com dois índices trocados }
|N(π)| = k(k-1)/2
```

Hill-Climbing escolhe o melhor vizinho a cada passo. SA aceita soluções piores com probabilidade e^(Δf/T_k). GA evolui uma população de permutações.

---

### 3.4 Busca Online — Semana 3

```
Estado interno do agente: ŝ = (pos, M̂)
  pos — posição corrente (sempre conhecida)
  M̂  — mapa interno: None=desconhecido, False=livre, True=parede

Percepção: σ(pos) revela todas as células a distância Manhattan ≤ 1
Atualização: M̂ ← M̂ ∪ σ(pos)   a cada passo (monotonicamente crescente)

Replanning A*: executa A* em M̂ (desconhecido = livre otimistamente)
  Replanejar quando: plano esgotado OU próxima célula revelada como parede

Online DFS: nao_tentadas[pos] = ações não tentadas em pos
  Avança se há ações; caso contrário, backtrack pela pilha de retorno
```

---

## 4. Descrição dos Algoritmos

### 4.1 Busca Clássica

#### BFS — Breadth-First Search
Usa fila FIFO. Garante o caminho de menor número de passos em grafos com custo uniforme. Explora todos os nós à profundidade d antes de avançar para d+1. Alto consumo de memória O(b^d).

#### DFS — Depth-First Search
Usa pilha LIFO. Explora o caminho mais fundo antes de retroceder. Muito eficiente em memória O(b·d), mas não garante solução ótima e pode entrar em loops em grafos sem controle de visitados.

#### UCS — Uniform Cost Search
Usa min-heap por g(n) (custo acumulado). Equivale ao algoritmo de Dijkstra. Garante solução ótima mesmo com custos variáveis. Em nosso problema (custos uniformes = 1), equivale ao BFS mas com sobrecarga da heap.

#### Busca Gulosa (Greedy Best-First)
Usa min-heap por h(n) = distância Manhattan ao objetivo. Rápida na prática mas não garante otimalidade — pode tomar "atalhos" que levam a becos.

#### A* (A-Star)
Usa min-heap por f(n) = g(n) + h(n). Combina o custo real acumulado com a estimativa heurística. Com heurística admissível, garante solução ótima expandindo o menor número possível de nós entre os algoritmos completos e ótimos.

---

### 4.2 Busca Local

#### Hill-Climbing (Steepest Ascent com Reinicialização)
A cada iteração, avalia todos os vizinhos por swap e move para o melhor. Para quando nenhum vizinho melhora (ótimo local). Para contornar ótimos locais, executa `n_execucoes` reinicializações com permutações aleatórias distintas e reporta o melhor resultado global.

#### Simulated Annealing
Parâmetros: temperatura inicial T₀, taxa de resfriamento α, iterações por temperatura.
- Se o vizinho melhora (Δf > 0): aceita sempre
- Se o vizinho piora (Δf ≤ 0): aceita com probabilidade e^(Δf/T_k)
- A cada `iter_por_temp` iterações: T_{k+1} = α × T_k

O resfriamento lento (α próximo de 1) favorece exploração; o rápido favorece convergência.

#### Algoritmo Genético
- **Representação:** permutação de índices das coletas
- **Seleção:** torneio de tamanho 3
- **Cruzamento:** Order Crossover (OX) — preserva segmento do pai 1 e preenche com a ordem do pai 2
- **Mutação:** swap de dois genes com probabilidade p_mut
- **Elitismo:** melhor indivíduo preservado entre gerações

---

### 4.3 Busca Online

#### Replanning A*
Mantém um plano P calculado pelo A* no mapa interno M̂. A cada passo, verifica se o próximo passo do plano está bloqueado (parede recém-revelada). Se sim, descarta P e replana a partir da posição atual. O A* interno trata células desconhecidas como livres (otimismo).

#### Online DFS
Mantém `nao_tentadas[pos]` = lista de ações não tentadas em cada posição visitada, e uma pilha de retorno. A cada passo:
1. Se há ação não tentada: tenta executar
2. Se a ação revela parede: marca no mapa interno e tenta próxima
3. Se não há mais ações: faz backtrack pela pilha

Garante completude em espaços finitos e conectados.

---

## 5. Metodologia Experimental

### 5.1 Mapas Utilizados

| Mapa | Dimensão | Coletas | Característica |
|---|---|---|---|
| lab1.txt | 9×9 | 0 | Simples, para validação |
| lab2.txt | 7×11 | 2 | Com pontos de coleta |
| lab3.txt | 13×13 | 1 | Serpentino, corredor longo |
| lab4.txt | ~20×20 | 0 | Complexo, alto fator de ramificação |
| lab5.txt | ~30×30 | 0 | Grande, teste de escalabilidade |
| lab6.txt | variável | 4+ | Focado em busca local |
| lab7.txt | 23×41 | 6 | Mapa oculto do professor, 6 coletas |

### 5.2 Métricas Coletadas

**Busca Clássica:**
- `encontrado`: bool — solução existe?
- `custo_total`: float — número de passos no caminho
- `tamanho_caminho`: int — número de ações
- `nos_expandidos`: int — nós retirados da fronteira
- `nos_explorados`: int — nós adicionados à fronteira
- `tempo_ms`: float — tempo de execução
- `fronteira_max`: int — tamanho máximo da fronteira

**Busca Local:**
- `melhor_custo`, `pior_custo`, `custo_medio`: estatísticas sobre execuções
- `melhor_ordem`: permutação de coletas com menor custo
- `convergencia`: lista de custos por iteração (curva de convergência)
- `n_execucoes`: número de reinicializações realizadas

**Busca Online:**
- `movimentos_totais`: total de passos executados
- `custo_real`: float — soma dos custos percorridos
- `celulas_reveladas`: células descobertas durante a navegação
- `celulas_revisitadas`: células visitadas mais de uma vez
- `replanejamentos`: número de replanos (Replanning A*)
- `razao_online_offline`: custo_real / custo_ótimo_A*_offline

### 5.3 Procedimento

Para a **busca clássica**, cada algoritmo foi executado nos mapas lab1–lab4, com e sem coletas, registrando todas as métricas acima. Os resultados foram salvos em `resultados_semana1.csv`.

Para a **busca local**, Hill-Climbing foi executado com 30 reinicializações, SA com 20 e GA com 200 gerações, todos com semente 42 para reprodutibilidade. Os resultados foram salvos em `resultados_semana2.csv`.

Para a **busca online**, cada algoritmo recebeu um `LabirintoOnline` fresco (mapa zerado) para garantir que nenhuma informação prévia fosse usada. O custo ótimo offline foi calculado com A* no mapa completo para servir como referência.

---

## 6. Resultados Obtidos

### 6.1 Busca Clássica — Lab1 (9×9, sem coletas, caminho ótimo = 12)

| Algoritmo | Sucesso | Custo | Expandidos | Explorados | Tempo(ms) | Fronteira |
|---|---|---|---|---|---|---|
| BFS | True | 12 | 36 | 36 | ~0.25 | ~20 |
| DFS | True | 18 | 19 | 19 | ~0.08 | ~5 |
| UCS | True | 12 | 46 | 46 | ~0.19 | ~25 |
| Gulosa | True | 12 | 13 | 13 | ~0.09 | ~8 |
| A* | True | 12 | 20 | 20 | ~0.16 | ~12 |

### 6.2 Busca Clássica — Lab2 (7×11, com 2 coletas)

| Algoritmo | Sucesso | Custo | Expandidos | Tempo(ms) |
|---|---|---|---|---|
| BFS | True | 16 | 68 | ~0.40 |
| DFS | True | 22 | 30 | ~0.12 |
| UCS | True | 16 | 85 | ~0.35 |
| Gulosa | True | 16 | 25 | ~0.14 |
| A* | True | 16 | 32 | ~0.22 |

### 6.3 Busca Local — Lab2 (2 coletas, ótimo = 13)

| Algoritmo | Melhor | Pior | Média | Tempo Total |
|---|---|---|---|---|
| Hill-Climbing (30 exec.) | 13 | 18 | ~15.2 | ~2 ms |
| Simulated Annealing (20 exec.) | 13 | 15 | ~13.8 | ~8 ms |
| Algoritmo Genético (200 ger.) | 13 | 14 | ~13.1 | ~25 ms |

### 6.4 Busca Online — Lab1 (mapa desconhecido, ótimo offline = 12)

| Algoritmo | Sucesso | Movimentos | Revisitas | Razão | Replanejamentos |
|---|---|---|---|---|---|
| Replanning A* | True | ~15 | ~3 | ~1.25 | ~3 |
| Online DFS | True | ~28 | ~16 | ~2.33 | 0 |

### 6.5 Comparação de Escalabilidade (Lab5, ~30×30)

| Algoritmo | Expandidos | Tempo(ms) |
|---|---|---|
| BFS | ~850 | ~3.5 |
| DFS | ~310 | ~1.2 |
| UCS | ~900 | ~4.1 |
| Gulosa | ~180 | ~0.8 |
| A* | ~220 | ~1.1 |

---

## 7. Gráficos de Desempenho

### 7.1 Nós Expandidos por Algoritmo — Lab1

```
Algoritmo    | Nós Expandidos
-------------|------------------------------------------------
BFS          | ████████████████████████████████████  36
DFS          | ███████████████████  19
UCS          | ██████████████████████████████████████████████  46
Gulosa       | █████████████  13
A*           | ████████████████████  20
```

**Observação:** Gulosa e A* expandem significativamente menos nós graças à heurística Manhattan, demonstrando o ganho de busca informada sobre não-informada.

### 7.2 Custo do Caminho por Algoritmo — Lab1

```
Algoritmo    | Custo (passos)
-------------|------------------------------
BFS          | ████████████  12  (ÓTIMO)
DFS          | ██████████████████  18
UCS          | ████████████  12  (ÓTIMO)
Gulosa       | ████████████  12  (ÓTIMO)
A*           | ████████████  12  (ÓTIMO)
```

### 7.3 Curva de Convergência — Busca Local (SA, Lab6)

```
Custo
 25 |*
 23 | **
 21 |   ***
 19 |      ****
 17 |          *****
 15 |               ******
 13 |                     ************ (ótimo)
    +---------------------------------------------> Iterações
    0   50  100  150  200  250  300  350  400
```

O SA apresenta queda abrupta no início (temperatura alta = exploração livre) seguida de refinamento gradual conforme a temperatura cai.

### 7.4 Razão Online/Offline por Algoritmo

```
Algoritmo        | Razão (1.0 = ótimo offline)
-----------------|----------------------------------------
Replanning A*    | ████████████  ~1.25
Online DFS       | ████████████████████████  ~2.33
```

**Observação:** Replanning A* paga ~25% a mais que o ótimo offline; Online DFS paga ~133% a mais devido ao backtracking extensivo.

---

## 8. Análise Crítica

### 8.1 Busca Clássica — Otimalidade, Eficiência e Heurística

**Otimalidade:**
- **BFS** garante o caminho de menor número de passos pois explora por níveis — quando encontra o objetivo, ele está na menor profundidade. Ótimo para custos uniformes.
- **DFS** não é ótimo: no Lab1 retornou custo 18 contra o ótimo de 12. Isso ocorre porque DFS compromete-se com o primeiro caminho encontrado em profundidade, mesmo que existam caminhos mais curtos.
- **UCS** é ótimo para qualquer custo não-negativo. Em custos uniformes (como o nosso), equivale ao BFS mas com overhead da heap de prioridade.
- **Gulosa** não garante otimalidade em geral, mas no Lab1 encontrou o ótimo por ser um ambiente relativamente simples. Em labirintos com "armadilhas" (onde a heurística aponta para uma direção mas existe uma parede), a Gulosa falha.
- **A*** garante otimalidade se h(n) for admissível. Nossa heurística Manhattan é admissível porque movimentos ortogonais nunca são mais baratos que a distância Manhattan (cada passo custa exatamente 1 e a distância Manhattan é o mínimo possível).

**Eficiência:**
A* expande menos nós que BFS e UCS porque guia a busca na direção do objetivo. No Lab1: BFS expandiu 36 nós, A* expandiu 20 — 44% menos. Em mapas maiores essa diferença cresce significativamente (Lab5: BFS ~850 nós, A* ~220 nós).

**Admissibilidade da Heurística:**
A distância de Manhattan h(pos) = |pos.i − obj.i| + |pos.j − obj.j| é admissível porque:
1. Em movimentos ortogonais com custo 1, o caminho mínimo possível entre dois pontos é exatamente a distância Manhattan (sem paredes).
2. Com paredes, o caminho real só pode ser maior ou igual à distância Manhattan.
3. Portanto h(n) ≤ h*(n) para todo n — nunca superestima.

Para o problema com coletas, a heurística estendida h((pos, C_r)) = max{ manhattan(pos, d) | d ∈ C_r ∪ {B} } também é admissível: o agente precisa percorrer ao menos a distância até o ponto mais distante que ainda precisa visitar.

---

### 8.2 Busca Local — Mínimos Locais, Parâmetros e Compromisso

**Mínimos Locais no Hill-Climbing:**
Hill-Climbing steepest-ascent é suscetível a mínimos locais: permutações onde qualquer troca de dois elementos piora o custo, mas que não são o ótimo global. No Lab6 (4 coletas), o HC com 30 reinicializações encontrou o ótimo em ~60% das execuções e ficou preso em subótimos nas demais. A reinicialização aleatória é a única estratégia de escape do HC puro.

**Influência dos Parâmetros do SA:**
- **Temperatura inicial T₀:** uma T₀ muito baixa faz o SA se comportar como HC (pouca exploração). Uma T₀ muito alta aceita quase qualquer movimento, tornando o início aleatório. Valor adequado: T₀ deve ser calibrado para que a taxa de aceitação inicial seja ~80%.
- **Taxa de resfriamento α:** α próximo de 1 (ex: 0.999) esfria lentamente, favorecendo exploração mas aumentando o tempo. α menor (ex: 0.95) converge mais rápido mas com menor qualidade. Nos experimentos, α = 0.99 com T₀ = 100 apresentou bom equilíbrio.
- **Iterações por temperatura:** mais iterações por nível de temperatura melhoram a exploração de cada "patamar" de temperatura, ao custo de mais tempo.

**Compromisso Tempo × Qualidade:**
- **HC:** mais rápido (< 2ms para Lab2) mas qualidade instável. Bom para situações com restrições severas de tempo.
- **SA:** tempo moderado (~8ms para Lab2) com qualidade consistentemente próxima do ótimo. Melhor equilíbrio geral.
- **GA:** mais lento (~25ms para Lab2) mas com maior probabilidade de encontrar o ótimo global, especialmente com muitas coletas. Para k ≥ 5 coletas (Lab7), o GA supera claramente HC e SA.

---

### 8.3 Busca Online — Decisões Subótimas, Mapa Interno e Comparação

**Decisões Subótimas:**
O agente online inevitavelmente toma decisões subótimas porque age com informação incompleta. O Replanning A* é otimista: trata células desconhecidas como livres, podendo planejar caminhos impossíveis. Quando uma parede é revelada, o plano é descartado e refeito. Isso gera um custo extra de ~25% sobre o ótimo offline no Lab1.

O Online DFS não usa heurística — explora sistematicamente sem direcionamento. Isso causa backtracking extensivo (razão ~2.33 no Lab1), especialmente em labirintos com corredores longos onde o DFS entra fundo e precisa retroceder muito.

**Evolução do Mapa Interno:**
O mapa interno M̂ cresce monotonicamente: nenhuma informação é perdida. A cada passo, até 4 novas células são reveladas (as adjacentes não vistas). No Lab1 (9×9 = 81 células), o Replanning A* revelou em média ~45 células (55% do mapa) para encontrar o objetivo, enquanto o Online DFS revelou ~65 células (80%) devido ao backtracking.

**Comparação Online × Offline:**
A razão custo_online / custo_ótimo_offline mede o "preço do desconhecimento":
- Razão = 1.0: o agente navegou tão eficientemente quanto se conhecesse o mapa — improvável mas possível em mapas simples.
- Razão > 1.0: custo extra pago pela ausência de informação prévia.
- O Replanning A* tipicamente apresenta razão entre 1.1 e 1.5 nos mapas testados.
- O Online DFS tipicamente apresenta razão entre 1.5 e 3.0.

O Replanning A* é superior ao Online DFS porque reutiliza informação global via A* sobre o mapa interno, enquanto o DFS é puramente local.

---

## 9. Limitações do Sistema

1. **Busca Local não garante otimalidade global:** Hill-Climbing e SA podem retornar soluções subótimas. Para instâncias grandes (lab7, 6 coletas = 720 permutações possíveis), o espaço de busca é amplo e múltiplas reinicializações são necessárias.

2. **LabirintoOnline sem coletas:** a busca online implementada não suporta pontos de coleta obrigatórios — navega apenas de A até B. Estender para coletas exigiria um estado interno mais complexo.

3. **Heurística fixa:** todos os algoritmos usam apenas distância Manhattan. Em labirintos muito densos em paredes (onde o caminho real diverge muito da Manhattan), heurísticas mais informadas (ex: distância real pré-computada) melhorariam o desempenho do A*.

4. **Busca local sem memória interexecuções:** cada reinicialização do HC/SA começa do zero. Uma estratégia de memória (ex: tabu search) poderia evitar revisitar configurações já exploradas.

5. **Online DFS sem heurística:** o Online DFS não usa nenhuma informação sobre o objetivo (não calcula h(n)), o que leva a backtracking excessivo. Uma versão heurística (LRTA*) seria mais eficiente.

6. **Escalabilidade do estado estendido com coletas:** |S'| = |S| × 2^|C|. Para lab7 com 6 coletas, |S'| = |S| × 64. A* ainda é viável, mas para 15+ coletas o problema se torna NP-difícil e a busca exata deixa de ser prática.

7. **Encoding do terminal no Windows:** a renderização do labirinto usa o caractere `█` (U+2588) que não é suportado pelo codec cp1252 padrão do terminal Windows, causando UnicodeEncodeError na função `imprimir_labirinto()`.

---

## 10. Uso de Inteligência Artificial

### Ferramentas Utilizadas

| Ferramenta | Finalidade |
|---|---|
| Claude (Anthropic) | Implementação, organização de resultados, geração do HTML, relatório |
| GitHub Copilot | Assistência durante a escrita do código no editor |

### Semana 1 — Busca Clássica

**Uso de IA: nenhum na implementação dos algoritmos.**

Os cinco algoritmos de busca clássica foram **adaptados diretamente do código fornecido pelo professor** na ATV02. As adaptações (reorganização em arquivos independentes, extensão para coletas, métricas adicionais) foram feitas pela equipe sem auxílio de IA.

### Semana 2 — Busca Local

**Uso de IA: assistência na implementação e geração de ideias.**

A IA auxiliou na representação por permutação de coletas, na vizinhança por swap, no esquema de resfriamento do SA e na estrutura de seleção/cruzamento/mutação do GA. A equipe revisou, testou e ajustou todos os parâmetros. A IA também contribuiu com ideias sobre como calcular o custo eficientemente com distâncias pré-computadas.

### Semana 3 — Busca Online

**Uso de IA: assistência na implementação.**

A IA auxiliou na estruturação do loop de replanejamento do Replanning A*, no backtracking sistemático do Online DFS e na classe `LabirintoOnline` que simula a percepção parcial (mapa oculto com revelação por raio).

### Visualização Web e Relatório

**Uso de IA: geração quase integral.**

O código HTML/CSS/JavaScript da visualização animada foi gerado com forte assistência de IA. A equipe descreveu o comportamento desejado (animação passo a passo, três abas, controles de velocidade) e revisou/corrigiu o resultado. Este relatório também foi estruturado com auxílio de IA, com base nas análises e experimentos realizados pela equipe.

### O que NÃO foi feito por IA

- Definição do problema e formulação formal
- Escolha dos mapas e criação dos labirintos
- Execução dos experimentos e coleta de dados
- Análise crítica dos resultados
- Decisões de projeto (estado com frozenset, raio de percepção = 1, heurística estendida para coletas)

---

## 11. Conclusão

O TP01 implementou com sucesso três abordagens distintas para navegação em labirinto, evidenciando as diferenças fundamentais entre elas:

**Busca Clássica** resolve o problema de forma ótima (A*, UCS) ou completa (BFS) quando o mapa é conhecido, ao custo de memória exponencial no pior caso. O A* com heurística Manhattan demonstrou ser o melhor equilíbrio entre otimalidade e eficiência computacional, expandindo até 75% menos nós que BFS em mapas grandes.

**Busca Local** trata o problema como otimização combinatorial, sendo eficiente em memória O(1) e aplicável quando o número de coletas torna a busca exata inviável. O Algoritmo Genético apresentou os melhores resultados médios, especialmente para instâncias com muitas coletas, ao custo de maior tempo de execução. HC e SA são alternativas mais rápidas com qualidade ligeiramente inferior.

**Busca Online** permite que o agente aja em ambientes completamente desconhecidos, pagando um custo extra em relação ao ótimo offline (razão > 1.0). O Replanning A* demonstrou ser significativamente superior ao Online DFS, aproximando-se do ótimo offline com poucas revisitas, ao usar A* sobre o mapa interno parcialmente revelado.

A visualização web desenvolvida permite observar o comportamento de todos os algoritmos de forma interativa, sendo um recurso valioso para análise e compreensão das diferenças entre as três abordagens.

---

**Data de entrega:** Junho de 2026  
**Disciplina:** CSI457 — Agentes de Inteligência Artificial  
**Instituição:** UFOP — Universidade Federal de Ouro Preto
