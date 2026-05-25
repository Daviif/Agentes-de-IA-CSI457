# Relatório Técnico - TP01: Agentes de Busca em Ambientes de Labirinto

## 1. Introdução

Este trabalho prático (TP01) consiste na implementação de um sistema de agentes inteligentes capazes de resolver problemas de busca em ambientes de labirinto. O projeto reutiliza e estende componentes desenvolvidos em atividades anteriores (ATV02), adaptando-os para suportar novos requisitos e padrões de arquitetura mais robustos.

## 2. Herança de Código da ATV02

### 2.1 Componentes Reutilizados

O TP01 aproveita os seguintes componentes principais da ATV02:

#### 2.1.1 Módulo `exibir.py`
- **Funcionalidade**: Renderização visual do labirinto e exibição de métricas de busca
- **Estrutura mantida**:
  - `imprimir_labirinto()`: Função que exibe o labirinto com representações visuais
  - `imprimir_metricas()`: Função que imprime estatísticas de execução
  
- **Adaptações realizadas**:
  - Suporte a estados estendidos (estados com coletas): `LabirintoComColetas` em TP01 pode ter tuplas como `((i, j), frozenset_coletas)`
  - Função auxiliar `_pos()` para extrair posições de estados complexos
  - Novo símbolo 'C' para representar pontos de coleta

#### 2.1.2 Estrutura de Dados `labirinto.py` / `buscas.py`
- **Conceitos mantidos**:
  - Classe `No`: Nó da árvore/grafo de busca com atributos `estado`, `pai`, `acao`, `g`
  - Classe `ResultadoBusca`: Dataclass que encapsula resultados com métricas
  - Classe `LabirintoBusca`: Carregamento e representação do labirinto

- **Evoluções em TP01**:
  - Introdução de Protocol `Labirinto` para polimorfismo
  - Extensão `LabirintoComColetas` para problemas com múltiplos objetivos
  - Novos atributos em `ResultadoBusca`: `custo_total`, `tempo_ms`, `fronteira_max`

#### 2.1.3 Algoritmos de Busca Clássica
Os cinco algoritmos fundamentais foram adaptados e reorganizados:

**Originais em ATV02** (métodos da classe `LabirintoBusca`):
- `busca_largura()` → BFS
- `busca_profundidade()` → DFS  
- `busca_custo_uniforme()` → UCS
- `busca_gulosa()` → Greedy Best-First
- `busca_weighted_astar()` → Weighted A*

**Reorganizados em TP01** (funções independentes em `buscas/classicas/`):
- `bfs.py` - Breadth-First Search
- `dfs.py` - Depth-First Search
- `ucs.py` - Uniform Cost Search
- `gulosa.py` - Greedy Best-First Search
- `a_estrela.py` - A* Search

### 2.2 Padrão de Busca Mantido

A lógica fundamental dos algoritmos permanece essencialmente a mesma:

```
1. Inicializar fronteira com estado inicial
2. Manter registro de estados explorados
3. Enquanto fronteira não estiver vazia:
   a. Extrair nó da fronteira (estratégia varia por algoritmo)
   b. Se nó é objetivo, retornar solução
   c. Marcar como explorado
   d. Expandir vizinhos e adicionar à fronteira
4. Se fronteira vazia, retornar falha
```

**Diferenças de estratégia por algoritmo**:
- **BFS**: Fronteira como fila (FIFO) - exploração por níveis
- **DFS**: Fronteira como pilha (LIFO) - exploração em profundidade
- **UCS**: Fronteira como fila de prioridade por custo acumulado
- **Gulosa**: Fronteira ordenada por heurística (distância Manhattan)
- **A***: Fronteira ordenada por `f(n) = g(n) + h(n)`

## 3. Adaptações para TP01

### 3.1 Arquitetura Modular

**Mudança significativa**: Os algoritmos foram convertidos de **métodos de classe** para **funções independentes**.

