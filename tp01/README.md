# TP01 — Agente Inteligente em Labirinto

Trabalho Prático 01 da disciplina **CSI457 — Inteligência Artificial**  
Curso: Sistemas de Informação  
Integrantes: Davi Emilio de Paula Fonseca, João Vitor Cota Silva, Thársos Gabriel Couto Fernandes

Implementação de um agente capaz de resolver labirintos sob três condições:
- **Busca Clássica** — mapa totalmente conhecido (BFS, DFS, UCS, Gulosa, A*)
- **Busca Local** — mapa com múltiplos pontos de coleta obrigatórios (Hill-Climbing, Simulated Annealing, Algoritmo Genético)
- **Busca Online** — mapa desconhecido, explorado em tempo real (Replanning A*, Online DFS)

---

## Requisitos

- Python 3.11 ou superior
- matplotlib (apenas para geração de gráficos)

```bash
pip install matplotlib
```

Ou usando o ambiente virtual já presente no projeto:

```bash
cd tp01
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install matplotlib
```

---

## Estrutura do Projeto

```
tp01/
├── src/
│   ├── main.py                    # Interface interativa principal
│   ├── experimentos.py            # Gera resultados_semana1.csv (busca clássica)
│   ├── gerar_graficos.py          # Gera todos os gráficos PNG
│   ├── labirinto.py               # Classes LabirintoBusca, LabirintoOnline, LabirintoComColetas
│   ├── agente.py                  # Modelagem PEAS
│   ├── formulacao_formal.py       # Formulação formal dos problemas
│   ├── exibir.py                  # Renderização do labirinto no terminal
│   ├── mapas/                     # Labirintos em formato .txt
│   │   ├── lab1.txt               # 9×9, sem coletas
│   │   ├── lab2.txt               # 30×30, 6 coletas
│   │   ├── lab3.txt               # 13×13, serpentino
│   │   ├── lab4.txt               # Mapa sem solução (teste de robustez)
│   │   ├── lab5.txt               # 81×81, corredor longo (escalabilidade)
│   │   ├── lab6.txt               # 15×15, 6 coletas
│   │   └── lab7.txt               # 20×20, 7 coletas
│   ├── buscas/
│   │   ├── classicas/             # bfs.py, dfs.py, ucs.py, gulosa.py, a_estrela.py
│   │   ├── local/                 # hill_climbing.py, simulated_annealing.py, genetic_algorithm.py
│   │   └── online/                # replanning_a_estrela.py, online_dfs.py
│   ├── resultados_semana1.csv     # Gerado por experimentos.py
│   ├── resultados_semana2.csv     # Resultados da busca local
│   └── resultados_semana3.csv     # Resultados da busca online
├── graficos/                      # Gerado por gerar_graficos.py
├── peas.md                        # Modelagem PEAS do agente
├── uso_ia.md                      # Auditoria do uso de IA generativa
└── README.md                      # Este arquivo
```

---

## Como Executar

### Interface interativa

Executa qualquer modo de busca de forma interativa:

```bash
cd tp01/src
python main.py
```

O programa pergunta qual labirinto usar e qual tipo de busca realizar:

```
Escolha o labirinto:
  1 - lab1 (simples, sem coletas)
  2 - lab2 (com pontos de coleta)
  3 - lab3 (serpentino, maior)
  4 - lab4 (muito complexo, para teste de performance)
  0 - Inserir caminho manualmente

Tipo de busca:
  1 - Busca Clássica (BFS, DFS, UCS, Gulosa, A*)
  2 - Busca Local    (Hill-Climbing, Simulated Annealing, Algoritmo Genético)
  3 - Busca Online   (Replanning A*, Online DFS)
```

### Experimentos automáticos (Semana 1)

Roda todos os algoritmos clássicos em lab1, lab2 e lab3 e salva os resultados:

```bash
cd tp01/src
python experimentos.py
```

Saída: `src/resultados_semana1.csv`

> **Nota metodológica:** A Semana 1 avalia os algoritmos clássicos como problema de navegação pura
> (A → B), sem impor a obrigatoriedade de visitar os pontos de coleta intermediários (C).
> O objetivo é isolar e comparar as propriedades intrínsecas de cada algoritmo
> (completude, otimalidade, complexidade) no espaço de estados simples `(linha, coluna)`.
> A otimização da ordem de visita dos pontos C é tratada na Semana 2 como um problema de
> busca local sobre permutações.

### Gerar todos os gráficos

