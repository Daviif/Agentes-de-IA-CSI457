# Nota do diretor financeiro

**Todos os valores estão em reais (R$); a ferramenta imprime "$" no corpo do relatório abaixo, que foi convertido para R$.** Cada "arena-dia" é R$ 99 ÷ 30 = R$ 3,30; o volume por dia é o número de arenas pagantes.
**Atenção: todos os custos e a rampa são estimativas minhas, sem cotação real** (ver `cfo-sources.md`). Os números valem o que valem esses dados.

- **A margem:** cada arena deixa **R$ 90 por mês** depois dos custos variáveis (91% do preço). Com 60 arenas pagantes, a margem de lucro é **13%**.
- **A linha a vigiar:** o número de arenas pagantes. O equilíbrio é de **52 arenas**; o plano só chega a 60 no mês 12. Com 20% menos arenas, o ano 1 perde R$ 27.768; com a metade, perde R$ 38.055.
- **Caixa:** o negócio precisa de cerca de **R$ 31.600** antes de se pagar (R$ 9.000 de partida + prejuízo operacional até o mês 9). O resultado operacional do ano 1 é **negativo (−R$ 20.910)** e a partida não se paga em 12 meses. Isto não considera o tempo do fundador.
- **Três jeitos de melhorar a margem** (rodados na ferramenta):
  1. **Preço médio R$ 119 em vez de R$ 99:** margem 28%, equilíbrio em 42 arenas, ano 1 de −R$ 13.252. (Ver o plano de R$ 149 para 4+ quadras em `pricing.md`; o painel v2 mostra R$ 149 como "começando a ficar caro" na mediana.)
  2. **Preço médio R$ 129:** margem 34%, equilíbrio em 39 arenas, ano 1 de −R$ 9.480. Fica acima do ponto de indiferença do painel (R$ 99); testar antes de assumir.
  3. **Cortar anúncios de R$ 1.500 para zero nos primeiros meses e vender por WhatsApp direto** (conta manual, não da ferramenta): reduz o fixo para R$ 3.100/mês e o equilíbrio cai de 52 para cerca de 35 arenas.
- **Condições financeiras do conselho:** o conselho pediu custo de aquisição medido e arenas pagantes reais. Nenhuma das duas foi atendida ainda; a rampa acima é suposição.
- Receita antes de impostos. Um contador deve conferir a estrutura da empresa, tributação do serviço e nota fiscal antes de qualquer dinheiro mover. Isto não é aconselhamento financeiro, jurídico ou tributário.

---

# Unit economics: Reserva de Quadras (assinatura por arena). Unidade = 1 arena-dia, ou seja, RR$ 99 / 30 dias; 'plan_per_day' = número de arenas pagantes

Every number below comes from the input file. Nothing is looked up or guessed.

## One arena-dia

| line | per arena-dia |
| --- | ---: |
| Price | R$3.30 |
| Hospedagem, banco de dados e e-mails por arena (ESTIMATIVA) | -R$0.12 |
| Mensagens/WhatsApp por arena (ESTIMATIVA) | -R$0.15 |
| Reserva para estorno/inadimplência do Pix (ESTIMATIVA) | -R$0.03 |
| **Contribution** (what each arena-dia leaves to pay the fixed costs) | **R$3.00** (91%) |

## The margin that matters

Fixed costs: R$4,600 a month (Atendente de suporte meio período, noite e fim de semana (ESTIMATIVA) R$2,500, Ferramentas: domínio, e-mail, monitoramento, contabilidade (ESTIMATIVA) R$600, Anúncios e materiais de venda (ESTIMATIVA) R$1,500).

- **Break-even: 52 arena-dias a day.** Below that you lose money every month.
- **Profit margin at your plan** (60 a day): **13%** of every sale, after every cost.

## Year 1, month by month

| month | arena-dias a day | revenue | profit | cumulative (after R$9,000 startup) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 3 | R$297 | -R$4,330 | -R$13,330 |
| 2 | 6 | R$594 | -R$4,060 | -R$17,390 |
| 3 | 10 | R$990 | -R$3,700 | -R$21,090 |
| 4 | 15 | R$1,485 | -R$3,250 | -R$24,340 |
| 5 | 21 | R$2,079 | -R$2,710 | -R$27,050 |
| 6 | 28 | R$2,772 | -R$2,080 | -R$29,130 |
| 7 | 35 | R$3,465 | -R$1,450 | -R$30,580 |
| 8 | 42 | R$4,158 | -R$820 | -R$31,400 |
| 9 | 49 | R$4,851 | -R$190 | -R$31,590 |
| 10 | 54 | R$5,346 | R$260 | -R$31,330 |
| 11 | 58 | R$5,742 | R$620 | -R$30,710 |
| 12 | 60 | R$5,940 | R$800 | -R$29,910 |

- **Year 1 operating profit: -R$20,910** on R$37,719 of revenue.
- After the R$9,000 startup spend: -R$29,910.
- Startup money earned back: not within year 1.
- Cash you need before it pays for itself: **R$31,590**.

## What if

| scenario | margin at plan | break-even a day | year 1 profit |
| --- | ---: | ---: | ---: |
| Base plan | 13% | 52 | -R$20,910 |
| Price -10% | 4% | 58 | -R$24,682 |
| Volume -20% | -6% | 52 | -R$27,768 |
| Unit costs +15% | 12% | 52 | -R$21,424 |

## Red flags

- Year 1 loses money on operations (-R$20,910).
- The startup spend is not earned back within year 1.
