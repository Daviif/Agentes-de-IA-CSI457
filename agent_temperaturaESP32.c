#include <DHT.h> include a biblioteca DHT para sensores de temperatura e umidade
#include <math.h>

#define DHTPIN 2     // Fio do sensor azul
#define DHTTYPE DHT11 
#define PIN_RELE 10  // Fio marrom do módulo relé
#define PIN_LED 13

DHT dht(DHTPIN, DHTTYPE);

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

    int ac_ligado;
    int tempo_espera_restante;
    int contador_estado;

    int tempo_min_ligado;
    int tempo_min_desligado;

    float taxa_r[5];
    float taxa_e[5];
    int count_r;
    int count_e;

    float T_inicio_episodio;
    int passos_episodio;

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

    a->ac_ligado = 0;
    a->tempo_espera_restante = 0;
    a->contador_estado = 0;

    a->tempo_min_ligado = 3;
    a->tempo_min_desligado = 3;

    a->count_r = 0;
    a->count_e = 0;
    a->passos_episodio = 0;
}

// ===== CUSTO =====
float calcular_custo(Agente *a, float Ta) {
    int ligado = a->ac_ligado ? 1 : 0;
    return a->alpha * fabs(Ta - a->Td) + a->beta * ligado;
}

// ===== MÉDIA =====
float media(float *arr, int n) {
    if (n == 0) return -1;
    float soma = 0;
    for (int i = 0; i < n; i++) soma += arr[i];
    return soma / n;
}

// ===== APRENDIZADO =====
void atualizar_aprendizado(Agente *a, float Ta) {
    if (a->passos_episodio > 0) {
        float dt = a->passos_episodio;

        if (a->ac_ligado && Ta < a->T_inicio_episodio) {
            float taxa = (a->T_inicio_episodio - Ta) / dt;
            if (taxa > 0) {
                a->taxa_r[a->count_r % 5] = taxa;
                a->count_r++;
            }
        }

        if (!a->ac_ligado && Ta > a->T_inicio_episodio) {
            float taxa = (Ta - a->T_inicio_episodio) / dt;
            if (taxa > 0) {
                a->taxa_e[a->count_e % 5] = taxa;
                a->count_e++;
            }
        }
    }

    a->T_inicio_episodio = Ta;
    a->passos_episodio = 0;
}

// ===== DECISÃO =====
const char* decidir(Agente *a, float Ta) {

    if (a->tempo_espera_restante > 0) {
        a->tempo_espera_restante--;
        a->passos_episodio++;
        return "ESPERA";
    }

    a->passos_episodio++;
    atualizar_aprendizado(a, Ta);

    int pode_ligar = (!a->ac_ligado && a->contador_estado >= a->tempo_min_desligado);
    int pode_desligar = (a->ac_ligado && a->contador_estado >= a->tempo_min_ligado);

    float limite_desligar = a->desligar_limite + 0.1;

    // CRÍTICO
    if (Ta >= a->limite_critico) {
        if (!a->ac_ligado) {
            a->ac_ligado = 1;
            a->contador_estado = 0;
            return "EMERGENCIA";
        }
        return "RESFRIANDO";
    }

    // DESLIGAR
    if (a->ac_ligado && Ta <= limite_desligar) {
        if (pode_desligar) {
            a->ac_ligado = 0;
            a->contador_estado = 0;
            a->tempo_espera_restante = 0;
            return "DESLIGAR";
        }
        return "MIN_ON";
    }

    // DEADBAND
    if (Ta >= (a->Td - a->deadband) && Ta <= (a->Td + a->deadband)) {
        return "DEADBAND";
    }

    // LIGAR
    if (Ta > a->ligar_limite) {
        if (!a->ac_ligado && pode_ligar) {
            a->ac_ligado = 1;
            a->contador_estado = 0;
        }

        float r = media(a->taxa_r, (a->count_r < 5 ? a->count_r : 5));

        int espera;
        if (r > 0)
            espera = ceil((Ta - a->Td) / r);
        else
            espera = ceil(a->k * (Ta - a->Td));

        if (espera < 1) espera = 1;
        if (espera > 8) espera = 8;

        a->tempo_espera_restante = espera;

        return "RESFRIANDO";
    }

    // ESPERA SUBIDA
    if (!a->ac_ligado && Ta < a->Td) {
        float r = media(a->taxa_e, (a->count_e < 5 ? a->count_e : 5));

        int espera;
        if (r > 0)
            espera = ceil((a->Td - Ta) / r);
        else
            espera = ceil(a->k * (a->Td - Ta));

        if (espera < 1) espera = 1;
        if (espera > 8) espera = 8;

        a->tempo_espera_restante = espera;
    }

    return "MANTER";
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