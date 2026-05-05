#include <DHT.h> include a biblioteca DHT para sensores de temperatura e umidade
#include <math.h>

#define DHTPIN 2     // Fio do sensor azul
#define DHTTYPE DHT11 
#define PIN_RELE 10  // Fio marrom do módulo relé
#define PIN_LED 13

DHT dht(DHTPIN, DHTTYPE);

#define MAX_HISTORICO 1000
#define MAX_TAXA_R 5
#define MAX_TAXA_E 5
#define MAX_ACAO_STR 30

// ===== ESTRUTURA DO AGENTE =====
typedef struct {
    float Td;
    float sigma;
    float alpha;
    float beta;
    float k;

    float ligar_limite;
    float desligar_limite;
    float deadband;
    float limite_critico;
    float MARGEM_DESLIGAMENTO;

    int ac_ligado;
    int tempo_espera_restante;
    int contador_estado;

    int tempo_min_ligado;
    int tempo_min_desligado;

    float taxa_r[MAX_TAXA_R];
    float taxa_e[MAX_TAXA_E];
    int count_r;
    int count_e;

    float T_inicio_episodio;
    int passos_episodio;
    float historico_leituras[MAX_HISTORICO];
    int tamanho_historico;

    int JANELA_TAXAS;
    int TEMPO_MIN_ESPERA;
    int TEMPO_MAX_ESPERA;

} Agente;

// ===== INIT =====
void init_agente(Agente *a, float Td) {
    a->Td = Td;
    a->sigma = 0.2;
    a->alpha = 1.0;
    a->beta = 2.0;
    a->k = 0.5;

    a->ligar_limite = Td + (3 * a->sigma);
    a->desligar_limite = Td + a->sigma;
    a->deadband = 0.3;
    a->limite_critico = Td + 5;
    a->MARGEM_DESLIGAMENTO = 0.1;

    a->ac_ligado = 0;
    a->tempo_espera_restante = 0;
    a->contador_estado = 0;

    a->tempo_min_ligado = 3;
    a->tempo_min_desligado = 3;

    a->count_r = 0;
    a->count_e = 0;
    a->passos_episodio = 0;
    a->T_inicio_episodio = -999.0;

    a->tamanho_historico = 0;

    a->JANELA_TAXAS = 5;
    a->TEMPO_MIN_ESPERA = 1;
    a->TEMPO_MAX_ESPERA = 8;

    // Inicializar arrays
    for (int i = 0; i < MAX_TAXA_R; i++) {
        a->taxa_r[i] = 0.0;
        a->taxa_e[i] = 0.0;
    }
}

// ===== CUSTO =====
float calcular_custo(Agente *a, float Ta) {
    int ligado = a->ac_ligado ? 1 : 0;
    return a->alpha * fabs(Ta - a->Td) + a->beta * ligado;
}

float calcular_limiar(Agente *a) {
    return a->ligar_limite;
}

// ===== MÉDIA =====
float media(float *arr, int n) {
    if (n == 0) return -1.0;
    float soma = 0.0;
    for (int i = 0; i < n; i++) soma += arr[i];
    return soma / n;
}

// ===== APRENDIZADO =====
void atualizar_aprendizado(Agente *a, float Ta) {
    if (a->T_inicio_episodio >= -999.0 && a->passos_episodio > 0) {
        float dt = (float)a->passos_episodio;

        if (a->ac_ligado && Ta < a->T_inicio_episodio) {
            float taxa = (a->T_inicio_episodio - Ta) / dt;
            if (taxa > 0.0) {
                a->taxa_r[a->count_r % MAX_TAXA_R] = taxa;
                a->count_r++;
            }
        }

        if (!a->ac_ligado && Ta > a->T_inicio_episodio) {
            float taxa = (Ta - a->T_inicio_episodio) / dt;
            if (taxa > 0.0) {
                a->taxa_e[a->count_e % MAX_TAXA_E] = taxa;
                a->count_e++;
            }
        }
    }

    a->T_inicio_episodio = Ta;
    a->passos_episodio = 0;
}

// ===== PERCEPÇÃO (separada da decisão - 100% fiel ao Python) =====
typedef struct {
    float Ta;
    float L;
    float custo;
} Percepcao;

Percepcao* perceber(Agente *a, Ambiente *env) {
    // Se está em espera, apenas decrementa o contador
    if (a->tempo_espera_restante > 0) {
        a->tempo_espera_restante--;
        a->passos_episodio++;
        return NULL;
    }

    float Ta = env->temperatura;

    // Armazena no histórico (Python: historico_leituras.append(Ta))
    if (a->tamanho_historico < MAX_HISTORICO) {
        a->historico_leituras[a->tamanho_historico] = Ta;
        a->tamanho_historico++;
    }

    a->passos_episodio++;
    atualizar_aprendizado(a, Ta);

    // Aloca memória para a percepção (será liberada após uso)
    static Percepcao perc;
    perc.Ta = Ta;
    perc.L = calcular_limiar(a);
    perc.custo = calcular_custo(a, Ta);

    return &perc;
}