```
ATV02:
lab = LabirintoBusca('arquivo.txt')
resultado = lab.busca_largura()

TP01:
from buscas.classicas.bfs import bfs
from labirinto import LabirintoBusca
lab = LabirintoBusca('arquivo.txt')
resultado = bfs(lab, historico_estados=[])
```

**Benefícios**:
- Separação de responsabilidades
- Facilita testes unitários
- Permite composição de algoritmos
- Suporta diferentes tipos de problemas (coletas, restrições, etc.)

### 3.2 Suporte a Problemas Estendidos

**ATV02**: Focava apenas em problemas de ponto A → ponto B

**TP01**: Estende para:
- Problemas com múltiplos pontos de coleta
- Estados complexos: `((posicao_i, posicao_j), coletas_realizadas)`
- Classe `LabirintoComColetas` que herda de `LabirintoBusca`
- Métodos `vizinhos()` e `h()` polimórficos

### 3.3 Métricas Expandidas

**ATV02**:
```
- algoritmo
- encontrado
- caminho
- acoes
- nos_explorados
- nos_expandidos
- estados_explorados
```

**TP01** - adicionado:
```
+ custo_total (custo real do caminho)
+ tempo_ms (tempo de execução em milissegundos)
+ fronteira_max (tamanho máximo da fronteira durante busca)
```

### 3.4 Interface Protocol

Novo em TP01: Uso de `Protocol` para definir contratos sem herança nominal:

```python
@runtime_checkable
class Labirinto(Protocol):
    inicio: Any
    objetivo: Any
    def vizinhos(self, estado: Any) -> List[Tuple]: ...
    def h(self, estado: Any) -> float: ...
    def reconstruir(self, no: 'No') -> Tuple[List, List]: ...
```

Permite que tanto `LabirintoBusca` quanto `LabirintoComColetas` sejam usados pelos algoritmos sem herança explícita.

## 4. Estrutura de Diretórios

```
tp01/
├── src/
│   ├── main.py                          # Menu interativo
│   ├── labirinto.py                     # Estruturas do problema
│   ├── exibir.py                        # Renderização (adaptado de ATV02)
│   ├── visualizacao.py                  # Geração de HTML
│   ├── gerar_html.py                    # Suporte de visualização
│   ├── formulacao_formal.py             # Definição PEAS/formulação
│   ├── agente.py                        # Implementação do agente
│   ├── experimentos.py                  # Suite de testes
│   ├── files.py                         # Utilitários de arquivo
│   ├── buscas/
│   │   ├── classicas/
│   │   │   ├── bfs.py                   # (adaptado de ATV02)
│   │   │   ├── dfs.py                   # (adaptado de ATV02)
│   │   │   ├── ucs.py                   # (adaptado de ATV02)
│   │   │   ├── gulosa.py                # (adaptado de ATV02)
│   │   │   └── a_estrela.py             # (adaptado de ATV02)
│   │   ├── local/
│   │   │   ├── hill-climbing.py         # Hill Climbing
│   │   │   └── simulated_annealing.py   # Simulated Annealing
│   │   └── online/
│   │       └── # Algoritmos online (futuro)
│   └── mapas/
│       ├── lab1.txt                     # Labirinto simples
│       ├── lab2.txt                     # Com coletas
│       ├── lab3.txt                     # Serpentino
│       └── lab4.txt                     # Complexo
├── peas.md                              # Formulação PEAS
└── formulacao_formal.md                 # Especificação formal
```

## 5. Algoritmos de Busca Clássica

### 5.1 BFS (Breadth-First Search)

**Origem**: Adaptado de `LabirintoBusca.busca_largura()` em ATV02

**Características**:
- Exploração por níveis (nível 0, 1, 2, ...)
- Fronteira: fila (FIFO)
- Completo: Sim (encontra solução se existir)
- Ótimo: Sim (para custos uniformes)

**Complexidade**:
- Tempo: O(V + E)
- Espaço: O(V)

### 5.2 DFS (Depth-First Search)

**Origem**: Adaptado de `LabirintoBusca.busca_profundidade()` em ATV02

