class AgenteLabirinto:
    """
    Modelagem PEAS do agente no labirinto.

    Performance:
        J = -alpha*custo_caminho - beta*nos_expandidos - gamma*tempo_execucao
        Objetivo: minimizar custo do caminho e esforço computacional.

    Environment:
        Labirinto em grade discreta com paredes (#), células livres ( ),
        posição inicial (A), objetivo final (B) e pontos de coleta (C).
        Modo clássico: totalmente observável, estático e determinístico.
        Modo online:   parcialmente observável (percepção local, raio r=1).

    Actuators:
        Movimentos ortogonais: {cima, baixo, esquerda, direita}.

    Sensors:
        Modo clássico: percebe o mapa completo desde o início.
        Modo online:   percebe apenas células adjacentes (raio r=1).

    Classificação:
        Agente baseado em objetivos com modelo interno do ambiente.
        Na parte online, atualiza o modelo interno a cada percepção.
    """

    ACOES = [(-1, 0, 'cima'), (1, 0, 'baixo'), (0, -1, 'esquerda'), (0, 1, 'direita')]

    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.posicao = labirinto.inicio
        self.historico = [self.posicao]
        self.custo_total = 0

    def mover(self, nova_pos):
        if self.labirinto.eh_livre(nova_pos):
            self.posicao = nova_pos
            self.historico.append(nova_pos)
            self.custo_total += 1
            return True
        return False

    def executar_plano(self, caminho):
        for passo in caminho[1:]:
            self.mover(passo)
        return self.posicao == self.labirinto.objetivo

    def perceber(self, raio=1):
        i, j = self.posicao
        percepcao = {}
        for di in range(-raio, raio + 1):
            for dj in range(-raio, raio + 1):
                pos = (i + di, j + dj)
                percepcao[pos] = self.labirinto.tipo_celula(pos)
        return percepcao
