"""Ejercicios resueltos (con respuesta publicada) para probar los solucionadores.
Cada ejercicio: id, tema, archivo, hoja, fuente, descripción, función que llena la copia, comprobaciones y
(opcional) un trabajo de Solver. Los valores 'esperados' se escriben tal como los publica la fuente
(como texto) para saber con cuántos decimales se redondearon."""

# ------------------------------------------------------------------ utilidades de llenado / lectura

def fila(ws, prefijo, col=1, n=1, exacto=False, desde=1, hasta=250):
    k = 0
    for r in range(desde, hasta):
        v = ws.cell(r, col).value
        if isinstance(v, str) and (v.strip() == prefijo if exacto else v.startswith(prefijo)):
            k += 1
            if k == n:
                return r
    raise KeyError(f"No encontré la etiqueta '{prefijo}' en {ws.title}")


def poner(ws, prefijo, valor, col=1, n=1, exacto=False):
    ws.cell(fila(ws, prefijo, col, n, exacto), col + 1).value = valor


def L(hoja, prefijo, col=1, n=1, exacto=False):
    """Lector: valor a la derecha de una etiqueta."""
    def f(wb):
        ws = wb[hoja]
        return ws.cell(fila(ws, prefijo, col, n, exacto), col + 1).value
    return f


def C(hoja, ref):
    return lambda wb: wb[hoja][ref].value


def RC(hoja, r, c):
    return lambda wb: wb[hoja].cell(r, c).value


def limpiar(ws, r1, c1, r2, c2):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            ws.cell(r, c).value = None


def matriz(ws, r0, c0, M):
    for i, fila_ in enumerate(M):
        for j, v in enumerate(fila_):
            ws.cell(r0 + i, c0 + j).value = v


def criticas(hoja, col_act, col_crit, r1=8, r2=37):
    def f(wb):
        ws = wb[hoja]
        return {str(ws.cell(r, col_act).value).strip().upper() for r in range(r1, r2 + 1)
                if ws.cell(r, col_crit).value == "Sí"}
    return f


def por_act(hoja, act, col, col_act=1, r1=8, r2=37):
    def f(wb):
        ws = wb[hoja]
        for r in range(r1, r2 + 1):
            if str(ws.cell(r, col_act).value).strip().upper() == act.upper():
                return ws.cell(r, col).value
        raise KeyError(act)
    return f


EJ = []


def ej(id, tema, archivo, hoja, fuente, desc, llenar, checks, solver=None):
    EJ.append(dict(id=id, tema=tema, archivo=archivo, hoja=hoja, fuente=fuente, desc=desc, llenar=llenar,
                   checks=checks, solver=solver))


F_RENDER = "Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)"
F_ANDERSON = "Anderson, Sweeney & Williams, Métodos cuantitativos para los negocios 11a ed. (libros/ de tu carpeta)"
F_LOCAL = "Presentaciones/problemas-resueltos-de-investigación-de-operaciones.pdf (tu carpeta)"
F_UTP_MK = "R. Caballero, UTP Panamá, Lectura 3 Cadenas de Markov — academia.utp.ac.pa/sites/default/files/docente/541/03_cadenas_de_markov.pdf"
F_UTP_ID = "R. Caballero, UTP Panamá, Lectura 4 Inventarios determinísticos — academia.utp.ac.pa/sites/default/files/docente/541/l4_modelos_de_inventario_deterministico.pdf"
F_UTP_IP = "R. Caballero, UTP Panamá, Lectura 5 Inventarios probabilísticos — academia.utp.ac.pa/sites/default/files/docente/541/05_modelos_de_inventario_probabilistico.pdf"
F_UAH = "Universidad de Alcalá, Sistemas de colas (Baron cap. 7) — hilera.web.uah.es/estadistica/teoria/t5/t52.pdf"
F_PDM = "Plan de Mejora, Ruta crítica: ejercicios resueltos PERT/CPM — ejloorc.github.io/Portafolio-An-lisisyE-Loor.E/RUTA_CRITICA.pdf"

# ================================================================== MARKOV
MK = "1_Markov.xlsx"


def mk_pasos(nombres, P, pi0, n):
    def f(wb):
        ws = wb["Matriz P"]
        limpiar(ws, 8, 2, 15, 10)
        limpiar(ws, 29, 3, 29, 10)
        ws["B4"] = len(P)
        for i, nm in enumerate(nombres):
            ws.cell(8 + i, 2).value = nm
        matriz(ws, 8, 3, P)
        for j, v in enumerate(pi0):
            ws.cell(29, 3 + j).value = v
        ws["B32"] = n
    return f


def mk_abs(nombres, P, montos):
    def f(wb):
        ws = wb["Absorbente"]
        limpiar(ws, 8, 2, 15, 10)
        limpiar(ws, 84, 2, 91, 2)
        ws["B4"] = len(P)
        for i, nm in enumerate(nombres):
            ws.cell(8 + i, 2).value = nm
        matriz(ws, 8, 3, P)
        for i, m in enumerate(montos):
            ws.cell(84 + i, 2).value = m
    return f


def pi_t(t, j):      # evolución π(t), estado j (1..)
    return RC("Matriz P", 57 + t, 2 + j)


def pi_e(j):         # estado estable
    return RC("Estado estable", 16 + j, 2)


def rec(j):
    return RC("Estado estable", 16 + j, 4)


ej("MK1", "Markov", MK, "Matriz P", F_UTP_MK, "Ej. 5 Tiendas de abarrotes: π(1)",
   mk_pasos(["American", "Food Mart", "Atlas"], [[.8, .1, .1], [.1, .7, .2], [.2, .2, .6]], [.4, .3, .3], 1),
   [("π1(1)", pi_t(1, 1), "0.41"), ("π2(1)", pi_t(1, 2), "0.31"), ("π3(1)", pi_t(1, 3), "0.28")])

ej("MK2", "Markov", MK, "Matriz P", F_UTP_MK, "Ej. 6 Fresadora: π(1), π(2) y estado estable",
   mk_pasos(["Funciona", "No funciona"], [[.8, .2], [.1, .9]], [1, 0], 2),
   [("π(1) funciona", pi_t(1, 1), "0.8"), ("π(2) funciona", pi_t(2, 1), "0.66"), ("π(2) no funciona", pi_t(2, 2), "0.34"),
    ("π1 estable", pi_e(1), "0.33333333"), ("π2 estable", pi_e(2), "0.66666667")])


def mk3_llenar(wb):
    mk_pasos(["Buena", "Regular", "Mala"], [[.3, .6, .1], [.1, .6, .3], [.05, .4, .55]], [1, 0, 0], 8)(wb)
    ws = wb["Estado estable"]
    for i, c in enumerate([100, 125, 160]):
        ws.cell(17 + i, 5).value = c


ej("MK3", "Markov", MK, "Matriz P", F_UTP_MK, "Ej. 7 Jardinero: π(n), estado estable, recurrencia, costo y primer paso",
   mk3_llenar,
   [("π(1) buena", pi_t(1, 1), "0.30"), ("π(1) regular", pi_t(1, 2), "0.60"),
    ("π(8) buena", pi_t(8, 1), "0.101753"), ("π(8) regular", pi_t(8, 2), "0.525514"), ("π(8) mala", pi_t(8, 3), "0.372733"),
    ("π(16) buena", pi_t(16, 1), "0.101659"), ("π(16) regular", pi_t(16, 2), "0.52454"), ("π(16) mala", pi_t(16, 3), "0.372881"),
    ("π1 estable", pi_e(1), "0.1017"), ("π2 estable", pi_e(2), "0.5254"), ("π3 estable", pi_e(3), "0.3729"),
    ("μ11 = 1/π1", rec(1), "9.83"), ("μ22", rec(2), "1.9"), ("μ33", rec(3), "2.68"),
    ("Costo esperado fertilizante", C("Estado estable", "F25"), "135.51"),
    ("Primer paso regular→buena μ21", RC("Estado estable", 46, 2), "12.50"),
    ("Primer paso mala→buena μ31", RC("Estado estable", 47, 2), "13.34")])

