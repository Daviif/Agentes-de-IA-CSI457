"""
Formulação Formal — Agente Inteligente em Labirinto
CSI457 · TP01 (3 semanas)

Notação unificada:  P = <S, A, T, s₀, G, c>
  S  — espaço de estados
  A  — ações disponíveis
  T  — função de transição  T: S × A → S
  s₀ — estado inicial
  G  — condição de objetivo  G ⊆ S  (ou  G: S → bool)
  c  — custo de ação  c: A → ℝ⁺
"""

# ══════════════════════════════════════════════════════════════════════════════
# SEMANA 1 — BUSCA CLÁSSICA
# Mapa totalmente conhecido, estático, determinístico.
# ══════════════════════════════════════════════════════════════════════════════

"""
──────────────────────────────────────────────────────────────────────────────
1A. Problema simples  (sem pontos de coleta)
──────────────────────────────────────────────────────────────────────────────

  S  = { (i,j) | 0 ≤ i < H, 0 ≤ j < W, labirinto[i][j] ≠ parede }

  A  = { cima, baixo, esquerda, direita }

  T  = determinístico e total:
         T((i,j), cima)      = (i−1, j)   se válido
         T((i,j), baixo)     = (i+1, j)   se válido
         T((i,j), esquerda)  = (i, j−1)   se válido
         T((i,j), direita)   = (i, j+1)   se válido
         T((i,j), a)         = ∅           caso contrário

  s₀ = coordenadas do marcador 'A'

  G  = { coordenadas do marcador 'B' }

  c  = c(a) = 1  para toda ação a ∈ A  (custo uniforme)

Classificação do ambiente:
  Totalmente observável · Determinístico · Estático · Discreto · Agente único

Complexidade (grade m×n, fator de ramificação b ≤ 4):
  Tempo:   O(b^d)   onde d = profundidade da solução
  Espaço:  O(b^d)   BFS  |  O(d·b) DFS  |  O(b^d) A*
"""

# ──────────────────────────────────────────────────────────────────────────────
# Implementação: labirinto.py → LabirintoBusca
# Algoritmos:    buscas/classicas/{bfs,dfs,ucs,gulosa,a_estrela}.py
# ──────────────────────────────────────────────────────────────────────────────


"""
──────────────────────────────────────────────────────────────────────────────
1B. Problema com coletas obrigatórias  (pontos C ⊂ S)
──────────────────────────────────────────────────────────────────────────────

O agente deve visitar todos os pontos de coleta antes de atingir B.
A posição sozinha não é suficiente para determinar o progresso — é preciso
registrar quais coletas ainda faltam.  Solução: estado estendido.

  S' = { (pos, C_r) | pos ∈ S,  C_r ⊆ C }
       onde C = conjunto fixo de pontos de coleta do mapa
       |S'| = |S| × 2^|C|

  s₀'= ( posição_A,  frozenset(C) )     ← nenhuma coleta visitada

  G' = { ( posição_B,  ∅ ) }            ← B atingido com todas as coletas

  T' = T'( (pos, C_r), a ) = ( pos',  C_r \ {pos'} )
       onde pos' = T(pos, a)
       (visitar pos' remove-a automaticamente de C_r)

  c  = c(a) = 1  (inalterado)

Heurística admissível para A*:
  h((pos, C_r)) = max{ manhattan(pos, d) | d ∈ C_r ∪ {B} }
  Nunca superestima: o agente precisa ao menos chegar ao destino mais distante.
"""

# ──────────────────────────────────────────────────────────────────────────────
# Implementação: labirinto.py → LabirintoComColetas
# ──────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# SEMANA 2 — BUSCA LOCAL
# Sem memória global; otimiza função objetivo a partir do estado corrente.
# ══════════════════════════════════════════════════════════════════════════════

