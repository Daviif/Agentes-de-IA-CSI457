# Parte 1 — Especificação do Agente

## 1. Percepções

- P1 Temperatura Atual do Ambiente
- P2 O ambiente está próximo da temperatura desejada
- P3 O ar condicionado está ligado
- P4 O ar condicionado está desligado
- P5 O sistema está em período de espera
- P6 Há histórico de taxa de resfriamento
- P7 Há histórico de taxa de aquecimento

## 2. Ações

- A1 Ligar o ar condicionado
- A2 Desligar o ar condicionado
- A3 Manter resfriando
- A4 Manter temperatura
- A5 Aguardar novo ciclo de percepção
- A6 Ligar em emergência
- A7 Manter resfriando em emergência

## 3. Função do agente

`f : P∗ → A`

A função do agente mapeia cada estado percebido a uma ação. Considerando a temperatura desejada em 23°C, histerese baseada em sigma e limites de segurança:

- Se a temperatura estiver acima do limite de acionamento e o AC estiver desligado, a ação é ligar o AC e resfriar.
- Se a temperatura estiver acima do limite de acionamento e o AC estiver ligado, a ação é manter resfriando.
- Se a temperatura estiver abaixo da temperatura desejada e o AC estiver desligado, a ação é aguardar o próximo ciclo ou ligar somente quando permitido pelo tempo mínimo.
- Se a temperatura estiver abaixo do limiar de desligamento com AC ligado, a ação é desligar quando o tempo mínimo ligado for respeitado; caso contrário, manter resfriando (min ON).
- Se a temperatura estiver na deadband ao redor da meta, a ação é manter temperatura.
- Se o sistema estiver em espera, a ação é manter (em espera).
- Se a temperatura atingir a faixa crítica, a ação é ligar em emergência ou manter resfriando em emergência.
- Se o AC estiver desligado e a temperatura estiver abaixo da meta, o agente calcula tempo de espera para nova percepção com base na taxa de elevação aprendida.

## 4. Critério de racionalidade

- Manter a temperatura o mais próximo possível da desejada.
- Evitar chaveamento excessivo com histerese e deadband.
- Minimizar consumo de energia quando não houver necessidade de resfriamento.
- Respeitar tempos mínimos ligado e desligado.
- Usar histórico de taxas para estimar o tempo de espera entre percepções.
- Priorizar resposta imediata em situação crítica.
- Aplicar custo de controle com erro de temperatura e penalidade de AC ligado.

# Parte 2 — Implementação

Em agente_temperatura1.py

# Parte 3 — Testes

## Cenário 1 — Oscilação

- Sequência: [24.9, 25.1, 24.8, 25.2]
- Temperatura desejada: 23.0°C

```text
Passo 01 | T= 24.9°C | ação=manter (min OFF)       | AC=OFF | espera= 0 | custo=1.90
Passo 02 | T= 25.1°C | ação=manter (min OFF)       | AC=OFF | espera= 0 | custo=2.10
Passo 03 | T= 24.8°C | ação=manter (min OFF)       | AC=OFF | espera= 0 | custo=1.80
Passo 04 | T= 25.2°C | ação=ligar e resfriar       | AC=ON | espera= 2 | custo=4.20

Estado final        : Temperatura: 25.20°C, Ar Condicionado: Ligado
Leituras armazenadas: 4
taxa_r aprendidas   : []
taxa_e aprendidas   : [0.2, 0.4]
```

## Cenário 2 — Calor extremo

- Sequência: [30, 32, 35]
- Temperatura desejada: 23.0°C

```text
Passo 01 | T= 30.0°C | ação=ligar emergencia       | AC=ON | espera= 0 | custo=9.00
Passo 02 | T= 32.0°C | ação=manter resfriando (emergencia) | AC=ON | espera= 0 | custo=11.00
Passo 03 | T= 35.0°C | ação=manter resfriando (emergencia) | AC=ON | espera= 0 | custo=14.00

Estado final        : Temperatura: 35.00°C, Ar Condicionado: Ligado
Leituras armazenadas: 3
taxa_r aprendidas   : []
taxa_e aprendidas   : []
```

## Cenário 3 — Resfriamento gradual

- Sequência: [28, 27, 26, 25, 24]
- Temperatura desejada: 23.0°C

