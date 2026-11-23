"""5_PERT_CPM.xlsx: CPM, PERT (probabilidad de terminación) y compresión (crashing) con Solver."""
from comun import *

NA = 30
R0 = 8               # primera fila de actividades
RL = R0 + NA - 1     # última fila
NG = 50              # columnas del Gantt

# Ejemplo: General Foundry (Render, Métodos cuantitativos para los negocios)
ACTS = [("A", "Construir componentes internos", "", 1, 2, 3, 2, 1, 22000, 23000),
        ("B", "Modificar techo y piso", "", 2, 3, 4, 3, 1, 30000, 34000),
        ("C", "Construir chimenea", "A", 1, 2, 3, 2, 1, 26000, 27000),
        ("D", "Vaciar concreto e instalar estructura", "B", 2, 4, 6, 4, 3, 48000, 49000),
        ("E", "Construir horno de alta temperatura", "C", 1, 4, 7, 4, 2, 56000, 58000),
        ("F", "Instalar sistema de control", "C", 1, 2, 9, 3, 2, 30000, 30500),
        ("G", "Instalar dispositivo contra contaminación", "D,E", 3, 4, 11, 5, 2, 80000, 86000),
        ("H", "Inspección y pruebas", "F,G", 1, 2, 3, 2, 1, 16000, 19000)]


def cpm(ws, c):
    """Pasadas hacia adelante y atrás. c: dict de letras de columna:
    act, pred, dur, es, ef, ls, lf, hol, crit, clean, chk, cum. Devuelve referencia de la duración del proyecto."""
    A = lambda r: f"${c['act']}${r}"
    rng = lambda col, r1, r2: f"${c[col]}${r1}:${c[col]}${r2}"
    T = f"$B$5"
    for r in range(R0, RL + 1):
        act, pred, dur = A(r), f"${c['pred']}${r}", f"${c['dur']}{r}"
        calc(ws, f"{c['clean']}{r}", f'=IF(OR(TRIM({pred})="",TRIM({pred})="-"),",",","&SUBSTITUTE(SUBSTITUTE({pred}," ",""),";",",")&",")')
        cl = f"${c['clean']}{r}"
        if r == R0:
            calc(ws, f"{c['es']}{r}", 0, "0.##")
            calc(ws, f"{c['chk']}{r}", f'=IF({act}="","",IF({cl}=",","✓","⚠ la primera actividad no puede tener predecesoras"))', center=True)
        else:
            above = rng("act", R0, r - 1)
            efab = rng("ef", R0, r - 1)
            m = f"ISNUMBER(SEARCH(\",\"&{above}&\",\",{cl}))*({above}<>\"\")"
            arr(ws, f"{c['es']}{r}", f'=IF({act}="",0,MAX(0,MAX(IF({m},{efab},0))))', "0.##")
            arr(ws, f"{c['chk']}{r}",
                f'=IF({act}="","",IF(IF({cl}=",",0,LEN({cl})-LEN(SUBSTITUTE({cl},",",""))-1)=SUM({m}),"✓","⚠ predecesora no encontrada ARRIBA"))')
        calc(ws, f"{c['ef']}{r}", f'=IF({act}="",0,{c["es"]}{r}+N({dur}))', "0.##")
        if r == RL:
            calc(ws, f"{c['lf']}{r}", f'=IF({act}="",0,{T})', "0.##")
        else:
            below = rng("act", r + 1, RL)
            clb = rng("clean", r + 1, RL)
            lsb = rng("ls", r + 1, RL)
            m = f"ISNUMBER(SEARCH(\",\"&{act}&\",\",{clb}))*({below}<>\"\")"
            arr(ws, f"{c['lf']}{r}", f'=IF({act}="",0,IF(SUM({m})=0,{T},MIN(IF({m},{lsb},1E+99))))', "0.##")
        calc(ws, f"{c['ls']}{r}", f'=IF({act}="",0,{c["lf"]}{r}-N({dur}))', "0.##")
        calc(ws, f"{c['hol']}{r}", f'=IF({act}="",0,{c["ls"]}{r}-{c["es"]}{r})', "0.##")
        calc(ws, f"{c['crit']}{r}", f'=IF({act}="","",IF(ABS({c["hol"]}{r})<0.000001,"Sí","No"))', center=True)
        prev = f"{c['cum']}{r - 1}" if r > R0 else '""'
        calc(ws, f"{c['cum']}{r}", f'={prev}&IF({c["crit"]}{r}="Sí",IF({prev}="",""," → ")&{act},"")')
    marcar_rojo(ws, f"{c['chk']}{R0}:{c['chk']}{RL}", f'LEFT({c["chk"]}{R0},1)="⚠"')
    ws.conditional_formatting.add(f"{c['crit']}{R0}:{c['crit']}{RL}", FormulaRule(formula=[f'{c["crit"]}{R0}="Sí"'], fill=F_ROJO,
                                                                                   font=Font(name=FONT, bold=True, color="9C0006")))
    # ocultar ceros de filas vacías
    ws.conditional_formatting.add(f"{c['es']}{R0}:{c['hol']}{RL}", FormulaRule(formula=[f'${c["act"]}{R0}=""'], font=Font(color="F2F2F2")))
    calc(ws, "B5", f"=MAX({rng('ef', R0, RL)})", "0.##", res=True)


