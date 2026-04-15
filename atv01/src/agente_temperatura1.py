# v1 do agente

import math

#Definido a classe Ambiente e AgenteTemperatura para simular o controle de temperatura
class Ambiente:
    def __init__(self, temperatura: float, estado_ac: bool):
        self.temperatura = temperatura
        self.ligado = estado_ac

    def atualizar(self):
        T_externa = 30

        if self.ligado:
            self.temperatura -= 0.3
        else:
            self.temperatura += (T_externa - self.temperatura) * 0.05
    
    def __str__ (self):
        estado = "Ligado" if self.ligado else "Desligado"
        return f"Temperatura: {self.temperatura:.2f}°C, Ar Condicionado: {estado}"
    
class AgenteTemperatura:
    def __init__(self, temp_desejada = 23.0, sigma = 0.2, alpha = 1.0, beta = 2.0, k = 0.5):
        self.Td = temp_desejada
        self.sigma = sigma
        self.alpha = alpha
        self.beta = beta
        self.k = k 

        # Histerese baseada em sigma para evitar chaveamento excessivo.
        self.ligar_limite = self.Td + (3 * self.sigma)
        self.desligar_limite = self.Td + self.sigma

        self.ac_ligado = False
        self.tempo_espera_restante = 0
        self.TEMPO_MAX_ESPERA = 10
        self.historico_leituras = []

        self.taxa_r = []
        self.taxa_e = []
        self.T_inicio_episodio = None
        self.passos_episodio = 0



    def calcular_limiar (self):
         #L = Td + 3σ
        return self.ligar_limite
    
    def calcular_custo(self, Ta):
        #Regra 5: J = α|Ta - Td| + β·C_ligado
        c_ligado = 1 if self.ac_ligado else 0
        return self.alpha * abs(Ta - self.Td) + self.beta * c_ligado
    
    def atualizar_aprendizado(self, Ta):
        #r↓ = (T_início - Td) / Δt   (resfriamento com AC ligado)
        #r↑ = (Td - T_início) / Δt   (elevação sem AC)

        if self.T_inicio_episodio is not None and self.passos_episodio > 0:
            delta_t = self.passos_episodio
            if self.ac_ligado and Ta < self.T_inicio_episodio:
                taxa = (self.T_inicio_episodio - Ta) / delta_t
                if taxa > 0:
                    self.taxa_r.append(taxa)
            elif not self.ac_ligado and Ta > self.T_inicio_episodio:
                taxa = (Ta - self.T_inicio_episodio) / delta_t
                if taxa > 0:
                    self.taxa_e.append(taxa)
        
        self.T_inicio_episodio = Ta
        self.passos_episodio = 0


    def perceber(self, ambiente):

        if self.tempo_espera_restante > 0:
            self.tempo_espera_restante -= 1
            self.passos_episodio += 1
            return None
        
        Ta = ambiente.temperatura
        self.historico_leituras.append(Ta)
        self.passos_episodio += 1
        self.atualizar_aprendizado(Ta)

        return {
            "Ta": Ta,
            "L": self.calcular_limiar(),
            "custo": self.calcular_custo(Ta)
        }

    def decidir(self, percepcao):
        if percepcao is None:
            return "manter (em espera)"
        
        Ta = percepcao["Ta"]
        L = self.ligar_limite

        # Regra 7: Ligar se exceder o limite L
        if Ta > L:
            if not self.ac_ligado:
                self.ac_ligado = True
                acao = "ligar e resfriar"
            else:
                acao = "manter resfriando"

            # Regra 8: Cálculo de espera para resfriamento
            r_desc = sum(self.taxa_r)/len(self.taxa_r) if self.taxa_r else None
            espera = math.ceil((Ta - self.Td) / r_desc) if r_desc else math.ceil(self.k * (Ta - self.Td))
            
            self.tempo_espera_restante = min(max(0, espera), self.TEMPO_MAX_ESPERA)
            return acao
            
        # Regra 9: Desligar usando limiar inferior (histerese)
        if self.ac_ligado and Ta <= self.desligar_limite:
            self.ac_ligado = False
            self.tempo_espera_restante = 0 # CORREÇÃO: Resetar espera ao mudar de estado
            return "desligado"

        # Regra 10: Espera durante a elevação (AC desligado)
        if not self.ac_ligado:
            if Ta < self.Td: # Se ainda está abaixo da meta, estima quanto tempo leva para subir
                r_elev = sum(self.taxa_e)/len(self.taxa_e) if self.taxa_e else None
                espera = math.ceil((self.Td - Ta) / r_elev) if r_elev else math.ceil(self.k * (self.Td - Ta))
                self.tempo_espera_restante = min(max(0, espera), self.TEMPO_MAX_ESPERA)
            else:
                # Se está acima da meta mas abaixo do limite L, checa com frequência máxima
                self.tempo_espera_restante = 0 

        return "manter"
        

    def agir(self, ambiente):
        percepcao = self.perceber(ambiente)
        acao = self.decidir(percepcao)
 
        ambiente.ligado = self.ac_ligado
        return acao

