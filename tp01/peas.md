# Modelagem PEAS - Agente de Busca em Labirinto

## Visão Geral

Este documento formaliza a modelagem **PEAS** (Performance, Environment, Actuators, Sensors) do agente inteligente que resolve problemas de busca em labirintos usando algoritmos clássicos de busca informada e não-informada.

---

## 1. PERFORMANCE (P) - Medida de Desempenho

### Objetivo Principal
Encontrar um caminho válido do estado inicial até o objetivo com **mínimo custo**.

### Função de Utilidade / Desempenho

$$J = -\alpha \cdot C - \beta \cdot E - \gamma \cdot T$$

Onde:
- **C**: Custo do caminho (número de passos)
- **E**: Nós expandidos durante a busca
- **T**: Tempo de execução (em ms)
- **α, β, γ**: Fatores de ponderação

### Métricas Coletadas

| Métrica | Significado | Objetivo |
|---------|------------|----------|
| **Sucesso** | Encontrou caminho? | ✓ True |
| **Custo Total** | Número de passos | ↓ Minimizar |
| **Tamanho do Caminho** | Número de ações | ↓ Minimizar |
| **Nós Expandidos** | Estados visitados | ↓ Minimizar |
| **Nós Explorados** | Estados na fronteira processada | ↓ Minimizar |
| **Tempo (ms)** | Tempo de execução | ↓ Minimizar |
| **Fronteira Máxima** | Tamanho máximo da fila/pilha | ↓ Minimizar |

### Desempenho Desejado

Para cada labirinto, buscamos:
- ✓ **Otimalidade**: Custo mínimo
- ✓ **Completude**: Garantia de encontrar solução se existir
- ✓ **Eficiência**: Poucos nós expandidos
- ✓ **Rapidez**: Tempo de execução reduzido

---

## 2. ENVIRONMENT (E) - Descrição do Ambiente

### Tipo de Ambiente

| Propriedade | Classificação | Justificativa |
|-------------|--------------|---------------|
| **Observabilidade** | Totalmente Observável | Estado completo conhecido desde o início |
| **Determinismo** | Determinístico | Ações têm efeito previsível e único |
| **Dinamicidade** | Estático | Ambiente não muda durante execução |
| **Continuidade** | Discreto | Estados e ações discretos |
| **Multiagente** | Single-Agent | Um único agente no labirinto |
| **Preferências** | Goal-Based | Objetivo bem definido |

### Características Físicas

#### Representação do Espaço
```
# = Parede (obstáculo)
A = Ponto inicial (agente)
B = Ponto objetivo (meta)
C = Ponto de coleta (opcional)
  = Célula livre
```

#### Exemplos de Mapas

**Lab1 (9×9)** - Sem coletas
```
#########
#A      #
#  ###  #
#  #    #
#  #  ###
#  #    #
#  ###  #
#      B#
#########
```
- Início: (1, 1)
- Objetivo: (7, 7)
- Caminho ótimo: 12 passos

**Lab2 (7×11)** - Com 2 coletas (ignoradas neste problema)
```
###########
#A    #   #
# ## # ## #
#    C  B #
# ##  # # #
#  C  #   #
###########
```

**Lab3 (13×13)** - Com 1 coleta (ignorada neste problema)
```
#############
#A          #
########### #
#           #
# ###########
#           #
########### #
#     C     #
# ###########
#           #
########### #
#          B#
#############
```

### Propriedades do Ambiente

1. **Totalmente Observável**
   - Agente conhece: layout completo, paredes, posição inicial, objetivo
   - Não há incerteza sobre o estado do ambiente

2. **Determinístico**
   - Ação 'cima' sempre move (-1, 0)
   - Resultado é previsível
   - Não há efeitos secundários aleatórios

3. **Estático**
   - Paredes não mudam durante execução
   - Objetivo não se move
   - Ambiente é imutável

4. **Discreto**
   - Estados: posições (i, j) na grade
   - Ações: 4 direções ortogonais
   - Tempo: simulado em passos

---

## 3. ACTUATORS (A) - Atuadores / Ações

### Ações Disponíveis

O agente pode executar exatamente **4 ações de movimento**:

