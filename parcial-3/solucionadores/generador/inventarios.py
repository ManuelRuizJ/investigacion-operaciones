"""3_Inventarios.xlsx: EOQ, faltantes, descuentos, POQ, revisión continua (3 casos), revisión periódica, un periodo."""
from openpyxl.chart import LineChart, Reference
from comun import *

H_NOTA = "Si te dan H directo escríbelo; si no, déjalo vacío y se usa H = I·C"


def _H(prefijo=""):
    return [
        R("C", "Costo unitario del artículo (C)", None, "$ por unidad", "in", "#,##0.00"),
        R("I", "Tasa de costo de mantener (I)", None, "% anual del costo", "in", "0.00%"),
        R("Hd", "Costo de mantener H (directo)", None, "$ por unidad por año", "in", "#,##0.0000"),
        R("H", "H usado en los cálculos", '=IF(ISNUMBER({Hd}),{Hd},N({I})*N({C}))', "$ por unidad por año", "calc", "#,##0.0000",
          '=IF(ISNUMBER({Hd}),"Se usa el H dado","Se usa H = I·C")'),
    ]


def generar(ruta):
    wb = libro()

    # ------------------------------------------------------------------ EOQ básico
    ws = hoja(wb, "EOQ", "Inventarios · Cantidad económica de pedido (EOQ básico)",
              "Basado en la plantilla del curso. Ejemplo: D = 1200 u/año, S = $20, H = $0.30, C = $20, 240 días, L = 5 días.")
    f = ["Datos",
         R("D", "Demanda (D)", 1200, "unidades por año", "in", "#,##0.##"),
         R("S", "Costo de ordenar (S)", 20, "$ por orden", "in", "#,##0.00"),
         *_H()[:0],
         R("C", "Costo unitario del artículo (C)", 20, "$ por unidad", "in", "#,##0.00"),
         R("I", "Tasa de costo de mantener (I)", None, "% anual del costo", "in", "0.00%"),
         R("Hd", "Costo de mantener H (directo)", 0.3, "$ por unidad por año", "in", "#,##0.0000"),
         R("H", "H usado en los cálculos", '=IF(ISNUMBER({Hd}),{Hd},N({I})*N({C}))', "$ por unidad por año", "calc", "#,##0.0000",
           '=IF(ISNUMBER({Hd}),"Se usa el H dado","Se usa H = I·C")'),
         R("dias", "Días hábiles por año", 240, "días", "in", "0"),
         R("LT", "Tiempo de entrega (L)", 5, "días", "in", "0.##"),
         R("Qu", "Cantidad a evaluar (opcional, Q propuesta)", 500, "unidades", "in", "#,##0.##"),
         "Resultados",
         R("Q", "Cantidad óptima de pedido Q* = √(2DS/H)", "=SQRT(2*{D}*{S}/{H})", "unidades", "res", "#,##0.00",
           '="Se deben pedir "&ROUND({Q},2)&" unidades por orden"'),
         R("N", "Número esperado de órdenes N = D/Q*", "={D}/{Q}", "órdenes por año", "res", "#,##0.00",
           '="Se realizan "&ROUND({N},2)&" órdenes al año"'),
         R("T", "Tiempo entre órdenes T = días/N", "={dias}/{N}", "días", "res", "#,##0.00",
           '="El tiempo entre órdenes es de "&ROUND({T},2)&" días"'),
         R("d", "Demanda diaria d = D/días", "={D}/{dias}", "unidades por día", "calc", "#,##0.00"),
         R("ROP", "Punto de reorden R = d·L", "={d}*{LT}", "unidades", "res", "#,##0.00",
           '="Cuando el inventario baje a "&ROUND({ROP},2)&" unidades, colocar una nueva orden"'),
         R("Imax", "Inventario máximo = Q*", "={Q}", "unidades", "calc", "#,##0.00"),
         R("Iprom", "Inventario promedio = Q*/2", "={Q}/2", "unidades", "calc", "#,##0.00"),
         R("CO", "Costo anual de ordenar = (D/Q)·S", "={D}/{Q}*{S}", "$ por año", "calc", "$#,##0.00"),
         R("CM", "Costo anual de mantener = (Q/2)·H", "={Q}/2*{H}", "$ por año", "calc", "$#,##0.00"),
         R("CTI", "Costo total de inventario = CO + CM", "={CO}+{CM}", "$ por año", "res", "$#,##0.00",
           '="Costo anual de ordenar + mantener: $"&TEXT({CTI},"#,##0.00")'),
         R("CC", "Costo de compra = C·D", "=N({C})*{D}", "$ por año", "calc", "$#,##0.00"),
         R("CT", "Costo total incluyendo compra", "={CTI}+{CC}", "$ por año", "res", "$#,##0.00"),
         "Evaluar la Q propuesta",
         R("CTu", "Costo ordenar + mantener con la Q propuesta", "={D}/{Qu}*{S}+{Qu}/2*{H}", "$ por año", "calc", "$#,##0.00",
           '="Pedir "&{Qu}&" cuesta $"&TEXT({CTu}-{CTI},"#,##0.00")&" más al año que el óptimo"'),
         ]
    rf = bloque(ws, 4, f)
    # tabla para gráfica
    seccion(ws, "F4", "Datos para la gráfica de costos")
    head(ws, 5, 6, ["Q", "Costo ordenar", "Costo mantener", "Costo total"])
    for k in range(15):
        r = 6 + k
        calc(ws, f"F{r}", f"={rf['Q']}*{(k + 1) / 7.5:.6f}", "#,##0")
        calc(ws, f"G{r}", f"={rf['D']}/F{r}*{rf['S']}", "#,##0.00")
        calc(ws, f"H{r}", f"=F{r}/2*{rf['H']}", "#,##0.00")
        calc(ws, f"I{r}", f"=G{r}+H{r}", "#,##0.00")
    ch = LineChart()
    ch.title = "Costos vs tamaño de lote"
    ch.y_axis.title = "$ por año"
    ch.x_axis.title = "Q"
    ch.add_data(Reference(ws, min_col=7, min_row=5, max_col=9, max_row=20), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=6, min_row=6, max_row=20))
    ch.roundedCorners = False
    ch.legend.overlay = False
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.height, ch.width = 8, 16
    ws.add_chart(ch, "F23")
    anchos(ws, {"A": 46, "B": 14, "C": 20, "D": 66, "E": 3, "F": 10, "G": 14, "H": 14, "I": 14})

    # ------------------------------------------------------------------ EOQ con faltantes
    ws = hoja(wb, "EOQ faltantes", "Inventarios · EOQ con faltantes planeados (pedidos pendientes / backorders)",
              "Ejemplo (Anderson, Higley Radio): D = 2000, S = $25, H = $10 (20% de $50), costo de faltante B = $30 por unidad por año.")
    f = ["Datos",
         R("D", "Demanda (D)", 2000, "unidades por año", "in", "#,##0.##"),
         R("S", "Costo de ordenar (S)", 25, "$ por orden", "in", "#,##0.00"),
         R("C", "Costo unitario del artículo (C)", 50, "$ por unidad", "in", "#,##0.00"),
         R("I", "Tasa de costo de mantener (I)", 0.2, "% anual del costo", "in", "0.00%"),
         R("Hd", "Costo de mantener H (directo)", None, "$ por unidad por año", "in", "#,##0.0000"),
         R("H", "H usado en los cálculos", '=IF(ISNUMBER({Hd}),{Hd},N({I})*N({C}))', "$ por unidad por año", "calc", "#,##0.0000"),
         R("B", "Costo de faltante (B / Cb)", 30, "$ por unidad faltante por año", "in", "#,##0.00"),
         R("dias", "Días hábiles por año", 250, "días", "in", "0"),
         R("LT", "Tiempo de entrega (L)", 5, "días", "in", "0.##"),
         "Resultados",
         R("Q", "Q* = √(2DS/H · (H+B)/B)", "=SQRT(2*{D}*{S}/{H}*({H}+{B})/{B})", "unidades", "res", "#,##0.00",
           '="Se deben pedir "&ROUND({Q},2)&" unidades por orden"'),
         R("Sf", "Faltante máximo S* = Q*·H/(H+B)", "={Q}*{H}/({H}+{B})", "unidades", "res", "#,##0.00",
           '="Se permite acumular hasta "&ROUND({Sf},2)&" unidades pendientes"'),
         R("Imax", "Inventario máximo = Q* − S*", "={Q}-{Sf}", "unidades", "res", "#,##0.00"),
         R("N", "Número de órdenes N = D/Q*", "={D}/{Q}", "órdenes por año", "calc", "#,##0.00"),
         R("T", "Tiempo de ciclo T = días·Q*/D", "={dias}*{Q}/{D}", "días", "calc", "#,##0.00"),
         R("fr", "Fracción del ciclo con faltante = S*/Q*", "={Sf}/{Q}", "", "calc", "0.00%"),
         R("ROP", "Punto de reorden = d·L − S*", "={D}/{dias}*{LT}-{Sf}", "unidades", "res", "#,##0.00",
           '=IF({ROP}<0,"Reordenar cuando haya "&ROUND(-{ROP},2)&" unidades pendientes","Reordenar con "&ROUND({ROP},2)&" unidades en inventario")'),
         R("CO", "Costo de ordenar = (D/Q)·S", "={D}/{Q}*{S}", "$ por año", "calc", "$#,##0.00"),
         R("CM", "Costo de mantener = (Q−S)²/(2Q)·H", "=({Q}-{Sf})^2/(2*{Q})*{H}", "$ por año", "calc", "$#,##0.00"),
         R("CF", "Costo de faltante = S²/(2Q)·B", "={Sf}^2/(2*{Q})*{B}", "$ por año", "calc", "$#,##0.00"),
         R("CT", "Costo total = CO + CM + CF", "={CO}+{CM}+{CF}", "$ por año", "res", "$#,##0.00",
           '="Costo anual total de inventario: $"&TEXT({CT},"#,##0.00")'),
         R("CTe", "Comparación: costo con EOQ sin faltantes", "=SQRT(2*{D}*{S}*{H})", "$ por año", "calc", "$#,##0.00"),
         ]
    bloque(ws, 4, f)
    anchos(ws, {"A": 46, "B": 14, "C": 26, "D": 66})

    # ------------------------------------------------------------------ Descuentos por cantidad
    ws = hoja(wb, "Descuentos", "Inventarios · EOQ con descuentos por cantidad",
              "Ejemplo (Render, Brass Department Store): D = 5000, S = $49, I = 20%. Precios: 0–999 $5.00, 1000–1999 $4.80, ≥2000 $4.75.")
    f = ["Datos",
         R("D", "Demanda (D)", 5000, "unidades por año", "in", "#,##0.##"),
         R("S", "Costo de ordenar (S)", 49, "$ por orden", "in", "#,##0.00"),
         R("I", "Tasa de costo de mantener (I)", 0.2, "% anual del precio", "in", "0.00%"),
         R("Hf", "H fijo (solo si NO depende del precio)", None, "$ por unidad por año", "in", "#,##0.0000"),
         R("dias", "Días hábiles por año", 250, "días", "in", "0"),
         R("LT", "Tiempo de entrega (L)", 0, "días", "in", "0.##"),
         ]
    rf = bloque(ws, 4, f)
    seccion(ws, "A13", "Rangos de precio (deja vacío 'Hasta' en el último rango)")
    head(ws, 14, 1, ["Rango", "Desde", "Hasta", "Precio unitario", "H del rango", "Q* del rango", "Q ajustada", "Costo ordenar",
                     "Costo mantener", "Costo compra", "Costo total", "Estado"])
    rangos = [(0, 999, 5), (1000, 1999, 4.8), (2000, None, 4.75)]
    D, S, I, Hf = rf["D"], rf["S"], rf["I"], rf["Hf"]
    for k in range(6):
        r = 15 + k
        calc(ws, f"A{r}", k + 1, "0", center=True)
        v = rangos[k] if k < len(rangos) else (None, None, None)
        inp(ws, f"B{r}", v[0], "#,##0")
        inp(ws, f"C{r}", v[1], "#,##0")
        inp(ws, f"D{r}", v[2], "#,##0.0000")
        ok = f"ISNUMBER(D{r})"
        calc(ws, f"E{r}", f'=IF({ok},IF(ISNUMBER({Hf}),{Hf},{I}*D{r}),"")', "#,##0.0000")
        calc(ws, f"F{r}", f'=IF({ok},SQRT(2*{D}*{S}/E{r}),"")', "#,##0.00")
        calc(ws, f"G{r}", f'=IF({ok},IF(F{r}<N(B{r}),N(B{r}),IF(AND(ISNUMBER(C{r}),F{r}>C{r}),"",F{r})),"")', "#,##0.00")
        okq = f"ISNUMBER(G{r})"
        calc(ws, f"H{r}", f'=IF({okq},{D}/G{r}*{S},"")', "$#,##0.00")
        calc(ws, f"I{r}", f'=IF({okq},G{r}/2*E{r},"")', "$#,##0.00")
        calc(ws, f"J{r}", f'=IF({okq},{D}*D{r},"")', "$#,##0.00")
        calc(ws, f"K{r}", f'=IF({okq},H{r}+I{r}+J{r},"")', "$#,##0.00")
        calc(ws, f"L{r}", f'=IF(NOT({ok}),"",IF(NOT({okq}),"Descartado (Q* > máximo)",IF(F{r}<N(B{r}),"Q ajustada al mínimo","Q* factible")))')
    ws.conditional_formatting.add("A15:L20", FormulaRule(formula=["AND(ISNUMBER($K15),$K15=MIN($K$15:$K$20))"],
                                                         fill=F_RES, font=Font(name=FONT, bold=True)))
    f = ["Mejor alternativa (menor costo total)",
         R("CT", "Costo total mínimo", "=MIN($K$15:$K$20)", "$ por año", "res", "$#,##0.00"),
         R("rg", "Rango elegido", "=MATCH({CT},$K$15:$K$20,0)", "", "res", "0"),
         R("Q", "Cantidad a ordenar Q", "=INDEX($G$15:$G$20,{rg})", "unidades", "res", "#,##0.00",
           '="Se deben pedir "&ROUND({Q},2)&" unidades a $"&INDEX($D$15:$D$20,{rg})&" c/u (rango "&{rg}&")"'),
         R("P", "Precio unitario", "=INDEX($D$15:$D$20,{rg})", "$", "calc", "#,##0.0000"),
         R("N", "Número de órdenes N = D/Q", "={D}/{Q}", "órdenes por año", "calc", "#,##0.00"),
         R("T", "Tiempo entre órdenes", "={dias}/{N}", "días", "calc", "#,##0.00"),
         R("ROP", "Punto de reorden = (D/días)·L", "={D}/{dias}*{LT}", "unidades", "calc", "#,##0.00"),
         ]
    bloque(ws, 23, f, ctx=rf)
    anchos(ws, {"A": 32, "B": 12, "C": 12, "D": 46, "E": 12, "F": 12, "G": 12, "H": 13, "I": 13, "J": 14, "K": 14, "L": 26})

    # ------------------------------------------------------------------ POQ
    ws = hoja(wb, "POQ", "Inventarios · Lote económico de producción (POQ / EPQ)",
              "Ejemplo: D = 10,000, S = $100, H = $0.50, p = 80/día, 250 días (d = 40/día).")
    f = ["Datos",
         R("D", "Demanda (D)", 10000, "unidades por año", "in", "#,##0.##"),
         R("S", "Costo de preparación / ordenar (S)", 100, "$ por corrida", "in", "#,##0.00"),
         R("C", "Costo unitario del artículo (C)", None, "$ por unidad", "in", "#,##0.00"),
         R("I", "Tasa de costo de mantener (I)", None, "% anual del costo", "in", "0.00%"),
         R("Hd", "Costo de mantener H (directo)", 0.5, "$ por unidad por año", "in", "#,##0.0000"),
         R("H", "H usado en los cálculos", '=IF(ISNUMBER({Hd}),{Hd},N({I})*N({C}))', "$ por unidad por año", "calc", "#,##0.0000"),
         R("dias", "Días hábiles por año", 250, "días", "in", "0"),
         R("p", "Tasa de producción (p)", 80, "unidades por día", "in", "#,##0.##"),
         R("dd", "Tasa de demanda diaria (d) (vacío = D/días)", None, "unidades por día", "in", "#,##0.##"),
         R("d", "d usada", "=IF(ISNUMBER({dd}),{dd},{D}/{dias})", "unidades por día", "calc", "#,##0.00"),
         R("LT", "Tiempo de entrega / preparación (L)", 3, "días", "in", "0.##"),
         "Resultados",
         R("Q", "Q* = √(2DS / (H(1 − d/p)))", "=SQRT(2*{D}*{S}/({H}*(1-{d}/{p})))", "unidades", "res", "#,##0.00",
           '="Se deben producir "&ROUND({Q},2)&" unidades por corrida"'),
         R("Imax", "Inventario máximo = Q(1 − d/p)", "={Q}*(1-{d}/{p})", "unidades", "res", "#,##0.00",
           '="El inventario máximo es de "&ROUND({Imax},2)&" unidades"'),
         R("t", "Tiempo de producción t = Q/p", "={Q}/{p}", "días", "res", "#,##0.00",
           '="Cada corrida dura "&ROUND({t},2)&" días"'),
         R("T", "Tiempo de ciclo T = Q/d", "={Q}/{d}", "días", "res", "#,##0.00",
           '="Entre una corrida y otra pasan "&ROUND({T},2)&" días"'),
         R("Tt", "Tiempo sólo de consumo T − t", "={T}-{t}", "días", "calc", "#,##0.00"),
         R("N", "Corridas por año N = D/Q", "={D}/{Q}", "corridas", "calc", "#,##0.00"),
         R("ROP", "Punto de reorden = d·L", "={d}*{LT}", "unidades", "calc", "#,##0.00"),
         R("CO", "Costo anual de preparación = (D/Q)·S", "={D}/{Q}*{S}", "$ por año", "calc", "$#,##0.00"),
         R("CM", "Costo anual de mantener = (Imax/2)·H", "={Imax}/2*{H}", "$ por año", "calc", "$#,##0.00"),
         R("CT", "Costo total = CO + CM", "={CO}+{CM}", "$ por año", "res", "$#,##0.00",
           '="Costo anual total: $"&TEXT({CT},"#,##0.00")'),
         ]
    rf = bloque(ws, 4, f)
    marcar_rojo(ws, rf["d"].replace("$", ""), f"{rf['d']}>={rf['p']}")
    anchos(ws, {"A": 46, "B": 14, "C": 22, "D": 66})

    # ------------------------------------------------------------------ Revisión continua (probabilístico)
    ws = hoja(wb, "Revision continua", "Inventarios probabilísticos · Sistema de revisión continua (Q, R) con inventario de seguridad",
              "Basado en la plantilla del curso. Usa las MISMAS unidades de tiempo en d, σ y LT (ej. todo en semanas). Periodos por año: 52 si es semanal, 365/días hábiles si es diario.")
    casos = [
        ("Caso 1: demanda variable, tiempo de entrega constante", dict(d=60, sd=15, LT=2, sLT=None, per=52, S=145, C=240, I=None, H=36, ns=0.9), 1),
        ("Caso 2: demanda constante, tiempo de entrega variable", dict(d=20, sd=None, LT=10, sLT=4, per=52, S=130, C=240, I=0.12, H=None, ns=0.98), 6),
        ("Caso 3: demanda y tiempo de entrega variables", dict(d=200, sd=20, LT=18, sLT=8, per=52, S=120, C=240, I=0.15, H=None, ns=0.95), 11),
    ]
    for t, v, col in casos:
        caso = col // 5 + 1
        filas = [t,
                 R("d", "Demanda promedio por periodo (d)", v["d"], "unidades/periodo", "in", "#,##0.##"),
                 ]
        if caso in (1, 3):
            filas.append(R("sd", "Desviación estándar de la demanda (σd)", v["sd"], "unidades/periodo", "in", "#,##0.##"))
        filas.append(R("LT", "Tiempo de entrega promedio (LT)", v["LT"], "periodos", "in", "#,##0.##"))
        if caso in (2, 3):
            filas.append(R("sLT", "Desviación estándar del LT (σLT)", v["sLT"], "periodos", "in", "#,##0.##"))
        sig = {1: "{sd}*SQRT({LT})", 2: "{d}*{sLT}", 3: "SQRT({LT}*{sd}^2+{d}^2*{sLT}^2)"}[caso]
        sig_t = {1: "σ_LT = σd·√LT", 2: "σ_LT = d·σLT", 3: "σ_LT = √(LT·σd² + d²·σLT²)"}[caso]
        filas += [
            R("per", "Periodos por año", v["per"], "52 = semanas", "in", "0.##"),
            R("Da", "Demanda anual D = d·periodos", "={d}*{per}", "unidades/año", "calc", "#,##0.##"),
            R("S", "Costo de ordenar (S)", v["S"], "$ por orden", "in", "#,##0.00"),
            R("C", "Costo unitario (C)", v["C"], "$ por unidad", "in", "#,##0.00"),
            R("I", "Tasa de mantener (I)", v["I"], "% anual", "in", "0.00%"),
            R("Hd", "H directo (opcional)", v["H"], "$/unidad/año", "in", "#,##0.00"),
            R("H", "H usado", '=IF(ISNUMBER({Hd}),{Hd},N({I})*N({C}))', "$/unidad/año", "calc", "#,##0.00"),
            R("ns", "Nivel de servicio", v["ns"], "probabilidad de no faltante", "in", "0.00%"),
            "Resultados",
            R("Z", "Z = DISTR.NORM.ESTAND.INV(nivel)", "=NORMSINV({ns})", "", "calc", "0.0000"),
            R("sg", sig_t, "=" + sig, "unidades", "calc", "#,##0.0000"),
            R("SS", "Inventario de seguridad SS = Z·σ_LT", "={Z}*{sg}", "unidades", "res", "#,##0.00",
              '="Con nivel de servicio de "&TEXT({ns},"0%")&" el inventario de seguridad es "&ROUND({SS},2)'),
            R("ROP", "Punto de reorden R = d·LT + SS", "={d}*{LT}+{SS}", "unidades", "res", "#,##0.00",
              '="Ordenar cuando el inventario llegue a "&ROUND({ROP},2)&" unidades"'),
            R("Q", "Q* = √(2DS/H)", "=SQRT(2*{Da}*{S}/{H})", "unidades", "res", "#,##0.00",
              '="Pedir "&ROUND({Q},2)&" unidades cada vez"'),
            R("N", "Órdenes por año N = D/Q", "={Da}/{Q}", "órdenes", "calc", "#,##0.00"),
            R("CO", "Costo de ordenar = (D/Q)·S", "={Da}/{Q}*{S}", "$ por año", "calc", "$#,##0.00"),
            R("CM", "Costo de mantener ciclo = (Q/2)·H", "={Q}/2*{H}", "$ por año", "calc", "$#,##0.00"),
            R("CS", "Costo de mantener SS = SS·H", "={SS}*{H}", "$ por año", "calc", "$#,##0.00"),
            R("CT", "Costo total = CO + CM + CS", "={CO}+{CM}+{CS}", "$ por año", "res", "$#,##0.00"),
            "Si te dan SS o R: ¿qué nivel de servicio implica?",
            R("SSd", "SS dado (o calcula R − d·LT)", None, "unidades", "in", "#,##0.00"),
            R("nsd", "Nivel de servicio implícito = Φ(SS/σ_LT)", '=IF(ISNUMBER({SSd}),NORMSDIST({SSd}/{sg}),"")', "", "calc", "0.00%"),
        ]
        bloque(ws, 4, filas, col=col if col == 1 else col, encabezado=("Concepto", "Valor", "Unidad", "Interpretación"))
    anchos(ws, {"A": 38, "B": 12, "C": 18, "D": 40, "E": 2, "F": 38, "G": 12, "H": 18, "I": 40, "J": 2, "K": 38, "L": 12, "M": 18, "N": 40})

    # ------------------------------------------------------------------ Revisión periódica
    ws = hoja(wb, "Revision periodica", "Inventarios probabilísticos · Sistema de revisión periódica (P) con nivel objetivo",
              "Cada R periodos se revisa el inventario y se pide lo necesario para llegar al nivel objetivo T.")
    f = ["Datos",
         R("d", "Demanda promedio por periodo (d)", 20, "unidades/periodo", "in", "#,##0.##"),
         R("sd", "Desviación estándar de la demanda por periodo (σd)", 5, "unidades/periodo", "in", "#,##0.##"),
         R("Rv", "Periodo de revisión (R)", 10, "periodos", "in", "#,##0.##"),
         R("LT", "Tiempo de entrega (L)", 3, "periodos", "in", "#,##0.##"),
         R("ns", "Nivel de servicio", 0.95, "", "in", "0.00%"),
         R("Ia", "Inventario disponible al revisar", 75, "unidades", "in", "#,##0.##"),
         "Resultados",
         R("Z", "Z", "=NORMSINV({ns})", "", "calc", "0.0000"),
         R("sg", "σ(R+L) = σd·√(R+L)", "={sd}*SQRT({Rv}+{LT})", "unidades", "calc", "#,##0.0000"),
         R("SS", "Inventario de seguridad = Z·σd·√(R+L)", "={Z}*{sg}", "unidades", "res", "#,##0.00"),
         R("T", "Nivel objetivo T = d(R+L) + SS", "={d}*({Rv}+{LT})+{SS}", "unidades", "res", "#,##0.00",
           '="Nivel máximo/objetivo: "&ROUND({T},2)&" unidades"'),
         R("q", "Cantidad a pedir = T − inventario disponible", "=MAX(0,{T}-{Ia})", "unidades", "res", "#,##0.00",
           '="En esta revisión hay que pedir "&ROUND({q},2)&" unidades"'),
         ]
    bloque(ws, 4, f)
    anchos(ws, {"A": 50, "B": 14, "C": 20, "D": 60})

    # ------------------------------------------------------------------ Un solo periodo
    ws = hoja(wb, "Un periodo", "Inventarios probabilísticos · Modelo de un solo periodo (vendedor de periódicos)",
              "Ejemplo (Anderson, Johnson Shoe): costo $40, precio $60, remate $30, demanda normal μ = 500, σ = 100.")
    f = ["Datos",
         R("pv", "Precio de venta", 60, "$ por unidad", "in", "#,##0.00"),
         R("c", "Costo", 40, "$ por unidad", "in", "#,##0.00"),
         R("v", "Valor de rescate / remate", 30, "$ por unidad", "in", "#,##0.00"),
         R("cud", "Cu directo (opcional: costo de faltante)", None, "$ por unidad", "in", "#,##0.00"),
         R("cod", "Co directo (opcional: costo de exceso)", None, "$ por unidad", "in", "#,##0.00"),
         R("cu", "Cu = precio − costo", "=IF(ISNUMBER({cud}),{cud},{pv}-{c})", "$ por unidad", "calc", "#,##0.00"),
         R("co", "Co = costo − rescate", "=IF(ISNUMBER({cod}),{cod},{c}-{v})", "$ por unidad", "calc", "#,##0.00"),
         R("P", "Razón crítica P(D ≤ Q*) = Cu/(Cu + Co)", "={cu}/({cu}+{co})", "", "res", "0.0000",
           '="Pedir de modo que la probabilidad de no faltante sea "&TEXT({P},"0.00%")'),
         "Demanda normal",
         R("mu", "Media de la demanda μ", 500, "unidades", "in", "#,##0.##"),
         R("sg", "Desviación estándar σ", 100, "unidades", "in", "#,##0.##"),
         R("z", "z = DISTR.NORM.ESTAND.INV(P)", "=NORMSINV({P})", "", "calc", "0.0000"),
         R("Qn", "Q* = μ + z·σ", "={mu}+{z}*{sg}", "unidades", "res", "#,##0.00",
           '="Pedir "&ROUND({Qn},0)&" unidades"'),
         "Demanda uniforme",
         R("a", "Mínimo a", 350, "unidades", "in", "#,##0.##"),
         R("b", "Máximo b", 650, "unidades", "in", "#,##0.##"),
         R("Qu", "Q* = a + P·(b − a)", "={a}+{P}*({b}-{a})", "unidades", "res", "#,##0.00"),
         "Demanda discreta (llena la tabla de la derecha)",
         R("Qd", "Q* = menor demanda con prob. acumulada ≥ P", "=IFERROR(INDEX($F$6:$F$25,MATCH(TRUE,INDEX($I$6:$I$25>={P}-0.0000001,0),0)),\"Revisa la tabla\")", "unidades", "res", "#,##0.##"),
         ]
    rf = bloque(ws, 4, f)
    seccion(ws, "F4", "Demanda discreta")
    head(ws, 5, 6, ["Demanda", "Probabilidad", "¿≥ P?", "Prob. acumulada"])
    arr(ws, rf["Qd"], f'=IFERROR(INDEX($F$6:$F$25,MATCH(1,ISNUMBER($I$6:$I$25)*($I$6:$I$25>={rf["P"]}-0.0000001),0)),"Revisa la tabla")', "#,##0.##", res=True)
    disc = [(20, 0.1), (21, 0.15), (22, 0.25), (23, 0.3), (24, 0.15), (25, 0.05)]
    for k in range(20):
        r = 6 + k
        v = disc[k] if k < len(disc) else (None, None)
        inp(ws, f"F{r}", v[0], "#,##0.##")
        inp(ws, f"G{r}", v[1], "0.0000")
        calc(ws, f"I{r}", f'=IF(ISNUMBER(F{r}),SUM($G$6:G{r}),"")', "0.0000")
        calc(ws, f"H{r}", f'=IF(ISNUMBER(F{r}),IF(I{r}>={rf["P"]}-0.0000001,"Sí","No"),"")', center=True)
    calc(ws, "F26", "Suma", bold=True)
    calc(ws, "G26", "=SUM(G6:G25)", "0.0000")
    marcar_rojo(ws, "G26", "ABS(G26-1)>0.000001")
    nota(ws, "F27", "Ordena las demandas de menor a mayor. Ejemplo discreto: costo de exceso/faltante del mismo producto.")
    anchos(ws, {"A": 46, "B": 14, "C": 16, "D": 50, "E": 3, "F": 12, "G": 13, "H": 10, "I": 15})

    inicio(wb, "Solucionador · Modelos de inventario",
           "Modelos determinísticos (EOQ, EOQ con faltantes, descuentos por cantidad, POQ) y probabilísticos (revisión continua con "
           "inventario de seguridad, revisión periódica, un solo periodo). Cada hoja calcula Q*, punto de reorden, tiempos y costos.",
           [("EOQ", "EOQ clásico: Q*, N, T, punto de reorden, costos y gráfica."),
            ("EOQ faltantes", "EOQ con faltantes planeados (backorders)."),
            ("Descuentos", "EOQ con descuentos por cantidad (hasta 6 rangos), elige el de menor costo total."),
            ("POQ", "Lote económico de producción (tasa de producción p > d)."),
            ("Revision continua", "Inventario de seguridad, ROP y Q: 3 casos (demanda y/o LT variables)."),
            ("Revision periodica", "Nivel objetivo T y cantidad a pedir en cada revisión."),
            ("Un periodo", "Vendedor de periódicos: razón crítica con demanda normal, uniforme o discreta."),
            ("Formulario", "Fórmulas del tema.")])
    formulario(wb, "Formulario · Inventarios", [
        ("EOQ básico", [
            ("Cantidad óptima", "Q* = √(2DS/H) ;  H = I·C"),
            ("Órdenes y tiempos", "N = D/Q* ;  T = días/N ;  d = D/días ;  ROP = d·L"),
            ("Costo total", "CT = (D/Q)S + (Q/2)H + C·D"),
        ]),
        ("EOQ con faltantes planeados", [
            ("Q* y faltante máximo", "Q* = √(2DS/H · (H+B)/B) ;  S* = Q*·H/(H+B)"),
            ("Costo total", "CT = (D/Q)S + (Q−S)²/(2Q)·H + S²/(2Q)·B"),
        ]),
        ("Descuentos por cantidad", [
            ("Procedimiento", "1) Q* de cada precio con H = I·Cᵢ  2) si Q* < mínimo → usar mínimo; si Q* > máximo → descartar  3) CT con compra, elegir el menor"),
            ("Costo total", "CT = (D/Q)S + (Q/2)·I·Cᵢ + Cᵢ·D"),
        ]),
        ("POQ / EPQ", [
            ("Q*", "Q* = √(2DS / (H(1 − d/p)))"),
            ("Inventario máximo", "Imax = Q(1 − d/p) ;  t = Q/p ;  T = Q/d"),
            ("Costo total", "CT = (D/Q)S + (Imax/2)H"),
        ]),
        ("Revisión continua (probabilístico)", [
            ("Punto de reorden", "ROP = d·LT + Z·σ_LT ;  SS = Z·σ_LT ;  Z = NORMSINV(nivel de servicio)"),
            ("Demanda variable, LT constante", "σ_LT = σd·√LT"),
            ("Demanda constante, LT variable", "σ_LT = d·σLT"),
            ("Ambos variables", "σ_LT = √(LT·σd² + d²·σLT²)"),
            ("Costo total", "CT = (D/Q)S + (Q/2)H + SS·H"),
        ]),
        ("Revisión periódica", [
            ("Nivel objetivo", "T = d(R + L) + Z·σd·√(R + L) ;  pedido = T − inventario disponible"),
        ]),
        ("Un solo periodo", [
            ("Razón crítica", "P(D ≤ Q*) = Cu/(Cu + Co) ;  Cu = precio − costo ;  Co = costo − rescate"),
            ("Normal / uniforme", "Q* = μ + z·σ ;  Q* = a + P(b − a)"),
        ]),
    ])
    wb.save(ruta)
