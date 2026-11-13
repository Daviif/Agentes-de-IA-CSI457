# Canal de promoções com links de afiliado (nome de trabalho; estilo "Rei da Promo")

- O que é: um canal de promoções no Telegram (base) que posta achados de Mercado Livre, Shopee, Amazon, Magalu e outras lojas, com link de afiliado do dono do canal. Ganha comissão por venda feita pelos links. Pode ter rankings ("top 10 promos mais clicadas da semana"). Parte técnica (coletar ofertas, converter link, formatar, publicar) é automatizável por um desenvolvedor.
- Para quem é: compradores brasileiros de internet que caçam desconto. Nicho inicial a escolher (ex.: tecnologia ou casa).
- O que vende, por quanto: nada diretamente ao público. O canal é grátis; a receita é a comissão paga pela loja (Mercado Livre até 16% em beleza, esportes e moda; demais taxas a confirmar).
- Onde e como: Telegram (canal e grupo, automação total por bot), vitrine no Instagram e X (manual ou agendado), WhatsApp só semi-manual. Um sub ID por canal para saber de onde nasce cada venda.
- Orçamento e restrições: não informados. O fundador é desenvolvedor. Cadastros nas lojas ainda não pedidos (Shopee leva 5 a 15 dias de aprovação manual).

## Plano do documento de origem
- Pipeline de 7 etapas, do coletor de ofertas às métricas de comissão, com uma aprovação humana antes de publicar; stack em Node com banco para histórico de preço.
- Roadmap de 4 fases com 3 portões de decisão: só constrói o bot depois de ver que o canal gera clique e venda; só tira a aprovação manual quando o filtro acertar.
- APIs: Shopee (GraphQL, aprovação manual), Amazon (Creators API; a PA-API 5 foi descontinuada), Mercado Livre e Magalu (gerador de links do painel; API pública não confirmada).
- Riscos listados: promoção falsa, repostar de outros canais trocando o link, conta de afiliado suspensa, automação não oficial no WhatsApp, transparência de afiliado e imposto de renda sobre comissões.

## Contexto adicional para o conselho
- Não foram informados: tamanho de audiência inicial, quanto tempo o fundador dedica, custos, taxas de comissão reais além do Mercado Livre, concorrentes conhecidos além do perfil @oreidapromobr no X. Trate esses pontos como perguntas em aberto; não invente números.
- Modelo de receita: comissão por venda, paga pela loja, com cancelamento e devolução podendo anular a comissão (a confirmar em cada programa).
