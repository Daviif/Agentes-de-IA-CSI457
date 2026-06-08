"""Gera RELATORIO_TECNICO.pdf a partir do RELATORIO_TECNICO.md usando fpdf."""
import re
from fpdf import FPDF

MD   = "tp01/RELATORIO_FINAL.md"
OUT  = "tp01/RELATORIO_FINAL.pdf"

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "TP01 - Agentes de Busca em Labirinto  |  CSI457 / 2026-1", align="R")
        self.ln(4)

    def footer(self):
        self.set_y(-13)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Página {self.page_no()}", align="C")


def safe(text: str) -> str:
    """Garante que o texto seja 100% latin-1 compatível."""
    box = {'│':'|','├':'+','└':'+','─':'-','┬':'+','┼':'+','┤':'+','┴':'+','╟':'+','╠':'+','╞':'+'}
    for k, v in box.items():
        text = text.replace(k, v)
    return text.encode('latin-1', errors='replace').decode('latin-1')


def clean(text):
    """Remove markdown inline e normaliza caracteres para latin-1."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*',     r'\1', text)
    text = re.sub(r'`(.+?)`',       r'\1', text)
    # Substitui caracteres fora do latin-1
    replacements = {
        '—': '-', '–': '-', '‒': '-',  # traços
        '‘': "'", '’': "'",                  # aspas simples
        '“': '"', '”': '"',                  # aspas duplas
        '•': '*', '◦': '-',                  # bullets
        '→': '->', '←': '<-',                # setas
        '✓': 'v', '✔': 'v',                  # check
        'é': 'e', 'ã': 'a', 'ç': 'c',  # acentos comuns
        'á': 'a', 'ê': 'e', 'ó': 'o',
        'ú': 'u', 'í': 'i', 'õ': 'o',
        'â': 'a', 'ô': 'o', 'î': 'i',
        'à': 'a', 'ü': 'u', 'ñ': 'n',
        'É': 'E', 'Ã': 'A', 'Ç': 'C',
        'Á': 'A', 'Ê': 'E', 'Ó': 'O',
        'Ú': 'U', 'Í': 'I', 'Õ': 'O',
        'Â': 'A', 'Ô': 'O', 'Î': 'I',
    }
    for orig, sub in replacements.items():
        text = text.replace(orig, sub)
    # Descarta qualquer outro char fora do latin-1
    text = text.encode('latin-1', errors='replace').decode('latin-1')
    return text.strip()


def render(pdf: PDF, lines: list[str]):
    in_code = False
    code_buf = []
    i = 0

    while i < len(lines):
        raw = lines[i]

        # ── Bloco de código ────────────────────────────────────────
        if raw.startswith("```"):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                pdf.set_fill_color(240, 240, 240)
                pdf.set_font("Courier", "", 8)
                pdf.set_text_color(40, 40, 40)
                for cline in code_buf:
                    pdf.set_x(18)
                    pdf.multi_cell(174, 4.5, safe(cline.rstrip()), fill=True)
                pdf.set_fill_color(255, 255, 255)
                pdf.ln(2)
            i += 1
            continue

        if in_code:
            code_buf.append(raw)
            i += 1
            continue

        # ── Cabeçalhos ─────────────────────────────────────────────
        if raw.startswith("#### "):
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(60, 60, 100)
            pdf.multi_cell(0, 6, clean(raw[5:]))
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)
        elif raw.startswith("### "):
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(40, 40, 140)
            pdf.multi_cell(0, 7, clean(raw[4:]))
            pdf.set_draw_color(180, 180, 220)
            pdf.line(pdf.get_x(), pdf.get_y(), 200, pdf.get_y())
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
        elif raw.startswith("## "):
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(20, 20, 120)
            pdf.multi_cell(0, 8, clean(raw[3:]))
            pdf.set_draw_color(100, 100, 200)
            pdf.set_line_width(0.5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.set_line_width(0.2)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)
        elif raw.startswith("# "):
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(10, 10, 80)
            pdf.multi_cell(0, 10, clean(raw[2:]))
            pdf.set_draw_color(60, 60, 180)
            pdf.set_line_width(0.8)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.set_line_width(0.2)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(5)

        # ── Linha horizontal ────────────────────────────────────────
        elif raw.strip() == "---":
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
            pdf.ln(5)

        # ── Tabela (linha com |) ────────────────────────────────────
        elif raw.strip().startswith("|"):
            cells = [c.strip() for c in raw.strip().strip("|").split("|")]
            # Pula linhas separadoras (---|---)
            if all(re.match(r'^[-: ]+$', c) for c in cells if c):
                i += 1
                continue
            col_w = 180 / max(len(cells), 1)
            is_header = (i == 0 or not lines[i-1].strip().startswith("|"))
            pdf.set_font("Helvetica", "B" if is_header else "", 8)
            pdf.set_fill_color(220, 220, 240)
            for c in cells:
                pdf.cell(col_w, 6, clean(c)[:40], border=1,
                         fill=is_header, align="L")
            pdf.ln()
            pdf.set_fill_color(255, 255, 255)

        # ── Item de lista ───────────────────────────────────────────
        elif re.match(r'^\s*[-*] ', raw):
            indent = len(raw) - len(raw.lstrip())
            bullet = "*" if indent < 4 else "-"
            margin = 18 + (indent // 2) * 4
            pdf.set_font("Helvetica", "", 10)
            text = clean(re.sub(r'^\s*[-*] ', '', raw))
            pdf.set_x(margin)
            pdf.cell(5, 6, bullet)
            pdf.set_x(margin + 5)
            pdf.multi_cell(185 - margin, 6, text)

        # ── Linha em negrito/destaque (** ... **) ──────────────────
        elif raw.strip().startswith("**") and raw.strip().endswith("**"):
            pdf.set_font("Helvetica", "B", 10)
            pdf.multi_cell(0, 6, clean(raw))

        # ── Linha vazia ─────────────────────────────────────────────
        elif raw.strip() == "":
            pdf.ln(2)

        # ── Parágrafo normal ────────────────────────────────────────
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, clean(raw))
            pdf.ln(1)

        i += 1


def main():
    with open(MD, encoding="utf-8") as f:
        lines = f.read().splitlines()

    pdf = PDF()
    pdf.set_margins(10, 15, 10)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)

    render(pdf, lines)

    pdf.output(OUT)
    print(f"PDF gerado: {OUT}")


if __name__ == "__main__":
    main()
