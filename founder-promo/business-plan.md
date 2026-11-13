# Canal de promoções com links de afiliado (nome de trabalho; estilo "Rei da Promo") · Business plan

**Verdict: Not yet**

- ✓ Each compra por link earns R$5.58 before fixed costs (85% contribution).
- ✗ Year 1 operating LOSS: R$2,822.
- ✓ 9 of 20 simulated buyers buy (45%, the bar is 25%).

| key number | |
| --- | ---: |
| Price | R$6.57 a compra por link |
| Profit margin at plan | 11% per compra por link |
| Break-even | 3 compra por links a day |
| Year 1 operating profit | R$-2,822 |
| Startup spend | R$800 |
| Cash needed before it pays for itself | R$3,687 |
| Startup money earned back | not in year 1 |
| Buyer panel | 9 buy · 11 pass |

## The idea

- O que é: um canal de promoções no Telegram (base) que posta achados de Mercado Livre, Shopee, Amazon, Magalu e outras lojas, com link de afiliado do dono do canal. Ganha comissão por venda feita pelos links. Pode ter rankings ("top 10 promos mais clicadas da semana"). Parte técnica (coletar ofertas, converter link, formatar, publicar) é automatizável por um desenvolvedor.
- Para quem é: compradores brasileiros de internet que caçam desconto. Nicho inicial a escolher (ex.: tecnologia ou casa).
- O que vende, por quanto: nada diretamente ao público. O canal é grátis; a receita é a comissão paga pela loja (Mercado Livre até 16% em beleza, esportes e moda; demais taxas a confirmar).
- Onde e como: Telegram (canal e grupo, automação total por bot), vitrine no Instagram e X (manual ou agendado), WhatsApp só semi-manual. Um sub ID por canal para saber de onde nasce cada venda.
- Orçamento e restrições: não informados. O fundador é desenvolvedor. Cadastros nas lojas ainda não pedidos (Shopee leva 5 a 15 dias de aprovação manual).

### Plano do documento de origem
- Pipeline de 7 etapas, do coletor de ofertas às métricas de comissão, com uma aprovação humana antes de publicar; stack em Node com banco para histórico de preço.
- Roadmap de 4 fases com 3 portões de decisão: só constrói o bot depois de ver que o canal gera clique e venda; só tira a aprovação manual quando o filtro acertar.
- APIs: Shopee (GraphQL, aprovação manual), Amazon (Creators API; a PA-API 5 foi descontinuada), Mercado Livre e Magalu (gerador de links do painel; API pública não confirmada).
- Riscos listados: promoção falsa, repostar de outros canais trocando o link, conta de afiliado suspensa, automação não oficial no WhatsApp, transparência de afiliado e imposto de renda sobre comissões.

## Summary

**O negócio:** dois canais grátis de ofertas no Telegram (A: ticket alto, como TVs e eletro; B: ticket baixo, como acessórios e casa), rodando em VPS própria, divulgados em várias redes sociais; a receita é a comissão de afiliado das lojas.

**Veredito (calculado):** ver o topo de `business-plan.md`: **"Ainda não"**. O ano 1 tem prejuízo operacional de R$ 2.822.

**Os números (cenário base, estimativas minhas):** custo fixo de R$ 420 por mês e R$ 800 de partida; equilíbrio com cerca de 4.600 inscritos; prejuízo até o mês 11 (caixa mais fundo: −R$ 3.687); lucro mensal a partir do mês 12; caixa de volta a zero no mês 20; R$ 1.024 de lucro por mês no mês 24. No cenário pessimista nunca se paga (−R$ 9.980 no mês 24); no otimista, lucro mensal no mês 4 e caixa de volta a zero no mês 8. **O tempo do fundador (R$ 3.250 por mês) não é coberto em 24 meses no cenário base.**

**O que decide:** o crescimento de inscritos e a conversão em compras, não a mistura entre TVs e cabos. Uma TV vale 13 cabos em comissão, mas quem compra TV pelo link é muito mais raro.

**Conselho e painel:** o conselho deu 3 "investe se" (nota média 3,7). O painel simulado, 9 de 20 entrariam e comprariam por um link (teto); ele não entrou nas contas.

**Como começar:** pedir os cadastros de afiliado hoje, escrever a regra de publicação e fazer um teste manual com dois canais, com três portões de decisão (inscritos e compras, não o caixa) e critério de parar; perda máxima em dinheiro de cerca de R$ 3.300 se parar no portão 3.

**Estudo completo:** documento "Estudo de viabilidade", gerado por `modelo_viabilidade.py`.

**Lembrete:** projeções, não previsões. Não é aconselhamento financeiro, jurídico ou tributário.

## What the board said

**Votação: 3 "investe se", 0 "investe", 0 "passa". Nota média: 3,7/10** (Ofertas 4, Monopólio 3, Produto 4).

### Riscos apontados por mais de um conselheiro
1. **Commodity, sem diferença** (os três): coletar ofertas, converter link e publicar qualquer desenvolvedor faz em dias; existe ao menos um concorrente conhecido (@oreidapromobr) e nenhum segredo declarado.
2. **Confiança e promoção falsa** (Ofertas, Produto): uma enganação percebida custa o canal. "Promoção que vale" ainda não tem regra escrita.
3. **Quem paga controla** (Ofertas, Monopólio): a loja define a comissão, pode anulá-la (cancelamento, devolução) ou suspender a conta. Só a taxa do Mercado Livre é conhecida.
4. **Falta de foco** (Ofertas, Produto): quatro lojas e quatro canais ao mesmo tempo, nicho "a escolher".
5. **Audiência inicial e custo por inscrito desconhecidos** (os três).

