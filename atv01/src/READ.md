# Parte 1 — Especificação do Agente

## 1. Percepções

- P1 Temperatura Atual do Ambiente
- P2 O ambiente está na temperatura ideal
- P3 O ar condicionado está ligado
- P4 O ar condicionado está desligado

## 2. Ações

- A1 Ligar o ar condicionado
- A2 Desligar o ar condicionado
- A3 Esquentar o ambiente
- A4 Esfriar o ambiente
- A5 Manter temperatura

## 3. Função do agente

`f : P∗ → A`

A função do agente mapeia cada estado percebido a uma ação. Considerando uma faixa ideal de temperatura entre 20°C e 24°C:

- Se a percepção da temperatura for < 20°C e AC desligado a ação seria ligar AC e esquentar o ambiente
- Se a percepção da temperatura for < 20°C e AC ligado a ação seria esquentar o ambiente
- Se a percepção da temperatura for entre 20°C e 24°C e AC ligado a ação seria manter temperatura do ambiente
- Se a percepção da temperatura for entre 20°C e 24°C e AC desligado a ação seria nenhuma ação (não ligar)
- Se a percepção da temperatura for > 24°C e AC desligado a ação seria ligar AC e esfriar o ambiente
- Se a percepção da temperatura for > 24°C e AC ligado a ação seria esfriar
- Se a percepção da temperatura for ideal por tempo prolongado a ação seria emitir alerta e desligar AC

## 4. Critério de racionalidade

- O ideal seria manter a temperatura em uma faixa específica
- Não oscilar muito a  temperatura
- Minimizar o consumo de energia
- Não desligar sem alerta.
- Quando abaixo da faixa, aumentar temperatura
- Quando acima da faixa , diminuir temperatura
- Se não tiver nescessidade de estar ligado desligue o ar condicionado

# Parte 2 — Implementação

Em agente_temperatura.py

# Parte 3 — Testes

## Cenário 1 — Oscilação

- Sequência: [24.9, 25.1, 24.8, 25.2]
- Faixa ideal: 20.0°C – 24.0°C | OSCILAÇÃO: ±0.5°C

```text
Passo 1: temperatura = 24.9°C | ação = ligar e resfriar ambiente | sistema = ON
Passo 2: temperatura = 25.1°C | ação = resfriar ambiente | sistema = ON
Passo 3: temperatura = 24.8°C | ação = resfriar ambiente | sistema = ON
Passo 4: temperatura = 25.2°C | ação = resfriar ambiente | sistema = ON

Estado final: Temperatura: 25.2°C, Ar Condicionado: Ligado
Total de percepções registradas: 4
```

## Cenário 2 — Calor extremo

- Sequência: [30, 32, 35]
- Faixa ideal: 20.0°C – 24.0°C | OSCILAÇÃO: ±0.5°C

```text
Passo 1: temperatura = 30.0°C | ação = ligar e resfriar ambiente | sistema = ON
Passo 2: temperatura = 32.0°C | ação = resfriar ambiente | sistema = ON
Passo 3: temperatura = 35.0°C | ação = resfriar ambiente | sistema = ON

Estado final: Temperatura: 35.0°C, Ar Condicionado: Ligado
Total de percepções registradas: 3
```

## Cenário 3 — Resfriamento gradual

- Sequência: [28, 27, 26, 25, 24]
- Faixa ideal: 20.0°C – 24.0°C | OSCILAÇÃO: ±0.5°C

```text
Passo 1: temperatura = 28.0°C | ação = ligar e resfriar ambiente | sistema = ON
Passo 2: temperatura = 27.0°C | ação = resfriar ambiente | sistema = ON
Passo 3: temperatura = 26.0°C | ação = resfriar ambiente | sistema = ON
Passo 4: temperatura = 25.0°C | ação = resfriar ambiente | sistema = ON
Passo 5: temperatura = 24.0°C | ação = desligar | sistema = OFF

Estado final: Temperatura: 24.0°C, Ar Condicionado: Desligado
Total de percepções registradas: 5
```