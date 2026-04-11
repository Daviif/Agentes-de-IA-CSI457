#Temperatura Máxima, Minima e Oscilação
TEMP_MIN = 20.0
TEMP_MAX = 24.0
OSCILAR = 0.5
TEMPO_PROLONGADO_IDEAL = 3

#Definido a classe Ambiente e AgenteTemperatura para simular o controle de temperatura
class Ambiente:
    def __init__(self, temperatura: float, estado_ac: bool):
        self.temperatura = temperatura
        self.ligado = estado_ac
    
    def __str__ (self):
        estado = "Ligado" if self.ligado else "Desligado"
        return f"Temperatura: {self.temperatura:.1f}°C, Ar Condicionado: {estado}"
    
class AgenteTemperatura:
    def __init__(self):
        self.historico_percepcoes = []
        self.ultima_acao = None
        self.tempo_ideal_consecutivo = 0

    def perceber(self, ambiente):
        percepcao = {
            "temperatura":      ambiente.temperatura,
            "ligado":           ambiente.ligado,
            "abaixo_da_faixa":  ambiente.temperatura < TEMP_MIN,
            "acima_da_faixa":   ambiente.temperatura > TEMP_MAX,
            "na_faixa_ideal":   TEMP_MIN <= ambiente.temperatura <= TEMP_MAX,
            "na_faixa_estavel": (TEMP_MIN + OSCILAR) <= ambiente.temperatura <= (TEMP_MAX - OSCILAR),
        }
        self.historico_percepcoes.append(percepcao)
        return percepcao

    def decidir(self, percepcao):
        ligado = percepcao["ligado"]
 
        # Fora da faixa alta: resfriar (ligando quando necessário)
        if percepcao["acima_da_faixa"]:
            self.tempo_ideal_consecutivo = 0
            if not ligado:
                return "ligar e resfriar ambiente"
            return "resfriar ambiente"

        # Fora da faixa baixa: esquentar (ligando quando necessário)
        if percepcao["abaixo_da_faixa"]:
            self.tempo_ideal_consecutivo = 0
            if not ligado:
                return "ligar e esquentar o ambiente"
            return "esquentar o ambiente"
        
        # Na faixa ideal com AC ligado: manter temperatura;
        # se permanecer por tempo prolongado na faixa estável, emitir alerta e desligar.
        if not ligado and percepcao["na_faixa_ideal"]:
            if percepcao["na_faixa_estavel"]:
                self.tempo_ideal_consecutivo += 1
            else:
                self.tempo_ideal_consecutivo = 0

            if self.tempo_ideal_consecutivo >= TEMPO_PROLONGADO_IDEAL:
                self.tempo_ideal_consecutivo = 0
                return "emitir alerta e desligar ar condicionado"

            return "manter temperatura do ambiente"

        # Na faixa ideal com AC desligado: nenhuma ação (não ligar)
        if percepcao["na_faixa_ideal"] and not ligado:
            self.tempo_ideal_consecutivo = 0
            return "nenhuma ação (não ligar)"
        
        # Segurança: mantém estado atual caso apareça algum estado não previsto.
        self.tempo_ideal_consecutivo = 0
        return "manter temperatura do ambiente"

    def agir(self, ambiente):
        percepcao = self.perceber(ambiente)
        acao = self.decidir(percepcao)
        self.ultima_acao = acao
 
        # Aplica a ação no ambiente
        if "ligar" in acao:
            ambiente.ligado = True
        if "desligar" in acao:
            ambiente.ligado = False

        return acao

def executar_cenario(nome: str, sequencia_temperaturas: list[float]):
    """
    Executa o agente em um cenário com uma sequência de temperaturas.
    Exibe os resultados de cada passo e uma interpretação final.
    """
    print(f"\n{'=' * 60}")
    print(f"  {nome}")
    print(f"  Sequência: {sequencia_temperaturas}")
    print(f"  Faixa ideal: {TEMP_MIN}°C – {TEMP_MAX}°C  |  OSCILAÇÃO: ±{OSCILAR}°C")
    print(f"{'=' * 60}")
 
    agente  = AgenteTemperatura()
    ambiente = Ambiente(temperatura=sequencia_temperaturas[0], estado_ac=False)
 
    for i, temp in enumerate(sequencia_temperaturas):
        ambiente.temperatura = temp
        acao = agente.agir(ambiente)
 
        estado = "ON" if ambiente.ligado else "OFF"
        print(f"  Passo {i+1}: temperatura ={temp:5.1f}°C | ação = {acao:8s} | sistema = {estado}")
 
    print(f"\n  Estado final: {ambiente}")
    print(f"  Total de percepções registradas: {len(agente.historico_percepcoes)}")
 
 
# ─── Parte 3 — Cenários de Teste ─────────────────────────────────────────────
 
if __name__ == "__main__":
 
    print("\n" + "=" * 60)
    print("  CSI457 — Agente de Controle de Temperatura")
    print("  Parte 3: Execução dos Cenários de Teste")
    print("=" * 60)
 
    # Cenário 1 — Oscilação
    executar_cenario(
        nome="Cenário 1 — Oscilação",
        sequencia_temperaturas=[24.9, 25.1, 24.8, 25.2]
    )
 
    # Cenário 2 — Calor extremo
    executar_cenario(
        nome="Cenário 2 — Calor extremo",
        sequencia_temperaturas=[30, 32, 35]
    )
 
    # Cenário 3 — Resfriamento gradual
    executar_cenario(
        nome="Cenário 3 — Resfriamento gradual",
        sequencia_temperaturas=[28, 27, 26, 25, 24]
    )
 