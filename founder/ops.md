# Operação

**Nenhum fornecedor ou preço abaixo foi cotado.** São categorias e nomes para você pedir orçamento; preços reais voltam ao CFO (`numbers.json`).

## 1. O ciclo diário
1. Manhã: ver alertas de falha (Pix, reservas, envio de mensagens) e fila de suporte.
2. Implantação de arena nova: coletar quadras, horários, preços, feriados e lista de mensalistas; lançar tudo; testar uma reserva de ponta a ponta com o dono; publicar o link.
3. Tarde: responder pendências, revisar pagamentos de sinal não conciliados.
4. Noite e fim de semana (o que o painel mais pediu): atendimento por WhatsApp em escala (ver rota).
5. Semana: relatório de ocupação para cada arena; revisar o que não deu certo; cobrança das mensalidades.
6. Mês: cobrança, renovações, cancelamentos, exportações pedidas.
**O que o cliente vê:** o link de reservas, o Pix, o comprovante, a primeira conversa de implantação e o suporte.

## 2. Fornecedores (a cotar)
| Insumo | Opções para cotar | Como obter preço |
| --- | --- | --- |
| Hospedagem e banco de dados | provedores de nuvem com região no Brasil | tabela pública + estimativa de uso |
| **Pix cobrado na reserva** | Mercado Pago, Asaas, Efí (ex-Gerencianet) e similares | pedir a tabela de taxa por transação e prazo de repasse; **o modelo escolhido é Pix direto na conta da arena** |
| WhatsApp automático (lembretes) | API oficial da Meta via parceiros | cotar por conversa; hoje o produto só gera texto pronto |
| Atendimento | pessoa de meio período, noite/fim de semana | salário local; ver abaixo |
Se o preço real divergir de `numbers.json`, atualizar e rodar `/founder-cfo`.

## 3. Pessoas
- **Fundador:** vendas, implantações, desenvolvimento (tempo não remunerado nos números).
- **Atendente meio período (R$ 2.500/mês, estimativa):** noites e fins de semana.
- **Rota do mês 1 (3 arenas):** fundador atende tudo; atendente só começa quando passar de ~10 arenas ativas. Encargos além do salário variam; o contador deve calcular.

## 4. Rotinas (resumo de uma página cada)
**Abertura do dia:** painel de alertas → fila de suporte → pagamentos de sinal sem conciliação.
**Implantação (2 dias):** formulário → lançar quadras e preços → lançar mensalistas → reserva de teste → link no Instagram e WhatsApp da arena → ligação de 10 min no dia 3.
**Reclamação:** responder em até 2 h úteis; pedir os dados (arena, horário, código); resolver ou explicar; registrar a causa.
**Fechamento do dia:** deixar o plantão avisado, falhas abertas anotadas.
**Reposição semanal:** revisar custos de nuvem e mensagens.

## 5. Ferramentas (a cotar)
Controle de tarefas gratuito, planilha, e-mail no domínio, monitoramento de disponibilidade com plano gratuito, nota fiscal pelo contador. Preços: ver o site de cada fornecedor.

## 6. Documentos e obrigações (confirme com contador e advogado)
- Empresa (CNPJ) e enquadramento tributário; a atividade de software como serviço pode ter regras próprias: https://www.gov.br/empresas-e-negocios/pt-br
- Nota fiscal de serviço no município.
- **LGPD:** o sistema guarda nome e telefone dos clientes da arena. Política de privacidade, base legal, contrato com a arena como operadora dos dados: https://www.gov.br/anpd/
- Termos de uso e contrato de assinatura (cancelamento, exportação, responsabilidade pelos Pix).
- Seguro de responsabilidade: perguntar ao corretor se faz sentido.
Isto não é aconselhamento jurídico; as regras variam e mudam.

## 7. Risco (10 principais)
| Risco | Prob. | Impacto | Plano |
| --- | :-: | :-: | --- |
| Pix de sinal e mensalista não ficam prontos a tempo | média | **alto** | não vender o que não existe; fase piloto só com o que funciona |
| Falha do Pix cobra ou não libera horário | média | alto | conciliação diária, alerta, reembolso manual |
| Reserva duplicada | baixa | alto | travar horário no servidor na hora; teste de concorrência antes do piloto |
| Fundador sozinho adoece | média | alto | documentação das rotinas; segundo contato de suporte |
| Perda de dados | baixa | muito alto | cópia diária e exportação para o cliente |
| Concorrente baixa o preço | alta | médio | foco em implantação e suporte |
| Cliente cancela após o mês grátis | **alta** | alto | medir retenção do mês 2; investigar causa |
| Arena exige nota fiscal/contrato | média | médio | contador e modelo de contrato |
| Reclamação pública | baixa | médio | resposta em 2 h |
| Vazamento de dados de clientes | baixa | muito alto | acesso mínimo, senhas e logs |
