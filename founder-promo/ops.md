# Operação

**Não cotei nem verifiquei nenhum fornecedor.** Os nomes abaixo são categorias para você conferir; preços reais voltam ao CFO (`numbers.json`).

## 1. O ciclo diário
1. Coletar ofertas das fontes próprias (API da Shopee, Creators API da Amazon, páginas e gerador de links do Mercado Livre e do Magalu).
2. Aplicar a regra de publicação (preço abaixo do histórico recente, estoque, avaliação mínima).
3. Gerar o link de afiliado com um sub ID por canal.
4. **Aprovação humana** (o documento de origem mantém um portão manual).
5. Publicar (máximo de 8 por dia) no Telegram; espelho semi-manual no WhatsApp; vitrine nas redes.
6. Atualizar posts de ofertas que expiraram.
7. Responder comentários e registrar erros.
8. Semana: ranking das mais clicadas. Mês: conferir comissões e cancelamentos nos painéis.
**O que o público vê:** os posts, as atualizações, o aviso de afiliado, o registro de erros.

## 2. Fornecedores e fontes (a conferir)
| Insumo | Opção | Como obter preço/termos |
| --- | --- | --- |
| Programas de afiliados | Shopee Afiliados, Amazon Associados, Mercado Livre Afiliados, Parceiro Magalu | cadastro e termos de cada programa; Shopee leva de 5 a 15 dias (documento de origem) |
| API para ofertas e links | Shopee (GraphQL), Amazon Creators API (a PA-API 5 foi descontinuada) | documentação oficial de cada loja; ML e Magalu sem API pública confirmada |
| Histórico de preço | construir o próprio a partir das APIs ou usar fonte pública | **não raspar sites contra os termos**; ler os termos de cada fonte |
| Telegram | Bot API oficial | gratuito |
| Servidor e banco | VPS no Brasil ou nuvem | cotar |
Se um preço real diferir de `numbers.json`, atualizar e rodar `/founder-cfo`.

## 3. Pessoas
- **Fundador:** curadoria, desenvolvimento e respostas. Horas por semana **não informadas**; definir antes de tudo (o conselho pediu).
- Rota do primeiro mês: 1 hora por dia de curadoria e aprovação, 2 a 4 horas por semana de construção, até o portão 1.
- Quando o volume crescer, pensar em um segundo curador; encargos e contratação: contador.

## 4. Rotinas (uma página cada)
**Regra de publicação:** só posta se (a) o preço atual está abaixo ou no mínimo dos últimos meses (a janela é uma decisão a definir), (b) há estoque, (c) a avaliação do produto passa de um mínimo definido, (d) o link leva ao produto certo. Caso contrário, descarta e registra.
**Oferta expirada:** editar o post em até 2 horas; registrar se o erro foi do canal.
**Erro de preço:** publicar a correção no registro público.
**Reclamação:** responder em até 1 dia útil.
**Fechamento:** conferir pendências e a fila do dia seguinte.

## 5. Ferramentas
Telegram (Bot API), Node com banco para histórico de preço (do documento), encurtador com sub ID, planilha para comissões. Preços: ver o site de cada um.

## 6. Documentos e obrigações (conferir com contador e advogado)
- **Contrato com cada programa:** ler e cumprir os termos (uso de links, divulgação, proibições). Contas são suspensas por uso fora das regras.
- **Divulgação de publicidade:** avisar que os links são de afiliado; seguir as regras de publicidade (CONAR): https://www.conar.org.br/
- **Empresa:** MEI ou CNPJ conforme o faturamento; conferir enquadramento: https://www.gov.br/empresas-e-negocios/pt-br/empreendedor
- **Imposto de renda** sobre comissões: perguntar ao contador.
- **LGPD:** se o bot guardar dados de inscritos (por exemplo, produtos que acompanham), política de privacidade: https://www.gov.br/anpd/
Isto não é aconselhamento jurídico; as regras variam e mudam.

## 7. Risco (10 principais)
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