ej("MK4", "Markov", MK, "Absorbente", F_UTP_MK, "Ej. 8 Cuentas por cobrar (absorbente)",
   mk_abs(["Pagada", "Incobrable", "<1 mes", "1-3 meses"], [[1, 0, 0, 0], [0, 1, 0, 0], [.6, 0, .2, .2], [.4, .1, .3, .2]], [2000, 5000]),
   [("F11", RC("Absorbente", 62, 2), "1.38"), ("F12", RC("Absorbente", 62, 3), "0.34"), ("F21", RC("Absorbente", 63, 2), "0.52"),
    ("F22", RC("Absorbente", 63, 3), "1.38"), ("FA <1 mes → pagada", RC("Absorbente", 73, 2), "0.97"),
    ("FA <1 mes → incobrable", RC("Absorbente", 73, 3), "0.03"), ("FA 1-3 → pagada", RC("Absorbente", 74, 2), "0.86"),
    ("FA 1-3 → incobrable", RC("Absorbente", 74, 3), "0.14"),
    ("$ que se pagan", C("Absorbente", "E84"), "6240"), ("$ incobrables", C("Absorbente", "F84"), "760")])

ej("MK5", "Markov", MK, "Matriz P", F_LOCAL, "Tema 3 #1: compradores (100 de 1000) en 1 y 2 meses",
   mk_pasos(["Compra", "No compra"], [[.8, .2], [.3, .7]], [.1, .9], 2),
   [("P²11", RC("Matriz P", 36, 3), "0.7"), ("P²21", RC("Matriz P", 37, 3), "0.45"),
    ("Compran mes 1 (de 1000)", lambda wb: 1000 * pi_t(1, 1)(wb), "350"),
    ("Compran mes 2 (de 1000)", lambda wb: 1000 * pi_t(2, 1)(wb), "475")])

ej("MK6", "Markov", MK, "Matriz P", F_LOCAL, "Tema 3 #2: fumadores en 10,000 habitantes",
   mk_pasos(["No fuma", "≤1 paquete", ">1 paquete"], [[.93, .05, .02], [.10, .80, .10], [.05, .10, .85]], [.5, .25, .25], 1),
   [("No fuman", lambda wb: 10000 * pi_t(1, 1)(wb), "5025"), ("≤1 paquete", lambda wb: 10000 * pi_t(1, 2)(wb), "2500"),
    (">1 paquete", lambda wb: 10000 * pi_t(1, 3)(wb), "2475")])

ej("MK7", "Markov", MK, "Matriz P", F_RENDER, "Problema resuelto 15-1 Bradley School",
   mk_pasos(["Bradley", "Career", "International"], [[.65, .2, .15], [.05, .9, .05], [.1, .1, .8]], [.4, .35, .25], 1),
   [("Bradley año siguiente", pi_t(1, 1), "0.303"), ("Career año siguiente", pi_t(1, 2), "0.420"),
    ("International año siguiente", pi_t(1, 3), "0.278"),
    ("Bradley equilibrio", pi_e(1), "0.158"), ("Career equilibrio", pi_e(2), "0.579"), ("International equilibrio", pi_e(3), "0.263")])

ej("MK8", "Markov", MK, "Absorbente", F_RENDER, "Problema resuelto 15-2 Central State University (absorbente)",
   mk_abs(["Exenta", "Toma curso", "Reprobó 1er", "Reprobó 2o"], [[1, 0, 0, 0], [0, 1, 0, 0], [.8, 0, .1, .1], [.2, .2, .4, .2]], [200, 50]),
   [("F11", RC("Absorbente", 62, 2), "1.176"), ("F12", RC("Absorbente", 62, 3), "0.147"), ("F21", RC("Absorbente", 63, 2), "0.588"),
    ("F22", RC("Absorbente", 63, 3), "1.324"), ("FA11", RC("Absorbente", 73, 2), "0.971"), ("FA12", RC("Absorbente", 73, 3), "0.029"),
    ("FA21", RC("Absorbente", 74, 2), "0.735"), ("FA22", RC("Absorbente", 74, 3), "0.265"),
    ("Estudiantes exentos", C("Absorbente", "E84"), "231"), ("Toman el curso", C("Absorbente", "F84"), "19")])

# ================================================================== COLAS
QC = "2_Colas.xlsx"


def q_mm1(lam, mu, cw=0, cs=0, n=0, u="hora"):
    def f(wb):
        ws = wb["MM1"]
        poner(ws, "Unidad de tiempo", u)
        poner(ws, "Tasa de llegadas λ", lam)
        poner(ws, "Tasa de servicio μ", mu)
        poner(ws, "n (para Pₙ", n)
        poner(ws, "Costo de espera por cliente", cw)
        poner(ws, "Costo del servidor", cs)
    return f


def q_mms(lam, mu, s, cw=0, cs=0, hoja="MMs"):
    def f(wb):
        ws = wb[hoja]
        poner(ws, "Tasa de llegadas λ", lam)
        poner(ws, "Tasa de servicio μ", mu)
        poner(ws, "Número de servidores s", s)
        poner(ws, "Costo de espera por cliente", cw)
        poner(ws, "Costo por servidor", cs)
    return f


def mm1(p):
    return L("MM1", p)


def mms(p):
    return L("MMs", p)


ej("Q1", "Colas", QC, "MM1", F_UAH, "Ej. 7.4 Transmisión de mensajes (M/M/1, λ=5/min, servicio 10 s)",
   q_mm1(5, 6, u="minuto"),
   [("ρ", mm1("Factor de utilización"), "0.83"), ("L", mm1("L = λ/"), "5"), ("Lq", mm1("Lq = λ²"), "4.17"),
    ("Wq (min)", mm1("Wq = λ/"), "0.83"), ("W (min)", mm1("W = 1/"), "1")])

ej("Q2", "Colas", QC, "MM1", F_UAH, "Ej. 7.5 Mensajes con 10% más llegadas (λ=5.5/min)",
   q_mm1(5.5, 6, u="minuto"),
   [("ρ", mm1("Factor de utilización"), "0.92"), ("L", mm1("L = λ/"), "11"), ("Lq", mm1("Lq = λ²"), "10.08"),
    ("Wq (s)", lambda wb: 60 * mm1("Wq = λ/")(wb), "110"), ("W (min)", mm1("W = 1/"), "2")])

ej("Q3", "Colas", QC, "MM1", F_RENDER, "Taller de silenciadores Arnold (M/M/1) con costos",
   q_mm1(2, 3, cw=50, cs=15),
   [("L", mm1("L = λ/"), "2"), ("W (h)", mm1("W = 1/"), "1"), ("Lq", mm1("Lq = λ²"), "1.33"),
    ("Wq (min)", lambda wb: 60 * mm1("Wq = λ/")(wb), "40"), ("ρ", mm1("Factor de utilización"), "0.67"), ("P0", mm1("P₀"), "0.33"),
    ("Costo diario (8 h) = 8·(Cw·Lq + Cs)", lambda wb: 8 * mm1("Costo total (espera en fila)")(wb), "653.33")])