// ===== DECISÃO =====
const char* decidir(Agente *a, Percepcao *perc) {
    if (perc == NULL) {
        return "ESPERA";
    }

    float Ta = perc->Ta;
    float L = a->ligar_limite;
    float limite_desligar = a->desligar_limite + a->MARGEM_DESLIGAMENTO;

    int pode_ligar = (!a->ac_ligado) && (a->contador_estado >= a->tempo_min_desligado);
    int pode_desligar = (a->ac_ligado) && (a->contador_estado >= a->tempo_min_ligado);

    if (Ta >= a->limite_critico) {
        if (!a->ac_ligado) {
            a->ac_ligado = 1;
            a->contador_estado = 0;
            return "EMERGENCIA";
        }
        return "RESFRIANDO_CRITICO";
    }

    if (a->ac_ligado && Ta <= limite_desligar) {
        if (pode_desligar) {
            a->ac_ligado = 0;
            a->contador_estado = 0;
            a->tempo_espera_restante = 0;  // CORREÇÃO Python: resetar espera
            return "DESLIGADO";
        }
        return "MIN_ON";
    }

     if ((a->Td - a->deadband) <= Ta && Ta <= (a->Td + a->deadband)) {
        return "DEADBAND";
    }

    if (Ta > L) {
        if (!a->ac_ligado) {
            if (!pode_ligar) {
                return "MIN_OFF";
            }
            a->ac_ligado = 1;
            a->contador_estado = 0;
        }
        
        int num_taxas = (a->count_r < MAX_TAXA_R) ? a->count_r : MAX_TAXA_R;
        float r_desc = media(a->taxa_r, num_taxas);

        int espera;
        if (r_desc > 0.0) {
            espera = (int)ceil((Ta - a->Td) / r_desc);
        } else {
            espera = (int)ceil(a->k * (Ta - a->Td));
        }

        // Clampa entre TEMPO_MIN_ESPERA e TEMPO_MAX_ESPERA
        if (espera < a->TEMPO_MIN_ESPERA) espera = a->TEMPO_MIN_ESPERA;
        if (espera > a->TEMPO_MAX_ESPERA) espera = a->TEMPO_MAX_ESPERA;

        a->tempo_espera_restante = espera;
        return "RESFRIANDO";
    }

    if (!a->ac_ligado && Ta < a->Td) {
        int num_taxas = (a->count_e < MAX_TAXA_E) ? a->count_e : MAX_TAXA_E;
        float r_elev = media(a->taxa_e, num_taxas);

        int espera;
        if (r_elev > 0.0) {
            espera = (int)ceil((a->Td - Ta) / r_elev);
        } else {
            espera = (int)ceil(a->k * (a->Td - Ta));
        }

        if (espera < a->TEMPO_MIN_ESPERA) espera = a->TEMPO_MIN_ESPERA;
        if (espera > a->TEMPO_MAX_ESPERA) espera = a->TEMPO_MAX_ESPERA;

        a->tempo_espera_restante = espera;
    } else if (!a->ac_ligado && Ta >= a->Td && Ta <= L) {
        // Acima da meta mas abaixo do limite - checa com frequência máxima
        a->tempo_espera_restante = 0;
    }

    return "MANTER";
}

const char* agir(Agente *a, Ambiente *env) {
    Percepcao *perc = perceber(a, env);
    const char *acao = decidir(a, perc);

    // Atualiza o estado do AC no ambiente
    env->ligado = a->ac_ligado;
    a->contador_estado++;

    return acao;
}

void imprimir_historico(Agente *a) {
    Serial.println("\n=== HISTÓRICO DE LEITURAS ===");
    Serial.print("Total de leituras: ");
    Serial.println(a->tamanho_historico);
    
    Serial.print("Primeiras 10: ");
    for (int i = 0; i < (a->tamanho_historico < 10 ? a->tamanho_historico : 10); i++) {
        Serial.print(a->historico_leituras[i]);
        Serial.print(" ");
    }
    Serial.println();

    if (a->tamanho_historico > 10) {
        Serial.print("Últimas 10: ");
        int inicio = a->tamanho_historico - 10;
        for (int i = inicio; i < a->tamanho_historico; i++) {
            Serial.print(a->historico_leituras[i]);
            Serial.print(" ");
        }
        Serial.println();
    }
}

void imprimir_taxas(Agente *a) {
    Serial.print("Taxa R (resfriamento): ");
    int n_r = (a->count_r < MAX_TAXA_R) ? a->count_r : MAX_TAXA_R;
    for (int i = 0; i < n_r; i++) {
        Serial.print("[");
        Serial.print(a->taxa_r[i], 3);
        Serial.print("] ");
    }
    Serial.println();

    Serial.print("Taxa E (elevação): ");
    int n_e = (a->count_e < MAX_TAXA_E) ? a->count_e : MAX_TAXA_E;
    for (int i = 0; i < n_e; i++) {
        Serial.print("[");
        Serial.print(a->taxa_e[i], 3);
        Serial.print("] ");
    }
    Serial.println();
}

// ===== AGENTE =====
Agente agente;

// ===== SETUP =====
void setup() {
    Serial.begin(9600);
    dht.begin();
    pinMode(PIN_RELE, OUTPUT);
    pinMode(PIN_LED, OUTPUT);
    
    float temp_desejada = 35.0;

    init_agente(&agente, temp_desejada);

    Serial.println("================================");
    Serial.println("AGENTE CSI457 v2 - ESP32 ONLINE");
    Serial.println("================================");
    Serial.print("Temperatura Desejada: ");
    Serial.println(temp_desejada);
    
}

// ===== LOOP =====
void loop() {
    float temp = dht.readTemperature();

    if (isnan(temp)) {
        Serial.println("Erro leitura");
        delay(2000);
        return;
    }

    const char* acao = decidir(&agente, temp);

    digitalWrite(PIN_RELE, agente.ac_ligado ? HIGH : LOW);
    digitalWrite(PIN_LED, agente.ac_ligado ? HIGH : LOW);
    
    agente.contador_estado++;

    float custo = calcular_custo(&agente, temp);

    Serial.print("T: ");
    Serial.print(temp);
    Serial.print(" | AC: ");
    Serial.print(agente.ac_ligado ? "ON" : "OFF");
    Serial.print(" | Espera: ");
    Serial.print(agente.tempo_espera_restante);
    Serial.print(" | ");
    Serial.println(acao);

    delay(2000);
}