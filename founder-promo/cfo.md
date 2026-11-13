# Nota do diretor financeiro (v3: custos revisados pelo fundador)

**Valores em reais (R$); a ferramenta imprime "$" no relatório abaixo, convertido para R$.** Cenário base de `modelo_viabilidade.py` com dois canais. Custos revisados em 13/11/2026: CNPJ/MEI gratuito, identidade visual feita com Claude, VPS e banco no Oracle Free Tier ou em máquina própria, ferramentas open source (todos a R$ 0). Restam dados de histórico de preço (R$ 100, estimativa), DAS do MEI (R$ 90, estimativa) e domínio (R$ 7, R$ 80 por ano). **O tempo do fundador não é contado, por decisão dele.** O estudo completo está no documento "Estudo de viabilidade"; as versões anteriores, em `cfo-v1.md` (um canal).
**Todos os números são estimativas minhas, sem dado real.**

- **Custo:** R$ 0 de partida e **R$ 197 por mês**.
- **A margem:** cada compra por link deixa R$ 5,58 (85%); margem de 50% no mês 12.
- **A linha a vigiar:** inscritos e receita por inscrito; o equilíbrio exige cerca de 2.200 inscritos.
- **Caixa:** o ponto mais fundo é **−R$ 831 (mês 7)**; o lucro mensal começa no mês 8 e o caixa volta a zero no mês 13. O ano 1 fecha em −R$ 146 de resultado operacional (por isso o veredito calculado ainda é "Ainda não", por pouco).
- **Dados de preço:** se o histórico for construído com as APIs das lojas, o custo fixo cai a R$ 97 e o caixa do mês 24 sobe de R$ 9.892 para R$ 12.292.
- **Oracle Free Tier:** contas e instâncias gratuitas podem ser suspensas; manter backup e uma máquina própria como plano B.
- Receita antes de impostos; um contador deve conferir o enquadramento (o teto anual do MEI pode ser excedido no cenário otimista). Não é aconselhamento financeiro, jurídico ou tributário.

---

# Unit economics: Dois canais de promoções no Telegram (A ticket alto, B ticket baixo) com links de afiliado. Unidade = 1 compra por link; 'price' = comissão média ponderada por compra (ESTIMATIVA, cenário base)

Every number below comes from the input file. Nothing is looked up or guessed.

## One compra por link

| line | per compra por link |
| --- | ---: |
| Price | R$6.57 |
| Reserva para cancelamento e devolução (ESTIMATIVA, média ponderada) | -R$0.99 |
| **Contribution** (what each compra por link leaves to pay the fixed costs) | **R$5.58** (85%) |

## The margin that matters

Fixed costs: R$197 a month (Dados de histórico de preço (ESTIMATIVA) R$100, Domínio (RR$ 80 por ano, diluído) (ESTIMATIVA) R$7, DAS do MEI (ESTIMATIVA) R$90).

- **Break-even: 2 compra por links a day.** Below that you lose money every month.
- **Profit margin at your plan** (3 a day): **50%** of every sale, after every cost.

## Year 1, month by month

| month | compra por links a day | revenue | profit | cumulative (after R$0 startup) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | R$16 | -R$184 | -R$184 |
| 2 | 0 | R$35 | -R$167 | -R$350 |
| 3 | 0 | R$57 | -R$148 | -R$499 |
| 4 | 0 | R$83 | -R$127 | -R$626 |
| 5 | 1 | R$112 | -R$102 | -R$727 |
| 6 | 1 | R$150 | -R$70 | -R$797 |
| 7 | 1 | R$193 | -R$33 | -R$830 |
| 8 | 1 | R$244 | R$11 | -R$819 |
| 9 | 2 | R$306 | R$62 | -R$757 |
| 10 | 2 | R$378 | R$124 | -R$632 |
| 11 | 2 | R$465 | R$198 | -R$434 |
| 12 | 3 | R$572 | R$288 | -R$146 |

- **Year 1 operating profit: -R$146** on R$2,612 of revenue.
- After the R$0 startup spend: -R$146.
- Startup money earned back: not within year 1.
- Cash you need before it pays for itself: **R$830**.

## What if

| scenario | margin at plan | break-even a day | year 1 profit |
| --- | ---: | ---: | ---: |
| Base plan | 50% | 2 | -R$146 |
| Price -10% | 45% | 2 | -R$407 |
| Volume -20% | 42% | 2 | -R$590 |
| Unit costs +15% | 48% | 2 | -R$205 |

## Red flags

- Year 1 loses money on operations (-R$146).
- The startup spend is not earned back within year 1.
