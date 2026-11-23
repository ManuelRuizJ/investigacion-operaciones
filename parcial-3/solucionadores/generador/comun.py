"""Utilidades comunes para generar los solucionadores (estilos, bloques, matrices)."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.formula import ArrayFormula
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter as CL
from openpyxl.utils.cell import range_boundaries

FONT = "Arial"
AZUL = "1F4E78"
F_IN = PatternFill("solid", fgColor="FFF2CC")     # entrada (amarillo claro)
F_CALC = PatternFill("solid", fgColor="F2F2F2")   # cálculo (gris)
F_RES = PatternFill("solid", fgColor="E2EFDA")    # resultado clave (verde)
F_HEAD = PatternFill("solid", fgColor=AZUL)
F_SUB = PatternFill("solid", fgColor="DDEBF7")
F_ROJO = PatternFill("solid", fgColor="F8CBAD")
_thin = Side(style="thin", color="A6A6A6")
BORDE = Border(left=_thin, right=_thin, top=_thin, bottom=_thin)

GRANDE = 1000000000  # "infinito" para redes


def libro():
    wb = Workbook()
    wb.remove(wb.active)
    return wb


def hoja(wb, nombre, titulo, subtitulo=None):
    ws = wb.create_sheet(nombre)
    ws.sheet_view.showGridLines = False
    c = ws["A1"]
    c.value = titulo
    c.font = Font(name=FONT, size=14, bold=True, color=AZUL)
    if subtitulo:
        c = ws["A2"]
        c.value = subtitulo
        c.font = Font(name=FONT, size=9, italic=True, color="595959")
    return ws


def _estilo(c, fill, fmt=None, bold=False, color="000000", center=False):
    c.fill = fill
    c.border = BORDE
    c.font = Font(name=FONT, size=10, bold=bold, color=color)
    if fmt:
        c.number_format = fmt
    if center:
        c.alignment = Alignment(horizontal="center", vertical="center")


def inp(ws, ref, val=None, fmt=None, center=False):
    c = ws[ref]
    if val is not None:
        c.value = val
    _estilo(c, F_IN, fmt, color="0000FF", center=center)
    return c


def calc(ws, ref, formula, fmt=None, res=False, center=False, bold=None):
    c = ws[ref]
    c.value = formula
    _estilo(c, F_RES if res else F_CALC, fmt, bold=res if bold is None else bold, center=center)
    return c


def arr(ws, rng, formula, fmt=None, res=False, style=True):
    """Fórmula matricial clásica (CSE) compatible con Excel y LibreOffice."""
    rng = rng.replace("$", "")
    tl = rng.split(":")[0]
    ws[tl] = ArrayFormula(rng, formula)
    if style:
        c1, r1, c2, r2 = range_boundaries(rng if ":" in rng else f"{rng}:{rng}")
        for r in range(r1, r2 + 1):
            for cc in range(c1, c2 + 1):
                _estilo(ws.cell(r, cc), F_RES if res else F_CALC, fmt)


def head(ws, row, col, labels, fill=F_HEAD, color="FFFFFF"):
    for i, t in enumerate(labels):
        c = ws.cell(row, col + i, t)
        c.fill = fill
        c.border = BORDE
        c.font = Font(name=FONT, size=10, bold=True, color=color)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def label(ws, ref, text, bold=False, color="000000", size=10, italic=False, fill=None, wrap=False):
    c = ws[ref]
    c.value = text
    c.font = Font(name=FONT, size=size, bold=bold, color=color, italic=italic)
    if fill:
        c.fill = fill
        c.border = BORDE
    if wrap:
        c.alignment = Alignment(wrap_text=True, vertical="top")
    return c


def seccion(ws, ref, text):
    return label(ws, ref, text, bold=True, color=AZUL, size=12)


def nota(ws, ref, text):
    return label(ws, ref, text, italic=True, color="595959", size=9)


def anchos(ws, d):
    for col, w in d.items():
        ws.column_dimensions[col].width = w


def R(key, etiqueta, valor, unidad="", tipo="calc", fmt="0.0000", interp=None):
    """Fila de un bloque. tipo: 'in' (entrada), 'calc', 'res' (resultado clave)."""
    return dict(key=key, etiqueta=etiqueta, valor=valor, unidad=unidad, tipo=tipo, fmt=fmt, interp=interp)


def bloque(ws, r0, filas, col=1, ctx=None, encabezado=("Concepto", "Valor", "Unidad", "Interpretación")):
    """Escribe un bloque Concepto | Valor | Unidad | Interpretación.
    Las fórmulas pueden usar {clave} para referirse a filas anteriores (o a ctx).
    Devuelve dict clave -> referencia absoluta de la celda de valor."""
    refs = dict(ctx or {})
    if encabezado:
        head(ws, r0, col, list(encabezado))
        r = r0 + 1
    else:
        r = r0
    vc = CL(col + 1)
    for f in filas:
        if f is None:
            r += 1
            continue
        if isinstance(f, str):
            for k in range(len(encabezado or (1, 2, 3, 4))):
                cc = ws.cell(r, col + k)
                cc.fill = F_SUB
                cc.border = BORDE
            c = ws.cell(r, col, f)
            c.font = Font(name=FONT, size=10, bold=True, color=AZUL)
            r += 1
            continue
        refs[f["key"]] = f"${vc}${r}"
        c = ws.cell(r, col, f["etiqueta"])
        c.font = Font(name=FONT, size=10, bold=f["tipo"] == "res")
        c.border = BORDE
        val = f["valor"]
        if isinstance(val, str) and val.startswith("="):
            val = val.format_map(refs)
        ref = f"{vc}{r}"
        if f["tipo"] == "in":
            inp(ws, ref, val, f["fmt"])
        else:
            calc(ws, ref, val, f["fmt"], res=f["tipo"] == "res")
        u = f["unidad"]
        if isinstance(u, str) and u.startswith("="):
            u = u.format_map(refs)
        cu = ws.cell(r, col + 2, u)
        cu.font = Font(name=FONT, size=9, color="595959")
        cu.border = BORDE
        if f["interp"]:
            ci = ws.cell(r, col + 3, f["interp"].format_map(refs))
            ci.font = Font(name=FONT, size=9, italic=True, color="375623")
        ws.cell(r, col + 3).border = BORDE
        r += 1
    refs["_fin"] = r
    return refs


def lista(ws, ref, opciones):
    dv = DataValidation(type="list", formula1='"' + ",".join(opciones) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(ref)


def entero(ws, ref, lo, hi):
    dv = DataValidation(type="whole", operator="between", formula1=str(lo), formula2=str(hi),
                        showErrorMessage=True, errorTitle="Valor fuera de rango",
                        error=f"Escribe un entero entre {lo} y {hi}")
    ws.add_data_validation(dv)
    dv.add(ref)


def marcar_rojo(ws, rng, formula):
    ws.conditional_formatting.add(rng, FormulaRule(formula=[formula], fill=F_ROJO,
                                                   font=Font(name=FONT, bold=True, color="9C0006")))


def link(ws, ref, hoja_destino, texto):
    c = ws[ref]
    c.value = texto
    c.hyperlink = Hyperlink(ref=ref, location=f"'{hoja_destino}'!A1", display=texto)
    c.font = Font(name=FONT, size=11, color="0563C1", underline="single", bold=True)


def inicio(wb, titulo, descripcion, hojas):
    """Hoja índice. hojas: lista de (nombre_hoja, descripción)."""
    ws = wb.create_sheet("Inicio", 0)
    ws.sheet_view.showGridLines = False
    label(ws, "A1", titulo, bold=True, color=AZUL, size=16)
    label(ws, "A2", "Investigación de Operaciones II · Solucionadores del parcial 3", italic=True, color="595959")
    label(ws, "A4", descripcion, wrap=True)
    ws.merge_cells("A4:F4")
    ws.row_dimensions[4].height = 45
    seccion(ws, "A6", "Código de colores")
    inp(ws, "A7", "Amarillo")
    label(ws, "B7", "Datos de entrada: escribe aquí los datos de TU problema.")
    calc(ws, "A8", "Gris")
    label(ws, "B8", "Cálculo automático (no modificar).")
    calc(ws, "A9", "Verde", res=True)
    label(ws, "B9", "Resultado principal / respuesta.")
    c = ws["A10"]
    c.value = "Rojo"
    c.fill = F_ROJO
    c.border = BORDE
    c.font = Font(name=FONT, size=10, bold=True, color="9C0006")
    label(ws, "B10", "Advertencia (dato inconsistente, sistema inestable, etc.).")
    seccion(ws, "A12", "Hojas de este libro")
    for i, (h, d) in enumerate(hojas):
        link(ws, f"A{13 + i}", h, h)
        label(ws, f"B{13 + i}", d)
    r = 14 + len(hojas)
    nota(ws, f"A{r}", "Cada hoja trae precargado un ejemplo resuelto: reemplaza los datos amarillos por los de tu ejercicio.")
    nota(ws, f"A{r + 1}", "Mantén las mismas unidades de tiempo en todos los datos (por ejemplo: todo por hora, o todo por año).")
    anchos(ws, {"A": 26, "B": 90})
    return ws


def formulario(wb, titulo, secciones):
    """Hoja de formulario. secciones: lista de (titulo, [(concepto, formula), ...])."""
    ws = hoja(wb, "Formulario", titulo, "Resumen de fórmulas del tema")
    r = 4
    for t, items in secciones:
        seccion(ws, f"A{r}", t)
        r += 1
        for concepto, formula in items:
            label(ws, f"A{r}", concepto, fill=F_SUB)
            c = label(ws, f"B{r}", formula, fill=F_CALC)
            c.font = Font(name="Consolas", size=10)
            r += 1
        r += 1
    anchos(ws, {"A": 42, "B": 95})
    return ws