ej("Q4", "Colas", QC, "MM1", F_RENDER, "Arnold con el mecánico rápido J. Smith (μ=4, $20/h)",
   q_mm1(2, 4, cw=50, cs=20),
   [("L", mm1("L = λ/"), "1"), ("W (h)", mm1("W = 1/"), "0.5"), ("Wq (min)", lambda wb: 60 * mm1("Wq = λ/")(wb), "15"),
    ("ρ", mm1("Factor de utilización"), "0.5"), ("P0", mm1("P₀"), "0.5"),
    ("Costo diario", lambda wb: 8 * mm1("Costo total (espera en fila)")(wb), "360")])

ej("Q5", "Colas", QC, "MMs", F_RENDER, "Arnold con dos mecánicos (M/M/2)",
   q_mms(2, 3, 2, cw=50, cs=15),
   [("P0", mms("P₀"), "0.5"), ("L", mms("L = Lq"), "0.75"), ("W (min)", lambda wb: 60 * mms("W = Wq")(wb), "22.5"),
    ("Lq", mms("Lq = P₀"), "0.083"), ("Wq (h)", mms("Wq = Lq/λ"), "0.0415"), ("Wq (min)", lambda wb: 60 * mms("Wq = Lq/λ")(wb), "2.5"),
    ("Costo diario", lambda wb: 8 * mms("Costo total = Cw·Lq")(wb), "273.20")])

ej("Q6", "Colas", QC, "MM1", F_RENDER, "Problema resuelto 13-2 Marty (M/M/1, λ=20, μ=30)",
   q_mm1(20, 30),
   [("L", mm1("L = λ/"), "2"), ("W (h)", mm1("W = 1/"), "0.1"), ("Lq", mm1("Lq = λ²"), "1.33"), ("Wq (min)", lambda wb: 60 * mm1("Wq = λ/")(wb), "4"),
    ("ρ", mm1("Factor de utilización"), "0.67"), ("P0", mm1("P₀"), "0.33"),
    ("P(n>0)", RC("MM1", 6, 9), "0.667"), ("P(n>1)", RC("MM1", 7, 9), "0.444"), ("P(n>2)", RC("MM1", 8, 9), "0.296"),
    ("P(n>3)", RC("MM1", 9, 9), "0.198"),
    ("Costo de espera diario 12 h a $0.10/min", lambda wb: 12 * 20 * 60 * mm1("Wq = λ/")(wb) * 0.10, "96")])

ej("Q7", "Colas", QC, "MMs", F_RENDER, "Problema resuelto 13-3 Marty con dos empleados (M/M/2)",
   q_mms(20, 30, 2),
   [("P0", mms("P₀"), "0.5"), ("L", mms("L = Lq"), "0.75"), ("W (h)", mms("W = Wq"), "0.0375"), ("Lq", mms("Lq = P₀"), "0.083"),
    ("Wq (min)", lambda wb: 60 * mms("Wq = Lq/λ")(wb), "0.25"), ("ρ", mms("Utilización ρ"), "0.33")])


def q_mg1(lam, mu, sg):
    def f(wb):
        ws = wb["MG1 y MD1"]
        poner(ws, "Tasa de llegadas λ", lam)
        poner(ws, "Tasa de servicio μ", mu)
        poner(ws, "Desviación estándar del tiempo", sg)
    return f


ej("Q8", "Colas", QC, "MG1 y MD1", F_RENDER, "García-Golding Recycling (M/D/1, λ=8, μ=12)",
   q_mg1(8, 12, 0),
   [("Wq (h) M/D/1", L("MG1 y MD1", "Wq = Lq/λ", n=2), "0.08333"),
    ("Costo de espera por viaje ($60/h)", lambda wb: 60 * L("MG1 y MD1", "Wq = Lq/λ", n=2)(wb), "5")])

ej("Q9", "Colas", QC, "MG1 y MD1", F_ANDERSON, "Hartlage's Seafood (M/G/1, λ=0.35, μ=0.5, σ=1.2 min)",
   q_mg1(0.35, 0.5, 1.2),
   [("P0", L("MG1 y MD1", "P₀ = 1 − ρ"), "0.30"), ("Lq", L("MG1 y MD1", "Lq = (λ²σ²"), "1.1107"),
    ("L", L("MG1 y MD1", "L = Lq + ρ"), "1.8107"), ("Wq (min)", L("MG1 y MD1", "Wq = Lq/λ"), "3.1733"), ("Pw", L("MG1 y MD1", "Pw = ρ"), "0.70")])


def q_pf(lam, mu, s, N, cw=0, cs=0):
    def f(wb):
        ws = wb["Poblacion finita"]
        poner(ws, "Tasa de llegada λ por unidad", lam)
        poner(ws, "Tasa de servicio μ", mu)
        poner(ws, "Número de servidores s", s)
        poner(ws, "Tamaño de la población N", N)
        poner(ws, "Costo por unidad en el sistema", cw)
        poner(ws, "Costo por servidor", cs)
    return f


def pf(p):
    return L("Poblacion finita", p)


ej("Q10", "Colas", QC, "Poblacion finita", F_RENDER, "Departamento de Comercio: 5 impresoras (población finita)",
   q_pf(0.05, 0.5, 1, 5, 120, 25),
   [("P0", pf("P₀"), "0.564"), ("Lq", pf("Lq = Σ"), "0.2"), ("L", pf("L = Σ"), "0.64"), ("Wq (h)", pf("Wq = Lq"), "0.91"),
    ("W (h)", pf("W = L"), "2.91"), ("Costo total por hora", pf("Costo total"), "101.80")])

ej("Q11", "Colas", QC, "Poblacion finita", F_ANDERSON, "Kolkmeyer: 6 máquinas, 1 mecánico",
   q_pf(0.05, 0.5, 1, 6),
   [("P0", pf("P₀"), "0.4845"), ("Lq", pf("Lq = Σ"), "0.3297"), ("L", pf("L = Σ"), "0.8451"), ("Wq (h)", pf("Wq = Lq"), "1.279"),
    ("W (h)", pf("W = L"), "3.279"), ("Pw", pf("Probabilidad de esperar"), "0.5155")])

ej("Q12", "Colas", QC, "Poblacion finita", F_ANDERSON, "Kolkmeyer con 2 mecánicos",
   q_pf(0.05, 0.5, 2, 6),
   [("Lq", pf("Lq = Σ"), "0.0227"), ("Wq (h)", pf("Wq = Lq"), "0.0834"), ("Pw", pf("Probabilidad de esperar"), "0.1036")])

ej("Q13", "Colas", QC, "MM1", F_ANDERSON, "Burger Dome, un canal (λ=0.75, μ=1 por min), costos Cw=$10, Cs=$7",
   q_mm1(0.75, 1, cw=10, cs=7, u="minuto"),
   [("P0", mm1("P₀"), "0.25"), ("Lq", mm1("Lq = λ²"), "2.25"), ("L", mm1("L = λ/"), "3"), ("Wq (min)", mm1("Wq = λ/"), "3"),
    ("W (min)", mm1("W = 1/"), "4"), ("Pw", mm1("Probabilidad de esperar"), "0.75"),
    ("Costo/h = Cw·L + Cs", mm1("Costo total (tiempo en sistema)"), "37.00")])

ej("Q14", "Colas", QC, "MM1", F_ANDERSON, "Burger Dome con servicio mejorado (μ=1.25/min)",
   q_mm1(0.75, 1.25, n=6, u="minuto"),
   [("P0", mm1("P₀"), "0.400"), ("Lq", mm1("Lq = λ²"), "0.900"), ("L", mm1("L = λ/"), "1.500"),
    ("P(7 o más) = P(N>6)", mm1("P(N > n)"), "0.028")])