### Condições (checklist para as próximas skills)
- [ ] Definir por escrito o que torna o canal diferente (nicho estreito, curadoria, prova de preço) antes de automatizar.
- [ ] Escolher UM nicho e UM canal (Telegram) e cortar o resto até provar clique e venda.
- [ ] Escrever a regra de publicação em critérios checáveis (preço real contra histórico, estoque, avaliação mínima) e manter aprovação humana.
- [ ] Teste manual do primeiro portão com meta de cliques e vendas fixada antes (`/founder-launch`).
- [ ] Confirmar por escrito comissões e regras de cancelamento de cada loja; não depender de uma só (`/founder-cfo`).
- [ ] Provar distribuição barata: meta de inscritos e custo por inscrito.
- [ ] Medir retenção (quem fica após 30 dias) e silenciamentos, além de clique.
- [ ] Linha fixa de transparência sobre afiliado e limite de posts por dia.
- [ ] Nomear o ativo durável (base de preço histórico própria, curadoria verificada, comunidade).

### Onde divergem
O Monopólio é o mais duro (3): não vê efeito de rede nem barreira à cópia no sexto mês. Ofertas e Produto (4) acham que o roadmap em portões limita o prejuízo e que o ranking ("mais clicadas") pode dar identidade.

### A versão mais forte que o conselho enxerga
Não é "um canal de promoções" genérico. É **um canal de um nicho estreito (por exemplo, tecnologia) cuja promessa é preço verificado**: só publica oferta que passa num histórico de preço próprio, avisa quando a oferta cai ou é falsa e declara que ganha comissão. O histórico de preço acumulado é o único ativo que pode virar durável. Sem isso, é commodity.

## The competition

**Como foi feito e o limite disto:** os dados vêm de resultados de busca na web em 13/11/2026; a sessão não conseguiu abrir os sites diretamente, então os números de usuários são os que as reportagens e páginas citaram (alguns antigos ou divergentes entre fontes). **Nenhuma nota de avaliação, contagem atual de membros ou reclamação de clientes foi verificada.** O perfil @oreidapromobr não foi aberto: a descrição vem do documento de origem.

