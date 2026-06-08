from dataclasses import dataclass, field


@dataclass
class ResultadoBuscaLocal:
    algoritmo: str

    # Métricas por execução (seção 6.5)
    melhor_custo:    float
    pior_custo:      float
    custo_medio:     float
    tempo_medio_ms:  float
    iteracoes_media: float
    n_execucoes:     int
    taxa_sucesso:    float          # fração dentro de 10% do melhor encontrado

    # Melhor solução encontrada
    melhor_permutacao: list         # índices em lab.coletas
    custo_otimo:       float        # brute-force (k≤8), inf caso contrário

    # Curva de convergência da melhor execução (iteração, custo)
    convergencia: list = field(default_factory=list)

def _exibir_resultado_local(res, lab, dist=None):
    """Imprime as métricas da seção 6.5 e a melhor ordem de visitação."""
    coletas = lab.coletas
    perm    = res.melhor_permutacao
    seq     = ['A'] + [f'C{i+1}' for i in perm] + ['B']

    print(f'\n── {res.algoritmo} ──────────────────────────────────────')
    print(f'  Melhor ordem:    {" → ".join(seq)}')
    print(f'  Melhor custo:    {res.melhor_custo:.1f}')
    if res.custo_otimo < float('inf'):
        gap = (res.melhor_custo / res.custo_otimo - 1) * 100
        print(f'  Ótimo (brute):   {res.custo_otimo:.1f}   gap={gap:.1f}%')
    print(f'  Pior custo:      {res.pior_custo:.1f}')
    print(f'  Custo médio:     {res.custo_medio:.2f}')
    print(f'  Tempo médio:     {res.tempo_medio_ms:.3f} ms')
    print(f'  Iterações médio: {res.iteracoes_media:.1f}')
    print(f'  Execuções:       {res.n_execucoes}')
    print(f'  Taxa de sucesso: {res.taxa_sucesso*100:.1f}%  (dentro de 10% do melhor)')
    print(f'  Convergência:    {res.convergencia[0]:.0f} → {res.convergencia[-1]:.0f}'
          f'  ({len(res.convergencia)-1} passos)')