ej("Q15", "Colas", QC, "MMs", F_ANDERSON, "Burger Dome con dos canales (M/M/2)",
   q_mms(0.75, 1, 2, cw=10, cs=7),
   [("P0", mms("P₀"), "0.4545"), ("Lq", mms("Lq = P₀"), "0.1227"), ("L", mms("L = Lq"), "0.8727"), ("Wq (min)", mms("Wq = Lq/λ"), "0.1636"),
    ("Pw", mms("Pw = P(esperar)"), "0.2045"), ("Costo/h = Cw·L + Cs·s", mms("Costo total = Cw·L +"), "22.73")])


def q_cap(lam, mu, s, K):
    def f(wb):
        ws = wb["Capacidad finita"]
        poner(ws, "Tasa de llegadas λ", lam)
        poner(ws, "Tasa de servicio μ", mu)
        poner(ws, "Número de servidores s", s)
        poner(ws, "Capacidad máxima del sistema K", K)
    return f


ej("Q16", "Colas", QC, "Capacidad finita", F_ANDERSON, "Microdata: 3 líneas sin espera (M/M/3/3)",
   q_cap(12, 6, 3, 3), [("P3 (llamadas bloqueadas)", L("Capacidad finita", "P_K"), "0.2105")])

ej("Q17", "Colas", QC, "Capacidad finita", F_ANDERSON, "Microdata con 4 líneas (M/M/4/4)",
   q_cap(12, 6, 4, 4),
   [("P4 (bloqueadas)", L("Capacidad finita", "P_K"), "0.0952"), ("L (líneas ocupadas)", L("Capacidad finita", "L = Σ"), "1.8095"),
    ("P0", RC("Capacidad finita", 6, 13), "0.1429"), ("P1", RC("Capacidad finita", 7, 13), "0.2857"),
    ("P2", RC("Capacidad finita", 8, 13), "0.2857"), ("P3", RC("Capacidad finita", 9, 13), "0.1905")])


def q_comp(lam, mu, cw, cs, base):
    def f(wb):
        ws = wb["Comparar servidores"]
        poner(ws, "Tasa de llegadas λ", lam)
        poner(ws, "Tasa de servicio μ", mu)
        poner(ws, "Costo de espera por cliente", cw)
        poner(ws, "Costo por servidor", cs)
        poner(ws, "Costo de espera sobre", base)
    return f


ej("Q18", "Colas", QC, "Comparar servidores", F_RENDER, "Arnold: ¿1 o 2 mecánicos? (costo con Lq)",
   q_comp(2, 3, 50, 15, "Lq"),
   [("Óptimo", L("Comparar servidores", "Número óptimo"), "2"), ("Costo diario s=1", lambda wb: 8 * wb["Comparar servidores"]["J17"].value, "653.33"),
    ("Costo diario s=2", lambda wb: 8 * wb["Comparar servidores"]["J18"].value, "273.20")])

ej("Q19", "Colas", QC, "Comparar servidores", F_ANDERSON, "Burger Dome: 1 vs 2 canales (costo con L)",
   q_comp(0.75, 1, 10, 7, "L"),
   [("Óptimo", L("Comparar servidores", "Número óptimo"), "2"), ("Costo s=1", C("Comparar servidores", "J17"), "37.00"),
    ("Costo s=2", C("Comparar servidores", "J18"), "22.73")])

# ================================================================== INVENTARIOS
IV = "3_Inventarios.xlsx"


def eoq(D, S, H=None, I=None, Cu=None, dias=250, LT=0):
    def f(wb):
        ws = wb["EOQ"]
        poner(ws, "Demanda (D)", D)
        poner(ws, "Costo de ordenar (S)", S)
        poner(ws, "Costo unitario del artículo (C)", Cu)
        poner(ws, "Tasa de costo de mantener (I)", I)
        poner(ws, "Costo de mantener H (directo)", H)
        poner(ws, "Días hábiles por año", dias)
        poner(ws, "Tiempo de entrega (L)", LT)
    return f


def e(p):
    return L("EOQ", p)


ej("I1", "Inventarios", IV, "EOQ", F_UTP_ID, "Ej. 2 Bebidas Nacionales (EOQ, H = 25% de $8)",
   eoq(104000, 32, I=0.25, Cu=8, dias=250, LT=2),
   [("Q*", e("Cantidad óptima"), "1824"), ("Costo total (ordenar + mantener)", e("Costo total de inventario"), "3648.56"),
    ("Punto de reorden", e("Punto de reorden"), "832"), ("Pedidos por año", e("Número esperado"), "57"),
    ("Tiempo entre pedidos (días)", e("Tiempo entre órdenes"), "4.39")])

ej("I2", "Inventarios", IV, "EOQ", F_UTP_ID, "Ej. 3 Carcasas para bomba (EOQ)",
   eoq(1000, 10, H=0.5, dias=250),
   [("Q*", e("Cantidad óptima"), "200"), ("N", e("Número esperado"), "5"), ("T (días)", e("Tiempo entre órdenes"), "50"),
    ("Inventario promedio", e("Inventario promedio"), "100"), ("Costo total", e("Costo total de inventario"), "100")])

ej("I3", "Inventarios", IV, "EOQ", F_RENDER, "Problema resuelto 6-1 Patterson Electronics (EOQ)",
   eoq(250, 20, H=1),
   [("Q*", e("Cantidad óptima"), "100"), ("Órdenes por año", e("Número esperado"), "2.5"),
    ("Inventario promedio (el libro imprime 500 por errata: Q/2 = 100/2 = 50)", e("Inventario promedio"), "50")])

ej("I4", "Inventarios", IV, "EOQ", F_RENDER, "Problema resuelto 6-4 F.W. Harris: punto de reorden (d=25/día, L=20)",
   eoq(6250, 10, H=1, dias=250, LT=20), [("Punto de reorden", e("Punto de reorden"), "500")])


def falt(D, S, B, H=None, I=None, Cu=None, dias=250):
    def f(wb):
        ws = wb["EOQ faltantes"]
        poner(ws, "Demanda (D)", D)
        poner(ws, "Costo de ordenar (S)", S)
        poner(ws, "Costo unitario del artículo (C)", Cu)
        poner(ws, "Tasa de costo de mantener (I)", I)
        poner(ws, "Costo de mantener H (directo)", H)
        poner(ws, "Costo de faltante", B)
        poner(ws, "Días hábiles por año", dias)
    return f


ej("I5", "Inventarios", IV, "EOQ faltantes", F_UTP_ID, "Ej. 6 Compañía de radio con faltantes planeados",
   falt(2000, 25, 30, I=0.2, Cu=50),
   [("Q*", L("EOQ faltantes", "Q* ="), "115"), ("Faltantes planeados", L("EOQ faltantes", "Faltante máximo"), "29"),
    ("Inventario máximo", L("EOQ faltantes", "Inventario máximo"), "86"), ("Tiempo de ciclo (días)", L("EOQ faltantes", "Tiempo de ciclo"), "14"),
    ("Costo total", L("EOQ faltantes", "Costo total = CO + CM + CF"), "867")])


def desc(D, S, I, rangos, dias=250):
    def f(wb):
        ws = wb["Descuentos"]
        poner(ws, "Demanda (D)", D)
        poner(ws, "Costo de ordenar (S)", S)
        poner(ws, "Tasa de costo de mantener (I)", I)
        poner(ws, "H fijo", None)
        poner(ws, "Días hábiles por año", dias)
        limpiar(ws, 15, 2, 20, 4)
        for k, (a, b, p) in enumerate(rangos):
            ws.cell(15 + k, 2).value, ws.cell(15 + k, 3).value, ws.cell(15 + k, 4).value = a, b, p
    return f