def executar_cenario(nome: str, sequencia_temperaturas: list[float]):
    print(f"\n{'=' * 62}")
    print(f"  {nome}")
    print(f"  Sequência: {sequencia_temperaturas}")
    print(f"{'=' * 62}")

    agente  = AgenteTemperatura()
    ambiente = Ambiente(temperatura=sequencia_temperaturas[0], estado_ac=False)

    for i, temp in enumerate(sequencia_temperaturas):
        ambiente.temperatura = temp
        acao = agente.agir(ambiente)
        estado = "ON" if ambiente.ligado else "OFF"
        print(
            f"  Passo {i+1:02d} | T={temp:5.1f}°C | "
            f"ação={acao:22s} | AC={estado} | "
            f"espera={agente.tempo_espera_restante:2d} | "
            f"custo={agente.calcular_custo(temp):.2f}"
        )

    print(f"\n  Estado final        : {ambiente}")
    # [CORRIGIDO B1] era agente.historico → corrigido para agente.historico_leituras
    print(f"  Leituras armazenadas: {len(agente.historico_leituras)}")
    print(f"  taxa_r aprendidas   : {[round(t,3) for t in agente.taxa_r]}")
    print(f"  taxa_e aprendidas   : {[round(t,3) for t in agente.taxa_e]}")


def executar_cenario_dinamico(
    nome: str,
    temp_inicial: float,
    passos: int,
    temp_desejada: float = 23.0,
):
    print(f"\n{'=' * 62}")
    print(f"  {nome}")
    print(f"  Temperatura desejada: {temp_desejada:.1f}°C")
    print(f"{'=' * 62}")

    agente  = AgenteTemperatura(temp_desejada=temp_desejada)
    ambiente = Ambiente(temperatura=temp_inicial, estado_ac=False)

    for t in range(passos):
        acao = agente.agir(ambiente)
        ambiente.atualizar()
        estado = "ON" if ambiente.ligado else "OFF"
        print(
            f"  t={t:02d} | {str(ambiente):44s} | "
            f"ação={acao:22s} | espera={agente.tempo_espera_restante:2d}"
        )

    print(f"\n  Estado final        : {ambiente}")
    print(f"  Leituras armazenadas: {len(agente.historico_leituras)}")
    print(f"  taxa_r aprendidas   : {[round(t,3) for t in agente.taxa_r]}")
    print(f"  taxa_e aprendidas   : {[round(t,3) for t in agente.taxa_e]}")
 
# ─── Parte 3 — Cenários de Teste ─────────────────────────────────────────────
 
if __name__ == "__main__":
 
    print("\n" + "=" * 60)
    print("  CSI457 — Agente de Controle de Temperatura (v2)")
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
    
    executar_cenario_dinamico(
        "Cenário 3 — Ambiente quente",
        temp_inicial=30.0,
        passos=30,
        temp_desejada=23.0,
    )

    # Cenário 4 — Ambiente estável
    executar_cenario_dinamico(
        "Cenário 4 — Ambiente moderado",
        temp_inicial=25.0,
        passos=30,
        temp_desejada=24.0,
    )