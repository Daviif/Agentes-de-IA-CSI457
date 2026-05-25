"""
Modelagem PEAS — Agente Inteligente em Labirinto
CSI457 · TP01 (3 semanas)

PEAS = Performance · Environment · Actuators · Sensors
"""

# ══════════════════════════════════════════════════════════════════════════════
# SEMANA 1 — BUSCA CLÁSSICA
# ══════════════════════════════════════════════════════════════════════════════

"""
┌─────────────────┬──────────────────────────────────────────────────────────┐
│ Performance     │ · Encontrou solução?  (binário)                          │
│                 │ · Custo do caminho    (minimizar — nº de passos)         │
│                 │ · Nós expandidos      (minimizar — esforço computacional)│
│                 │ · Tempo de execução   (minimizar — ms)                   │
│                 │ · Fronteira máxima    (minimizar — uso de memória)       │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Environment     │ · Grade discreta com paredes, espaços livres,            │
│                 │   início (A), objetivo (B) e coletas obrigatórias (C)    │
│                 │ · Totalmente observável  — mapa completo conhecido a     │
│                 │   priori; agente não precisa explorar para planejar       │
│                 │ · Determinístico         — T(s,a) retorna sempre o mesmo │
│                 │   estado; sem incerteza de resultado                      │
│                 │ · Estático               — paredes não mudam durante a   │
│                 │   busca                                                   │
│                 │ · Discreto               — posições inteiras (i,j)       │
│                 │ · Agente único                                            │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Actuators       │ · Mover cima      (i,j) → (i−1, j)                      │
│                 │ · Mover baixo     (i,j) → (i+1, j)                      │
│                 │ · Mover esquerda  (i,j) → (i,  j−1)                     │
│                 │ · Mover direita   (i,j) → (i,  j+1)                     │
│                 │ Ação inválida (parede ou borda) é silenciosamente        │
│                 │ ignorada pela função de transição.                       │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Sensors         │ · Mapa completo  (matriz de paredes inteira)             │
│                 │ · Posição de início, objetivo e todos os pontos C        │
│                 │ Percepção ocorre uma única vez, antes da busca iniciar.  │
└─────────────────┴──────────────────────────────────────────────────────────┘

Tipo de agente: baseado em objetivos com modelo interno completo do ambiente.
Estratégia:     planeja o caminho completo antes de executar qualquer ação.
"""

# ══════════════════════════════════════════════════════════════════════════════
# SEMANA 2 — BUSCA LOCAL
# ══════════════════════════════════════════════════════════════════════════════

"""
┌─────────────────┬──────────────────────────────────────────────────────────┐
│ Performance     │ · Qualidade da solução  f(s) = −h(s)  (maximizar)       │
│                 │   onde h(s) = distância estimada ao objetivo mais longe  │
│                 │ · Convergência: nº de iterações até estabilizar          │
│                 │ · Para SA: taxa de escape de ótimos locais               │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Environment     │ · Mesma grade da Semana 1                                │
│                 │ · Totalmente observável  — mapa conhecido                │
│                 │ · Determinístico e Estático                              │
│                 │ · Discreto · Agente único                                │
│                 │                                                          │
│                 │ Diferença-chave: o agente trata o mapa como uma         │
│                 │ superfície de fitness e otimiza localmente; não mantém  │
│                 │ fronteira global nem conjunto de explorados.             │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Actuators       │ · Mesmos 4 movimentos ortogonais                        │
│                 │ · O agente considera apenas N(s) = vizinhos imediatos   │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Sensors         │ · Valores de f para cada vizinho imediato               │
│                 │ · Temperatura atual T_k  (apenas Simulated Annealing)   │
│                 │ Memória: O(1) — apenas estado corrente e seus vizinhos. │
└─────────────────┴──────────────────────────────────────────────────────────┘

Tipo de agente: baseado em utilidade — maximiza f(s) sem objetivo global.
Limitações:     Hill-Climbing fica preso em máximos locais e platôs.
                SA escapa com probabilidade e^(Δf/T_k), decrescente no tempo.
"""

# ══════════════════════════════════════════════════════════════════════════════
# SEMANA 3 — BUSCA ONLINE
# ══════════════════════════════════════════════════════════════════════════════