ej("I6", "Inventarios", IV, "Descuentos", F_UTP_ID + " / " + F_RENDER, "Ej. 7 Autos de juguete (Brass Department Store)",
   desc(5000, 49, 0.2, [(0, 999, 5), (1000, 1999, 4.8), (2000, None, 4.75)]),
   [("Q* precio $5", C("Descuentos", "F15"), "700"), ("Q* precio $4.80", C("Descuentos", "F16"), "714"),
    ("Q* precio $4.75", C("Descuentos", "F17"), "718"), ("Q ajustada 2", C("Descuentos", "G16"), "1000"),
    ("Q ajustada 3", C("Descuentos", "G17"), "2000"), ("CT rango 1", C("Descuentos", "K15"), "25700"),
    ("CT rango 2", C("Descuentos", "K16"), "24725"), ("CT rango 3", C("Descuentos", "K17"), "24822.50"),
    ("Cantidad elegida", L("Descuentos", "Cantidad a ordenar Q"), "1000")])

ej("I7", "Inventarios", IV, "Descuentos", F_RENDER, "Problema resuelto 6-3 Distribuidores Dorsey (5% de descuento desde 300)",
   desc(1400, 25, 0.2, [(0, 299, 400), (300, None, 380)]),
   [("EOQ sin descuento", C("Descuentos", "F15"), "29.6"), ("EOQ con descuento", C("Descuentos", "F16"), "30.3"),
    ("CT sin descuento", C("Descuentos", "K15"), "562366"), ("CT con descuento", C("Descuentos", "K16"), "543517"),
    ("Cantidad elegida", L("Descuentos", "Cantidad a ordenar Q"), "300")])


def poq(D, S, p, H=None, I=None, Cu=None, d=None, dias=250, LT=0):
    def f(wb):
        ws = wb["POQ"]
        poner(ws, "Demanda (D)", D)
        poner(ws, "Costo de preparación", S)
        poner(ws, "Costo unitario del artículo (C)", Cu)
        poner(ws, "Tasa de costo de mantener (I)", I)
        poner(ws, "Costo de mantener H (directo)", H)
        poner(ws, "Días hábiles por año", dias)
        poner(ws, "Tasa de producción (p)", p)
        poner(ws, "Tasa de demanda diaria (d)", d)
        poner(ws, "Tiempo de entrega", LT)
    return f


def pq(p):
    return L("POQ", p)


ej("I8", "Inventarios", IV, "POQ", F_UTP_ID, "Ej. 4 Jabón de tocador (POQ, capacidad 60,000/año)",
   poq(26000, 135, 60000 / 250, I=0.24, Cu=4.5, dias=250, LT=5),
   [("Q*", pq("Q* ="), "3387"), ("Punto de reorden", pq("Punto de reorden"), "520"), ("Tiempo de ciclo (días)", pq("Tiempo de ciclo T"), "33")])

ej("I9", "Inventarios", IV, "POQ", F_UTP_ID, "Ej. 5 Brown Manufacturing (POQ, d=60, p=80)",
   poq(10000, 100, 80, H=0.5, d=60),
   [("Q*", pq("Q* ="), "4000"), ("Duración de la producción (días)", pq("Tiempo de producción t"), "50"), ("Corridas por año", pq("Corridas por año"), "2.5")])

ej("I10", "Inventarios", IV, "POQ", F_RENDER, "Problema resuelto 6-2 Flemming Accessories (POQ)",
   poq(6750, 150, 125, H=1, d=30), [("Q*", pq("Q* ="), "1632")])


def rcont(d, sd, LT, ns, H=1, S=1):
    def f(wb):
        ws = wb["Revision continua"]
        poner(ws, "Demanda promedio por periodo (d)", d)
        poner(ws, "Desviación estándar de la demanda (σd)", sd)
        poner(ws, "Tiempo de entrega promedio (LT)", LT)
        poner(ws, "Costo de ordenar (S)", S)
        poner(ws, "Costo unitario (C)", 1)
        poner(ws, "Tasa de mantener (I)", None)
        poner(ws, "H directo", H)
        poner(ws, "Nivel de servicio", ns)
    return f


ej("I11", "Inventarios", IV, "Revision continua", F_UTP_IP, "Ej. 1 Hospital Regional: equipos código azul (5% de faltantes)",
   rcont(350, 10, 1, 0.95),
   [("Inventario de seguridad (Z tabla = 1.65)", L("Revision continua", "Inventario de seguridad SS"), "16.5"),
    ("Punto de reorden", L("Revision continua", "Punto de reorden R"), "366.5")])

ej("I12", "Inventarios", IV, "Revision continua", F_RENDER, "Problema resuelto 6-5 Thayer & Thaht (96% de servicio)",
   rcont(1000, 200, 1, 0.96, H=4),
   [("Inventario de seguridad (Z tabla = 1.75; el libro imprime 375 por errata, sus cuentas usan 350)",
     L("Revision continua", "Inventario de seguridad SS"), "350"),
    ("Punto de reorden", L("Revision continua", "Punto de reorden R"), "1350"),
    ("Costo de mantener el inventario de seguridad (parte de los $11,400)", L("Revision continua", "Costo de mantener SS"), "1400")])


def rper(d, sd, R, LT, ns, Ia=0):
    def f(wb):
        ws = wb["Revision periodica"]
        poner(ws, "Demanda promedio por periodo (d)", d)
        poner(ws, "Desviación estándar de la demanda por periodo", sd)
        poner(ws, "Periodo de revisión (R)", R)
        poner(ws, "Tiempo de entrega (L)", LT)
        poner(ws, "Nivel de servicio", ns)
        poner(ws, "Inventario disponible", Ia)
    return f


ej("I13", "Inventarios", IV, "Revision periodica", F_UTP_IP, "Ej. 4 Revisión periódica: nivel de reposición con 1% de agotamiento",
   rper(250, 45, 1, 0, 0.99), [("Nivel de reposición M (Z tabla = 2.33)", L("Revision periodica", "Nivel objetivo T"), "355")])


def unper(cu, co, mu=None, sg=None, a=None, b=None):
    def f(wb):
        ws = wb["Un periodo"]
        poner(ws, "Cu directo", cu)
        poner(ws, "Co directo", co)
        poner(ws, "Media de la demanda", mu)
        poner(ws, "Desviación estándar σ", sg)
        poner(ws, "Mínimo a", a)
        poner(ws, "Máximo b", b)
    return f


def up(p):
    return L("Un periodo", p)


ej("I14", "Inventarios", IV, "Un periodo", F_UTP_IP, "Ej. 3 Car Rental: autos grandes para el fin de semana",
   unper(200, 80, 150, 14, 350, 650),
   [("Razón crítica", up("Razón crítica"), "0.7143"), ("Autos a tener (Z tabla = 0.57)", up("Q* = μ + z·σ"), "158")])
for k, (dia, m, s, q) in enumerate([("Lunes-Viernes", 422, 67, "467.56"), ("Sábado", 719, 113, "795.84"), ("Domingo", 528, 85, "585.80")]):
    ej(f"I15{'abc'[k]}", "Inventarios", IV, "Un periodo", F_UTP_IP, f"Ej. 4 Limonada de Don ({dia})",
       unper(7.5, 2.5, m, s, 350, 650),
       [("Nivel de servicio", up("Razón crítica"), "0.75"), ("Galones (Z tabla = 0.68)", up("Q* = μ + z·σ"), q)])
ej("I16", "Inventarios", IV, "Un periodo", F_UTP_IP, "Ej. 5 Zapatería con demanda uniforme 350–650",
   unper(20, 10, 500, 1, 350, 650), [("Q (uniforme)", up("Q* = a + P"), "550")])