```text
Passo 01 | T= 28.0°C | ação=ligar emergencia       | AC=ON | espera= 0 | custo=7.00
Passo 02 | T= 27.0°C | ação=manter resfriando      | AC=ON | espera= 4 | custo=6.00
Passo 03 | T= 26.0°C | ação=manter (em espera)     | AC=ON | espera= 3 | custo=5.00
Passo 04 | T= 25.0°C | ação=manter (em espera)     | AC=ON | espera= 2 | custo=4.00
Passo 05 | T= 24.0°C | ação=manter (em espera)     | AC=ON | espera= 1 | custo=3.00

Estado final        : Temperatura: 24.00°C, Ar Condicionado: Ligado
Leituras armazenadas: 2
taxa_r aprendidas   : [1.0]
taxa_e aprendidas   : []
```

## Cenário 4 — Ambiente quente em evolução

- Sequência: simulação dinâmica com temperatura inicial de 30.0°C
- Temperatura desejada: 23.0°C

```text
O agente percebe o ambiente, atualiza o estado do ar condicionado e reduz gradualmente a temperatura até estabilizar.
t=00 | Temperatura: 29.70°C, Ar Condicionado: Ligado | ação=ligar emergencia       | espera= 0 | custo=8.70
t=01 | Temperatura: 29.40°C, Ar Condicionado: Ligado | ação=manter resfriando (emergencia) | espera= 0 | custo=8.40
t=02 | Temperatura: 29.10°C, Ar Condicionado: Ligado | ação=manter resfriando (emergencia) | espera= 0 | custo=8.10
t=03 | Temperatura: 28.80°C, Ar Condicionado: Ligado | ação=manter resfriando (emergencia) | espera= 0 | custo=7.80
t=04 | Temperatura: 28.50°C, Ar Condicionado: Ligado | ação=manter resfriando (emergencia) | espera= 0 | custo=7.50
t=05 | Temperatura: 28.20°C, Ar Condicionado: Ligado | ação=manter resfriando (emergencia) | espera= 0 | custo=7.20
t=06 | Temperatura: 27.90°C, Ar Condicionado: Ligado | ação=manter resfriando (emergencia) | espera= 0 | custo=6.90
t=07 | Temperatura: 27.60°C, Ar Condicionado: Ligado | ação=manter resfriando      | espera= 8 | custo=6.60
t=08 | Temperatura: 27.30°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 7 | custo=6.30
t=09 | Temperatura: 27.00°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 6 | custo=6.00
t=10 | Temperatura: 26.70°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 5 | custo=5.70
t=11 | Temperatura: 26.40°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 4 | custo=5.40
t=12 | Temperatura: 26.10°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 3 | custo=5.10
t=13 | Temperatura: 25.80°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 2 | custo=4.80
t=14 | Temperatura: 25.50°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 1 | custo=4.50
t=15 | Temperatura: 25.20°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 0 | custo=4.20
t=16 | Temperatura: 24.90°C, Ar Condicionado: Ligado | ação=manter resfriando      | espera= 8 | custo=3.90
t=17 | Temperatura: 24.60°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 7 | custo=3.60
t=18 | Temperatura: 24.30°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 6 | custo=3.30
t=19 | Temperatura: 24.00°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 5 | custo=3.00
t=20 | Temperatura: 23.70°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 4 | custo=2.70
t=21 | Temperatura: 23.40°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 3 | custo=2.40
t=22 | Temperatura: 23.10°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 2 | custo=2.10
t=23 | Temperatura: 22.80°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 1 | custo=2.20
t=24 | Temperatura: 22.50°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 0 | custo=2.50
t=25 | Temperatura: 22.87°C, Ar Condicionado: Desligado | ação=desligado              | espera= 0 | custo=0.13
t=26 | Temperatura: 23.23°C, Ar Condicionado: Desligado | ação=manter (deadband)      | espera= 0 | custo=0.23
t=27 | Temperatura: 23.57°C, Ar Condicionado: Desligado | ação=manter (deadband)      | espera= 0 | custo=0.57
t=28 | Temperatura: 23.89°C, Ar Condicionado: Desligado | ação=manter                 | espera= 0 | custo=0.89
t=29 | Temperatura: 23.59°C, Ar Condicionado: Ligado | ação=ligar e resfriar       | espera= 3 | custo=2.59

Estado final        : Temperatura: 23.59°C, Ar Condicionado: Ligado
Leituras armazenadas: 14
taxa_r aprendidas   : [0.3, 0.3, 0.3, 0.3, 0.3]
taxa_e aprendidas   : [0.375, 0.356, 0.338, 0.322]
```
## Cenário 5 - Ambiente Moderado