"""
┌─────────────────┬──────────────────────────────────────────────────────────┐
│ Performance     │ · Encontrou o objetivo B?  (binário)                    │
│                 │ · Custo total percorrido   (inclui backtracking)         │
│                 │ · Nº de backtrackings necessários                        │
│                 │ · Completude do mapa construído ao final                 │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Environment     │ · Grade desconhecida a priori                           │
│                 │ · Parcialmente observável — agente vê apenas as células  │
│                 │   adjacentes (raio r = 1) a cada passo                  │
│                 │ · Determinístico  — T(s,a) é fixo, sem surpresas        │
│                 │ · Estático        — paredes não mudam                   │
│                 │ · Discreto · Agente único                                │
│                 │                                                          │
│                 │ Estado do agente: ŝ = (pos, M̂)                         │
│                 │   pos — posição corrente (sempre conhecida)              │
│                 │   M̂  — modelo interno do mapa, cresce a cada percepção │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Actuators       │ · Mesmos 4 movimentos ortogonais                        │
│                 │ · Backtrack: retornar a posição anterior se necessário   │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Sensors         │ · Percepção local a cada passo:                         │
│                 │   σ(pos) = { (pos', tipo) | pos' adjacente a pos }      │
│                 │   tipo ∈ { livre, parede, início, objetivo, coleta }    │
│                 │ · Posição corrente (assume localização conhecida)        │
└─────────────────┴──────────────────────────────────────────────────────────┘

Tipo de agente: baseado em objetivos com modelo interno parcial e incremental.
Estratégia:     intercala  percepção → atualização de M̂ → ação  a cada passo.
Algoritmo:      LRTA* — aprende heurísticas H(s) durante a travessia.
"""

# ══════════════════════════════════════════════════════════════════════════════
# QUADRO COMPARATIVO
# ══════════════════════════════════════════════════════════════════════════════

"""
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│ PEAS             │ Busca Clássica   │ Busca Local      │ Busca Online     │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Performance      │ custo + exp +    │ f(s) local       │ custo + backtr.  │
│                  │ tempo + memória  │ (qualidade)      │ + cobertura      │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Observabilidade  │ Total            │ Total            │ Parcial (r=1)    │
│ Determinismo     │ Sim              │ Sim              │ Sim              │
│ Estaticidade     │ Sim              │ Sim              │ Sim              │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Actuators        │ 4 movimentos     │ 4 movimentos     │ 4 mov. + volta   │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Sensors          │ Mapa completo    │ Vizinhos + f     │ Células adj. r=1 │
│                  │ (pré-busca)      │ (por passo)      │ (por passo)      │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Tipo de agente   │ Baseado em       │ Baseado em       │ Baseado em obj.  │
│                  │ objetivos        │ utilidade        │ + modelo parcial │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
"""


# ══════════════════════════════════════════════════════════════════════════════
# IMPLEMENTAÇÃO DO AGENTE
# ══════════════════════════════════════════════════════════════════════════════

class AgenteLabirinto:
    """Agente que opera no labirinto nos três modos: clássico, local e online."""

    ACOES = [(-1, 0, 'cima'), (1, 0, 'baixo'), (0, -1, 'esquerda'), (0, 1, 'direita')]

    def __init__(self, labirinto):
        self.labirinto   = labirinto
        self.posicao     = labirinto.inicio
        self.historico   = [self.posicao]
        self.custo_total = 0
        self.mapa_interno = {}          # usado na busca online

    # ── Actuators ─────────────────────────────────────────────────────────────

    def mover(self, nova_pos) -> bool:
        linha, col = nova_pos
        if (0 <= linha < self.labirinto.altura and
                0 <= col < self.labirinto.largura and
                not self.labirinto.paredes[linha][col]):
            self.posicao = nova_pos
            self.historico.append(nova_pos)
            self.custo_total += 1
            return True
        return False

    def executar_plano(self, caminho) -> bool:
        """Semana 1: executa sequência de posições planejada antecipadamente."""
        for passo in caminho:
            self.mover(passo)
        return self.posicao == self.labirinto.objetivo

    # ── Sensors ───────────────────────────────────────────────────────────────

    def perceber(self) -> dict:
        """Semana 3: percepção local — células adjacentes (raio r=1)."""
        i, j = self.posicao
        percepcao = {}
        for di, dj, _ in self.ACOES:
            pos = (i + di, j + dj)
            li, co = pos
            if 0 <= li < self.labirinto.altura and 0 <= co < self.labirinto.largura:
                if self.labirinto.paredes[li][co]:
                    percepcao[pos] = 'parede'
                elif pos == self.labirinto.objetivo:
                    percepcao[pos] = 'objetivo'
                elif pos in self.labirinto.coletas:
                    percepcao[pos] = 'coleta'
                else:
                    percepcao[pos] = 'livre'
            else:
                percepcao[pos] = 'parede'
        return percepcao

    def atualizar_mapa(self) -> None:
        """Semana 3: integra percepção corrente ao modelo interno M̂."""
        self.mapa_interno.update(self.perceber())