ej("I17", "Inventarios", IV, "Un periodo", F_UTP_IP, "Ej. 6 Muffins (uniforme 30–50 y normal μ=40, σ=5)",
   unper(0.6, 0.2, 40, 5, 30, 50),
   [("Nivel de servicio", up("Razón crítica"), "0.75"), ("Q uniforme", up("Q* = a + P"), "45"), ("Q normal (Z tabla = 0.68)", up("Q* = μ + z·σ"), "43.4")])

# ================================================================== REDES
RD = "4_Redes.xlsx"

N_LOCAL = ["O", "A", "B", "C", "D", "E", "F", "G", "H", "I", "T"]
A_LOCAL_RC = [("O", "A", 4), ("O", "C", 6), ("O", "B", 3), ("A", "D", 3), ("A", "C", 5), ("D", "G", 4), ("D", "C", 2),
              ("D", "F", 2), ("G", "F", 2), ("G", "H", 2), ("G", "T", 7), ("C", "F", 2), ("C", "B", 4), ("C", "E", 5),
              ("F", "H", 5), ("F", "E", 1), ("H", "E", 2), ("H", "T", 8), ("H", "I", 3), ("B", "E", 6), ("E", "I", 5), ("I", "T", 4)]
N_LOCAL_FM = ["AI", "B", "C", "D", "E", "F", "GT"]
A_LOCAL_FM = [("AI", "B", 6), ("AI", "C", 4), ("AI", "D", 1), ("B", "E", 4), ("C", "E", 1), ("C", "F", 3), ("C", "D", 3),
              ("D", "F", 4), ("E", "GT", 4), ("F", "GT", 9)]
N_LOCAL_MST = ["1", "2", "3", "4", "5"]
A_LOCAL_MST = [("1", "2", 5), ("1", "3", 3), ("1", "5", 5), ("2", "3", 5), ("2", "4", 7), ("2", "5", 7), ("3", "4", 4),
               ("3", "5", 3), ("4", "5", 5)]
N_R111 = [str(i) for i in range(1, 9)]
A_R111 = [("1", "2", 10), ("1", "3", 8), ("1", "4", 12), ("2", "5", 12), ("2", "6", 18), ("3", "6", 15), ("4", "6", 12),
          ("4", "7", 8), ("5", "6", 10), ("5", "8", 13), ("6", "8", 9), ("6", "7", 10), ("7", "8", 14)]
N_R113 = [str(i) for i in range(1, 8)]
A_R113 = [("1", "2", 8), ("1", "3", 16), ("1", "4", 18), ("2", "3", 6), ("2", "5", 14), ("3", "4", 8), ("3", "6", 12),
          ("4", "6", 16), ("5", "6", 10), ("5", "7", 12), ("6", "7", 6)]
# Render 11-2 (PetroChem): capacidad en cada sentido leída de la figura 11.17 (número junto al nodo de salida)
A_R112 = [("1", "2", 4), ("1", "5", 5), ("5", "1", 1), ("1", "3", 8), ("2", "4", 3), ("4", "2", 3), ("2", "5", 3),
          ("4", "5", 3), ("4", "7", 4), ("7", "4", 2), ("5", "7", 5), ("7", "5", 1), ("3", "5", 3), ("5", "3", 2),
          ("3", "6", 1), ("6", "3", 1), ("5", "6", 1), ("6", "5", 4), ("6", "7", 6)]


def red(hoja, nodos, arcos, extra=None):
    def f(wb):
        ws = wb[hoja]
        limpiar(ws, 9, 2, 20, 2)
        limpiar(ws, 9, 5, 38, 7)
        for i, n in enumerate(nodos):
            ws.cell(9 + i, 2).value = n
        for k, (a, b, w) in enumerate(arcos):
            ws.cell(9 + k, 5).value, ws.cell(9 + k, 6).value, ws.cell(9 + k, 7).value = a, b, w
        for ref, v in (extra or {}).items():
            ws[ref] = v
    return f


def ruta_txt(wb):
    return wb["Ruta mas corta"]["L28"].value


def dist_nodo(nodo):
    def f(wb):
        ws = wb["Ruta mas corta"]
        for r in range(13, 25):
            if str(ws.cell(r, 11).value) == nodo:
                return ws.cell(r, 12).value
    return f


ej("N1", "Redes", RD, "Ruta mas corta", F_LOCAL, "Tema 1 #1: ruta más corta de O a T (11 nodos)",
   red("Ruta mas corta", N_LOCAL, A_LOCAL_RC, {"B5": "No", "L4": "O", "L5": "T"}),
   [("Distancia mínima", C("Ruta mas corta", "L27"), "17"), ("Ruta", ruta_txt, "O-C-F-G-T"),
    ("Distancia a A", dist_nodo("A"), "4"), ("a B", dist_nodo("B"), "3"), ("a C", dist_nodo("C"), "6"), ("a D", dist_nodo("D"), "7"),
    ("a E", dist_nodo("E"), "9"), ("a F", dist_nodo("F"), "8"), ("a G", dist_nodo("G"), "10"), ("a H", dist_nodo("H"), "11"),
    ("a I", dist_nodo("I"), "14")])

ej("N2", "Redes", RD, "Ruta mas corta", F_RENDER, "Problema resuelto 11-3 Leadville → Dillon",
   red("Ruta mas corta", N_R113, A_R113, {"B5": "No", "L4": "1", "L5": "7"}),
   [("Distancia mínima", C("Ruta mas corta", "L27"), "32"), ("Ruta", ruta_txt, "1-2-3-6-7"),
    ("Distancia a 2", dist_nodo("2"), "8"), ("a 3", dist_nodo("3"), "14"), ("a 4", dist_nodo("4"), "18"),
    ("a 5", dist_nodo("5"), "22"), ("a 6", dist_nodo("6"), "26")])

ej("N3", "Redes", RD, "Arbol expansion minima", F_LOCAL, "Tema 1 #3: líneas telefónicas en 5 subdivisiones",
   red("Arbol expansion minima", N_LOCAL_MST, A_LOCAL_MST, {"B5": "1"}),
   [("Longitud mínima (km)", C("Arbol expansion minima", "N17"), "15")])

ej("N4", "Redes", RD, "Arbol expansion minima", F_RENDER, "Problema resuelto 11-1 Granja de Roxie LaMothe",
   red("Arbol expansion minima", N_R111, A_R111, {"B5": "1"}),
   [("Distancia total", C("Arbol expansion minima", "N17"), "67"),
    ("Arcos elegidos", lambda wb: {"-".join(sorted([str(wb["Arbol expansion minima"].cell(r, 12).value), str(wb["Arbol expansion minima"].cell(r, 13).value)]))
                                   for r in range(5, 12)}, {"1-3", "1-2", "1-4", "4-7", "6-7", "6-8", "5-6"})])

FLUJO = dict(hoja="Flujo maximo", objetivo="Q4", maximizar=True, variables=["H9:H38", "Q4"],
             restricciones=[["H9:H38", "<=", "G9:G38"], ["Q8:Q19", "=", 0]])
ej("N5", "Redes", RD, "Flujo maximo", F_LOCAL, "Tema 1 #2: flujo máximo de AI a GT (Solver)",
   red("Flujo maximo", N_LOCAL_FM, A_LOCAL_FM, {"B4": "AI", "B5": "GT"}),
   [("Flujo máximo", C("Flujo maximo", "Q4"), "9"), ("Verificación", C("Flujo maximo", "N21"), "✓")], solver=FLUJO)

ej("N6", "Redes", RD, "Flujo maximo", F_RENDER, "Problema resuelto 11-2 PetroChem (Solver; capacidades por sentido según la figura 11.17)",
   red("Flujo maximo", N_R113, A_R112, {"B4": "1", "B5": "7"}),
   [("Flujo máximo (miles de galones)", C("Flujo maximo", "Q4"), "10"), ("Verificación", C("Flujo maximo", "N21"), "✓")], solver=FLUJO)