```python
AÇÕES = {
    'cima':     Δ(i, j) = (-1,  0)    # Move para linha anterior
    'baixo':    Δ(i, j) = (+1,  0)    # Move para próxima linha
    'esquerda': Δ(i, j) = ( 0, -1)    # Move para coluna anterior
    'direita':  Δ(i, j) = ( 0, +1)    # Move para próxima coluna
}
```

### Restrições de Ação

Uma ação é **válida** se:
1. ✓ O novo estado está dentro dos limites: `0 ≤ i < altura AND 0 ≤ j < largura`
2. ✓ O novo estado não é uma parede: `labirinto[i][j] ≠ '#'`

Se qualquer condição falhar, a ação é **inválida** e não é executada.

### Custo das Ações

- **Custo de cada movimento**: 1 unidade
- **Custo de ação inválida**: Não é permitida
- **Custo total do caminho**: Σ(custos das ações) = número de passos

---

## 4. SENSORS (S) - Sensores / Percepções

### Modo Clássico (Búsqueda Informada)

**Tipo**: Totalmente observável, acesso completo

O agente percebe:
```
Percepção = {
    'mapa_completo': grid_2d,       # Layout todo
    'posicao_atual': (i, j),        # Localização do agente
    'posicao_inicial': (i_a, j_a),  # Localização de 'A'
    'posicao_objetivo': (i_b, j_b), # Localização de 'B'
    'coletas': [(i_c1, j_c1), ...], # Posições de 'C'
    'paredes': grid_boolean         # Localização de '#'
}
```

**Uso**: 
- Algoritmos BFS, DFS, UCS, Gulosa, A* usam informação completa
- Planejamento offline: mapa todo conhecido antes da busca
- Heurística Manhattan usável: conhece objetivo

### Modo Online (Búsqueda Local)

**Tipo**: Parcialmente observável, vizinhança local (raio r = 1)

O agente percebe apenas células adjacentes:

```python
percepção_local = {
    (i, j):     'A' ou 'B' ou 'C' ou ' ' ou '#',  # Célula atual
    (i-1, j):   tipo,    # Cima
    (i+1, j):   tipo,    # Baixo
    (i, j-1):   tipo,    # Esquerda
    (i, j+1):   tipo,    # Direita
}
```

Raio de percepção: **1 célula em cada direção** (máximo 9 células)

### Estrutura de Dados do Mapa Percebido

```python
class LabirintoBusca:
    altura: int                    # Número de linhas
    largura: int                   # Número de colunas
    paredes: List[List[bool]]      # True = parede, False = célula livre
    inicio: Tuple[int, int]        # Posição (i, j) de 'A'
    objetivo: Tuple[int, int]      # Posição (i, j) de 'B'
    coletas: List[Tuple[int, int]] # Lista de posições (i, j) de 'C'
    
    def vizinhos(estado: Estado) -> List[Tuple[str, Estado, float]]:
        """Retorna ações válidas (ação, novo_estado, custo=1.0)"""
    
    def h(estado: Estado) -> float:
        """Heurística Manhattan: |i_estado - i_objetivo| + |j_estado - j_objetivo|"""
```

---

## 5. ARQUITETURA DO AGENTE

### Tipo de Agente

**Agente Baseado em Objetivos com Modelo**

```
┌─────────────────────────────────────┐
│   Agente de Busca em Labirinto     │
├─────────────────────────────────────┤
│ Percepto (Sensores) ─────────────┐  │
│      ↓                             │  │
│ ┌──────────────────────────────┐  │  │
│ │  Modelo Interno do Ambiente  │  │  │
│ │  - Layout do labirinto       │  │  │
│ │  - Posições conhecidas       │  │  │
│ │  - Paredes mapeadas          │  │  │
│ └──────────────────────────────┘  │  │
│      ↓                             │  │
│ ┌──────────────────────────────┐  │  │
│ │   Módulo de Busca            │  │  │
│ │   - Escolhe algoritmo        │  │  │
│ │   - Executa busca            │  │  │
│ │   - Retorna caminho          │  │  │
│ └──────────────────────────────┘  │  │
│      ↓                             │  │
│ Ação (Atuadores) ────────────────┘  │
│      ↓ Executa plano de movimento   │
│   Movimento: cima/baixo/esq/dir     │
└─────────────────────────────────────┘
```

