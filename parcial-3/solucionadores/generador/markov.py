"""1_Markov.xlsx: n pasos, estado estable, tiempos de primer paso, cadenas absorbentes."""
from comun import *

M = 8  # máximo de estados


def _matriz_P(ws, r_names, c0, k_ref, nombres, P):
    """Escribe nombres (columna B) y matriz P de entrada a partir de (r_names, c0). Devuelve rangos."""
    head(ws, r_names - 1, 2, ["Estado"])
    for j in range(M):
        calc(ws, f"{CL(c0 + j)}{r_names - 1}", f'=IF({j + 1}<={k_ref},B{r_names + j},"")', center=True, bold=True)
    for i in range(M):
        r = r_names + i
        inp(ws, f"B{r}", nombres[i] if i < len(nombres) else None)
        for j in range(M):
            v = P[i][j] if i < len(P) and j < len(P) else None
            inp(ws, f"{CL(c0 + j)}{r}", v, "0.0000")
    return f"$B${r_names}:$B${r_names + M - 1}"


def generar(ruta):
    wb = libro()

    # ------------------------------------------------------------------ Matriz P / n pasos
    ws = hoja(wb, "Matriz P", "Cadenas de Markov · Matriz de transición y probabilidades en n pasos",
              "Escribe los nombres de los estados, la matriz P (cada FILA debe sumar 1), el vector inicial y n.")
    nombres = ["Tienda 1", "Tienda 2", "Tienda 3"]
    P = [[0.8, 0.1, 0.1], [0.1, 0.7, 0.2], [0.2, 0.2, 0.6]]
    label(ws, "A4", "Número de estados (k):", bold=True)
    inp(ws, "B4", 3, "0")
    entero(ws, "B4", 2, M)
    nota(ws, "C4", f"Máximo {M}. Deja en blanco las filas/columnas que no uses.")
    K = "$B$4"
    seccion(ws, "A6", "Matriz de transición P (de fila i → a columna j)")
    nm = _matriz_P(ws, 8, 3, K, nombres, P)  # B8:B15, C8:J15
    head(ws, 7, 11, ["Suma fila"])
    for i in range(M):
        r = 8 + i
        calc(ws, f"K{r}", f'=IF({i + 1}<={K},SUM(C{r}:J{r}),"")', "0.0000")
    marcar_rojo(ws, "K8:K15", f'AND(K8<>"",ABS(K8-1)>0.000001)')
    arr(ws, "L8", f'=IF(SUM((ROW(K8:K15)-7<={K})*(ABS(IF(ISNUMBER(K8:K15),K8:K15,1)-1)>0.000001))>0,"⚠ Alguna fila NO suma 1","✓ Matriz válida")', res=True)
    ws.merge_cells("L8:N8")

    # Matriz limpia (ceros fuera de k) — usada por todas las fórmulas
    seccion(ws, "A17", "P limpia (uso interno: ceros en estados no usados)")
    for i in range(M):
        for j in range(M):
            calc(ws, f"{CL(3 + j)}{18 + i}", f"=IF(AND({i + 1}<={K},{j + 1}<={K}),N({CL(3 + j)}{8 + i}),0)", "0.0000")
    PC = "$C$18:$J$25"

    seccion(ws, "A27", "Vector de estado inicial π(0)")
    for j in range(M):
        calc(ws, f"{CL(3 + j)}28", f"={CL(3 + j)}7", center=True, bold=True)
        inp(ws, f"{CL(3 + j)}29", [0.4, 0.3, 0.3][j] if j < 3 else None, "0.0000")
        calc(ws, f"{CL(3 + j)}30", f"=IF({j + 1}<={K},N({CL(3 + j)}29),0)", "0.0000")
    label(ws, "B29", "π(0) =", bold=True)
    label(ws, "B30", "π(0) limpio")
    calc(ws, "K29", "=SUM(C30:J30)", "0.0000")
    marcar_rojo(ws, "K29", "ABS(K29-1)>0.000001")
    PI0 = "$C$30:$J$30"

    label(ws, "A32", "Número de pasos n:", bold=True)
    inp(ws, "B32", 3, "0")
    entero(ws, "B32", 0, 63)
    nota(ws, "C32", "Entero entre 0 y 63")
    NREF = "$B$32"

    # Potencias por cuadrados sucesivos: P^1, P^2, P^4, ..., P^32 (área auxiliar, columnas P en adelante)
    seccion(ws, "P6", "Área auxiliar: potencias P^(2^b) y producto acumulado (no modificar)")
    base_col = 16  # P
    sq = []      # rangos P^(2^b)
    acc = []     # rangos acumulados
    for b in range(6):
        r0 = 8 + b * 10
        c_sq = base_col
        c_ac = base_col + 9
        rng_sq = f"${CL(c_sq)}${r0}:${CL(c_sq + 7)}${r0 + 7}"
        rng_ac = f"${CL(c_ac)}${r0}:${CL(c_ac + 7)}${r0 + 7}"
        label(ws, f"{CL(c_sq)}{r0 - 1}", f"P^{2 ** b}", bold=True)
        label(ws, f"{CL(c_ac)}{r0 - 1}", f"Producto acumulado (bit {b})", bold=True)
        if b == 0:
            arr(ws, rng_sq, f"=1*{PC}", "0.0000")
            ident = f"(ROW({rng_sq})-ROW({CL(c_sq)}{r0})=COLUMN({rng_sq})-COLUMN({CL(c_sq)}{r0}))*1"
            arr(ws, rng_ac, f"=IF(MOD(INT({NREF}/1),2)=1,{rng_sq},{ident})", "0.0000")
        else:
            arr(ws, rng_sq, f"=MMULT({sq[-1]},{sq[-1]})", "0.0000")
            arr(ws, rng_ac, f"=IF(MOD(INT({NREF}/{2 ** b}),2)=1,MMULT({acc[-1]},{rng_sq}),{acc[-1]})", "0.0000")
        sq.append(rng_sq)
        acc.append(rng_ac)
    PN_AUX = acc[-1]

    seccion(ws, "A34", "Resultado: matriz P^n (probabilidad de pasar de i a j en n pasos)")
    label(ws, "B35", '="P^"&' + NREF, bold=True)
    calc(ws, "B35", '="P^"&' + NREF, bold=True)
    for j in range(M):
        calc(ws, f"{CL(3 + j)}35", f"={CL(3 + j)}7", center=True, bold=True)
    pn_tl_r, pn_tl_c = int(PN_AUX.split(":")[0].split("$")[2]), PN_AUX.split(":")[0].split("$")[1]
    for i in range(M):
        r = 36 + i
        calc(ws, f"B{r}", f"=IF({i + 1}<={K},B{8 + i},\"\")", bold=True)
        for j in range(M):
            src = f"{CL(base_col + 9 + j)}{pn_tl_r + i}"
            calc(ws, f"{CL(3 + j)}{r}", f'=IF(AND({i + 1}<={K},{j + 1}<={K}),{src},"")', "0.0000", res=True)

    seccion(ws, "A45", "Resultado: π(n) = π(0) · P^n")
    for j in range(M):
        calc(ws, f"{CL(3 + j)}46", f"={CL(3 + j)}7", center=True, bold=True)
    label(ws, "B47", '=', bold=True)
    calc(ws, "B47", '="π("&' + NREF + '&")"', bold=True)
    arr(ws, "$C$48:$J$48", f"=MMULT({PI0},{PN_AUX})", "0.0000")
    for j in range(M):
        calc(ws, f"{CL(3 + j)}47", f'=IF({j + 1}<={K},{CL(3 + j)}48,"")', "0.0000", res=True)
    label(ws, "A48", "(interno)", italic=True, color="808080")

    seccion(ws, "A50", "Consulta rápida")
    label(ws, "A51", "Desde el estado:")
    inp(ws, "B51", "Tienda 1")
    label(ws, "A52", "Hacia el estado:")
    inp(ws, "B52", "Tienda 3")
    dv_rng = "$B$8:$B$15"
    dv = DataValidation(type="list", formula1=dv_rng, allow_blank=True)
    ws.add_data_validation(dv)
    dv.add("B51")
    dv.add("B52")
    label(ws, "A53", "P(en n pasos) =", bold=True)
    calc(ws, "B53", f"=IFERROR(INDEX($C$36:$J$43,MATCH(B51,{nm},0),MATCH(B52,{nm},0)),\"Nombre no encontrado\")", "0.0000", res=True)
    calc(ws, "C53", '="Probabilidad de que, estando en "&B51&", después de "&' + NREF + '&" pasos esté en "&B52', bold=False)

    seccion(ws, "A55", "Evolución π(t) para t = 0, 1, 2, … 30")
    head(ws, 56, 2, ["t"])
    for j in range(M):
        calc(ws, f"{CL(3 + j)}56", f"={CL(3 + j)}7", center=True, bold=True)
    for t in range(31):
        r = 57 + t
        calc(ws, f"B{r}", t, "0", center=True)
        if t == 0:
            for j in range(M):
                calc(ws, f"{CL(3 + j)}{r}", f"={CL(3 + j)}30", "0.0000")
        else:
            arr(ws, f"$C${r}:$J${r}", f"=MMULT($C${r - 1}:$J${r - 1},{PC})", "0.0000")
    anchos(ws, {"A": 22, "B": 14, **{CL(c): 10 for c in range(3, 12)}})

    # ------------------------------------------------------------------ Estado estable
    we = hoja(wb, "Estado estable", "Cadenas de Markov · Probabilidades de estado estable (largo plazo)",
              "Usa la matriz P de la hoja 'Matriz P'. Resuelve π·P = π con Σπ = 1. Válido para cadenas regulares (ergódicas).")
    MP = "'Matriz P'!"
    KK = f"{MP}$B$4"
    seccion(we, "A4", "Sistema M·π = b (interno): (Pᵀ − I) con la última ecuación reemplazada por Σπ = 1")
    for i in range(M):
        for j in range(M):
            d = 1 if i == j else 0
            pji = f"{MP}{CL(3 + i)}{18 + j}"  # P[j][i]
            calc(we, f"{CL(2 + j)}{6 + i}",
                 f"=IF(AND({i + 1}<={KK},{j + 1}<={KK}),IF({i + 1}={KK},1,{pji}-{d}),{d})", "0.0000")
        calc(we, f"K{6 + i}", f"=IF({i + 1}={KK},1,0)", "0")
    label(we, "K5", "b", bold=True)
    arr(we, "$M$6:$M$13", "=MMULT(MINVERSE($B$6:$I$13),$K$6:$K$13)", "0.000000")
    label(we, "M5", "π (interno)", bold=True)

    seccion(we, "A15", "Resultado")
    head(we, 16, 1, ["Estado", "π (largo plazo)", "%", "Tiempo medio de recurrencia 1/π", "Costo/ganancia por periodo en el estado", "π · costo"])
    for i in range(M):
        r = 17 + i
        calc(we, f"A{r}", f'=IF({i + 1}<={KK},{MP}B{8 + i},"")', bold=True)
        calc(we, f"B{r}", f'=IF({i + 1}<={KK},M{6 + i},"")', "0.0000", res=True)
        calc(we, f"C{r}", f'=IF({i + 1}<={KK},M{6 + i},"")', "0.00%")
        calc(we, f"D{r}", f'=IF({i + 1}<={KK},IFERROR(1/M{6 + i},"∞"),"")', "0.0000")
        inp(we, f"E{r}", None, "#,##0.00")
        calc(we, f"F{r}", f'=IF({i + 1}<={KK},M{6 + i}*N(E{r}),"")', "#,##0.0000")
    calc(we, "A25", "Suma", bold=True)
    calc(we, "B25", "=SUM(B17:B24)", "0.0000")
    label(we, "E25", "Costo/ganancia esperado por periodo:", bold=True)
    calc(we, "F25", "=SUM(F17:F24)", "#,##0.0000", res=True)
    nota(we, "A26", "1/πᵢ = número esperado de periodos para regresar al estado i, partiendo de i. La columna de costos es opcional (p. ej. ganancia por cliente en cada tienda).")
    calc(we, "A27", '=IF(COUNT(B17:B24)=0,"⚠ No se pudo resolver: la cadena no es regular (¿tiene estados absorbentes?). Usa la hoja Absorbente.","✓ Interpretación: a largo plazo el sistema pasa "&TEXT(B17,"0.00%")&" del tiempo en "&A17&", "&TEXT(B18,"0.00%")&" en "&A18&IF(N(B19)>0,", "&TEXT(B19,"0.00%")&" en "&A19,"")&IF(N(B20)>0,", "&TEXT(B20,"0.00%")&" en "&A20,"")&"…")')
    we.merge_cells("A27:H27")

    seccion(we, "A29", "Verificación π·P (debe ser igual a π)")
    arr(we, "$B$30:$I$30", f"=MMULT(TRANSPOSE($M$6:$M$13),{MP}$C$18:$J$25)", "0.0000")
    label(we, "A30", "π·P =", bold=True)

    # Tiempos de primer paso: Z = (I − P + Π)^-1 ; m_ij = (z_jj − z_ij)/π_j, m_jj = 1/π_j
    seccion(we, "A32", "Matriz fundamental Z = (I − P + Π)⁻¹ (interno)")
    for i in range(M):
        for j in range(M):
            d = 1 if i == j else 0
            pij = f"{MP}{CL(3 + j)}{18 + i}"
            calc(we, f"{CL(2 + j)}{34 + i}",
                 f"=IF(AND({i + 1}<={KK},{j + 1}<={KK}),{d}-{pij}+$M${6 + j},{d})", "0.0000")
    arr(we, "$L$34:$S$41", "=MINVERSE($B$34:$I$41)", "0.0000")
    label(we, "B33", "I − P + Π", bold=True)
    label(we, "L33", "Z", bold=True)

    seccion(we, "A43", "Tiempos esperados de primer paso mᵢⱼ (número de pasos para llegar por primera vez a j desde i)")
    label(we, "A44", "desde ↓ / hacia →", italic=True)
    for j in range(M):
        calc(we, f"{CL(2 + j)}44", f'=IF({j + 1}<={KK},{MP}B{8 + j},"")', center=True, bold=True)
    for i in range(M):
        r = 45 + i
        calc(we, f"A{r}", f'=IF({i + 1}<={KK},{MP}B{8 + i},"")', bold=True)
        for j in range(M):
            zjj = f"{CL(12 + j)}{34 + j}"
            zij = f"{CL(12 + j)}{34 + i}"
            pj = f"$M${6 + j}"
            f = (f'=IF(AND({i + 1}<={KK},{j + 1}<={KK}),IFERROR(' +
                 (f"1/{pj}" if i == j else f"({zjj}-{zij})/{pj}") + ',"—"),"")')
            calc(we, f"{CL(2 + j)}{r}", f, "0.0000", res=True)
    nota(we, "A53", "La diagonal mᵢᵢ es el tiempo medio de recurrencia (= 1/πᵢ).")
    anchos(we, {"A": 22, **{CL(c): 13 for c in range(2, 20)}})
    we.column_dimensions["D"].width = 16
    we.column_dimensions["E"].width = 18

    # ------------------------------------------------------------------ Absorbente
    wa = hoja(wb, "Absorbente", "Cadenas de Markov · Cadenas absorbentes",
              "Escribe la matriz P COMPLETA. Un estado es absorbente si pᵢᵢ = 1. La hoja separa Q y R automáticamente.")
    label(wa, "A4", "Número de estados (k):", bold=True)
    inp(wa, "B4", 4, "0")
    entero(wa, "B4", 2, M)
    KA = "$B$4"
    seccion(wa, "A6", "Matriz de transición P completa")
    nombres_a = ["Pagado", "Incobrable", "0-30 días", "31-90 días"]
    PA = [[1, 0, 0, 0], [0, 1, 0, 0], [0.4, 0, 0.3, 0.3], [0.4, 0.2, 0.3, 0.1]]
    _matriz_P(wa, 8, 3, KA, nombres_a, PA)
    head(wa, 7, 11, ["Suma fila", "¿Absorbente?"])
    for i in range(M):
        r = 8 + i
        calc(wa, f"K{r}", f'=IF({i + 1}<={KA},SUM(C{r}:J{r}),"")', "0.0000")
        calc(wa, f"L{r}", f'=IF({i + 1}<={KA},IF(ABS(N({CL(3 + i)}{r})-1)<0.0000001,"Sí","No"),"")', center=True)
        calc(wa, f"N{r}", f"={i + 1}", "0")  # índice
        calc(wa, f"O{r}", f'=IF(L{r}="Sí",1,0)')
        calc(wa, f"P{r}", f'=IF(L{r}="No",1,0)')
    marcar_rojo(wa, "K8:K15", 'AND(K8<>"",ABS(K8-1)>0.000001)')
    label(wa, "N7", "idx", italic=True, color="808080")
    label(wa, "O7", "abs", italic=True, color="808080")
    label(wa, "P7", "trans", italic=True, color="808080")
    seccion(wa, "A17", "Clasificación (orden canónico)")
    head(wa, 18, 1, ["#", "Transitorio", "idx", "Absorbente", "idx"])
    for r_ in range(M):
        r = 19 + r_
        calc(wa, f"A{r}", r_ + 1, "0", center=True)
        arr(wa, f"C{r}", f"=IFERROR(SMALL(IF($P$8:$P$15=1,$N$8:$N$15),{r_ + 1}),0)", "0")
        arr(wa, f"E{r}", f"=IFERROR(SMALL(IF($O$8:$O$15=1,$N$8:$N$15),{r_ + 1}),0)", "0")
        calc(wa, f"B{r}", f'=IF(C{r}=0,"",INDEX($B$8:$B$15,C{r}))', bold=True)
        calc(wa, f"D{r}", f'=IF(E{r}=0,"",INDEX($B$8:$B$15,E{r}))', bold=True)
    label(wa, "G19", "Transitorios (t):", bold=True)
    calc(wa, "H19", "=SUM(P8:P15)", "0", res=True)
    label(wa, "G20", "Absorbentes (a):", bold=True)
    calc(wa, "H20", "=SUM(O8:O15)", "0", res=True)
    calc(wa, "G21", '=IF(H20=0,"⚠ No hay estados absorbentes (ningún pᵢᵢ = 1)","✓ Cadena con estados absorbentes")', res=True)
    marcar_rojo(wa, "G21", "$H$20=0")
    T_, A_ = "$H$19", "$H$20"

    # Q y R
    seccion(wa, "A28", "Q (transitorio → transitorio)")
    seccion(wa, "K28", "R (transitorio → absorbente)")
    for i in range(M):
        r = 30 + i
        calc(wa, f"A{r}", f"=B{19 + i}", bold=True)
        calc(wa, f"K{r}", f"=B{19 + i}", bold=True)
        for j in range(M):
            calc(wa, f"{CL(2 + j)}{r}", f"=IF(AND($C${19 + i}>0,$C${19 + j}>0),INDEX($C$8:$J$15,$C${19 + i},$C${19 + j}),0)", "0.0000")
            calc(wa, f"{CL(12 + j)}{r}", f"=IF(AND($C${19 + i}>0,$E${19 + j}>0),INDEX($C$8:$J$15,$C${19 + i},$E${19 + j}),0)", "0.0000")
    for j in range(M):
        calc(wa, f"{CL(2 + j)}29", f"=B{19 + j}", center=True, bold=True)
        calc(wa, f"{CL(12 + j)}29", f"=D{19 + j}", center=True, bold=True)

    # I - Q con relleno identidad
    seccion(wa, "A39", "I − Q (interno, con identidad en filas no usadas)")
    for i in range(M):
        for j in range(M):
            d = 1 if i == j else 0
            calc(wa, f"{CL(2 + j)}{40 + i}", f"=IF(AND({i + 1}<={T_},{j + 1}<={T_}),{d}-{CL(2 + j)}{30 + i},{d})", "0.0000")
    arr(wa, "$L$40:$S$47", "=MINVERSE($B$40:$I$47)", "0.0000")
    arr(wa, "$L$50:$S$57", "=MMULT($L$40:$S$47,$L$30:$S$37)", "0.0000")
    arr(wa, "$U$40:$U$47", "=MMULT($L$40:$S$47,(ROW($L$40:$L$47)-ROW($L$40)+1<=" + T_ + ")*1)", "0.0000")
    label(wa, "L39", "N interna", italic=True, color="808080")
    label(wa, "L49", "B interna", italic=True, color="808080")
    label(wa, "U39", "t interno", italic=True, color="808080")

    seccion(wa, "A60", "Resultado 1: Matriz fundamental N = (I − Q)⁻¹  (visitas esperadas a cada transitorio)")
    for j in range(M):
        calc(wa, f"{CL(2 + j)}61", f"=B{19 + j}", center=True, bold=True)
    for i in range(M):
        r = 62 + i
        calc(wa, f"A{r}", f"=B{19 + i}", bold=True)
        for j in range(M):
            calc(wa, f"{CL(2 + j)}{r}", f'=IF(AND({i + 1}<={T_},{j + 1}<={T_}),{CL(12 + j)}{40 + i},"")', "0.0000", res=True)

    seccion(wa, "A71", "Resultado 2: B = N·R  (probabilidad de terminar en cada estado absorbente)")
    for j in range(M):
        calc(wa, f"{CL(2 + j)}72", f"=D{19 + j}", center=True, bold=True)
    head(wa, 72, 11, ["Pasos esperados hasta absorción (t = N·1)"])
    wa.column_dimensions["K"].width = 22
    for i in range(M):
        r = 73 + i
        calc(wa, f"A{r}", f"=B{19 + i}", bold=True)
        for j in range(M):
            calc(wa, f"{CL(2 + j)}{r}", f'=IF(AND({i + 1}<={T_},{j + 1}<={A_}),{CL(12 + j)}{50 + i},"")', "0.0000", res=True)
        calc(wa, f"K{r}", f'=IF({i + 1}<={T_},U{40 + i},"")', "0.0000", res=True)

    seccion(wa, "A82", "Resultado 3 (opcional): cantidades actuales en cada estado transitorio → cantidad esperada que termina en cada absorbente")
    head(wa, 83, 1, ["Transitorio", "Cantidad actual"])
    amounts = [1000, 2000]
    for i in range(M):
        r = 84 + i
        calc(wa, f"A{r}", f"=B{19 + i}", bold=True)
        inp(wa, f"B{r}", amounts[i] if i < 2 else None, "#,##0.00")
        calc(wa, f"C{r}", f"=IF({i + 1}<={T_},N(B{r}),0)", "#,##0.00")
    label(wa, "C83", "(limpio)", italic=True, color="808080")
    for j in range(M):
        calc(wa, f"{CL(5 + j)}83", f"=D{19 + j}", center=True, bold=True)
    arr(wa, "$E$95:$L$95", "=MMULT(TRANSPOSE($C$84:$C$91),$L$50:$S$57)", "#,##0.00")
    label(wa, "D95", "(interno)", italic=True, color="808080")
    label(wa, "D84", "Total esperado:", bold=True)
    for j in range(M):
        calc(wa, f"{CL(5 + j)}84", f'=IF({j + 1}<={A_},{CL(5 + j)}95,"")', "#,##0.00", res=True)
    nota(wa, "A93", "Ejemplo (Anderson): cuentas por cobrar. $1,000 en 0-30 días y $2,000 en 31-90 días → se espera cobrar ≈ $2,370 y perder ≈ $630.")
    anchos(wa, {"A": 18, **{CL(c): 12 for c in range(2, 22)}})
    wa.column_dimensions["G"].width = 16
    wa.column_dimensions["K"].width = 14

    inicio(wb, "Solucionador · Cadenas de Markov",
           "Calcula probabilidades en n pasos, π(n), probabilidades de estado estable, tiempos de recurrencia y de primer paso, "
           "y para cadenas absorbentes la matriz fundamental N, probabilidades de absorción B y pasos esperados.",
           [("Matriz P", "Matriz de transición, P^n, π(n) = π(0)·P^n, evolución t = 0..30, consulta i→j en n pasos."),
            ("Estado estable", "π a largo plazo, 1/π (recurrencia), tiempos de primer paso mᵢⱼ, costo esperado."),
            ("Absorbente", "Separa Q y R, N = (I−Q)⁻¹, B = N·R, pasos hasta absorción, montos esperados."),
            ("Formulario", "Fórmulas del tema.")])
    formulario(wb, "Formulario · Cadenas de Markov", [
        ("Básicos", [
            ("Propiedad de Markov", "P(Xₙ₊₁ = j | Xₙ = i, …, X₀) = P(Xₙ₊₁ = j | Xₙ = i) = pᵢⱼ"),
            ("Condición de la matriz P", "0 ≤ pᵢⱼ ≤ 1 ;  Σⱼ pᵢⱼ = 1 para cada fila i"),
            ("Probabilidades en n pasos", "P⁽ⁿ⁾ = Pⁿ ;  pᵢⱼ⁽ⁿ⁾ = Σₖ pᵢₖ⁽ⁿ⁻¹⁾ pₖⱼ  (Chapman-Kolmogorov)"),
            ("Vector de estado", "π(n) = π(0) · Pⁿ = π(n−1) · P"),
        ]),
        ("Estado estable (cadena regular / ergódica)", [
            ("Ecuaciones", "π = π · P  y  π₁ + π₂ + … + πₖ = 1"),
            ("2 estados", "π₁ = p₂₁ / (p₁₂ + p₂₁) ;  π₂ = p₁₂ / (p₁₂ + p₂₁)"),
            ("Tiempo medio de recurrencia", "μᵢᵢ = 1 / πᵢ"),
            ("Tiempo de primer paso", "mᵢⱼ = 1 + Σₖ≠ⱼ pᵢₖ mₖⱼ"),
            ("Costo esperado a largo plazo", "E[C] = Σᵢ πᵢ · Cᵢ"),
        ]),
        ("Cadenas absorbentes", [
            ("Estado absorbente", "pᵢᵢ = 1"),
            ("Forma canónica", "P = [ I  0 ; R  Q ]  (absorbentes primero) — Q: transitorio→transitorio, R: transitorio→absorbente"),
            ("Matriz fundamental", "N = (I − Q)⁻¹   (nᵢⱼ = visitas esperadas a j partiendo de i)"),
            ("Probabilidades de absorción", "B = N · R"),
            ("Pasos esperados hasta absorción", "t = N · 1"),
            ("Montos esperados", "(montos actuales) · B"),
        ]),
    ])
    wb.save(ruta)