**Características**:
- Exploração em profundidade máxima primeiro
- Fronteira: pilha (LIFO)
- Completo: Não (pode entrar em ciclo infinito)
- Ótimo: Não

**Complexidade**:
- Tempo: O(V + E)
- Espaço: O(V)

### 5.3 UCS (Uniform Cost Search)

**Origem**: Adaptado de `LabirintoBusca.busca_custo_uniforme()` em ATV02

**Características**:
- Expande nó com menor custo acumulado g(n)
- Fronteira: fila de prioridade (min-heap)
- Completo: Sim
- Ótimo: Sim (encontra caminho de menor custo)

**Implementação**:
- Custo acumulado armazenado em `No.g`
- Usa `heapq` para eficiência

### 5.4 Busca Gulosa (Greedy Best-First)

**Origem**: Adaptado de `LabirintoBusca.busca_gulosa()` em ATV02

**Características**:
- Expande nó com menor heurística h(n)
- Fronteira: fila de prioridade por h(n)
- Completo: Não (depende da heurística)
- Ótimo: Não

**Heurística usada**: Distância Manhattan
```
h(n) = |x_atual - x_objetivo| + |y_atual - y_objetivo|
```

### 5.5 A* (A-Star)

**Origem**: Adaptado de `LabirintoBusca.busca_weighted_astar()` em ATV02

**Características**:
- Expande nó com menor f(n) = g(n) + h(n)
- Combina custo real e heurística
- Fronteira: fila de prioridade por f(n)
- Completo: Sim (se h é admissível)
- Ótimo: Sim (se h é admissível)

**Implementação em TP01**:
```python
f = g + h(estado)
heapq.heappush(fronteira, (f, No(estado, g=g)))
```

## 6. Diferenças Técnicas Principais

|          Aspecto         |         ATV02          |               TP01              |
|--------------------------|------------------------|---------------------------------|
| **Estrutura Algoritmos** | Métodos de classe      | Funções independentes           |
| **Tipos de Problemas**   | Ponto A → B            | A → B e com coletas             |
| **Estados**              | Tupla simples (i,j)    | Complexos: ((i,j), frozenset)   |
| **Interface**            | Classe concreta        | Protocol (typing)               |
| **Métricas**             | 7 atributos            | 10 atributos                    |
| **Menu**                 | Via input() interativo | Menu estruturado + experimentos |
| **Saída**                | Console                | Console + HTML                  |

## 7. Fluxo de Execução Típico

```
1. Usuario executa: python main.py

2. Menu oferece opcoes:
   - Escolher labirinto (1-4 ou custom)
   - Executar busca classica
   - Executar busca local
   - Ver experimentos
   - Gerar visualizacao HTML

3. Para busca classica:
   - Carregar mapa com LabirintoBusca()
   - Selecionar algoritmo (BFS, DFS, UCS, etc.)
   - Chamar funcao do algoritmo: bfs(lab, [])
   - Exibir resultado com imprimir_labirinto()
   - Mostrar metricas com imprimir_metricas()

4. Para busca com coletas:
   - Carregar mapa
   - Envolver em LabirintoComColetas()
   - Usar mesmo algoritmo: bfs(lab_coletas, [])
   - Estados automaticamente incluem coletas
```

## 8. Conclusão

O TP01 demonstra evolução arquitetural mantendo núcleo funcional estável:

✓ **Reutilização eficiente** de código ATV02  
✓ **Modularização** através de separação de algoritmos  
✓ **Extensibilidade** via Protocols e herança  
✓ **Manutenibilidade** com separação de responsabilidades  
✓ **Adaptação** para problemas mais complexos  

Os algoritmos fundamentais de busca mantêm sua essência enquanto a arquitetura evoluiu para suportar novos requisitos de forma elegante e extensível.

---

**Documentado em**: 25 de maio de 2026  
**Componentes de ATV02 utilizados**: `exibir.py`, estrutura `LabirintoBusca`, 5 algoritmos clássicos  
**Extensões do TP01**: `LabirintoComColetas`, `Protocol Labirinto`, buscas locais, visualização HTML