```bash
cd tp01/src
python gerar_graficos.py
```

Saída: pasta `tp01/graficos/` com 9 arquivos PNG.

---

## Formato dos Mapas

Os mapas são arquivos `.txt` onde cada caractere representa uma célula:

| Símbolo | Significado |
|---------|-------------|
| `#` | Parede / obstáculo |
| `A` | Posição inicial do agente |
| `B` | Objetivo final |
| `C` | Ponto de coleta obrigatório |
| ` ` | Célula livre |
| `?` | Célula desconhecida (modo online) |

Exemplo de mapa simples (`lab1.txt`):

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

### Criar um mapa personalizado

Crie um arquivo `.txt` seguindo o formato acima. Regras:
- Exatamente um `A` e um `B`
- Zero ou mais pontos `C`
- Bordas devem ser `#`
- O mapa deve ser retangular (todas as linhas com o mesmo comprimento)

Para testar:

```bash
cd tp01/src
python main.py
# Escolha a opção 0 e informe o caminho do arquivo
```

---

## Métricas Coletadas

### Busca Clássica

| Métrica | Descrição |
|---------|-----------|
| `sucesso` | Solução encontrada? |
| `custo_total` | Custo do caminho |
| `tamanho_caminho` | Número de passos |
| `nos_expandidos` | Nós retirados da fronteira |
| `nos_explorados` | Estados únicos visitados |
| `tempo_ms` | Tempo de execução (ms) |
| `fronteira_max` | Tamanho máximo da fronteira |

### Busca Local

| Métrica | Descrição |
|---------|-----------|
| `melhor_custo` | Menor custo encontrado nas execuções |
| `pior_custo` | Maior custo encontrado |
| `custo_medio` | Média sobre todas as execuções |
| `tempo_medio_ms` | Tempo médio por execução |
| `iteracoes_media` | Iterações médias até convergência |
| `taxa_sucesso` | Fração das execuções dentro de 10% do melhor |

### Busca Online

| Métrica | Descrição |
|---------|-----------|
| `movimentos_totais` | Total de passos dados |
| `custo_real` | Custo acumulado percorrido |
| `celulas_reveladas` | Células do mapa descobertas |
| `celulas_revisitadas` | Células pisadas mais de uma vez |
| `replanejamentos` | Vezes que o plano foi recalculado |
| `razao_online_offline` | `custo_real / custo_ótimo_offline` |

---

## Algoritmos Implementados

### Busca Clássica (`buscas/classicas/`)

- **BFS** — Busca em Largura; garante caminho com menor número de passos
- **DFS** — Busca em Profundidade; não garante otimalidade
- **UCS** — Busca de Custo Uniforme; garante custo ótimo
- **Gulosa** — Heurística Manhattan; rápida mas não ótima
- **A\*** — Combina custo real e heurística; ótimo e completo

Heurística utilizada: distância de Manhattan `h(n) = |xₙ − xB| + |yₙ − yB|`

### Busca Local (`buscas/local/`)

Problema: encontrar a permutação ótima de pontos de coleta.  
Representação: lista de índices `[π(1), π(2), ..., π(k)]`.  
Vizinhança: troca de dois elementos (swap).

- **Hill-Climbing** — Steepest-ascent com reinicialização aleatória (30 execuções)
- **Simulated Annealing** — T₀ = 5×custo inicial, α = 0.995, 5000 iterações (20 execuções)
- **Algoritmo Genético** — Bônus; seleção por torneio, crossover por ponto, mutação por swap

### Busca Online (`buscas/online/`)

- **Replanning A\*** — Mantém mapa interno; replaneja apenas quando o próximo passo é bloqueado
- **Online DFS** — Exploração sistemática conforme AIMA Cap. 4; backtracking quando sem vizinhos livres

---

## Resultados Experimentais

Os arquivos CSV estão em `src/`:

| Arquivo | Conteúdo | Formulação do problema |
|---------|----------|------------------------|
| `resultados_semana1.csv` | Busca clássica — lab1, lab2, lab3 | Navegação A → B (espaço de estados simples) |
| `resultados_semana2.csv` | Busca local — lab2, lab6, lab7 | Otimização da ordem de visita dos pontos C |
| `resultados_semana3.csv` | Busca online — lab1, lab2, lab3, lab6 | Navegação A → B com mapa inicialmente desconhecido |

Os gráficos estão em `graficos/` (gerados por `gerar_graficos.py`).
