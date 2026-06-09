# Auditoria de Uso de IA Generativa — TP01 CSI457

## 1. Ferramentas Utilizadas

| Ferramenta | Versão / Modelo | Uso principal |
|------------|-----------------|---------------|
| Claude (Anthropic) | Claude Sonnet 4.6 via Claude Code CLI | Suporte contínuo ao longo das 3 semanas |
| GitHub Copilot | GPT-4o (integração VS Code) | Autocompletar pontual em trechos de código |

## 2. Principais Prompts Utilizados

### Semana 1 — Busca Clássica

**Prompt 1 — Estrutura inicial do projeto**
> "Quero criar um agente para resolver labirintos em Python. O labirinto é uma grade 2D com paredes (#), início (A), objetivo (B) e pontos de coleta (C). Como estruturar o projeto para suportar BFS, DFS, UCS, Gulosa e A*?"

*Resultado:* A IA sugeriu separar os algoritmos em módulos independentes em `buscas/classicas/`, com uma classe `LabirintoBusca` para leitura do mapa e uma dataclass `ResultadoBusca` para encapsular métricas. A estrutura foi adotada integralmente.

**Prompt 2 — Formulação formal do problema**
> "Como formular o problema de busca em labirinto como ⟨S, A, T, s₀, G, c⟩? Quais são os estados, ações, função de transição e custo?"

*Resultado:* A IA explicou a formalização corretamente. Usamos como base para o arquivo `formulacao_formal.py` e para o relatório.

**Prompt 3 — Heurística admissível para A***
> "A distância de Manhattan é admissível para este labirinto? Como provar?"

*Resultado:* A IA forneceu a justificativa formal: como cada movimento custa 1 e a distância de Manhattan representa o número mínimo de movimentos em linha reta (sem paredes), ela nunca superestima o custo real — portanto é admissível. A justificativa foi incorporada ao relatório.

### Semana 2 — Busca Local

**Prompt 4 — Modelagem dos pontos de coleta como permutação**
> "Como modelar o problema de visitar múltiplos pontos C como um problema de otimização local? Qual representação usar para Hill-Climbing e Simulated Annealing?"

*Resultado:* A IA sugeriu representar uma solução como uma permutação `π` dos índices dos pontos de coleta e definir a vizinhança por troca de dois elementos (swap). Adotamos essa representação em `hill_climbing.py` e `simulated_annealing.py`.

**Prompt 5 — Calibração do Simulated Annealing**
> "Como calibrar T0 e alpha para o Simulated Annealing em problemas de labirinto com custo na casa de 100–300?"

*Resultado:* A IA sugeriu `T0 = 5 × custo_inicial` e `alpha = 0.995` com `max_iter = 5000`. Testamos os valores nos três mapas e verificamos que o SA convergia ao ótimo em todos os casos — os parâmetros foram mantidos conforme sugeridos.

**Prompt 6 — Vizinhança por inversão de trecho (2-opt)**
> "Devo usar swap ou inversão de trecho como vizinhança? Qual é mais eficaz para o TSP em labirintos pequenos?"

*Resultado:* A IA argumentou que para k ≤ 7 pontos, o swap é mais simples e a diferença de qualidade é negligenciável. A inversão de trecho (2-opt) foi descartada por complexidade adicional desnecessária para os mapas do TP.

### Semana 3 — Busca Online

**Prompt 7 — Ciclo perceber-atualizar-planejar-agir**
> "Como implementar o ciclo perceber → atualizar mapa interno → planejar → agir em Python? O agente começa com mapa de '?' e percebe vizinhos ao se mover."

*Resultado:* A IA sugeriu a classe `LabirintoOnline` com um `mapa` interno iniciado como `None` (desconhecido) e o método `perceber()` para revelar células dentro do raio. A estrutura foi adotada integralmente em `labirinto.py`.

**Prompt 8 — Replanning com A***
> "No Replanning A*, quando o agente deve replanejar? Apenas quando o plano é bloqueado por parede ou a cada passo?"

*Resultado:* A IA explicou que replaneja apenas quando: (a) o plano está vazio, ou (b) o próximo passo é uma célula agora conhecida como parede. Replanejar a cada passo seria correto mas ineficiente. Implementamos conforme sugerido em `replanning_a_estrela.py`.

## 3. Trechos de Código Sugeridos por IA