def gantt(ws, c, col0):
    """Diagrama de Gantt con formato condicional a partir de la columna col0."""
    seccion(ws, f"{CL(col0)}5", "Diagrama de Gantt (rojo = crítica)")
    label(ws, f"{CL(col0)}6", "Escala (unidades por columna):", size=9)
    calc(ws, f"{CL(col0 + 6)}6", f"=MAX(1,CEILING($B$5/{NG},1))", "0")
    sc = f"${CL(col0 + 6)}$6"
    for k in range(NG):
        col = CL(col0 + k)
        calc(ws, f"{col}7", f"={k + 1}*{sc}", "0", center=True)
        ws.column_dimensions[col].width = 3.2
        ws[f"{col}7"].font = Font(name=FONT, size=7)
    rng = f"{CL(col0)}{R0}:{CL(col0 + NG - 1)}{RL}"
    f0 = CL(col0)
    base = f'AND(${c["act"]}{R0}<>"",${c["es"]}{R0}<{f0}$7,${c["ef"]}{R0}>{f0}$7-{sc})'
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND({base},${c["crit"]}{R0}="Sí")'], fill=PatternFill("solid", fgColor="C00000"), stopIfTrue=True))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[base], fill=PatternFill("solid", fgColor="5B9BD5")))
    for r in range(R0, RL + 1):
        for k in range(NG):
            ws.cell(r, col0 + k).border = Border(left=Side(style="hair", color="D9D9D9"))


def _cabecera(ws, titulo_dur):
    label(ws, "A4", "Instrucciones:", bold=True)
    nota(ws, "B4", "Escribe cada actividad con sus predecesoras separadas por coma (ej. D,E). Una actividad debe ir DEBAJO de todas sus predecesoras.")
    label(ws, "A5", "Duración del proyecto:", bold=True)


