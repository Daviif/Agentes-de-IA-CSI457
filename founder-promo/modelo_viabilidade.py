#!/usr/bin/env python3
"""Modelo de viabilidade: dois canais de promoções (A: ticket alto, B: ticket baixo).
Biblioteca padrão apenas. TODAS as premissas são estimativas (ver o estudo).
    python3 modelo_viabilidade.py            # imprime tabelas
    python3 modelo_viabilidade.py --json     # saída em JSON
    python3 modelo_viabilidade.py --numbers  # grava numbers.json (cenário base, 12 meses) p/ o CFO
"""
import json, sys

MESES = 24
SPLIT_A = 0.40          # fatia da audiência no canal A (ticket alto)
FIXO = {"VPS e banco de dados": 100, "Dados de histórico de preço": 100,
        "Ferramentas de arte e agendamento": 100, "Domínio e encurtador": 30,
        "Contador / DAS de MEI": 90}
PARTIDA = {"Abertura de CNPJ/MEI e contador": 500, "Identidade visual, domínios, contas": 300}
HORAS_SEMANA, VALOR_HORA = 15, 50   # custo de oportunidade do fundador (não é caixa)

CEN = {
 "pessimista": dict(a0=80,  g=0.08, cap=500,  churn=0.05,
    A=dict(ticket=1500, taxa=0.02, conv=0.0015, reserva=0.25),
    B=dict(ticket=70,   taxa=0.04, conv=0.008,  reserva=0.15)),
 "base": dict(a0=150, g=0.20, cap=1200, churn=0.03,
    A=dict(ticket=1500, taxa=0.03, conv=0.003,  reserva=0.20),
    B=dict(ticket=70,   taxa=0.05, conv=0.025,  reserva=0.10)),
 "otimista": dict(a0=300, g=0.25, cap=3000, churn=0.02,
    A=dict(ticket=1500, taxa=0.05, conv=0.006,  reserva=0.15),
    B=dict(ticket=70,   taxa=0.06, conv=0.05,   reserva=0.08)),
}

def por_inscrito(c):
    """receita liquida e compras por inscrito/mes, ponderado pela divisao da audiencia"""
    def canal(p):
        com = p["ticket"] * p["taxa"]
        return p["conv"], com, p["conv"] * com, p["conv"] * com * (1 - p["reserva"])
    a, b = canal(c["A"]), canal(c["B"])
    compras = SPLIT_A * a[0] + (1 - SPLIT_A) * b[0]
    bruto = SPLIT_A * a[2] + (1 - SPLIT_A) * b[2]
    liquido = SPLIT_A * a[3] + (1 - SPLIT_A) * b[3]
    return compras, bruto, liquido

def simula(c, anuncios=0.0, cpf=2.5):
    compras_f, bruto_f, liq_f = por_inscrito(c)
    fixo = sum(FIXO.values()) + anuncios
    seg, caixa, linhas = 0.0, -sum(PARTIDA.values()), []
    for m in range(1, MESES + 1):
        adds = min(c["a0"] * (1 + c["g"]) ** (m - 1), c["cap"]) + (anuncios / cpf if anuncios else 0)
        seg = seg * (1 - c["churn"]) + adds
        receita = seg * liq_f
        lucro = receita - fixo
        caixa += lucro
        linhas.append(dict(mes=m, seguidores=round(seg), compras_dia=seg * compras_f / 30,
                           receita=receita, custo=fixo, lucro=lucro, caixa=caixa))
    return linhas

def resumo(linhas):
    eq = next((l["mes"] for l in linhas if l["lucro"] >= 0), None)
    # lucro mensal estavel (>=0 do mes eq em diante)
    estavel = next((l["mes"] for i, l in enumerate(linhas) if all(x["lucro"] >= 0 for x in linhas[i:])), None)
    pior = min(l["caixa"] for l in linhas)
    mes_pior = next(l["mes"] for l in linhas if l["caixa"] == pior)
    retorno = next((l["mes"] for i, l in enumerate(linhas) if l["caixa"] >= 0 and i > 0 and linhas[i-1]["caixa"] < 0), None)
    return dict(equilibrio_mensal=eq, equilibrio_estavel=estavel, caixa_minimo=pior, mes_caixa_minimo=mes_pior,
                retorno_total=retorno, caixa_24=linhas[-1]["caixa"], lucro_mes24=linhas[-1]["lucro"],
                receita_12=sum(l["receita"] for l in linhas[:12]), lucro_12=sum(l["lucro"] for l in linhas[:12]),
                receita_24=sum(l["receita"] for l in linhas), seguidores_12=linhas[11]["seguidores"],
                seguidores_24=linhas[-1]["seguidores"])

def tudo():
    out = {}
    for nome, c in CEN.items():
        compras_f, bruto_f, liq_f = por_inscrito(c)
        ls = simula(c)
        out[nome] = dict(por_inscrito=dict(compras=compras_f, bruto=bruto_f, liquido=liq_f),
                         equilibrio_seguidores=sum(FIXO.values()) / liq_f, linhas=ls, **resumo(ls))
    return out

if __name__ == "__main__":
    r = tudo()
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    elif "--numbers" in sys.argv:
        c = CEN["base"]; compras_f, bruto_f, liq_f = por_inscrito(c)
        preco = bruto_f / compras_f; res = (bruto_f - liq_f) / compras_f
        ls = r["base"]["linhas"][:12]
        json.dump({
          "business": "Dois canais de promoções no Telegram (A ticket alto, B ticket baixo) com links de afiliado. Unidade = 1 compra por link; 'price' = comissão média ponderada por compra (ESTIMATIVA, cenário base)",
          "unit": "compra por link", "price": round(preco, 2),
          "variable": [{"label": "Reserva para cancelamento e devolução (ESTIMATIVA, média ponderada)", "cost": round(res, 2)}],
          "fixed_monthly": [{"label": k + " (ESTIMATIVA)", "cost": v} for k, v in FIXO.items()],
          "startup": [{"label": k + " (ESTIMATIVA; tempo do fundador NÃO incluído)", "cost": v} for k, v in PARTIDA.items()],
          "days_per_month": 30, "plan_per_day": round(ls[-1]["compras_dia"], 2),
          "ramp_per_day": [round(l["compras_dia"], 2) for l in ls]},
          open("numbers.json", "w"), ensure_ascii=False, indent=2)
        print("numbers.json gravado (cenário base)")
    else:
        for n, d in r.items():
            print("==", n, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in d.items() if k != "linhas"})
            for l in d["linhas"]:
                if l["mes"] in (1, 3, 6, 9, 12, 15, 18, 21, 24):
                    print("  mes %2d seg %6d compras/dia %5.1f receita %7.0f lucro %7.0f caixa %8.0f" % (l["mes"], l["seguidores"], l["compras_dia"], l["receita"], l["lucro"], l["caixa"]))
