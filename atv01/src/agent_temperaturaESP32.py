#import machine import machine para controle de GPIO
#import dht import dht para sensor DHT11
import time
import math

class AgenteTemperatura:
    def __init__(self, temp_desejada=23.0, sigma=0.2, alpha=1.0, beta=2.0, k=0.5):
        self.Td = temp_desejada
        self.sigma = sigma
        self.alpha = alpha
        self.beta = beta
        self.k = k 

        # Histerese e Limites
        self.ligar_limite = self.Td + (3 * self.sigma)
        self.desligar_limite = self.Td + self.sigma
        self.deadband = 0.3
        self.limite_critico = self.Td + 5

        # Estado do Agente
        self.ac_ligado = False
        self.tempo_espera_restante = 0
        self.contador_estado = 0
        
        # Configurações de tempo
        self.TEMPO_MIN_ESPERA = 1
        self.TEMPO_MAX_ESPERA = 8
        self.tempo_min_ligado = 3
        self.tempo_min_desligado = 3
        
        # Aprendizado
        self.JANELA_TAXAS = 5
        self.MARGEM_DESLIGAMENTO = 0.1
        self.historico_leituras = []
        self.taxa_r = []
        self.taxa_e = []
        self.T_inicio_episodio = None
        self.passos_episodio = 0

    def calcular_limiar(self):
        return self.ligar_limite
    
    def calcular_custo(self, Ta):
        c_ligado = 1 if self.ac_ligado else 0
        return self.alpha * abs(Ta - self.Td) + self.beta * c_ligado
    
    def atualizar_aprendizado(self, Ta):
        if self.T_inicio_episodio is not None and self.passos_episodio > 0:
            delta_t = self.passos_episodio
            if self.ac_ligado and Ta < self.T_inicio_episodio:
                taxa = (self.T_inicio_episodio - Ta) / delta_t
                if taxa > 0:
                    self.taxa_r.append(taxa)
                    self.taxa_r = self.taxa_r[-self.JANELA_TAXAS:]
            elif not self.ac_ligado and Ta > self.T_inicio_episodio:
                taxa = (Ta - self.T_inicio_episodio) / delta_t
                if taxa > 0:
                    self.taxa_e.append(taxa)
                    self.taxa_e = self.taxa_e[-self.JANELA_TAXAS:]
        
        self.T_inicio_episodio = Ta
        self.passos_episodio = 0

    def decidir(self, Ta):
        # Gerenciamento de espera (Sleep do Agente)
        if self.tempo_espera_restante > 0:
            self.tempo_espera_restante -= 1
            self.passos_episodio += 1
            return "manter (em espera)"

        self.historico_leituras.append(Ta)
        self.passos_episodio += 1
        self.atualizar_aprendizado(Ta)

        L = self.ligar_limite
        limite_desligar = self.desligar_limite + self.MARGEM_DESLIGAMENTO
        pode_ligar = (not self.ac_ligado) and (self.contador_estado >= self.tempo_min_desligado)
        pode_desligar = self.ac_ligado and (self.contador_estado >= self.tempo_min_ligado)

        # 1. Caso Crítico
        if Ta >= self.limite_critico:
            if not self.ac_ligado:
                self.ac_ligado = True
                self.contador_estado = 0
                return "ligar emergencia"
            return "manter resfriando (emergencia)"

        # 2. Desligamento (Meta atingida + Tempo mínimo ON)
        if self.ac_ligado and Ta <= limite_desligar:
            if pode_desligar:
                self.ac_ligado = False
                self.contador_estado = 0
                self.tempo_espera_restante = 0
                return "desligado"
            return "manter resfriando (min ON)"

        # 3. Deadband (Zona morta)
        if (self.Td - self.deadband) <= Ta <= (self.Td + self.deadband):
            return "manter (deadband)"

        # 4. Ligar (Acima do Limite L)
        if Ta > L:
            if not self.ac_ligado:
                if not pode_ligar: return "manter (min OFF)"
                self.ac_ligado = True
                self.contador_estado = 0
                acao = "ligar e resfriar"
            else:
                acao = "manter resfriando"

            r_desc = sum(self.taxa_r)/len(self.taxa_r) if self.taxa_r else None
            espera = math.ceil((Ta - self.Td) / r_desc) if r_desc else math.ceil(self.k * (Ta - self.Td))
            self.tempo_espera_restante = min(max(self.TEMPO_MIN_ESPERA, espera), self.TEMPO_MAX_ESPERA)
            return acao

        # 5. Espera (Abaixo da meta, subindo)
        if not self.ac_ligado:
            if Ta < self.Td:
                r_elev = sum(self.taxa_e)/len(self.taxa_e) if self.taxa_e else None
                espera = math.ceil((self.Td - Ta) / r_elev) if r_elev else math.ceil(self.k * (self.Td - Ta))
                self.tempo_espera_restante = min(max(self.TEMPO_MIN_ESPERA, espera), self.TEMPO_MAX_ESPERA)
            else:
                self.tempo_espera_restante = 0 

        return "manter"

# --- CONFIGURAÇÃO DE HARDWARE ---
PINO_SENSOR = 15
PINO_RELE = 14

sensor = dht.DHT22(machine.Pin(PINO_SENSOR))
rele = machine.Pin(PINO_RELE, machine.Pin.OUT)

# Inicializa o agente (ex: meta 25°C)
agente = AgenteTemperatura(temp_desejada=25.0)

print("="*40)
print(" AGENTE CSI457 v2 - ESP32 ONLINE")
print("="*40)

while True:
    try:
        # 1. Percepção (Leitura do sensor real)
        sensor.measure()
        temp_real = sensor.temperature()
        
        # 2. Decisão (Lógica do Agente)
        acao = agente.decidir(temp_real)
        
        # 3. Ação (Controle do Relé)
        rele.value(1 if agente.ac_ligado else 0)
        agente.contador_estado += 1
        
        # Saída de Monitoramento
        custo = agente.calcular_custo(temp_real)
        status_ac = "ON" if agente.ac_ligado else "OFF"
        
        print(f"T: {temp_real:.1f}°C | AC: {status_ac} | Espera: {agente.tempo_espera_restante} | {acao}")
        
        if agente.taxa_r:
            print(f"   [Aprendizado] Taxa R média: {sum(agente.taxa_r)/len(agente.taxa_r):.3f}")

    except Exception as e:
        print("Falha na leitura:", e)

    # O ciclo do agente acontece a cada 2 segundos (limite do DHT22)
    time.sleep(2)