RPL = dict(hoja="Ruta corta PL", objetivo="S4", maximizar=False, variables=["H9:I38"],
           restricciones=[["Q8:Q19", "=", "R8:R19"], ["I9:I38", "<=", "N9:N38"], ["H9:I38", "<=", 1]])
ej("N7", "Redes", RD, "Ruta corta PL", F_LOCAL, "Tema 1 #1 resuelto como PL con Solver",
   red("Ruta corta PL", N_LOCAL, A_LOCAL_RC, {"B4": "O", "B5": "T", "D4": "No"}),
   [("Distancia mínima", C("Ruta corta PL", "S4"), "17"), ("Verificación", C("Ruta corta PL", "P21"), "✓")], solver=RPL)
ej("N8", "Redes", RD, "Ruta corta PL", F_RENDER, "Problema resuelto 11-3 resuelto como PL con Solver",
   red("Ruta corta PL", N_R113, A_R113, {"B4": "1", "B5": "7", "D4": "No"}),
   [("Distancia mínima", C("Ruta corta PL", "S4"), "32"), ("Verificación", C("Ruta corta PL", "P21"), "✓")], solver=RPL)

# ================================================================== PERT / CPM
PC = "5_PERT_CPM.xlsx"


def cpm(acts):
    def f(wb):
        ws = wb["CPM"]
        limpiar(ws, 8, 1, 37, 4)
        for k, (a, p, d) in enumerate(acts):
            ws.cell(8 + k, 1).value, ws.cell(8 + k, 3).value, ws.cell(8 + k, 4).value = a, p, d
    return f


def pert(acts):
    def f(wb):
        ws = wb["PERT"]
        limpiar(ws, 8, 1, 37, 5)
        for k, (a, p, o, m, pe) in enumerate(acts):
            for c, v in enumerate((a, p, o, m, pe)):
                ws.cell(8 + k, 1 + c).value = v
    return f


T_CPM, T_PERT = C("CPM", "B5"), C("PERT", "B5")
CR_CPM, CR_PERT = criticas("CPM", 1, 10), criticas("PERT", 1, 13)

ej("P1", "PERT/CPM", PC, "CPM", F_PDM, "Ejercicio 1: auditoría (3 rutas críticas)",
   cpm([("a", "", 3), ("b", "a", 2), ("c", "", 5), ("d", "b, c", 2), ("e", "a", 4), ("f", "b, c", 6), ("g", "e, d", 5)]),
   [("Duración", T_CPM, "12"), ("Actividades críticas (a-e-g, a-b-d-g, c-d-g)", CR_CPM, {"A", "B", "C", "D", "E", "G"})])
ej("P2", "PERT/CPM", PC, "CPM", F_PDM, "Ejercicio 2: arranque de planta",
   cpm([("a", "", 4), ("b", "", 8), ("c", "", 3), ("d", "a", 3), ("e", "a", 6), ("f", "c", 5), ("g", "b, d", 6)]),
   [("Duración", T_CPM, "14"), ("Ruta crítica b-g", CR_CPM, {"B", "G"})])
ej("P3", "PERT/CPM", PC, "CPM", F_PDM, "Ejercicio 3: preparación de un curso",
   cpm([("a", "", 3), ("b", "", 2), ("c", "", 4), ("d", "b", 3), ("e", "b", 6), ("f", "a", 4), ("g", "c, d", 4)]),
   [("Duración", T_CPM, "9"), ("Ruta crítica b-d-g", CR_CPM, {"B", "D", "G"})])
ej("P4", "PERT/CPM", PC, "CPM", F_PDM, "Ejercicio 4: proyecto en semanas, holgura de B",
   cpm([("A", "", 3), ("B", "A", 3), ("C", "A", 7), ("D", "C", 2), ("E", "B, D", 4), ("F", "D", 3), ("G", "E, F", 7)]),
   [("Duración", T_CPM, "23"), ("Ruta crítica A-C-D-E-G", CR_CPM, {"A", "C", "D", "E", "G"}), ("Holgura de B", por_act("CPM", "B", 9), "6")])
P5 = [("A", "", 3), ("B", "A", 2), ("C", "A", 4), ("D", "A", 4), ("E", "B", 6), ("F", "C, D", 6), ("G", "D, F", 2), ("H", "D", 3), ("I", "E, G, H", 3)]
ej("P5", "PERT/CPM", PC, "CPM", F_PDM, "Ejercicio 5: sistema de comunicación (dos rutas críticas)",
   cpm(P5), [("Rutas críticas A-C-F-G-I y A-D-F-G-I", CR_CPM, {"A", "C", "D", "F", "G", "I"})])
P5b = [(a, p, d - 1 if a in "CDG" else d) for a, p, d in P5]
ej("P5b", "PERT/CPM", PC, "CPM", F_PDM, "Ejercicio 5c-d: acortar C, D y G una semana",
   cpm(P5b), [("Nueva duración", T_CPM, "16"), ("Rutas críticas A-C-F-G-I y A-D-F-G-I", CR_CPM, {"A", "C", "D", "F", "G", "I"})])
ej("P6", "PERT/CPM", PC, "CPM", F_PDM, "Ejercicio 6: Duplaga Corporation",
   cpm([("A", "", 9), ("B", "A", 7), ("C", "A", 3), ("D", "B", 6), ("E", "B", 9), ("F", "C", 4), ("G", "E, F", 6), ("H", "D", 5), ("I", "G, H", 3)]),
   [("Duración", T_CPM, "34"), ("Ruta crítica A-B-E-G-I", CR_CPM, {"A", "B", "E", "G", "I"})])
ej("P7", "PERT/CPM", PC, "CPM", F_PDM, "Ejercicio 7: Charlie Cook Corp. (holguras)",
   cpm([("A", "", 6), ("B", "", 7), ("C", "A", 3), ("D", "A", 2), ("E", "B", 4), ("F", "B", 6), ("G", "C, E", 10), ("H", "D, F", 7)]),
   [("Duración", T_CPM, "21"), ("Ruta crítica B-E-G", CR_CPM, {"B", "E", "G"}),
    ("Holgura A", por_act("CPM", "A", 9), "2"), ("Holgura C", por_act("CPM", "C", 9), "2"), ("Holgura D", por_act("CPM", "D", 9), "6"),
    ("Holgura F", por_act("CPM", "F", 9), "1"), ("Holgura H", por_act("CPM", "H", 9), "1")])
P8 = [("A", "", 3, 4, 6), ("B", "", 1, 2, 3), ("C", "A", 2, 3, 5), ("D", "A", 4, 6, 10), ("E", "A", 1, 2, 4), ("F", "B", 3, 5, 7),
      ("G", "B", 2, 4, 6), ("H", "C", 1, 3, 5), ("I", "H", 3, 5, 8), ("J", "D", 3, 5, 9), ("K", "E", 1, 2, 4), ("L", "G", 3, 6, 12),
      ("M", "L", 1, 3, 5), ("N", "I,J,K", 1, 3, 6), ("O", "", 2, 5, 9), ("P", "O", 1, 5, 8), ("Q", "O", 1, 4, 7), ("R", "O", 1, 3, 5),
      ("S", "E,P", 1, 2, 3), ("T", "R,S", 1, 2, 4), ("U", "T", 1, 3, 5), ("V", "T", 1, 3, 6), ("W", "T", 1, 4, 7), ("X", "B", 2, 4, 8),
      ("Y", "W", 1, 2, 4)]