### A tabela
| nome | tipo | o que oferece | tamanho citado |
| --- | --- | --- | --- |
| [Promobit](https://www.promobit.com.br/Index/como-funciona) | direto | comunidade; ofertas cadastradas pelos próprios consumidores | "mais de 3 milhões de usuários cadastrados" |
| [Pelando](https://www.pelando.com.br/) | direto | social commerce; usuários recomendam e avaliam promoções e cupons | "mais de 800.000 membros" (reportagem) |
| [Achados do TB](https://tecnoblog.net/noticias/quer-promocao-100-mil-pessoas-ja-seguem-canal-no-whatsapp/) | direto | curadoria de uma equipe; WhatsApp e Telegram com o mesmo conteúdo | canal do WhatsApp com 100 mil inscritos |
| [Rei da Promo](https://x.com/oreidapromobr) | direto | achados com link encurtado e rankings semanais, no X | não verificado |
| [Zoom/Buscapé](https://www.shopify.com/br/blog/sites-para-comparar-preco) | indireto | comparação de preço, alertas, histórico de preço, cashback | não verificado |
| [Cuponomia](https://olhardigital.com.br/2022/01/28/dicas-e-tutoriais/quer-economizar-conheca-6-sites-de-cupons-de-descontos/) | indireto | cupons | fontes divergem |
| Grupos e canais pequenos de ofertas | direto | repostagem de ofertas com link de afiliado | milhares, não listados |
| Comprar direto, sem caçar | substituto | histórico de preço do navegador, esperar a Black Friday | |

### Preço para o público
Todos custam **R$ 0** ao usuário. Não há faixa de preço a comparar: a disputa é por **atenção e confiança**, e a receita de todos vem de comissão de loja (ou, no caso de Promobit e Pelando, de operação própria que esta pesquisa não verificou).

### Comissão de afiliado (o que paga a conta)
Sem tabela oficial verificada; as fontes divergem e **algumas confundem taxa de vendedor com comissão de afiliado**:
- Amazon Associados Brasil: faixas citadas de 1% a 10%, 7% a 15% ou 1% a 20%, conforme o site; varia por categoria ([fontes](https://www.cupomonline.com.br/afiliado-amazon-vale-a-pena/)).
- Shopee: "normalmente entre 3% e 15%" segundo um artigo; o Tecnoblog noticiou o lançamento do programa com comissões "de até 14%" ([Tecnoblog](https://tecnoblog.net/comunidade/t/exclusivo-shopee-lanca-programa-de-afiliados-no-brasil-com-comissoes-de-ate-14/44227?tl=fr)).
- Mercado Livre: "até 16% em beleza, esportes e moda" (documento de origem); API pública não confirmada.
- Magalu: não encontrei taxa de afiliado confiável.
**Para as contas usei uma média de 4% como estimativa conservadora, a trocar pelo painel real de cada programa.**

### Mapa de posicionamento
Eixos: tamanho da comunidade e confiança no preço.
```
confia no preço   |  Zoom/Buscapé (histórico)        Achados do TB (curadoria)
                  |
                  |                                   Promobit / Pelando (voto da comunidade)
sem verificação   |  grupos pequenos de repostagem    <<< este canal hoje >>>
                  +---------------------------------------------------------
                     pequeno                                   enorme
```
Começar do zero em "sem verificação e pequeno" é o pior canto: qualquer um dos acima já faz mais e é maior.

### Reclamações
Não levantadas (sem acesso a avaliações). O documento de origem e a pesquisa de mercado citam promoção falsa e desconto inflado como a queixa recorrente; confirmar lendo avaliações dos aplicativos e fóruns antes de afirmar.

### A lacuna
Com a evidência disponível, **não há lacuna de formato**: ofertas por Telegram/WhatsApp já existem em escala (Achados do TB) e a verificação de preço já é feita por comparadores (Zoom/Buscapé) e por comunidades (Promobit, Pelando). O que pode ser uma lacuna, **a testar**:
1. **Um nicho estreito com curadoria honesta** (ex.: tecnologia ou casa), em vez de "tudo".
2. **Histórico de preço próprio e visível em cada post**, que diga "esse já foi mais barato" quando for o caso.
3. **Transparência de afiliado como marca**, num mercado em que confiança é o problema.
Nada disso é um segredo técnico; todos copiáveis.

### A ameaça
Qualquer grande (Achados do TB, Promobit, Pelando) pode abrir um canal de nicho no Telegram em dias, com audiência de partida. E a loja pode suspender a conta de afiliado.

Fontes: [Promobit](https://www.promobit.com.br/Index/como-funciona) · [Tecnoblog: 100 mil no canal](https://tecnoblog.net/noticias/quer-promocao-100-mil-pessoas-ja-seguem-canal-no-whatsapp/) · [Tecnoblog: 1 ano do Achados do TB](https://tecnoblog.net/noticias/achados-do-tb-completa-1-ano-trazendo-ofertas-no-whatsapp-e-telegram/) · [Shopee afiliados (Tecnoblog)](https://tecnoblog.net/comunidade/t/exclusivo-shopee-lanca-programa-de-afiliados-no-brasil-com-comissoes-de-ate-14/44227?tl=fr) · [Amazon Associados](https://www.cupomonline.com.br/afiliado-amazon-vale-a-pena/) · [Sebrae: sites de cupons](https://sebraepr.com.br/comunidade/artigo/sites-para-encontrar-cupons-de-desconto-na-web)

## The buyer panel

**9 buy · 11 pass** (45% buy) out of 20 simulated buyers. Seed 303359, so the same cards can be dealt again.

These are simulated buyers, not customers. Use this to find objections and weak spots, then confirm the big ones with real people before you spend.

### By segment

| group | buyers | buy rate |
| --- | ---: | ---: |
| Adulto, 41 a 55, renda média alta, compra para casa e trabalho | 5 | 60%  (thin) |
| Adulto, 26 a 40, renda média, família ou casa nova | 8 | 50% |
| Jovem, 18 a 25, estudante ou primeiro emprego | 7 | 29%  (thin) |

### By buying behaviour

| group | buyers | buy rate |
| --- | ---: | ---: |
| Compra por impulso | 3 | 100%  (thin) |
| Odeia notificação | 1 | 100%  (thin) |
| Só na Black Friday | 4 | 50%  (thin) |
| Vive no WhatsApp | 3 | 33%  (thin) |
| Confere o histórico de preço | 3 | 33%  (thin) |
| Caçador de promoção assíduo | 4 | 25%  (thin) |
| Cético com afiliado | 2 | 0%  (thin) |

### By income

| group | buyers | buy rate |
| --- | ---: | ---: |
| R$93,000 and up | 7 | 57%  (thin) |
| R$37,000 to R$93,000 | 7 | 57%  (thin) |
| under R$37,000 | 6 | 17%  (thin) |

### Why they pass

| reason | buyers | in their words |
| --- | ---: | --- |
| habit | 7 | "Eu vivo no WhatsApp e quase não abro o Telegram, então não ia ver os posts. Já me arrependi de compra que parecia promoção e prefiro conferir o histórico de preço eu mesma." (P003) · "Eu só compro de verdade na Black Friday e já estou em uns grupos de promoção, então outro canal só ia me dar mais notificação. Entrar de graça eu até entro, mas comprar por ele num mês normal, não." (P006) |
| trust | 3 | "Entrar eu até entro, não custa nada, mas comprar por link de canal não. Eu só compro na Black Friday e já confiro no Zoom ou no Buscapé, então não preciso de outro intermediário." (P004) · "Entrar não custa nada, até posso entrar pra olhar, mas eu sempre confiro o preço no Zoom e no Buscapé antes de comprar e não compro pelo link de um canal que ganha comissão. Já vi muita 'promoção' que era desconto inflado." (P016) |
| need | 1 | "Entrar eu entraria, é grátis e mostrar o menor preço dos últimos meses é o que eu mesma confiro. Mas não compro tecnologia ou casa com frequência, então num mês normal provavelmente não aparece nada que eu precise." (P007) |

### Why they buy

| reason | buyers | in their words |
| --- | ---: | --- |
| trust | 7 | "Entrar não custa nada e o limite de 8 posts com o menor preço dos últimos meses me atrai mais do que os grupos de WhatsApp que silenciei. Se aparecer algo que eu já queria com preço realmente baixo, compro na hora, mas uma vez no mês, não mais." (P001) · "Entrar é grátis e mostrar o menor preço dos últimos meses ajuda a saber se a promoção é real, porque já me arrependi de compra que parecia promoção. Se aparecer algo que eu já queria, compro uma vez pelo link." (P002) |
| price | 2 | "Entrar é grátis e já abro o Pelando quando quero comprar algo grande, então um canal que mostra o menor preço dos últimos meses no post me poupa pesquisa. Compro por impulso, então se vejo um bom desconto com histórico ao lado, clico e compro." (P017) · "Entrar é de graça e mostrar o menor preço dos últimos meses me ajuda, porque eu compro por impulso e só depois pesquiso. Se aparecer algo que eu já queria para a casa nova com desconto de verdade, eu pego." (P019) |

### What would flip a no

- Ter o canal no WhatsApp e o post trazer o link do histórico de preço de uma fonte independente, para eu conferir em um clique.
- Ver o canal acertar na Black Friday, com preço igual ou menor que no Zoom e no Buscapé, em uma compra que eu já queria fazer.
- Ver o canal acertando em alguns posts de produtos que eu já queria comprar, com o histórico de preço conferindo no site, antes da Black Friday.
- Poder pedir aviso só dos produtos que estou de olho, com alerta quando chegarem ao menor preço do histórico.
- Provar que posta ofertas antes do Pelando e do Promobit e que o histórico de preço mostrado é correto, com alguns posts que eu confira e que realmente fossem o menor preço.
- Ver o canal postando ofertas que eu não vi em nenhum outro grupo, ou com antecedência clara, e provar que o menor preço mostrado bate com o Zoom.
- Ver nos primeiros posts que o preço mostrado bate com o histórico que eu mesmo confiro, e que o canal tem poucos posts de verdade, só os que valem a pena.
- Ter o mesmo canal no WhatsApp, com o link do histórico de preço de terceiros no post para eu conferir.
- Se o canal mostrasse ofertas que eu não vejo nos outros grupos, com o histórico de preço de verdade, e eu visse isso por algumas semanas, eu poderia comprar por um link dele.
- Ver que o menor preço mostrado no post bate com o histórico no Zoom/Buscapé em várias ofertas seguidas, de forma que eu consiga conferir sozinha.
- Ver o canal acertando preço em produtos que eu mesmo conferi por um tempo, com um histórico de preço que eu possa checar fora do post, e saber quem está por trás.

Buyers say they would buy **1.1 times** in the first month on average.

20 buyers gave all four price answers. Run founder-pricing's van_westendorp.py on the answers folder.

## Pricing

**O público não paga nada: entrar no canal é grátis, e a receita é a comissão da loja.** Por isso o painel de preço do pacote (Van Westendorp) **não se aplica**: os compradores simulados responderam as quatro perguntas de preço com valores de produtos (de R$ 0 a R$ 2.500), não com o preço do canal. Não calculei a faixa aceitável, e qualquer número dali seria ruído.

### O "preço" que existe: a comissão
- Receita por compra: **R$ 7,20 (hipótese: pedido de R$ 180 × 4%).** Não é decisão do canal: é a tabela de cada programa. Ver `cfo.md` e `competitors.md`.
- A alavanca é **qual categoria e qual loja** o canal promove, não o preço do canal: com 6% o ano 1 sai de −R$ 953 para +R$ 3.820 (ferramenta do CFO).

### Os concorrentes
Todos gratuitos para o usuário (`competitors.md`). Cobrar do público no início seria vender contra Promobit, Pelando, Achados do TB e Zoom/Buscapé, todos de graça.

### Degraus (hipóteses, nada a cobrar agora)
1. **Canal grátis** (o produto).
2. **Alertas personalizados** por produto ou categoria (o painel pediu: "aviso só dos produtos que estou de olho"): começar grátis como arma de retenção.
3. Só depois de ter audiência e de medir retenção: avaliar patrocínio pago de mensagens (o Telegram tem), com regras claras de divulgação. Valor e viabilidade não foram pesquisados.

### O que testar com gente real
- **Duas fontes de tráfego com sub ID diferente** (Instagram/X vs. indicações) para ver qual gera inscrito que clica e compra.
- Uma enquete no canal: "você pagaria R$ 5/mês por alertas só dos produtos que você escolher?" Só como sinal; não é preço.

### Regras
- Nunca anunciar "de R$ X por R$ Y" onde o preço antigo não foi praticado de verdade (é exatamente a queixa do público).
- Preço de produto citado no post sempre com o menor preço dos últimos meses ao lado.

## The offer

### 1. Problemas de quem entra (do painel e do conselho)
Antes: "já estou em grupos"; "quase não uso Telegram"; "vai encher de notificação"; "promoção de canal é desconto inflado"; "prefiro ver o histórico eu mesmo"; "não conheço quem está por trás".
Durante: oferta que acaba quando clica; muitos posts; preço que subiu; link que não leva ao produto.
Depois: arrependimento de compra que "parecia promoção"; sensação de venda disfarçada.

### 2. A pilha
| Item | Objeção que mata | Valor | Custo |
| --- | --- | :-: | :-: |
| **Núcleo:** canal de nicho (tecnologia e casa) que só posta oferta abaixo do histórico, com o **menor preço dos últimos meses no post** (já no pitch) | desconto inflado | 5 | 3 (precisa de histórico) |
| **Link do histórico de uma fonte que o inscrito confere sozinho** (o painel pediu) | "prefiro ver eu mesmo" | 5 | 2 |
| **Máximo de 8 posts por dia, sem repostar** (já no pitch) | notificação | 4 | 1 |
| **Post atualizado quando acaba ou o preço sobe** (já no pitch) | oferta expirada | 4 | 2 |
| **Aviso de afiliado em todo post** (já no pitch) | venda disfarçada | 3 | 1 |
| **Registro público de erros:** quando o preço mostrado não bate, o canal corrige e publica o erro | confiança | 4 | 1 |
| **Alertas só dos produtos que o inscrito escolhe** | "só o que eu quero" | 4 | 3 |
| **Espelho no WhatsApp** (canal; publicação semi-manual) | "vivo no WhatsApp" | 4 | 3 |
| **Quem está por trás:** página com o nome e o que ganha | "não conheço" | 3 | 0 |
| Ranking semanal das 10 mais clicadas (já no pitch) | identidade | 2 | 1 |
**Garantia:** a "garantia" possível é o registro público de erros: se o menor preço mostrado estiver errado, o canal corrige em horas e publica. Custo: tempo do fundador.
**Urgência e escassez:** só as verdadeiras (datas como Black Friday 27/11/2026 e Natal). Nunca "só restam 3".
**O nome:** "Só o preço de verdade" (nome da oferta, não do canal).

### 3. Pontuação (1 a 10, estimativa minha)
| | antes | depois | o que move |
| --- | :-: | :-: | --- |
| Resultado sonhado (comprar mais barato, sem arrependimento) | 5 | 7 | histórico no post + registro de erros |
| Probabilidade percebida | 3 | 6 | fonte externa de histórico, quem está por trás |
| Tempo até o resultado | 7 | 8 | alertas dos produtos do inscrito |
| Esforço (nota alta = menos esforço) | 6 | 8 | limite de posts, sem repostar |

### 4. Reteste
**Não rodei o segundo painel.** O pitch testado já tinha o histórico no post, o limite de 8 posts, a atualização e a divulgação de afiliado; os itens novos acima (link de fonte externa, registro de erros, alertas pessoais, espelho no WhatsApp, página "quem somos") são justamente o que o painel pediu para virar o "não". Sugiro reteste com a mesma semente depois de o canal publicar de verdade os primeiros 50 posts, para pontuar o que de fato existir. O painel atual mostrou: 9 de 20 (45%) entrariam e comprariam ao menos uma vez por link; vale lembrar que esse número é teto, e "entrar não custa nada" aparece em quase todas as respostas, de modo que parte dos "sim" é "entro para olhar".

### 5. Pitch v2 (proposta, ainda não testada)
> Canal de ofertas de tecnologia e casa no Telegram (e espelho no WhatsApp), grátis. Só posta oferta abaixo do histórico, com o menor preço dos últimos meses e o link de um histórico externo para você conferir. Máximo de 8 posts por dia. Se a oferta acaba, o post é atualizado; se o preço mostrado estiver errado, a correção é pública. Todo post avisa que o canal ganha comissão, sem custo extra para você. Você pode pedir aviso só dos produtos que está de olho.

**Regras:** nenhuma promessa que o canal não possa cumprir hoje (histórico externo, alertas e WhatsApp ainda não existem). Cumprir as regras de divulgação de publicidade (CONAR) e dos termos de cada programa. Não é aconselhamento jurídico.

## The numbers

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

## Unit economics: Dois canais de promoções no Telegram (A ticket alto, B ticket baixo) com links de afiliado. Unidade = 1 compra por link; 'price' = comissão média ponderada por compra (ESTIMATIVA, cenário base)

Every number below comes from the input file. Nothing is looked up or guessed.

### One compra por link

| line | per compra por link |
| --- | ---: |
| Price | R$6.57 |
| Reserva para cancelamento e devolução (ESTIMATIVA, média ponderada) | -R$0.99 |
| **Contribution** (what each compra por link leaves to pay the fixed costs) | **R$5.58** (85%) |

### The margin that matters

Fixed costs: R$420 a month (VPS e banco de dados (ESTIMATIVA) R$100, Dados de histórico de preço (ESTIMATIVA) R$100, Ferramentas de arte e agendamento (ESTIMATIVA) R$100, Domínio e encurtador (ESTIMATIVA) R$30, Contador / DAS de MEI (ESTIMATIVA) R$90).

- **Break-even: 3 compra por links a day.** Below that you lose money every month.
- **Profit margin at your plan** (3 a day): **11%** of every sale, after every cost.

### Year 1, month by month

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

### What if

| scenario | margin at plan | break-even a day | year 1 profit |
| --- | ---: | ---: | ---: |
| Base plan | 11% | 3 | -R$2,822 |
| Price -10% | 2% | 3 | -R$3,083 |
| Volume -20% | -7% | 3 | -R$3,266 |
| Unit costs +15% | 9% | 3 | -R$2,881 |

### Red flags

- Year 1 loses money on operations (-R$2,822).
- The startup spend is not earned back within year 1.

## Marketing

> **Nota (13/11/2026):** este plano de marketing é da versão de um canal só. Com dois canais, cada canal e cada rede tem o seu sub ID; ver o documento "Estudo de viabilidade".

## Marketing

**Base:** painel simulado (45% entrariam e comprariam ao menos uma vez; teto), `competitors.md` (Promobit, Pelando, Achados do TB e Zoom/Buscapé já ocupam o espaço, todos de graça) e `cfo.md` (cada inscrito rende cerca de R$ 0,19/mês).

### Posicionamento (3 versões)
1. Para **quem compra tecnologia e casa e já se arrependeu de "promoção" que não era**, o *[nome]* é o canal de Telegram que **só posta oferta abaixo do histórico e mostra o menor preço dos últimos meses no post**, ao contrário de grupos que repostam qualquer desconto.
2. Para **quem já está em grupos e silenciou**, é o canal com **no máximo 8 posts por dia**, ao contrário do despejo de links.
3. Para **quem confere o preço no Zoom antes de comprar**, é o canal que **já fez essa conferência e deixa você conferir sozinho**.
**Recomendada: a 1.** Evidência: nas respostas do painel, o histórico de preço no post foi a razão de 7 das 9 respostas "sim" (reason "trust"); a 3 é a que responde ao pedido mais repetido nos "não".

### Primeira audiência
Adultos de 26 a 55 anos (50% e 60% de "sim") e quem compra por impulso. **Os jovens de 18 a 25 e os "caçadores assíduos", que já estão em vários grupos, são os que menos entram (29% e 25%); os céticos com afiliado, 0%.** Amostra pequena em todos os grupos.

### Canais (começar com dois)
| Canal | Por que serve | Custo | Como saber que funcionou |
| --- | --- | --- | --- |
| **Posts curtos no Instagram, X e TikTok "isso não era promoção"** mostrando o histórico de produtos populares | conteúdo que prova o diferencial e atrai quem desconfia | R$ 0 (tempo) | inscritos vindos por sub ID de cada rede |
| **Indicação dentro do próprio canal** (convite no ranking semanal) | o público que confia é o que traz outro | R$ 0 | novos inscritos por convite |
| Parcerias com criadores de tecnologia e casa (divulgação paga, sempre identificada) | audiência já qualificada | a cotar | custo por inscrito |
| Anúncios do Telegram | escala | evitar no início | custo por inscrito (ver abaixo) |
**Não fazer agora:** repostar ofertas de outros canais trocando o link (o conselho e o documento de origem listam como risco), entrar em grupos alheios para jogar links, e comprar seguidores.

### Calendário (abertura pública em 07/12/2026; datas propostas)
| Quando | Canal | O que sai |
| --- | --- | --- |
| 23/11 a 29/11 (−14 a −8) | Telegram (teste fechado) | 15 a 20 posts à mão para amigos; checar histórico e corrigir erros |
| 27/11 | Telegram | **Black Friday:** só se algum cadastro de afiliado estiver aprovado; senão, publicar sem link e só para treinar o formato |
| 30/11 a 06/12 (−7 a −1) | Instagram/X | 3 posts "isso não era promoção" com histórico real |
| **07/12 (0)** | Todas | Abertura pública: link do canal e o que o canal promete |
| 08/12 a 13/12 | Telegram | Primeiros rankings "mais clicadas" e correção pública de erros |
| 14/12 a 20/12 | Instagram/TikTok | "Antes do Natal: o que realmente baixou" com histórico |
| 21/12 a 23/12 (+14 a +16) | Telegram | Balanço: acertos e erros do mês, em público |
**Quando não há nada novo:** mostrar os bastidores de como o filtro descartou ofertas ("hoje rejeitei 12 de 20").

### Dez ganchos (cada um responde a uma objeção do painel)
1. "Esse 'desconto' de 40% era o preço normal há 2 meses. Aqui você vê o histórico." (desconto inflado)
2. "Máximo de 8 posts por dia. Se não valer, eu não posto." (notificação)
3. "Quer conferir sozinho? O link do histórico está no post." (prefiro ver eu mesmo)
4. "Oferta acabou? O post muda para 'expirou'." (oferta expirada)
5. "Eu ganho comissão, e o preço para você é o mesmo. Está escrito em todo post." (afiliado)
6. "Errei o preço ontem. Aqui está a correção." (confiança)
7. "Hoje descartei 12 ofertas e postei 3." (filtro)
8. "Me diga o produto que você quer, eu aviso quando chegar no menor preço." (só o que eu quero)
9. "Black Friday: quem postou preço falso do ano passado?" (cuidado: só com prova)
10. "Quem está por trás do canal." (não conheço)

### Orçamento e custo por inscrito
- Orçamento: R$ 0 no teste; R$ 500/mês de parcerias e anúncios (do CFO) só depois de o canal provar retenção.
- **Máximo que dá para pagar por inscrito:** cada inscrito rende cerca de **R$ 0,19/mês** (0,03 compra × R$ 6,34). Supondo que fique 6 meses (suposição minha), o valor é de cerca de **R$ 1,10**; tudo acima disso é prejuízo. A regra prática é só pagar por inscrito quando o custo medido ficar abaixo disso.
- **Números semanais:** (1) novos inscritos e saídas, (2) cliques por post e por fonte (sub ID), (3) compras confirmadas e comissão. **Mudar algo** se a retenção em 30 dias ficar abaixo de 70% ou se menos de 3% dos inscritos clicarem em um post.

**Regras:** nenhuma promoção falsa, nenhum "falso desconto", nenhuma citação do painel como depoimento. Divulgação de afiliado em todo post e nas parcerias. Seguir as regras do CONAR; não é aconselhamento jurídico.

## Brand

**Posição:** "só o preço de verdade", com o histórico à mostra (`marketing.md`).
**Limite:** não consegui checar domínio, marca nem @ (sem acesso aos sites oficiais). A lista abaixo é de verificação para você. Nada está registrado.

### Dez nomes
| Nome | Estilo | Risco |
| --- | --- | --- |
| Mínimo Histórico | evocativo | gíria conhecida de preço ("mínimo histórico"); difícil de proteger como marca |
| Preço Honesto | evocativo | pode já existir em varejo |
| Oferta de Verdade | descritivo | genérico e longo |
| Preço Checado | descritivo | parecido com "comparadores" |
| Achado Certo | evocativo | parecido com "Achados do TB" (evitar) |
| Radar de Preço | evocativo | muito usado em comparadores |
| Faro de Oferta | evocativo | curto; confere se existe |
| Caçador de Preço | evocativo | muito comum |
| Promo Limpa | invenção | "promo" já saturado |
| Menor Preço Hoje | descritivo | longo e genérico |
**Evitar** qualquer coisa com "Rei da Promo", "Promobit", "Pelando", "Zoom", "Buscapé", "Achados do TB" ou "Cuponomia".
**Finalistas: Mínimo Histórico, Preço Honesto, Faro de Oferta.**

### Checagens para você fazer
- **Marca:** busca no INPI (https://busca.inpi.gov.br/), classes **35** (publicidade e comparação de preços) e **41/42** conforme o serviço. Um advogado de propriedade intelectual confirma.
- **Domínio:** https://registro.br/ (.com.br) e .com.
- **Handles:** Telegram (canal público), Instagram, X, TikTok, WhatsApp.
- **Confusão:** nenhum nome próximo de `competitors.md`.

### Voz e promessa
- **Promessa:** "Só posto se o preço for o menor ou perto do menor dos últimos meses, e mostro a prova."
- **Slogans (3):** "Só o preço de verdade" · "Menor preço, com histórico" · "Posto pouco, posto certo".
- **Voz:** direta, honesta e discreta. Faz: mostrar o histórico, assumir o erro. Não faz: gritar "corre!", usar contagem regressiva falsa, prometer "o melhor preço do Brasil".
  - Antes: "🔥🔥 SUPER PROMOÇÃO IMPERDÍVEL, CORRE QUE ACABA! 🔥🔥"
  - Depois: "Fone X: R$ 189. É o menor preço dos últimos 3 meses (era R$ 249). Histórico: [link]. Ganho comissão pelo link; o preço é o mesmo."

### O visual (brief)
| Uso | Cor | Hex | Contraste do texto |
| --- | --- | --- | --- |
| Principal (títulos) | azul-noite | #0F2B46 | branco sobre ele: **14,44:1** (AA ok) |
| Destaque (selo "menor preço") | amarelo | #FFC93C | azul-noite sobre amarelo: **9,4:1** (AA ok) |
| Apoio (confirmado) | verde | #1B7F5C | branco sobre verde: **4,96:1** (AA ok para texto normal); azul-noite sobre verde: só **2,91:1**, não usar |
| Fundo | cinza claro | #F5F7FA | azul-noite sobre ele: **13,45:1** |
- **Tipografia:** Inter para texto e Barlow Condensed para títulos, ambas gratuitas no Google Fonts; confirmar a licença.
- **Logo:** um selo simples que diga "preço verificado" (um check dentro de uma etiqueta); funcionar em 32 px (foto do canal no Telegram), em post quadrado e em vídeo. Evitar cifrões e fogo (lembram desconto falso). Conceitos feitos por ferramenta de imagem seriam **conceitos**.
- **Os cinco primeiros pontos de contato:** (1) foto e descrição do canal; (2) o post fixado com as regras e quem está por trás; (3) o formato do post de oferta (menor preço, histórico, aviso de afiliado); (4) o primeiro post nas redes; (5) a resposta ao primeiro "isso não era promoção" ("Você tem razão, corrigi e publiquei o erro").

## Operations

**Não cotei nem verifiquei nenhum fornecedor.** Os nomes abaixo são categorias para você conferir; preços reais voltam ao CFO (`numbers.json`).

### 1. O ciclo diário
1. Coletar ofertas das fontes próprias (API da Shopee, Creators API da Amazon, páginas e gerador de links do Mercado Livre e do Magalu).
2. Aplicar a regra de publicação (preço abaixo do histórico recente, estoque, avaliação mínima).
3. Gerar o link de afiliado com um sub ID por canal.
4. **Aprovação humana** (o documento de origem mantém um portão manual).
5. Publicar (máximo de 8 por dia) no Telegram; espelho semi-manual no WhatsApp; vitrine nas redes.
6. Atualizar posts de ofertas que expiraram.
7. Responder comentários e registrar erros.
8. Semana: ranking das mais clicadas. Mês: conferir comissões e cancelamentos nos painéis.
**O que o público vê:** os posts, as atualizações, o aviso de afiliado, o registro de erros.

### 2. Fornecedores e fontes (a conferir)
| Insumo | Opção | Como obter preço/termos |
| --- | --- | --- |
| Programas de afiliados | Shopee Afiliados, Amazon Associados, Mercado Livre Afiliados, Parceiro Magalu | cadastro e termos de cada programa; Shopee leva de 5 a 15 dias (documento de origem) |
| API para ofertas e links | Shopee (GraphQL), Amazon Creators API (a PA-API 5 foi descontinuada) | documentação oficial de cada loja; ML e Magalu sem API pública confirmada |
| Histórico de preço | construir o próprio a partir das APIs ou usar fonte pública | **não raspar sites contra os termos**; ler os termos de cada fonte |
| Telegram | Bot API oficial | gratuito |
| Servidor e banco | VPS no Brasil ou nuvem | cotar |
Se um preço real diferir de `numbers.json`, atualizar e rodar `/founder-cfo`.

### 3. Pessoas
- **Fundador:** curadoria, desenvolvimento e respostas. Horas por semana **não informadas**; definir antes de tudo (o conselho pediu).
- Rota do primeiro mês: 1 hora por dia de curadoria e aprovação, 2 a 4 horas por semana de construção, até o portão 1.
- Quando o volume crescer, pensar em um segundo curador; encargos e contratação: contador.

### 4. Rotinas (uma página cada)
**Regra de publicação:** só posta se (a) o preço atual está abaixo ou no mínimo dos últimos meses (a janela é uma decisão a definir), (b) há estoque, (c) a avaliação do produto passa de um mínimo definido, (d) o link leva ao produto certo. Caso contrário, descarta e registra.
**Oferta expirada:** editar o post em até 2 horas; registrar se o erro foi do canal.
**Erro de preço:** publicar a correção no registro público.
**Reclamação:** responder em até 1 dia útil.
**Fechamento:** conferir pendências e a fila do dia seguinte.

### 5. Ferramentas
Telegram (Bot API), Node com banco para histórico de preço (do documento), encurtador com sub ID, planilha para comissões. Preços: ver o site de cada um.

### 6. Documentos e obrigações (conferir com contador e advogado)
- **Contrato com cada programa:** ler e cumprir os termos (uso de links, divulgação, proibições). Contas são suspensas por uso fora das regras.
- **Divulgação de publicidade:** avisar que os links são de afiliado; seguir as regras de publicidade (CONAR): https://www.conar.org.br/
- **Empresa:** MEI ou CNPJ conforme o faturamento; conferir enquadramento: https://www.gov.br/empresas-e-negocios/pt-br/empreendedor
- **Imposto de renda** sobre comissões: perguntar ao contador.
- **LGPD:** se o bot guardar dados de inscritos (por exemplo, produtos que acompanham), política de privacidade: https://www.gov.br/anpd/
Isto não é aconselhamento jurídico; as regras variam e mudam.

### 7. Risco (10 principais)
| Risco | Prob. | Impacto | Plano |
| --- | :-: | :-: | --- |
| Postar promoção falsa por erro de dado | média | **alto** | aprovação humana, histórico próprio, registro de erros |
| Conta de afiliado suspensa | média | **alto** | ler termos, nunca repostar com troca de link, não depender de uma loja |
| Comissão menor ou anulada por cancelamento | alta | médio | medir por programa e por categoria |
| Concorrente grande abre canal de nicho | alta | médio | histórico próprio e correção pública |
| Audiência cresce mas não compra | **alta** | alto | medir compras por inscrito antes de gastar com anúncios |
| Inscritos silenciam/saem | alta | alto | limite de 8 posts, medir retenção |
| Telegram muda regras ou limita bots | baixa | alto | espelho no WhatsApp e lista própria (e-mail) |
| Fundador sem tempo | **alta** | alto | definir horas por semana e parar se o portão 1 não passar |
| Erro de link de afiliado (sub ID errado) | média | médio | teste automático antes de publicar |
| Reclamação pública ou denúncia | baixa | médio | correção rápida e divulgação clara |

## Launch plan

> **Nota (13/11/2026):** este roteiro foi escrito para o plano de um canal só. O roteiro atual, com dois canais, três portões e datas propostas, está no documento "Estudo de viabilidade" (seção "Como e quando começar").

## Lançamento

### 1. O teste barato antes de gastar (portão 1 do documento)
**Tipo:** canal pequeno com postagem **manual** por 2 a 4 semanas, sem escrever o bot.
**Linha de sucesso, definida antes de rodar (proposta minha; ajuste):**
- 200 inscritos até o dia 14 (indicação de amigos e redes sociais), sem anúncio pago;
- pelo menos **3% dos inscritos clicam** em um post comum;
- pelo menos **10 compras confirmadas** no painel de afiliado (por sub ID) nos primeiros 14 dias de posts;
- **retenção em 30 dias de pelo menos 70%.**
**Comparação com o painel:** o painel disse 45% entram e compram (teto). Se o canal real não passar de 3% de cliques e 10 compras, **confie nos números reais e volte a `offer.md`**; não construa o bot.
**Condição anterior:** pelo menos um cadastro de afiliado aprovado (Shopee leva de 5 a 15 dias). Hoje é 13/11/2026: **Black Friday (27/11) está a 14 dias**, então só serve se algum programa aprovar antes.

### 2. Contagem regressiva (datas **propostas**, ajuste à sua data-alvo)
| Quando | O que | Dono |
| --- | --- | --- |
| 13/11 a 16/11 | Pedir cadastro em Shopee, Mercado Livre, Amazon e Magalu; escolher o nicho (tecnologia ou casa) | Fundador |
| 16/11 a 22/11 | Escrever a regra de publicação; criar o canal e a página "quem somos"; montar o formato do post | Fundador |
| 23/11 a 06/12 | **Teste fechado com postagem manual**; registrar cliques e compras por sub ID | Fundador |
| 07/12 | **Decisão do portão 1**: abrir ao público ou voltar à oferta | Fundador |
| 07/12 a 20/12 | Abertura pública, Natal | Fundador |
| 21/12 a 10/01 | Se o portão passar: construir o MVP do pipeline (fase 1 do roadmap do documento) | Fundador |
**Caminho crítico:** (1) aprovação do afiliado, (2) regra de publicação escrita, (3) 14 dias de dados. Qualquer atraso move a decisão.

### 3. Dia da abertura pública (07/12)
- 09:00 conferir links de afiliado e sub ID.
- 10:00 post fixado com regras e quem está por trás.
- 12:00 primeiros 3 posts de oferta (histórico visível).
- 18:00 post da segunda leva; atualizar expirados.
- 21:00 registrar erros e fechar o dia.
**Se algo quebrar:** pausar a publicação, avisar no canal e corrigir (riscos em `ops.md`).

### 4. Primeiros 30 dias
| Número | Como ver | Mudar se |
| --- | --- | --- |
| Inscritos e saídas | Telegram | retenção em 30 dias abaixo de 70% |
| Cliques por post | encurtador com sub ID | abaixo de 3% dos inscritos |
| Compras por link e comissão | painéis de afiliado | menos de 10 em 14 dias |
| Compras por inscrito por mês (premissa do CFO: 0,03) | cálculo | muito abaixo, parar anúncios |
| Posts por dia | contagem | acima de 8 |
**Revisões:** dia 7 (formato certo?), dia 14 (cliques e compras), dia 30 (retenção e comissão por programa).

_The panel is simulated buyers and the numbers are projections from your inputs. Confirm demand with real customers and costs with real quotes before you spend. Not financial, legal or tax advice._
