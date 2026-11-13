# Nota do diretor financeiro

**Valores em reais (R$); a ferramenta imprime "$" no relatório abaixo, convertido para R$.** Cada "compra por link" vale a comissão média estimada de R$ 7,20 (pedido de R$ 180 × 4%).
**Todos os números são estimativas minhas** (ver `cfo-sources.md`). A taxa de compra por inscrito (0,03 por mês) não veio do painel simulado, e sim de dois relatos anedóticos de fontes com interesse comercial. **O tempo do fundador não está incluído.**

- **A margem:** cada compra deixa **R$ 6,34** depois da reserva para cancelamento (88%). Com 9 compras por dia (cerca de 9.000 inscritos, no mês 12), a margem é de **48%**.
- **A linha a vigiar:** compras por inscrito por mês. O equilíbrio exige cerca de **4 compras por dia** (a ferramenta arredonda para 5), o que, a 0,03 por inscrito, são cerca de **4.100 inscritos**. Com um terço do volume, o ano 1 perde **R$ 6.586**; com o dobro, ganha **R$ 7.454**.
- **Caixa:** pouco, **R$ 3.830** (R$ 500 de partida mais o prejuízo até o mês 7). O ano 1 fecha em **−R$ 953** de resultado operacional e **−R$ 1.453** depois da partida; o negócio só se paga no ano 2 com essas hipóteses. O risco real é o **tempo**: o dinheiro em jogo é pequeno, mas as horas de desenvolvimento e de curadoria não são pagas.
- **Três jeitos de melhorar a margem:**
  1. **Vender onde a comissão é maior:** com comissão média de 6% (R$ 10,80 por compra) em vez de 4%, o ano 1 passa a **+R$ 3.820** e o equilíbrio cai para 3 compras por dia. Depende da categoria e do programa; confirmar nos painéis.
  2. **Subir a taxa de compra por inscrito** com menos posts e melhores (a hipótese do conselho e do painel), em vez de comprar audiência: dobrar a taxa leva o ano 1 a **+R$ 7.454**.
  3. **Cortar os R$ 500/mês de anúncios no início** (conta manual, não da ferramenta): o fixo cai de R$ 780 para R$ 280 e o equilíbrio para cerca de 1,5 compra por dia, mas a audiência cresceria só de forma orgânica, mais devagar.
- **Atenção ao custo de aquisição:** uma pessoa inscrita rende em média **R$ 0,19 por mês** (0,03 × R$ 6,34). Pagar R$ 1 a R$ 3 por inscrito em anúncio leva muitos meses para se pagar, e a pessoa pode sair antes. Anúncios de crescimento devem ser testados com cautela.
- **Condições financeiras do conselho:** (1) confirmar por escrito comissões e regras de cancelamento de cada loja: **não atendida**; (2) distribuição barata com custo por inscrito medido: **não atendida**.
- Receita antes de impostos. Um contador deve conferir o enquadramento (MEI tem teto anual de faturamento) e a tributação das comissões. Isto não é aconselhamento financeiro, jurídico ou tributário.

---

# Unit economics: Canal de promoções no Telegram com links de afiliado. Unidade = 1 compra feita por link do canal; 'price' = comissão média por compra (estimativa)

Every number below comes from the input file. Nothing is looked up or guessed.

## One compra por link

| line | per compra por link |
| --- | ---: |
| Price | R$7.20 |
| Reserva para cancelamento e devolução que anulam a comissão: 12% da comissão (ESTIMATIVA) | -R$0.86 |
| **Contribution** (what each compra por link leaves to pay the fixed costs) | **R$6.34** (88%) |

## The margin that matters

Fixed costs: R$780 a month (Servidor e banco de dados (ESTIMATIVA) R$80, Domínio, encurtador e extras (ESTIMATIVA) R$20, Dados de histórico de preço, API ou assinatura (ESTIMATIVA) R$100, Anúncios e parcerias para crescer a audiência (ESTIMATIVA) R$500, Contador / DAS de MEI ou equivalente (ESTIMATIVA) R$80).

- **Break-even: 5 compra por links a day.** Below that you lose money every month.
- **Profit margin at your plan** (9 a day): **48%** of every sale, after every cost.

## Year 1, month by month

| month | compra por links a day | revenue | profit | cumulative (after R$500 startup) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | R$43 | -R$742 | -R$1,242 |
| 2 | 0 | R$108 | -R$685 | -R$1,927 |
| 3 | 1 | R$194 | -R$609 | -R$2,536 |
| 4 | 1 | R$302 | -R$514 | -R$3,049 |
| 5 | 2 | R$432 | -R$400 | -R$3,449 |
| 6 | 3 | R$583 | -R$266 | -R$3,715 |
| 7 | 4 | R$756 | -R$114 | -R$3,830 |
| 8 | 4 | R$950 | R$57 | -R$3,773 |
| 9 | 5 | R$1,166 | R$247 | -R$3,526 |
| 10 | 6 | R$1,404 | R$456 | -R$3,070 |
| 11 | 8 | R$1,663 | R$685 | -R$2,385 |
| 12 | 9 | R$1,944 | R$932 | -R$1,453 |

- **Year 1 operating profit: -R$953** on R$9,547 of revenue.
- After the R$500 startup spend: -R$1,453.
- Startup money earned back: not within year 1.
- Cash you need before it pays for itself: **R$3,830**.

## What if

| scenario | margin at plan | break-even a day | year 1 profit |
| --- | ---: | ---: | ---: |
| Base plan | 48% | 5 | -R$953 |
| Price -10% | 42% | 5 | -R$1,908 |
| Volume -20% | 38% | 5 | -R$2,635 |
| Unit costs +15% | 46% | 5 | -R$1,124 |

## Red flags

- Year 1 loses money on operations (-R$953).
- The startup spend is not earned back within year 1.
