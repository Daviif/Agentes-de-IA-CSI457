# Nota do diretor financeiro (v2: dois canais)

**Valores em reais (R$); a ferramenta imprime "$" no relatório abaixo, convertido para R$.** Este relatório usa o **cenário base** de `modelo_viabilidade.py`: dois canais (A ticket alto, B ticket baixo), 40% da audiência no A, comissão média ponderada de R$ 6,57 por compra e 15% de reserva para cancelamento. O estudo completo, com 24 meses e três cenários, está no documento "Estudo de viabilidade". A versão de um canal só está em `cfo-v1.md`.
**Todos os números são estimativas minhas, sem dado real.** O tempo do fundador (15 h por semana, R$ 3.250 por mês) não está incluído.

- **A margem:** cada compra por link deixa **R$ 5,58** (85%) depois da reserva. A margem de lucro do mês 12 é de 11%.
- **A linha a vigiar:** inscritos e receita por inscrito. O equilíbrio exige cerca de **4.600 inscritos** (a ferramenta arredonda para 3 compras por dia). Dobrar o crescimento de inscritos leva o caixa do mês 24 de R$ 3.740 para R$ 18.360; cortá-lo pela metade o leva a −R$ 3.570.
- **A mistura de canais mexe pouco:** passar de 20% para 60% da audiência no canal A muda o caixa do mês 24 em R$ 1.891.
- **Caixa:** o ponto mais fundo é **−R$ 3.687 (mês 11)**; o caixa volta a zero no mês 20 e o lucro mensal começa no mês 12. O ano 1 fecha em −R$ 2.822 de resultado operacional.
- **Não gastar com anúncios no início:** a R$ 2,50 por inscrito, o caixa do mês 24 cai para −R$ 3.899.
- **Condições financeiras do conselho:** confirmar comissões e cancelamento por escrito, e medir distribuição barata: **ainda não atendidas.**
- Receita antes de impostos. Um contador deve conferir o enquadramento (o teto anual do MEI pode ser excedido no cenário otimista). Isto não é aconselhamento financeiro, jurídico ou tributário.

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

Fixed costs: R$420 a month (VPS e banco de dados (ESTIMATIVA) R$100, Dados de histórico de preço (ESTIMATIVA) R$100, Ferramentas de arte e agendamento (ESTIMATIVA) R$100, Domínio e encurtador (ESTIMATIVA) R$30, Contador / DAS de MEI (ESTIMATIVA) R$90).

- **Break-even: 3 compra por links a day.** Below that you lose money every month.
- **Profit margin at your plan** (3 a day): **11%** of every sale, after every cost.

## Year 1, month by month

| month | compra por links a day | revenue | profit | cumulative (after R$800 startup) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | R$16 | -R$407 | -R$1,207 |
| 2 | 0 | R$35 | -R$390 | -R$1,596 |
| 3 | 0 | R$57 | -R$371 | -R$1,968 |
| 4 | 0 | R$83 | -R$350 | -R$2,318 |
| 5 | 1 | R$112 | -R$325 | -R$2,642 |
| 6 | 1 | R$150 | -R$293 | -R$2,935 |
| 7 | 1 | R$193 | -R$256 | -R$3,191 |
| 8 | 1 | R$244 | -R$212 | -R$3,403 |
| 9 | 2 | R$306 | -R$161 | -R$3,564 |
| 10 | 2 | R$378 | -R$99 | -R$3,662 |
| 11 | 2 | R$465 | -R$25 | -R$3,687 |
| 12 | 3 | R$572 | R$65 | -R$3,622 |

- **Year 1 operating profit: -R$2,822** on R$2,612 of revenue.
- After the R$800 startup spend: -R$3,622.
- Startup money earned back: not within year 1.
- Cash you need before it pays for itself: **R$3,687**.

## What if

| scenario | margin at plan | break-even a day | year 1 profit |
| --- | ---: | ---: | ---: |
| Base plan | 11% | 3 | -R$2,822 |
| Price -10% | 2% | 3 | -R$3,083 |
| Volume -20% | -7% | 3 | -R$3,266 |
| Unit costs +15% | 9% | 3 | -R$2,881 |

## Red flags

- Year 1 loses money on operations (-R$2,822).
- The startup spend is not earned back within year 1.
