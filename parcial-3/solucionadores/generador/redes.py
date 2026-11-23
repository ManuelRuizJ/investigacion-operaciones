"""4_Redes.xlsx: ruta más corta (Floyd-Warshall con fórmulas), árbol de expansión mínima (Prim con fórmulas),
flujo máximo y ruta más corta como PL (Solver)."""
from comun import *

NN = 12   # nodos máximos
NA = 30   # arcos máximos
B = GRANDE

# Ejemplo: Seervada Park (Hillier & Lieberman)
NODOS = ["O", "A", "B", "C", "D", "E", "T"]
ARCOS_RC = [("O", "A", 2), ("O", "B", 5), ("O", "C", 4), ("A", "B", 2), ("A", "D", 7), ("B", "C", 1), ("B", "D", 4),
            ("B", "E", 3), ("C", "E", 4), ("D", "E", 1), ("D", "T", 5), ("E", "T", 7)]
ARCOS_FM = [("O", "A", 5), ("O", "B", 7), ("O", "C", 4), ("A", "B", 1), ("A", "D", 3), ("B", "C", 2), ("B", "D", 4),
            ("B", "E", 5), ("C", "E", 4), ("D", "T", 9), ("E", "D", 1), ("E", "T", 6)]


def _flujo_max(nodos, arcos, s, t):
    """Edmonds-Karp sólo para precargar la solución del ejemplo (las variables las ajusta Solver)."""
    from collections import deque
    cap = {}
    for a, b, c in arcos:
        cap[(a, b)] = cap.get((a, b), 0) + c
        cap.setdefault((b, a), 0)
    flow = {k: 0 for k in cap}
    total = 0
    while True:
        prev = {s: None}
        q = deque([s])
        while q and t not in prev:
            u = q.popleft()
            for (x, y), c in cap.items():
                if x == u and y not in prev and c - flow[(x, y)] > 0:
                    prev[y] = u
                    q.append(y)
        if t not in prev:
            break
        path, v = [], t
        while prev[v] is not None:
            path.append((prev[v], v))
            v = prev[v]
        f = min(cap[e] - flow[e] for e in path)
        for (x, y) in path:
            flow[(x, y)] += f
            flow[(y, x)] -= f
        total += f
    return total, {(a, b): max(0, flow[(a, b)]) for a, b, _ in arcos}


def _nodos_y_arcos(ws, nodos, arcos, n_ref_cell="B4", col_peso="Distancia / costo", extra_cols=()):
    """Tabla de nodos (A9:B20) y de arcos (D9:G38 + índices H, I). Devuelve dict de rangos."""
    seccion(ws, "A7", "Nodos")
    head(ws, 8, 1, ["#", "Nombre"])
    for i in range(NN):
        r = 9 + i
        calc(ws, f"A{r}", i + 1, "0", center=True)
        inp(ws, f"B{r}", nodos[i] if i < len(nodos) else None, center=True)
    seccion(ws, "D7", "Arcos (una fila por conexión)")
    head(ws, 8, 4, ["#", "Desde", "Hasta", col_peso, *extra_cols, "idx desde", "idx hasta"])
    ci = 8 + len(extra_cols)  # columna de idx desde
    dv = DataValidation(type="list", formula1="$B$9:$B$20", allow_blank=True)
    ws.add_data_validation(dv)
    for k in range(NA):
        r = 9 + k
        calc(ws, f"D{r}", k + 1, "0", center=True)
        a = arcos[k] if k < len(arcos) else (None, None, None)
        inp(ws, f"E{r}", a[0], center=True)
        inp(ws, f"F{r}", a[1], center=True)
        inp(ws, f"G{r}", a[2], "#,##0.##")
        dv.add(f"E{r}")
        dv.add(f"F{r}")
        calc(ws, f"{CL(ci)}{r}", f'=IF(E{r}="",0,IFERROR(MATCH(E{r},$B$9:$B${8 + NN},0),0))', "0", center=True)
        calc(ws, f"{CL(ci + 1)}{r}", f'=IF(F{r}="",0,IFERROR(MATCH(F{r},$B$9:$B${8 + NN},0),0))', "0", center=True)
    chk = f"{CL(ci + 2)}9"
    calc(ws, chk, f'=IF(SUMPRODUCT((E9:E38<>"")*({CL(ci)}9:{CL(ci)}38=0)+(F9:F38<>"")*({CL(ci + 1)}9:{CL(ci + 1)}38=0))>0,"⚠ Hay arcos con nodos que no existen en la lista","✓ Arcos válidos")', res=True)
    marcar_rojo(ws, chk, f'LEFT({chk},1)="⚠"')
    return dict(F=f"${CL(ci)}$9:${CL(ci)}$38", T=f"${CL(ci + 1)}$9:${CL(ci + 1)}$38", W="$G$9:$G$38",
                names=f"$B$9:$B${8 + NN}", ci=ci)