ej("P8", "PERT/CPM", PC, "PERT", F_PDM, "Ejercicio 8: proyecto PERT de 25 actividades",
   pert(P8), [("Duración esperada (20.(3))", T_PERT, "20.3333"), ("Varianza del proyecto (4.(3))", L("PERT", "Varianza de la ruta crítica", col=16), "4.3333"),
              ("Ruta crítica O-P-S-T-W-Y", CR_PERT, {"O", "P", "S", "T", "W", "Y"})])
DW = [("A", "", 1, 2, 3), ("B", "", 2, 3, 4), ("C", "A", 4, 5, 6), ("D", "B", 8, 9, 10), ("E", "C, D", 2, 5, 8), ("F", "B", 4, 5, 6), ("G", "E", 1, 2, 3)]
dw_checks = [("Duración esperada", T_PERT, "19"), ("Varianza ruta crítica", L("PERT", "Varianza de la ruta crítica", col=16), "1.333"),
             ("Desviación estándar", L("PERT", "Desviación estándar σ", col=16), "1.155"), ("Ruta crítica B-D-E-G", CR_PERT, {"B", "D", "E", "G"})]
for act, vals in {"A": (2, 0, 2, 5, 7, 5), "B": (3, 0, 3, 0, 3, 0), "C": (5, 2, 7, 7, 12, 5), "D": (9, 3, 12, 3, 12, 0),
                  "E": (5, 12, 17, 12, 17, 0), "F": (5, 3, 8, 14, 19, 11), "G": (2, 17, 19, 17, 19, 0)}.items():
    for nombre, col, v in zip(("t", "IC", "TC", "IL", "TL", "Holgura"), (6, 8, 9, 10, 11, 12), vals):
        dw_checks.append((f"{act} {nombre}", por_act("PERT", act, col), str(v)))
ej("P9", "PERT/CPM", PC, "PERT", F_RENDER, "Problemas resueltos 12-1 y 12-2 Ensamble del ala (Scott DeWitte)", pert(DW), dw_checks)

GF = [("A", "", 1, 2, 3), ("B", "", 2, 3, 4), ("C", "A", 1, 2, 3), ("D", "B", 2, 4, 6), ("E", "C", 1, 4, 7), ("F", "C", 1, 2, 9),
      ("G", "D, E", 3, 4, 11), ("H", "F, G", 1, 2, 3)]


def gf_pert(wb):
    pert(GF)(wb)
    poner(wb["PERT"], "Fecha objetivo T", 16, col=16)


ej("P10", "PERT/CPM", PC, "PERT", F_RENDER, "General Foundry: probabilidad de terminar en 16 semanas",
   gf_pert, [("Duración esperada", T_PERT, "15"), ("Varianza del proyecto", L("PERT", "Varianza de la ruta crítica", col=16), "3.111"),
             ("Desviación estándar", L("PERT", "Desviación estándar σ", col=16), "1.76"),
             ("Z", L("PERT", "Z = (T", col=16), "0.57"), ("P(T ≤ 16) (tabla con Z = 0.57)", L("PERT", "P(terminar en ≤ T)", col=16), "0.71566")])

GF_CRASH = [("A", "", 2, 1, 22000, 23000), ("B", "", 3, 1, 30000, 34000), ("C", "A", 2, 1, 26000, 27000), ("D", "B", 4, 3, 48000, 49000),
            ("E", "C", 4, 2, 56000, 58000), ("F", "C", 3, 2, 30000, 30500), ("G", "D, E", 5, 2, 80000, 86000), ("H", "F, G", 2, 1, 16000, 19000)]


def crash(meta):
    def f(wb):
        ws = wb["Compresion"]
        limpiar(ws, 8, 1, 37, 6)
        for k, row in enumerate(GF_CRASH):
            for c, v in enumerate(row):
                ws.cell(8 + k, 1 + c).value = v
        ws["Q6"] = meta
    return f


CRASH = dict(hoja="Compresion", objetivo="Q7", maximizar=False, variables=["I8:J37"],
             restricciones=[["J8:J37", "<=", "G8:G37"], ["K8:K37", "<=", "Q6"], ["B42:AE71", ">=", 0]])
ej("P11", "PERT/CPM", PC, "Compresion", F_RENDER, "General Foundry: acelerar a 14 semanas (Solver)", crash(14),
   [("Costo de aceleración", C("Compresion", "Q7"), "1000"), ("Costo por semana de B", C("Compresion", "H9"), "2000"),
    ("Duración lograda", L("Compresion", "Duración lograda", col=16), "14")], solver=CRASH)
ej("P12", "PERT/CPM", PC, "Compresion", F_RENDER, "General Foundry: acelerar a 12 semanas (Solver)", crash(12),
   [("Costo de aceleración", C("Compresion", "Q7"), "5000"), ("Duración lograda", L("Compresion", "Duración lograda", col=16), "12"),
    ("Factible", L("Compresion", "¿Solución factible?", col=16), "✓")], solver=CRASH)

# ------------------------------------------------------------------ explicación de diferencias con la fuente
NOTAS = {
    ("MK3", "π(16) buena"): "Errata de la fuente (dígitos invertidos): el valor exacto es 6/59 = 0.101695, igual que su propio estado estable 0.1017.",
    ("MK3", "π(16) regular"): "Errata de la fuente: el valor exacto es 31/59 = 0.525424 (su estado estable dice 0.5254).",
    ("MK3", "Primer paso mala→buena μ31"): "La fuente usa la inversa redondeada (6.67 + 6.67); el exacto es 13.333.",
    ("MK4", "$ que se pagan"): "La fuente multiplica por FA redondeada a 2 decimales (0.97, 0.86).",
    ("MK4", "$ incobrables"): "Mismo redondeo de FA en la fuente.",
    ("Q5", "Wq (h)"): "El libro redondea 1/24 h = 0.041667 a 0.0415.",
    ("Q5", "Costo diario"): "El libro usa Wq = 0.0415 redondeado; con el valor exacto es $273.33.",
    ("Q18", "Costo diario s=2"): "Mismo redondeo de Wq que en Q5.",
    ("Q10", "Wq (h)"): "El libro redondea Lq = 0.2035 a 0.2 antes de dividir (0.2/0.218 = 0.917 → 0.91). Con Lq exacto: 0.2035/0.218 = 0.933. La hoja es correcta.",
    ("Q10", "W (h)"): "Arrastra el redondeo de Wq del libro.",
    ("Q10", "Costo total por hora"): "El libro usa L = 0.64 redondeado (exacto 0.6395).",
    ("I5", "Inventario máximo"): "La fuente redondea Q = 115 y B = 29 antes de restar (exacto 115.47 − 28.87 = 86.60).",
    ("I5", "Costo total"): "La fuente calcula con Q = 115 redondeado; con Q* exacto el costo es $866.03.",
    ("I11", "Inventario de seguridad (Z tabla = 1.65)"): "La fuente usa Z = 1.65 de tabla; Excel usa Z = 1.6449 exacto.",
    ("I11", "Punto de reorden"): "Misma Z de tabla.",
    ("I12", "Costo de mantener el inventario de seguridad (parte de los $11,400)"): "El libro usa Z = 1.75 de tabla (exacto 1.7507).",
    ("I15a", "Galones (Z tabla = 0.68)"): "La fuente usa Z = 0.68 de tabla; exacto 0.6745.",
    ("I15b", "Galones (Z tabla = 0.68)"): "La fuente usa Z = 0.68 de tabla; exacto 0.6745.",
    ("I15c", "Galones (Z tabla = 0.68)"): "La fuente usa Z = 0.68 de tabla; exacto 0.6745.",
    ("P10", "P(T ≤ 16) (tabla con Z = 0.57)"): "El libro redondea Z = 0.567 a 0.57 antes de buscar en la tabla.",
}