- Sequência: simulação dinâmica com temperatura inicial de 25.0°C
- Temperatura desejada: 24.0°C

```text
t=00 | Temperatura: 25.25°C, Ar Condicionado: Desligado | ação=manter (min OFF)       | espera= 0 | custo=1.25
t=01 | Temperatura: 25.49°C, Ar Condicionado: Desligado | ação=manter (min OFF)       | espera= 0 | custo=1.49
t=02 | Temperatura: 25.71°C, Ar Condicionado: Desligado | ação=manter (min OFF)       | espera= 0 | custo=1.71
t=03 | Temperatura: 25.41°C, Ar Condicionado: Ligado | ação=ligar e resfriar       | espera= 1 | custo=3.41
t=04 | Temperatura: 25.11°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 0 | custo=3.11
t=05 | Temperatura: 24.81°C, Ar Condicionado: Ligado | ação=manter resfriando      | espera= 4 | custo=2.81
t=06 | Temperatura: 24.51°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 3 | custo=2.51
t=07 | Temperatura: 24.21°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 2 | custo=2.21
t=08 | Temperatura: 23.91°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 1 | custo=2.09
t=09 | Temperatura: 23.61°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 0 | custo=2.39
t=10 | Temperatura: 23.93°C, Ar Condicionado: Desligado | ação=desligado              | espera= 0 | custo=0.07
t=11 | Temperatura: 24.24°C, Ar Condicionado: Desligado | ação=manter (deadband)      | espera= 0 | custo=0.24
t=12 | Temperatura: 24.52°C, Ar Condicionado: Desligado | ação=manter (deadband)      | espera= 0 | custo=0.52
t=13 | Temperatura: 24.80°C, Ar Condicionado: Desligado | ação=manter                 | espera= 0 | custo=0.80
t=14 | Temperatura: 24.50°C, Ar Condicionado: Ligado | ação=ligar e resfriar       | espera= 3 | custo=2.50
t=15 | Temperatura: 24.20°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 2 | custo=2.20
t=16 | Temperatura: 23.90°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 1 | custo=2.10
t=17 | Temperatura: 23.60°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 0 | custo=2.40
t=18 | Temperatura: 23.92°C, Ar Condicionado: Desligado | ação=desligado              | espera= 0 | custo=0.08
t=19 | Temperatura: 24.22°C, Ar Condicionado: Desligado | ação=manter (deadband)      | espera= 0 | custo=0.22
t=20 | Temperatura: 24.51°C, Ar Condicionado: Desligado | ação=manter (deadband)      | espera= 0 | custo=0.51
t=21 | Temperatura: 24.79°C, Ar Condicionado: Desligado | ação=manter                 | espera= 0 | custo=0.79
t=22 | Temperatura: 24.49°C, Ar Condicionado: Ligado | ação=ligar e resfriar       | espera= 3 | custo=2.49
t=23 | Temperatura: 24.19°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 2 | custo=2.19
t=24 | Temperatura: 23.89°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 1 | custo=2.11
t=25 | Temperatura: 23.59°C, Ar Condicionado: Ligado | ação=manter (em espera)     | espera= 0 | custo=2.41
t=26 | Temperatura: 23.91°C, Ar Condicionado: Desligado | ação=desligado              | espera= 0 | custo=0.09
t=27 | Temperatura: 24.21°C, Ar Condicionado: Desligado | ação=manter (deadband)      | espera= 0 | custo=0.21
t=28 | Temperatura: 24.50°C, Ar Condicionado: Desligado | ação=manter (deadband)      | espera= 0 | custo=0.50
t=29 | Temperatura: 24.78°C, Ar Condicionado: Desligado | ação=manter                 | espera= 0 | custo=0.78

Estado final        : Temperatura: 24.78°C, Ar Condicionado: Desligado
Leituras armazenadas: 19
taxa_r aprendidas   : [0.3, 0.3, 0.3, 0.3]
taxa_e aprendidas   : [0.289, 0.274, 0.321, 0.305, 0.289]
```