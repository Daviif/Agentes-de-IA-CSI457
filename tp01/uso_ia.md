# Auditoria de Uso de Inteligência Artificial — TP01

**Disciplina:** CSI457 — Agentes de IA  
**Período:** 2026/1  
**Trabalho:** TP01 — Agentes de Busca em Labirinto  

---

## 1. Ferramentas de IA Utilizadas

| Ferramenta | Finalidade |
|---|---|
| Claude (Anthropic) | Implementação, organização de resultados, geração do HTML |
| GitHub Copilot | Assistência durante a escrita do código no editor |

---

## 2. Semana 1 — Busca Clássica

**Uso de IA:** Nenhum para a implementação dos algoritmos.

Os cinco algoritmos de busca clássica (BFS, DFS, UCS, Busca Gulosa e A*) foram **adaptados diretamente do código fornecido pelo professor** em trabalho anterior (ATV02). A IA não foi utilizada na implementação desta semana. As adaptações realizadas pela equipe foram:

- Reorganização dos algoritmos em arquivos independentes (`buscas/classicas/`)
- Extensão para suportar estados com coletas (`LabirintoComColetas`)
- Adição das métricas de desempenho (`ResultadoBusca`)

---

## 3. Semana 2 — Busca Local

**Uso de IA:** Assistência na implementação e geração de ideias.

A equipe utilizou IA (Claude) para auxiliar na implementação dos algoritmos de busca local, que não foram fornecidos pelo professor:

- **Hill-Climbing (Steepest Ascent):** a IA ajudou a estruturar a representação por permutação de coletas e a definir a vizinhança por swap.
- **Simulated Annealing:** a IA auxiliou na implementação do esquema de resfriamento geométrico e no critério de aceitação de soluções piores.
- **Algoritmo Genético:** a IA contribuiu com a estrutura de seleção, cruzamento e mutação aplicada à ordem de visitação das coletas.

Em todos os casos, a equipe **revisou, testou e ajustou** o código gerado, corrigindo comportamentos incorretos e adaptando os parâmetros (temperatura inicial, taxa de resfriamento, tamanho da população) aos mapas do trabalho.

A IA também foi usada para **gerar ideias** sobre qual representação de estado usar para a busca local (permutação de índices das coletas) e como calcular a função de custo de forma eficiente com distâncias pré-computadas.

---

## 4. Semana 3 — Busca Online

**Uso de IA:** Assistência na implementação.

Os dois algoritmos de busca online também contaram com auxílio de IA:

- **Replanning A\*:** a IA ajudou a estruturar o loop de replanejamento, o critério de detecção de parede não mapeada e a integração com o mapa interno do `LabirintoOnline`.
- **Online DFS:** a IA auxiliou na implementação do backtracking sistemático com pilha de retorno e controle de ações não tentadas por posição.

A classe `LabirintoOnline` — que simula a percepção parcial ocultando o mapa real — foi estruturada com apoio da IA para garantir que o agente só acesse células dentro do raio de percepção.

---

## 5. Visualização Web (HTML)

**Uso de IA:** Geração quase integral.

O arquivo `gerar_html.py`, que produz a animação interativa dos algoritmos no navegador, foi **gerado com forte assistência de IA**. A equipe descreveu o comportamento desejado (animação passo a passo, três abas — clássica, local e online, controles de velocidade) e a IA gerou o código HTML/CSS/JavaScript correspondente.

A equipe revisou e testou o resultado no navegador, corrigindo problemas de renderização e ajustando a legenda de cores.

---

## 6. Organização dos Resultados

**Uso de IA:** Apoio na análise e formatação.

Após executar os experimentos e coletar os dados nos arquivos `.csv`, a IA foi utilizada para:

- Sugerir quais métricas comparar entre os algoritmos (custo, nós expandidos, tempo, razão online/offline)
- Ajudar a estruturar o texto do relatório técnico com base nos números obtidos
- Organizar tabelas e quadros comparativos presentes no `RELATORIO_TECNICO.md`

---

## 7. O que NÃO foi feito por IA

- Definição do problema e formulação formal (PEAS, espaço de estados, heurísticas)
- Escolha dos mapas de teste e criação dos labirintos
- Execução dos experimentos e coleta dos dados
- Análise crítica dos resultados (por que A* é melhor que BFS em custo, por que HC fica preso em ótimos locais, etc.)
- Decisões de projeto (representação de estado estendido com frozenset, raio de percepção = 1)

---

## 8. Avaliação Crítica do Uso

O uso de IA foi produtivo nas partes de **implementação** e **visualização**, onde o volume de código é alto e os padrões são bem definidos. Nas partes de **raciocínio** — formular o problema, escolher heurísticas, interpretar resultados — a contribuição da IA foi secundária, servindo principalmente como ponto de partida para discussão entre os membros da equipe.

Todo código gerado com assistência de IA foi **lido, compreendido e testado** pela equipe antes de ser incorporado ao projeto.