def generar(ruta):
    wb = libro()

    # ================================================================== CPM
    ws = hoja(wb, "CPM", "PERT/CPM · Método de la ruta crítica (tiempos determinísticos)",
              "Ejemplo: General Foundry (Render). Duración = 15 semanas, ruta crítica A → C → E → G → H.")
    _cabecera(ws, "Duración")
    head(ws, R0 - 1, 1, ["Actividad", "Descripción", "Predecesoras", "Duración", "ES (inicio temprano)", "EF (fin temprano)",
                          "LS (inicio tardío)", "LF (fin tardío)", "Holgura", "¿Crítica?", "Revisión"])
    for k in range(NA):
        r = R0 + k
        a = ACTS[k] if k < len(ACTS) else (None,) * 10
        inp(ws, f"A{r}", a[0], center=True)
        inp(ws, f"B{r}", a[1])
        inp(ws, f"C{r}", a[2], center=True)
        inp(ws, f"D{r}", a[6], "0.##")
    c = dict(act="A", pred="C", dur="D", es="E", ef="F", ls="G", lf="H", hol="I", crit="J", chk="K", clean="BN", cum="BO")
    cpm(ws, c)
    label(ws, "C5", "Ruta crítica:", bold=True)
    calc(ws, "D5", f"=BO{RL}", res=True)
    ws.merge_cells("D5:J5")
    calc(ws, "D6", '="El proyecto dura "&B5&" unidades de tiempo. Las actividades críticas (holgura 0) son: "&D5', bold=False)
    ws.merge_cells("D6:K6")
    gantt(ws, c, 13)
    label(ws, f"BN{R0 - 1}", "pred limpia", italic=True, color="808080")
    label(ws, f"BO{R0 - 1}", "acumulado crítica", italic=True, color="808080")
    nota(ws, f"A{RL + 2}", "Si hay varias rutas críticas, 'Ruta crítica' lista todas las actividades críticas en orden de captura.")
    anchos(ws, {"A": 22, "B": 36, "C": 13, "D": 10, "E": 11, "F": 11, "G": 11, "H": 11, "I": 9, "J": 9, "K": 30, "L": 2})

    # ================================================================== PERT
    ws = hoja(wb, "PERT", "PERT/CPM · PERT con tres estimaciones de tiempo y probabilidad de terminación",
              "tₑ = (a + 4m + b)/6, σ² = ((b − a)/6)². Ejemplo General Foundry: T = 15, σ² ruta = 3.11, P(T ≤ 16) ≈ 71.5%.")
    _cabecera(ws, "Duración esperada")
    head(ws, R0 - 1, 1, ["Actividad", "Predecesoras", "a (optimista)", "m (más probable)", "b (pesimista)", "tₑ esperado", "σ² varianza",
                          "ES", "EF", "LS", "LF", "Holgura", "¿Crítica?", "Revisión"])
    for k in range(NA):
        r = R0 + k
        a = ACTS[k] if k < len(ACTS) else (None,) * 10
        inp(ws, f"A{r}", a[0], center=True)
        inp(ws, f"B{r}", a[2], center=True)
        inp(ws, f"C{r}", a[3], "0.##")
        inp(ws, f"D{r}", a[4], "0.##")
        inp(ws, f"E{r}", a[5], "0.##")
        calc(ws, f"F{r}", f'=IF(A{r}="","",(N(C{r})+4*N(D{r})+N(E{r}))/6)', "0.00")
        calc(ws, f"G{r}", f'=IF(A{r}="","",((N(E{r})-N(C{r}))/6)^2)', "0.0000")
    c = dict(act="A", pred="B", dur="F", es="H", ef="I", ls="J", lf="K", hol="L", crit="M", chk="N", clean="BX", cum="BY")
    cpm(ws, c)
    label(ws, f"BX{R0 - 1}", "pred limpia", italic=True, color="808080")
    label(ws, f"BY{R0 - 1}", "acumulado crítica", italic=True, color="808080")
    label(ws, "C5", "Ruta crítica:", bold=True)
    calc(ws, "D5", f"=BY{RL}", res=True)
    ws.merge_cells("D5:G5")
    seccion(ws, "P3", "Probabilidad de terminación")
    f = [R("var", "Varianza de la ruta crítica Σσ²", f'=SUMIF($M${R0}:$M${RL},"Sí",$G${R0}:$G${RL})', "", "calc", "0.0000"),
         R("sg", "Desviación estándar σ", "=SQRT({var})", "", "calc", "0.0000"),
         R("To", "Fecha objetivo T", 16, "unidades de tiempo", "in", "0.##"),
         R("z", "Z = (T − tₑ proyecto)/σ", "=({To}-$B$5)/{sg}", "", "calc", "0.0000"),
         R("p", "P(terminar en ≤ T)", "=NORMSDIST({z})", "", "res", "0.00%",
           '="Probabilidad de terminar en "&{To}&" o menos: "&TEXT({p},"0.00%")'),
         R("pm", "P(terminar después de T)", "=1-{p}", "", "calc", "0.00%"),
         R("Tb", "Otra fecha T₂ (para P(T ≤ T₂) y P(T entre T y T₂))", 18, "", "in", "0.##"),
         R("p2", "P(terminar en ≤ T₂)", "=NORMSDIST(({Tb}-$B$5)/{sg})", "", "calc", "0.00%"),
         R("pb", "P(T ≤ tiempo ≤ T₂)", "=ABS({p2}-{p})", "", "calc", "0.00%"),
         R("pd", "Probabilidad deseada", 0.99, "", "in", "0.00%"),
         R("Td", "Fecha que garantiza esa probabilidad = tₑ + Z·σ", "=$B$5+NORMSINV({pd})*{sg}", "unidades de tiempo", "res", "0.00",
           '="Con "&TEXT({pd},"0%")&" de confianza el proyecto termina en "&ROUND({Td},2)'),
         ]
    bloque(ws, 4, f, col=16)
    nota(ws, "P17", "Si hay más de una ruta crítica, el libro suma la varianza de todas las críticas; usa la ruta con MAYOR varianza (revisa a mano).")
    gantt(ws, c, 22)
    anchos(ws, {"A": 22, "B": 13, "C": 10, "D": 10, "E": 10, "F": 10, "G": 10, "H": 8, "I": 8, "J": 8, "K": 8, "L": 8, "M": 9, "N": 28,
                "O": 2, "P": 44, "Q": 12, "R": 16, "S": 50, "T": 2, "U": 2})

    # ================================================================== Compresión (crashing)
    ws = hoja(wb, "Compresion", "PERT/CPM · Compresión de proyectos (crashing) con programación lineal",
              "Ejemplo General Foundry (Render, tabla 12.9): reducir de 15 a 12 semanas cuesta $5,000 (acelerar A 1 semana y G 2 semanas).")
    _cabecera(ws, "Duración normal")
    head(ws, R0 - 1, 1, ["Actividad", "Predecesoras", "Tiempo normal", "Tiempo acelerado", "Costo normal", "Costo acelerado",
                          "Reducción máxima", "Costo por unidad de reducción", "S inicio (variable)", "Y reducción (variable)",
                          "Fin = S + t − Y", "¿Y ≤ máx?", "¿Fin ≤ meta?", "Crítica (normal)"])
    for k in range(NA):
        r = R0 + k
        a = ACTS[k] if k < len(ACTS) else (None,) * 10
        inp(ws, f"A{r}", a[0], center=True)
        inp(ws, f"B{r}", a[2], center=True)
        inp(ws, f"C{r}", a[6], "0.##")
        inp(ws, f"D{r}", a[7], "0.##")
        inp(ws, f"E{r}", a[8], "$#,##0")
        inp(ws, f"F{r}", a[9], "$#,##0")
        calc(ws, f"G{r}", f'=IF(A{r}="",0,N(C{r})-N(D{r}))', "0.##")
        calc(ws, f"H{r}", f'=IF(OR(A{r}="",G{r}<=0),0,(N(F{r})-N(E{r}))/G{r})', "$#,##0.00")
    # solución óptima del ejemplo (Solver la recalcula si cambias datos)
    sol_S = dict(A=0, B=0, C=1, D=3, E=3, F=3, G=7, H=10)
    sol_Y = dict(A=1, G=2)
    for k in range(NA):
        r = R0 + k
        a = ACTS[k][0] if k < len(ACTS) else None
        for col, v in (("I", sol_S.get(a, 0)), ("J", sol_Y.get(a, 0))):
            inp(ws, f"{col}{r}", v, "0.##")
            ws[f"{col}{r}"].fill = F_RES
        calc(ws, f"K{r}", f"=I{r}+N(C{r})-J{r}", "0.##")
        calc(ws, f"L{r}", f'=IF(A{r}="","",IF(AND(J{r}>=-0.000001,J{r}<=G{r}+0.000001),"✓","⚠"))', center=True)
        calc(ws, f"M{r}", f'=IF(A{r}="","",IF(K{r}<=$Q$6+0.000001,"✓","⚠"))', center=True)
    c = dict(act="A", pred="B", dur="C", es="BA", ef="BB", ls="BC", lf="BD", hol="BE", crit="N", chk="BF", clean="BG", cum="BH")
    cpm(ws, c)
    for k, t in enumerate(["ES", "EF", "LS", "LF", "Holgura", "Revisión", "pred limpia", "acum"]):
        label(ws, f"{CL(53 + k)}{R0 - 1}", t, italic=True, color="808080")
    marcar_rojo(ws, f"L{R0}:M{RL}", f'L{R0}="⚠"')
    # matriz de precedencias: holgura[i][p] = M(i,p)·(S_i − Fin_p) ≥ 0
    PR = RL + 4
    seccion(ws, f"A{PR - 1}", "Restricciones de precedencia (interno): M(i,p)·(Sᵢ − Finₚ) ≥ 0 — fila i = actividad, columna p = predecesora")
    for p in range(NA):
        calc(ws, f"{CL(2 + p)}{PR}", f"=$A${R0 + p}", center=True, bold=True)
    for i in range(NA):
        r = PR + 1 + i
        calc(ws, f"A{r}", f"=$A${R0 + i}", center=True, bold=True)
        for p in range(NA):
            m = f'ISNUMBER(SEARCH(","&$A${R0 + p}&",",$BG${R0 + i}))*($A${R0 + p}<>"")*($A${R0 + i}<>"")'
            calc(ws, f"{CL(2 + p)}{r}", f"={m}*($I${R0 + i}-$K${R0 + p})", "0.##")
    PREC = f"$B${PR + 1}:${CL(1 + NA)}${PR + NA}"
    marcar_rojo(ws, PREC.replace("$", ""), f"B{PR + 1}<-0.000001")

    seccion(ws, "P3", "Modelo")
    f = [R("Tn", "Duración normal del proyecto", "=$B$5", "", "calc", "0.##"),
         R("Tm", "Duración meta (objetivo)", 12, "unidades de tiempo", "in", "0.##"),
         R("cc", "Costo de compresión (minimizar) = Σ costo unitario·Y", f"=SUMPRODUCT($H${R0}:$H${RL},$J${R0}:$J${RL})", "$", "res", "$#,##0.00",
           '="Comprimir a "&{Tm}&" cuesta $"&TEXT({cc},"#,##0.00")&" adicionales"'),
         R("cn", "Costo normal total", f"=SUM($E${R0}:$E${RL})", "$", "calc", "$#,##0.00"),
         R("ct", "Costo total del proyecto comprimido", "={cn}+{cc}", "$", "res", "$#,##0.00"),
         R("Tf", "Duración lograda = máx Fin", f"=MAX($K${R0}:$K${RL})", "", "calc", "0.##"),
         R("ok", "¿Solución factible?", f'=IF(AND(COUNTIF($L${R0}:$M${RL},"⚠")=0,MIN({PREC})>=-0.000001,MIN($I${R0}:$I${RL})>=0),"✓ Factible","⚠ No factible: corre Solver")', "", "res", "General"),
         ]
    bloque(ws, 4, f, col=16)
    marcar_rojo(ws, "Q11", 'LEFT($Q$11,1)="⚠"')
    seccion(ws, "P14", "Cómo resolver con Solver")
    pasos = [
        "1) Llena actividades, predecesoras, tiempos y costos (normal/acelerado) y la duración meta en Q6.",
        "2) EXCEL: Datos → Solver.  LIBREOFFICE: Herramientas → Solver.",
        "   • Objetivo: $Q$7  → Mín",
        f"   • Cambiando celdas: $I${R0}:$J${RL}",
        f"   • Restricciones:  $J${R0}:$J${RL} <= $G${R0}:$G${RL}   (no reducir más de lo posible)",
        f"                     $K${R0}:$K${RL} <= $Q$6   (todo termina antes de la meta)",
        f"                     {PREC} >= 0   (cada actividad empieza después de sus predecesoras)",
        "   • Variables no negativas, método Simplex LP / motor lineal → Resolver.",
        "Las celdas verdes de las columnas I y J son las variables; vienen con la solución del ejemplo.",
    ]
    for k, p in enumerate(pasos):
        label(ws, f"P{15 + k}", p, size=9)
    anchos(ws, {"A": 11, "B": 13, "C": 10, "D": 10, "E": 12, "F": 12, "G": 10, "H": 13, "I": 11, "J": 11, "K": 11, "L": 8, "M": 9, "N": 10,
                "O": 2, "P": 46, "Q": 13, "R": 12, "S": 46})

    inicio(wb, "Solucionador · PERT / CPM",
           "Pasadas hacia adelante y hacia atrás (ES, EF, LS, LF), holguras, ruta crítica y diagrama de Gantt automáticos (hasta 30 actividades). "
           "PERT con probabilidad de terminación y compresión de proyectos con Solver.",
           [("CPM", "Tiempos determinísticos: ES, EF, LS, LF, holgura, ruta crítica, Gantt."),
            ("PERT", "Tres estimaciones (a, m, b): tₑ, σ², ruta crítica, probabilidad de terminar en T."),
            ("Compresion", "Costo mínimo para reducir la duración (PL con Solver) y pendiente de costo."),
            ("Formulario", "Fórmulas del tema.")])
    formulario(wb, "Formulario · PERT / CPM", [
        ("CPM", [
            ("Pasada hacia adelante", "ES = máx(EF de las predecesoras) ;  EF = ES + t"),
            ("Pasada hacia atrás", "LF = mín(LS de las sucesoras) ;  LS = LF − t ;  (última: LF = duración del proyecto)"),
            ("Holgura", "Holgura = LS − ES = LF − EF ;  crítica si holgura = 0"),
            ("Ruta crítica", "Ruta más larga de la red; su longitud = duración del proyecto"),
        ]),
        ("PERT", [
            ("Tiempo esperado", "tₑ = (a + 4m + b) / 6"),
            ("Varianza", "σ² = ((b − a) / 6)²"),
            ("Proyecto", "T = Σ tₑ (ruta crítica) ;  σ²_T = Σ σ² (ruta crítica)"),
            ("Probabilidad", "Z = (fecha − T)/σ_T ;  P(terminar ≤ fecha) = Φ(Z) = NORMSDIST(Z)"),
        ]),
        ("Compresión (crashing)", [
            ("Costo por unidad de reducción", "(costo acelerado − costo normal) / (tiempo normal − tiempo acelerado)"),
            ("Regla manual", "Reduce la actividad crítica más barata, una unidad a la vez; revisa si aparecen nuevas rutas críticas."),
            ("PL", "Min Σ cᵢYᵢ ;  Sⱼ ≥ Sᵢ + tᵢ − Yᵢ (i predecesora de j) ;  Sᵢ + tᵢ − Yᵢ ≤ meta ;  0 ≤ Yᵢ ≤ máx reducciónᵢ"),
        ]),
    ])
    wb.save(ruta)