### Ciclo de Operação

1. **PERCEPÇÃO**: Lê mapa do labirinto
2. **RACIOCÍNIO**: Executa algoritmo de busca
   - BFS, DFS, UCS, Gulosa ou A*
3. **AÇÃO**: Executa caminho retornado pelo algoritmo
4. **AVALIAÇÃO**: Coleta métricas (nós expandidos, tempo, custo)

---

## 6. HEURÍSTICA DE AVALIAÇÃO

### Heurística de Manhattan

Para algoritmos informados (Gulosa, A*), usa-se heurística admissível:

$$h(n) = |i_n - i_B| + |j_n - j_B|$$

**Propriedades**:
- ✓ Admissível: nunca superestima o custo real (h(n) ≤ h*(n))
- ✓ Consistente: |h(n) - h(n')| ≤ c(n,n')
- ✓ Eficiente: fácil computação O(1)

**Interpretação**: Distância mínima em movimentos ortogonais

---

## 7. MODELOS DE BUSCA IMPLEMENTADOS

### 1. Busca em Largura (BFS)
- **Completude**: Sim
- **Otimalidade**: Sim (custos iguais)
- **Tempo**: O(b^d)
- **Espaço**: O(b^d)
- **Heurística**: Nenhuma

### 2. Busca em Profundidade (DFS)
- **Completude**: Não (em grafos)
- **Otimalidade**: Não
- **Tempo**: O(b^m)
- **Espaço**: O(b·m)
- **Heurística**: Nenhuma

### 3. Busca de Custo Uniforme (UCS)
- **Completude**: Sim
- **Otimalidade**: Sim
- **Tempo**: O(b^(1+⌊C*/ε⌋))
- **Espaço**: O(b^(1+⌊C*/ε⌋))
- **Heurística**: Nenhuma

### 4. Busca Gulosa
- **Completude**: Não
- **Otimalidade**: Não
- **Tempo**: O(b^m)
- **Espaço**: O(b·m)
- **Heurística**: h(n) = Manhattan

### 5. Busca A* (Melhor-Primeiro)
- **Completude**: Sim
- **Otimalidade**: Sim
- **Tempo**: Depende de h, geralmente muito menor
- **Espaço**: Depende de h
- **Heurística**: h(n) = Manhattan

---

## 8. RESUMO DA MODELAGEM

| Aspecto | Descrição |
|---------|-----------|
| **Tipo de Agente** | Baseado em Objetivos com Modelo Interno |
| **Tipo de Ambiente** | Totalmente Observável, Determinístico, Estático |
| **Observabilidade** | Completa (conhece mapa todo antes de agir) |
| **Ações Disponíveis** | 4 movimentos ortogonais: cima, baixo, esquerda, direita |
| **Custo de Ação** | 1 unidade por movimento |
| **Objetivo** | Alcançar posição 'B' com mínimo custo |
| **Heurística** | Distância de Manhattan (para A* e Gulosa) |
| **Métrica de Sucesso** | Encontrou objetivo? Caminho é ótimo? |
| **Métricas Secundárias** | Nós expandidos, explorados, tempo, fronteira máxima |

---

## 9. VALIDAÇÃO E RESULTADOS ESPERADOS

### Lab1 (9×9)
```
Algoritmo | Sucesso | Custo | Nós_Exp | Tempo(ms) | Ótimo?
----------|---------|-------|---------|-----------|--------
BFS       | True    | 12    | 36      | 0.247     | ✓
DFS       | True    | 18    | 19      | 0.079     | ✗
UCS       | True    | 12    | 46      | 0.189     | ✓
Gulosa    | True    | 12    | 13      | 0.090     | ✓
A*        | True    | 12    | 36      | 0.157     | ✓
```

### Conclusões
- BFS, UCS e A* encontram caminho ótimo (12 passos)
- DFS encontra caminho subótimo (18 passos)
- Gulosa é mais rápida mas ainda ótima (neste caso)
- A* expande menos nós que BFS com igual otimalidade

---

**Versão**: 1.0  
**Data**: 2026-05-25  
**Disciplina**: CSI457 - Agentes de IA  
**Instituição**: Universidade Federal de Viçosa