def generar(ruta):
    wb = libro()

    # ================================================================== RUTA MÁS CORTA
    ws = hoja(wb, "Ruta mas corta", "Redes · Ruta más corta (todas las parejas, algoritmo de Floyd–Warshall con fórmulas)",
              "Ejemplo: Seervada Park (Hillier & Lieberman). Escribe nodos y arcos; elige origen y destino. Resultado = mismo que Dijkstra.")
    label(ws, "A4", "Número de nodos n:", bold=True)
    calc(ws, "B4", '=COUNTA(B9:B20)', "0", res=True)
    label(ws, "A5", "¿Red dirigida? (Sí/No)", bold=True)
    inp(ws, "B5", "No", center=True)
    lista(ws, "B5", ["No", "Sí"])
    nota(ws, "C5", "No = cada arco se puede recorrer en ambos sentidos")
    rg = _nodos_y_arcos(ws, NODOS, ARCOS_RC)
    F, T, W = rg["F"], rg["T"], rg["W"]
    UND = '($B$5<>"Sí")'

    # Bloques D0..D12 y N0..N12 (área de cálculo)
    R0 = 60
    seccion(ws, f"A{R0 - 2}", "Iteraciones de Floyd–Warshall (cálculo interno, no modificar). Izquierda: distancias Dₖ. Derecha: siguiente nodo Nₖ.")

    def dpos(k):  # esquina superior izquierda (fila) del bloque k
        return R0 + k * (NN + 2)

    DC, NC = 2, 16  # columnas iniciales (B y P)
    for k in range(NN + 1):
        r0 = dpos(k)
        label(ws, f"A{r0}", f"D{k}" if k else "D0 (directas)", bold=True)
        label(ws, f"O{r0}", f"N{k}", bold=True)
        for i in range(NN):
            for j in range(NN):
                dref = f"{CL(DC + j)}{r0 + i}"
                nref = f"{CL(NC + j)}{r0 + i}"
                if k == 0:
                    match = f"((({F}={i + 1})*({T}={j + 1})+{UND}*({F}={j + 1})*({T}={i + 1}))>0)"
                    if i == j:
                        calc(ws, dref, 0, "0.##")
                    else:
                        arr(ws, dref, f"=IF(OR({i + 1}>$B$4,{j + 1}>$B$4),{B},MIN(IF({match},{W},{B})))", "0.##")
                    calc(ws, nref, f"=IF(AND({i + 1}<>{j + 1},{dref}<{B}),{j + 1},0)", "0")
                else:
                    p = dpos(k - 1)
                    dij = f"{CL(DC + j)}{p + i}"
                    dik = f"{CL(DC + k - 1)}{p + i}"
                    dkj = f"{CL(DC + j)}{p + k - 1}"
                    nij = f"{CL(NC + j)}{p + i}"
                    nik = f"{CL(NC + k - 1)}{p + i}"
                    cond = f"{dik}+{dkj}<{dij}-0.000000001"
                    calc(ws, dref, f"=IF({cond},{dik}+{dkj},{dij})", "0.##")
                    calc(ws, nref, f"=IF({cond},{nik},{nij})", "0")
    DF = f"$B${dpos(NN)}:${CL(DC + NN - 1)}${dpos(NN) + NN - 1}"
    NF = f"${CL(NC)}${dpos(NN)}:${CL(NC + NN - 1)}${dpos(NN) + NN - 1}"

    # Consulta origen-destino
    seccion(ws, "K3", "Consulta")
    label(ws, "K4", "Origen:", bold=True)
    inp(ws, "L4", "O", center=True)
    label(ws, "K5", "Destino:", bold=True)
    inp(ws, "L5", "T", center=True)
    dv = DataValidation(type="list", formula1="$B$9:$B$20", allow_blank=False)
    ws.add_data_validation(dv)
    dv.add("L4")
    dv.add("L5")
    calc(ws, "N4", f"=IFERROR(MATCH(L4,{rg['names']},0),0)", "0")
    calc(ws, "N5", f"=IFERROR(MATCH(L5,{rg['names']},0),0)", "0")
    label(ws, "M4", "idx", italic=True, color="808080")
    label(ws, "M5", "idx", italic=True, color="808080")

    # Tabla de rutas desde el origen a cada nodo: pasos (área auxiliar columnas AD..AP)
    PC0 = 30  # AD
    seccion(ws, f"{CL(PC0)}7", "Pasos de cada ruta desde el origen (interno)")
    head(ws, 8, PC0, [f"p{m}" for m in range(NN + 1)])
    for j in range(NN):
        r = 9 + j
        for m in range(NN + 1):
            c = f"{CL(PC0 + m)}{r}"
            if m == 0:
                calc(ws, c, "=$N$4", "0")
            else:
                prev = f"{CL(PC0 + m - 1)}{r}"
                calc(ws, c, f"=IF(OR({prev}=0,{prev}={j + 1}),0,INDEX({NF},{prev},{j + 1}))", "0")
    seccion(ws, "K11", "Distancias mínimas desde el origen a todos los nodos")
    head(ws, 12, 11, ["Nodo", "Distancia", "Nodo anterior", "Ruta"])
    for j in range(NN):
        r = 13 + j
        pr = 9 + j
        steps = [f"{CL(PC0 + m)}{pr}" for m in range(NN + 1)]
        txt = f"INDEX({rg['names']},{steps[0]})" + "".join(
            f'&IF({s}>0," → "&INDEX({rg["names"]},{s}),"")' for s in steps[1:])
        dist = f"INDEX({DF},$N$4,{j + 1})"
        ok = f"AND({j + 1}<=$B$4,$N$4>0)"
        calc(ws, f"K{r}", f'=IF({j + 1}<=$B$4,B{9 + j},"")', bold=True, center=True)
        calc(ws, f"L{r}", f'=IF({ok},IF({dist}>={B},"∞",{dist}),"")', "#,##0.##", res=True)
        cnt = f"COUNTIF({CL(PC0)}{pr}:{CL(PC0 + NN)}{pr},\">0\")"
        calc(ws, f"M{r}", f'=IF({ok},IF(OR({dist}>={B},{cnt}<2),"—",INDEX({rg["names"]},INDEX({CL(PC0)}{pr}:{CL(PC0 + NN)}{pr},{cnt}-1))),"")', center=True)
        calc(ws, f"N{r}", f'=IF({ok},IF({dist}>={B},"Sin ruta",{txt}),"")')
        ws.merge_cells(f"N{r}:R{r}")
    seccion(ws, "K26", "Resultado para el destino elegido")
    label(ws, "K27", "Distancia mínima:", bold=True)
    calc(ws, "L27", f'=IF(AND($N$4>0,$N$5>0),IF(INDEX({DF},$N$4,$N$5)>={B},"No hay ruta",INDEX({DF},$N$4,$N$5)),"Revisa origen/destino")', "#,##0.##", res=True)
    label(ws, "K28", "Ruta:", bold=True)
    calc(ws, "L28", f'=IF($N$5>0,INDEX($N$13:$N$24,$N$5),"")', res=True)
    ws.merge_cells("L28:R28")
    calc(ws, "K29", '="La ruta más corta de "&L4&" a "&L5&" mide "&L27&": "&L28', bold=False)
    ws.merge_cells("K29:R29")

    seccion(ws, "K31", "Matriz de distancias mínimas entre todos los pares")
    for j in range(NN):
        calc(ws, f"{CL(12 + j)}32", f'=IF({j + 1}<=$B$4,B{9 + j},"")', bold=True, center=True)
    for i in range(NN):
        r = 33 + i
        calc(ws, f"K{r}", f'=IF({i + 1}<=$B$4,B{9 + i},"")', bold=True, center=True)
        for j in range(NN):
            d = f"INDEX({DF},{i + 1},{j + 1})"
            calc(ws, f"{CL(12 + j)}{r}", f'=IF(AND({i + 1}<=$B$4,{j + 1}<=$B$4),IF({d}>={B},"∞",{d}),"")', "#,##0.##")
    nota(ws, "K46", "Si hay empate entre dos rutas de la misma longitud se muestra una de ellas.")
    anchos(ws, {"A": 16, "B": 9, "C": 9, "D": 5, "E": 9, "F": 9, "G": 11, "H": 8, "I": 8, "J": 30, "K": 18, "L": 12, "M": 12})
    for c in range(14, 28):
        ws.column_dimensions[CL(c)].width = 8
    ws.column_dimensions["J"].width = 9
    for c in range(PC0, PC0 + NN + 1):
        ws.column_dimensions[CL(c)].width = 5

    # ================================================================== ÁRBOL DE EXPANSIÓN MÍNIMA
    ws = hoja(wb, "Arbol expansion minima", "Redes · Árbol de expansión mínima (algoritmo de Prim con fórmulas)",
              "Ejemplo: Seervada Park (Hillier & Lieberman). Red NO dirigida. Cada paso agrega el arco más barato que une un nodo conectado con uno no conectado.")
    label(ws, "A4", "Número de nodos n:", bold=True)
    calc(ws, "B4", '=COUNTA(B9:B20)', "0", res=True)
    label(ws, "A5", "Nodo inicial:", bold=True)
    inp(ws, "B5", "O", center=True)
    dv = DataValidation(type="list", formula1="$B$9:$B$20")
    ws.add_data_validation(dv)
    dv.add("B5")
    calc(ws, "C5", "=IFERROR(MATCH(B5,$B$9:$B$20,0),1)", "0")
    rg = _nodos_y_arcos(ws, NODOS, ARCOS_RC)
    F, T, W = rg["F"], rg["T"], rg["W"]
    Fc, Tc = CL(rg["ci"]), CL(rg["ci"] + 1)
    # banderas "en el árbol": filas 46..57 (t = 0..11), columnas C..N (nodos 1..12)
    FR0 = 46
    seccion(ws, f"A{FR0 - 2}", "Cálculo interno: nodos conectados después de cada paso (1 = conectado)")
    head(ws, FR0 - 1, 2, ["Paso t"] + [f"n{j + 1}" for j in range(NN)])
    EC0 = 16  # P: columnas de costos elegibles por iteración (P..Z)
    seccion(ws, f"{CL(EC0)}7", "Costos elegibles por paso (interno)")
    head(ws, 8, EC0, [f"t{t + 1}" for t in range(NN - 1)])
    for t in range(NN):
        r = FR0 + t
        calc(ws, f"B{r}", t, "0", center=True)
        for j in range(NN):
            c = f"{CL(3 + j)}{r}"
            if t == 0:
                calc(ws, c, f"=IF({j + 1}=$C$5,1,0)", "0")
            else:
                sel = f"{CL(EC0 + t - 1)}$40"
                prev = f"{CL(3 + j)}{r - 1}"
                calc(ws, c, f"=IF(OR({prev}=1,AND({sel}>0,OR(INDEX({F},MAX(1,{sel}))={j + 1},INDEX({T},MAX(1,{sel}))={j + 1}))),1,0)", "0")
    for t in range(NN - 1):
        col = CL(EC0 + t)
        flags = f"$C${FR0 + t}:${CL(2 + NN)}${FR0 + t}"
        for k in range(NA):
            r = 9 + k
            calc(ws, f"{col}{r}", f"=IF(AND({t + 1}<=$B$4-1,${Fc}{r}>0,${Tc}{r}>0,ISNUMBER($G{r})),IF(INDEX({flags},1,${Fc}{r})+INDEX({flags},1,${Tc}{r})=1,$G{r},{B}),{B})", "0.##")
        calc(ws, f"{col}40", f"=IF(MIN({col}9:{col}38)>={B},0,MATCH(MIN({col}9:{col}38),{col}9:{col}38,0))", "0", res=True)
    label(ws, f"{CL(EC0 - 1)}40", "arco elegido →", italic=True, color="808080")

    seccion(ws, "K3", "Resultado: arcos del árbol en el orden en que se agregan")
    head(ws, 4, 11, ["Paso", "Desde", "Hasta", "Costo", "Acumulado"])
    for t in range(NN - 1):
        r = 5 + t
        sel = f"{CL(EC0 + t)}$40"
        ok = f"AND({t + 1}<=$B$4-1,{sel}>0)"
        calc(ws, f"K{r}", f'=IF({t + 1}<=$B$4-1,{t + 1},"")', "0", center=True)
        calc(ws, f"L{r}", f'=IF({ok},INDEX($E$9:$E$38,{sel}),IF({t + 1}<=$B$4-1,"⚠ sin arco",""))', center=True, res=True)
        calc(ws, f"M{r}", f'=IF({ok},INDEX($F$9:$F$38,{sel}),"")', center=True, res=True)
        calc(ws, f"N{r}", f'=IF({ok},INDEX($G$9:$G$38,{sel}),"")', "#,##0.##", res=True)
        calc(ws, f"O{r}", f'=IF({ok},SUM($N$5:N{r}),"")', "#,##0.##")
    label(ws, "K17", "Costo total del árbol:", bold=True)
    calc(ws, "N17", "=SUM(N5:N15)", "#,##0.##", res=True)
    calc(ws, "K18", f'=IF(COUNTIF(L5:L15,"⚠ sin arco")>0,"⚠ La red no es conexa: no se pueden conectar todos los nodos","✓ Se conectan los "&$B$4&" nodos con "&($B$4-1)&" arcos y costo total "&N17)', res=True)
    ws.merge_cells("K18:O18")
    marcar_rojo(ws, "K18", 'LEFT($K$18,1)="⚠"')
    nota(ws, "K19", "El costo total es el mismo con Kruskal o con cualquier nodo inicial.")
    anchos(ws, {"A": 14, "B": 9, "C": 9, "D": 5, "E": 9, "F": 9, "G": 11, "H": 8, "I": 8, "J": 30, "K": 8, "L": 10, "M": 10, "N": 10, "O": 11})
    for c in range(EC0, EC0 + NN):
        ws.column_dimensions[CL(c)].width = 7

    # ================================================================== FLUJO MÁXIMO (Solver)
    ws = hoja(wb, "Flujo maximo", "Redes · Flujo máximo (modelo de programación lineal para Solver)",
              "Ejemplo: Seervada Park (Hillier & Lieberman), flujo máximo de O a T = 14. Los arcos son dirigidos: si un tramo es de doble sentido, escríbelo dos veces.")
    label(ws, "A4", "Fuente (origen):", bold=True)
    inp(ws, "B4", "O", center=True)
    label(ws, "A5", "Sumidero (destino):", bold=True)
    inp(ws, "B5", "T", center=True)
    rg = _nodos_y_arcos(ws, NODOS, ARCOS_FM, col_peso="Capacidad", extra_cols=("Flujo (variable)",))
    total, flujos = _flujo_max(NODOS, ARCOS_FM, "O", "T")
    for k in range(NA):
        r = 9 + k
        val = flujos[(ARCOS_FM[k][0], ARCOS_FM[k][1])] if k < len(ARCOS_FM) else 0
        c = ws[f"H{r}"]
        c.value = val
        _ = inp(ws, f"H{r}", None, "#,##0.##")
        ws[f"H{r}"].fill = F_RES
    ws["H8"].value = "Flujo (variable)"
    head(ws, 8, 12, ["¿≤ capacidad?"])
    for k in range(NA):
        r = 9 + k
        calc(ws, f"L{r}", f'=IF(E{r}="","",IF(AND(N(H{r})>=0,N(H{r})<=N(G{r})+0.000001),"✓","⚠"))', center=True)
    marcar_rojo(ws, "L9:L38", 'L9="⚠"')
    seccion(ws, "N3", "Arco ficticio sumidero → fuente")
    label(ws, "N4", "Flujo total (variable objetivo):", bold=True)
    inp(ws, "Q4", total, "#,##0.##")
    ws["Q4"].fill = F_RES
    ws["Q4"].font = Font(name=FONT, size=12, bold=True, color="0000FF")
    seccion(ws, "N6", "Conservación de flujo (debe ser 0 en todos)")
    head(ws, 7, 14, ["Nodo", "Entra", "Sale", "Entra − Sale"])
    for i in range(NN):
        r = 8 + i
        nm = f"$B${9 + i}"
        calc(ws, f"N{r}", f'=IF({nm}="","",{nm})', center=True, bold=True)
        calc(ws, f"O{r}", f'=IF({nm}="",0,SUMIF($F$9:$F$38,{nm},$H$9:$H$38)+IF({nm}=$B$4,$Q$4,0))', "#,##0.##")
        calc(ws, f"P{r}", f'=IF({nm}="",0,SUMIF($E$9:$E$38,{nm},$H$9:$H$38)+IF({nm}=$B$5,$Q$4,0))', "#,##0.##")
        calc(ws, f"Q{r}", f"=O{r}-P{r}", "#,##0.##")
    marcar_rojo(ws, "Q8:Q19", "ABS(Q8)>0.000001")
    calc(ws, "N21", '=IF(AND(COUNTIF(L9:L38,"⚠")=0,SUMPRODUCT(ABS(Q8:Q19))<0.000001),"✓ Flujo factible: el flujo máximo es "&Q4,"⚠ La solución actual NO es factible: corre Solver")', res=True)
    ws.merge_cells("N21:T21")
    seccion(ws, "N23", "Cómo resolver con Solver")
    pasos = [
        "1) Escribe nodos, fuente, sumidero, arcos y capacidades. Pon 0 en todos los flujos (columna H) y en Q4.",
        "EXCEL: Datos → Solver (si no aparece: Archivo → Opciones → Complementos → Solver).",
        "   • Establecer objetivo: $Q$4   → Para: Máx",
        "   • Cambiando las celdas: $H$9:$H$38;$Q$4",
        "   • Restricciones:  $H$9:$H$38 <= $G$9:$G$38   y   $Q$8:$Q$19 = 0",
        "   • Marca 'Convertir variables sin restricciones en no negativas' y método 'Simplex LP' → Resolver.",
        "LIBREOFFICE: Herramientas → Solver.",
        "   • Celda objetivo $Q$4, Máximo; Cambiando celdas $H$9:$H$38;$Q$4",
        "   • Condiciones: $H$9:$H$38 <= $G$9:$G$38 ; $Q$8:$Q$19 = 0",
        "   • Opciones: motor lineal, 'Asumir variables no negativas' → Resolver.",
        "Nota: deja vacías (sin capacidad) las filas de arcos que no uses; su flujo queda en 0.",
    ]
    for k, p in enumerate(pasos):
        label(ws, f"N{24 + k}", p, size=9)
    anchos(ws, {"A": 18, "B": 9, "C": 3, "D": 5, "E": 9, "F": 9, "G": 11, "H": 13, "I": 8, "J": 8, "K": 30, "L": 12, "M": 3,
                "N": 12, "O": 10, "P": 10, "Q": 12})

    # ================================================================== RUTA MÁS CORTA COMO PL
    ws = hoja(wb, "Ruta corta PL", "Redes · Ruta más corta como programación lineal (Solver)",
              "Por si te piden la formulación. xᵢⱼ = 1 si el arco se usa. Balance: sale − entra = 1 en el origen, −1 en el destino, 0 en los demás.")
    label(ws, "A4", "Origen:", bold=True)
    inp(ws, "B4", "O", center=True)
    label(ws, "A5", "Destino:", bold=True)
    inp(ws, "B5", "T", center=True)
    label(ws, "C4", "¿Dirigida?", bold=True)
    inp(ws, "D4", "No", center=True)
    lista(ws, "D4", ["No", "Sí"])
    rg = _nodos_y_arcos(ws, NODOS, ARCOS_RC, extra_cols=("x (desde→hasta)", "x (hasta→desde)"))
    usados = {("O", "A"), ("A", "B"), ("B", "D"), ("D", "T")}
    for k in range(NA):
        r = 9 + k
        a = ARCOS_RC[k] if k < len(ARCOS_RC) else None
        inp(ws, f"H{r}", 1 if a and (a[0], a[1]) in usados else 0, "0.##")
        inp(ws, f"I{r}", 0, "0.##")
        ws[f"H{r}"].fill = F_RES
        ws[f"I{r}"].fill = F_RES
        calc(ws, f"N{r}", f'=IF($D$4="Sí",0,1)', "0")
    head(ws, 8, 14, ["Máx x(hasta→desde)"])
    seccion(ws, "P3", "Función objetivo")
    label(ws, "P4", "Distancia total (minimizar):", bold=True)
    calc(ws, "S4", "=SUMPRODUCT($G$9:$G$38,$H$9:$H$38+$I$9:$I$38)", "#,##0.##", res=True)
    seccion(ws, "P6", "Balance de cada nodo")
    head(ws, 7, 16, ["Nodo", "Sale − Entra", "Requerido"])
    for i in range(NN):
        r = 8 + i
        nm = f"$B${9 + i}"
        calc(ws, f"P{r}", f'=IF({nm}="","",{nm})', center=True, bold=True)
        calc(ws, f"Q{r}", f'=IF({nm}="",0,SUMIF($E$9:$E$38,{nm},$H$9:$H$38)+SUMIF($F$9:$F$38,{nm},$I$9:$I$38)-SUMIF($F$9:$F$38,{nm},$H$9:$H$38)-SUMIF($E$9:$E$38,{nm},$I$9:$I$38))', "0.##")
        calc(ws, f"R{r}", f'=IF({nm}="",0,IF({nm}=$B$4,1,IF({nm}=$B$5,-1,0)))', "0")
    marcar_rojo(ws, "Q8:Q19", "ABS(Q8-R8)>0.000001")
    calc(ws, "P21", '=IF(SUMPRODUCT(ABS(Q8:Q19-R8:R19))<0.000001,"✓ Balance correcto. Arcos usados: los que tienen x = 1. Distancia = "&S4,"⚠ Balance incorrecto: corre Solver")', res=True)
    ws.merge_cells("P21:V21")
    seccion(ws, "P23", "Solver")
    pasos = [
        "Objetivo: $S$4 → Mín.   Cambiando: $H$9:$I$38",
        "Restricciones: $Q$8:$Q$19 = $R$8:$R$19 ;  $I$9:$I$38 <= $N$9:$N$38 ;  $H$9:$I$38 <= 1",
        "No negativas, Simplex LP (Excel) o motor lineal (LibreOffice).",
        "Arcos sin usar: deja vacía la distancia (vale 0) pero también su 'Desde/Hasta', o bórralos.",
    ]
    for k, p in enumerate(pasos):
        label(ws, f"P{24 + k}", p, size=9)
    anchos(ws, {"A": 12, "B": 9, "C": 10, "D": 5, "E": 9, "F": 9, "G": 11, "H": 12, "I": 12, "J": 8, "K": 8, "L": 30, "M": 3,
                "N": 10, "O": 3, "P": 12, "Q": 12, "R": 11})

    inicio(wb, "Solucionador · Modelos de redes",
           "Ruta más corta y árbol de expansión mínima se resuelven automáticamente con fórmulas (hasta 12 nodos y 30 arcos). "
           "Flujo máximo (y la ruta más corta como PL) quedan formulados como programación lineal listos para Solver.",
           [("Ruta mas corta", "Floyd–Warshall: distancia y ruta entre cualquier par; tabla desde el origen (como Dijkstra)."),
            ("Arbol expansion minima", "Prim paso a paso: arcos elegidos, costo total."),
            ("Flujo maximo", "Modelo PL con arco ficticio; instrucciones para Solver de Excel y LibreOffice."),
            ("Ruta corta PL", "Formulación de ruta más corta como PL (por si la piden)."),
            ("Formulario", "Algoritmos y formulaciones.")])
    formulario(wb, "Formulario · Modelos de redes", [
        ("Ruta más corta (Dijkstra)", [
            ("Etiquetas", "Etiqueta de j = [distancia acumulada, nodo anterior]. Distancia(j) = min( distancia(i) + dᵢⱼ )"),
            ("Procedimiento", "1) Origen = 0 permanente. 2) Actualiza vecinos del último permanente. 3) La menor etiqueta temporal se vuelve permanente. 4) Repite hasta el destino."),
            ("Floyd–Warshall", "Dₖ(i,j) = min( Dₖ₋₁(i,j) , Dₖ₋₁(i,k) + Dₖ₋₁(k,j) ) para k = 1..n"),
            ("Como PL", "Min Σ dᵢⱼxᵢⱼ ;  Σ xₒⱼ = 1 (origen) ;  Σ xᵢₜ = 1 (destino) ;  Σentra = Σsale (intermedios) ;  xᵢⱼ ≥ 0"),
        ]),
        ("Árbol de expansión mínima", [
            ("Prim", "1) Empieza en cualquier nodo. 2) Agrega el arco más barato que conecte un nodo conectado con uno no conectado. 3) Repite n−1 veces."),
            ("Kruskal", "Ordena arcos de menor a mayor y agrégalos si no forman ciclo, hasta tener n−1 arcos."),
        ]),
        ("Flujo máximo", [
            ("Como PL", "Max f ;  0 ≤ xᵢⱼ ≤ capᵢⱼ ;  Σentra − Σsale = 0 en cada nodo (con arco ficticio sumidero→fuente de flujo f)"),
            ("Ford–Fulkerson", "1) Encuentra una ruta de la fuente al sumidero con capacidad residual > 0. 2) Envía el mínimo residual. 3) Actualiza residuales (y sentido contrario). 4) Repite."),
            ("Corte mínimo", "Flujo máximo = capacidad del corte mínimo"),
        ]),
    ])
    wb.save(ruta)