"""
──────────────────────────────────────────────────────────────────────────────
2A. Formulação por função objetivo
──────────────────────────────────────────────────────────────────────────────

  S  = { (pos, C_r) }   (mesmo espaço estendido de 1B)

  N(s) = vizinhos imediatos de s  (estados alcançáveis em uma ação)

  f(s) = −h(s)          ← função a MAXIMIZAR
       = −max{ manhattan(pos, d) | d ∈ C_r ∪ {B} }

  Não existe fronteira global; o agente conhece apenas N(s_corrente).

──────────────────────────────────────────────────────────────────────────────
2B. Hill-Climbing  (subida de encosta)
──────────────────────────────────────────────────────────────────────────────

  Algoritmo:
    s ← s₀
    enquanto f(melhor vizinho de s) > f(s):
        s ← argmax_{s' ∈ N(s)} f(s')
    retorna s

  Propriedades:
    · Completo?  Não — fica preso em máximos locais e platôs
    · Ótimo?     Não
    · Memória:   O(1)  — guarda apenas o estado corrente

──────────────────────────────────────────────────────────────────────────────
2C. Simulated Annealing
──────────────────────────────────────────────────────────────────────────────

  Permite movimentos para estados piores com probabilidade decrescente:

    P(aceitar s') = 1                    se Δf > 0  (melhora)
                    e^(Δf / T_k)         se Δf ≤ 0  (piora)

  onde  Δf = f(s') − f(s)  e  T_k → 0  conforme o "resfriamento".

  Esquema de resfriamento geométrico:  T_{k+1} = α · T_k,  0 < α < 1

  Propriedades:
    · Completo?  Sim, com resfriamento suficientemente lento (probabilístico)
    · Ótimo?     Sim no limite (resfriamento logarítmico) — impraticável
    · Memória:   O(1)
"""

# ──────────────────────────────────────────────────────────────────────────────
# Implementação (prevista): buscas/local/hill_climbing.py
#                           buscas/local/simulated_annealing.py
# ──────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# SEMANA 3 — BUSCA ONLINE
# Mapa desconhecido; o agente descobre o ambiente durante a execução.
# ══════════════════════════════════════════════════════════════════════════════

"""
──────────────────────────────────────────────────────────────────────────────
3. Formulação online  (percepção parcial)
──────────────────────────────────────────────────────────────────────────────

O agente não tem acesso ao mapa completo.  A cada passo percebe apenas
as células adjacentes (raio r = 1).

  Estado interno:  ŝ = (pos, M̂)
    pos — posição atual (conhecida pelo agente)
    M̂  — modelo interno do mapa construído até o momento
           M̂ ⊆ S,  cresce monotonicamente a cada percepção

  Percepção:  σ(pos) = { (pos', tipo) | pos' adjacente a pos }
              tipo ∈ { livre, parede, início, objetivo, coleta }

  Atualização do modelo:
    M̂ ← M̂ ∪ σ(pos)   a cada novo passo

  Objetivo online:
    Alcançar B com custo mínimo sabendo apenas M̂.

──────────────────────────────────────────────────────────────────────────────
Algoritmo: LRTA*  (Learning Real-Time A*)
──────────────────────────────────────────────────────────────────────────────

  Mantém tabela de heurísticas aprendidas  H: S → ℝ  (inicializada com h).

  A cada passo em estado s:
    1. Perceber σ(s) e atualizar M̂
    2. Atualizar heurística:
         H(s) ← max{ H(s),  min_{a∈A} [ c(s,a) + H(T(s,a)) ] }
    3. Executar ação:
         a* ← argmin_{a∈A} [ c(s,a) + H(T(s,a)) ]
         s  ← T(s, a*)

  Propriedades:
    · Completo?  Sim, em espaços finitos e exploráveis
    · Ótimo?     Não na primeira travessia; converge com repetidas tentativas
    · Memória:   O(|S̃|) onde S̃ = estados visitados até o momento

Diferença fundamental em relação à busca clássica:
  Clássica — planeja globalmente antes de agir
  Online   — age imediatamente e planeja localmente a cada passo
             (intercala percepção → atualização → ação)
"""

# ──────────────────────────────────────────────────────────────────────────────
# Implementação (prevista): buscas/online/lrta_estrela.py
# ──────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# QUADRO COMPARATIVO
# ══════════════════════════════════════════════════════════════════════════════

"""
┌─────────────┬──────────────────┬──────────────────┬──────────────────────┐
│ Propriedade │ Busca Clássica   │ Busca Local      │ Busca Online         │
├─────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ Observab.   │ Total            │ Total            │ Parcial (raio 1)     │
│ Memória     │ O(b^d)           │ O(1)             │ O(|visitados|)       │
│ Completo    │ Sim (BFS/A*)     │ Não (HC)         │ Sim (LRTA*)          │
│ Ótimo       │ Sim (UCS/A*)     │ Não              │ Não (1ª travessia)   │
│ Estado      │ pos [ou ext.]    │ pos [ou ext.]    │ (pos, mapa interno)  │
│ Planejam.   │ Antes de agir    │ Antes de agir    │ Durante a ação       │
└─────────────┴──────────────────┴──────────────────┴──────────────────────┘
"""