### Trecho 1 — Estrutura de `ResultadoBuscaOnline`
A IA sugeriu incluir `replanejamentos` e `razao_online_offline` como atributos/propriedades da dataclass. O trecho foi adaptado para incluir `custo_otimo_offline` calculado após a execução:

```python
@dataclass
class ResultadoBuscaOnline:
    algoritmo: str
    encontrado: bool
    movimentos_totais: int
    custo_real: float
    celulas_reveladas: int
    celulas_revisitadas: int
    replanejamentos: int
    custo_otimo_offline: float
    caminho_percorrido: list
    tempo_ms: float

    @property
    def razao_online_offline(self):
        if self.custo_otimo_offline and self.custo_otimo_offline > 0:
            return self.custo_real / self.custo_otimo_offline
        return None
```

### Trecho 2 — Online DFS com backtracking
A IA sugeriu a estrutura de `nao_tentadas` (dicionário pos → ações não testadas) e `pilha` de retorno para implementar o Online DFS conforme descrito no AIMA Cap. 4. O trecho foi usado diretamente com ajustes de nomenclatura.

### Trecho 3 — Cálculo de distâncias com A*
A IA sugeriu usar A* para pré-computar as distâncias entre todos os pares (A, C₁, C₂, ..., Cₖ, B) e armazenar em dicionário para consulta O(1) durante a busca local. Implementado em `buscas/local/distancias.py`.

## 4. Sugestões Rejeitadas

| Sugestão | Motivo da Rejeição |
|----------|--------------------|
| Usar `networkx` para representar o grafo do labirinto | O enunciado penaliza uso de bibliotecas prontas de busca sem implementação própria |
| Implementar A* bidirecional como heurística para a busca online | Complexidade excessiva para o escopo do TP |
| Usar `multiprocessing` para paralelizar as múltiplas execuções do HC/SA | Dificultaria reprodutibilidade das sementes aleatórias e a análise dos resultados |
| Usar `scipy.optimize` para o problema de permutação | Mesma razão: biblioteca pronta substitui implementação própria |

## 5. Erros Cometidos pela IA

### Erro 1 — Heurística inadmissível na busca online
A IA inicialmente sugeriu usar distância Euclidiana como heurística para o A* interno da busca online. Identificamos que isso pode superestimar o custo quando há paredes (a distância real pode ser maior que a reta), tornando o A* não ótimo no mapa interno. Corrigimos para distância de Manhattan.

### Erro 2 — Condição de parada do Online DFS
A IA sugeriu verificar `pos == objetivo` dentro do loop de backtracking, o que causava saída prematura quando o agente retornava ao início. Corrigimos para verificar antes de qualquer movimento.

### Erro 3 — Cálculo incorreto de `taxa_sucesso` no Hill-Climbing
A IA inicialmente definiu taxa de sucesso como "chegar ao ótimo global". Como o ótimo só é conhecível por força bruta (limitado a k ≤ 8), redefinimos como "custo ≤ 1.10 × melhor encontrado", o que é mais robusto para instâncias maiores.

## 6. Como o Grupo Validou a Solução

1. **Busca clássica:** Verificamos manualmente os caminhos encontrados nos mapas pequenos (lab1, lab2) comparando com soluções traçadas à mão. BFS e A* retornaram o mesmo custo ótimo em todos os casos.

2. **Busca local:** Comparamos os resultados do HC e SA com o custo ótimo calculado por força bruta (para k ≤ 8 pontos). O SA atingiu o ótimo em 100% das execuções nos três mapas testados.

3. **Busca online:** Comparamos o custo percorrido pelo agente online com o custo ótimo calculado pelo A* com mapa completo. A razão online/offline ficou entre 1.0 e 2.5 dependendo do mapa e da estratégia.

4. **Testes em mapas novos:** Executamos todos os algoritmos em lab4 (mapa sem solução) para verificar que o sistema retornava `sucesso=False` sem travar.

## 7. Modificações Feitas pelo Grupo

- A modelagem PEAS foi elaborada integralmente pela equipe, sem sugestão direta da IA.
- Os mapas `lab4.txt` a `lab7.txt` foram criados manualmente pela equipe para testar casos específicos (mapa sem solução, labirinto com 7 coletas, mapa grande).
- A análise crítica dos resultados (questões de análise das seções 5.4, 6.6 e 7.5 do enunciado) foi produzida pela equipe com base nos experimentos, sem delegar à IA.
- A estrutura do `experimentos.py` e os scripts de geração de CSV/gráficos foram escritos pela equipe com orientação da IA sobre a API do matplotlib.
