"""2_Colas.xlsx: M/M/1, M/M/s, capacidad finita, población finita, M/G/1 y M/D/1, comparador de costos."""
from comun import *

NT = 101  # filas de tablas auxiliares n = 0..100


def _entradas_basicas(lam, mu, unidad="hora", extra=()):
    return [
        "Datos",
        R("u", "Unidad de tiempo", unidad, "texto", "in", "@"),
        R("lam", "Tasa de llegadas λ", lam, '="clientes por "&{u}', "in", "0.0000"),
        R("mu", "Tasa de servicio μ (por servidor)", mu, '="clientes por "&{u}', "in", "0.0000"),
        *extra,
    ]


def _conv():
    return [
        R("cf", "Factor para convertir tiempos (opcional)", 60, "ej. 60 = horas→minutos", "in", "0.####"),
        R("cn", "Nombre de la unidad convertida", "minutos", "texto", "in", "@"),
    ]


def _tabla_pn(ws, r0, c0, n_hasta, p_formula, titulo="Distribución del número de clientes en el sistema"):
    """Tabla n | Pn | P(N≤n) | P(N>n). p_formula(nref) devuelve la fórmula de Pn."""
    seccion(ws, f"{CL(c0)}{r0 - 1}", titulo)
    head(ws, r0, c0, ["n", "Pₙ", "P(N ≤ n)", "P(N > n)"])
    for k in range(n_hasta + 1):
        r = r0 + 1 + k
        nref = f"{CL(c0)}{r}"
        calc(ws, nref, k, "0", center=True)
        calc(ws, f"{CL(c0 + 1)}{r}", p_formula(nref), "0.0000")
        calc(ws, f"{CL(c0 + 2)}{r}", f"=SUM({CL(c0 + 1)}${r0 + 1}:{CL(c0 + 1)}{r})", "0.0000")
        calc(ws, f"{CL(c0 + 3)}{r}", f"=1-{CL(c0 + 2)}{r}", "0.0000")


def _anchos(ws):
    anchos(ws, {"A": 40, "B": 14, "C": 20, "D": 62, "E": 3, "F": 8, "G": 12, "H": 12, "I": 12, "J": 3, "K": 8, "L": 13, "M": 13})


def generar(ruta):
    wb = libro()

    # ------------------------------------------------------------------ M/M/1
    ws = hoja(wb, "MM1", "Teoría de colas · Modelo M/M/1 (un servidor, llegadas Poisson, servicio exponencial)",
              "Ejemplo precargado: Arnold's Muffler Shop (Render): λ = 2 autos/hora, μ = 3 autos/hora.")
    f = _entradas_basicas(2, 3) + [
        R("n", "n (para Pₙ y P(N > n))", 3, "clientes", "in", "0"),
        R("t", "t (para P(W > t) y P(Wq > t))", 0.5, '={u}', "in", "0.####"),
        R("cw", "Costo de espera por cliente", 50, '="$ por "&{u}', "in", "#,##0.00"),
        R("cs", "Costo del servidor", 15, '="$ por "&{u}', "in", "#,##0.00"),
        *_conv(),
        "Resultados",
        R("rho", "Factor de utilización ρ = λ/μ", "={lam}/{mu}", "", "res", "0.0000",
          '=IF({rho}<1,"El servidor está ocupado el "&TEXT({rho},"0.00%")&" del tiempo","⚠ ρ ≥ 1: el sistema es INESTABLE (la cola crece sin límite)")'),
        R("p0", "P₀ = 1 − ρ (sistema vacío)", "=1-{rho}", "", "res", "0.0000",
          '="Probabilidad de que no haya clientes: "&TEXT({p0},"0.00%")'),
        R("L", "L = λ/(μ − λ)", "={lam}/({mu}-{lam})", "clientes", "res", "0.0000",
          '="En promedio hay "&ROUND({L},4)&" clientes en el sistema"'),
        R("Lq", "Lq = λ²/(μ(μ − λ))", "={lam}^2/({mu}*({mu}-{lam}))", "clientes", "res", "0.0000",
          '="En promedio hay "&ROUND({Lq},4)&" clientes esperando en la fila"'),
        R("W", "W = 1/(μ − λ)", "=1/({mu}-{lam})", '={u}', "res", "0.0000",
          '="Cada cliente pasa en promedio "&ROUND({W},4)&" "&{u}&" en el sistema"'),
        R("Wq", "Wq = λ/(μ(μ − λ))", "={lam}/({mu}*({mu}-{lam}))", '={u}', "res", "0.0000",
          '="Cada cliente espera en promedio "&ROUND({Wq},4)&" "&{u}&" en la fila"'),
        R("Wc", "W convertido", "={W}*{cf}", '={cn}', "calc", "0.0000"),
        R("Wqc", "Wq convertido", "={Wq}*{cf}", '={cn}', "calc", "0.0000"),
        R("pw", "Probabilidad de esperar Pw = ρ", "={rho}", "", "calc", "0.0000"),
        R("pn", "Pₙ = (1 − ρ)ρⁿ", "=(1-{rho})*{rho}^{n}", "", "calc", "0.0000",
          '="Probabilidad de que haya exactamente "&{n}&" clientes"'),
        R("pmas", "P(N > n) = ρⁿ⁺¹", "={rho}^({n}+1)", "", "calc", "0.0000",
          '="Probabilidad de que haya más de "&{n}&" clientes"'),
        R("pwt", "P(W > t) = e^(−(μ−λ)t)", "=EXP(-({mu}-{lam})*{t})", "", "calc", "0.0000"),
        R("pwqt", "P(Wq > t) = ρ·e^(−(μ−λ)t)", "={rho}*EXP(-({mu}-{lam})*{t})", "", "calc", "0.0000"),
        "Costos",
        R("ctq", "Costo total (espera en fila) = Cw·Lq + Cs", "={cw}*{Lq}+{cs}", '="$ por "&{u}', "res", "$#,##0.00"),
        R("ct", "Costo total (tiempo en sistema) = Cw·L + Cs", "={cw}*{L}+{cs}", '="$ por "&{u}', "res", "$#,##0.00"),
    ]
    rf = bloque(ws, 4, f)
    marcar_rojo(ws, rf["rho"].replace("$", ""), f'{rf["rho"]}>=1')
    _tabla_pn(ws, 5, 6, 25, lambda n: f"=IF({rf['rho']}<1,(1-{rf['rho']})*{rf['rho']}^{n},\"\")")
    _anchos(ws)

    # ------------------------------------------------------------------ M/M/s
    ws = hoja(wb, "MMs", "Teoría de colas · Modelo M/M/s (varios servidores en paralelo, una sola fila)",
              "Ejemplo precargado: Arnold's Muffler Shop con 2 mecánicos: λ = 2, μ = 3 por hora, s = 2.")
    tcol = 11  # K: tabla auxiliar n, término a^n/n!
    T_N = f"${CL(tcol)}$7:${CL(tcol)}${6 + 60}"
    T_T = f"${CL(tcol + 1)}$7:${CL(tcol + 1)}${6 + 60}"
    f = _entradas_basicas(2, 3, extra=[R("s", "Número de servidores s", 2, "servidores", "in", "0")]) + [
        R("n", "n (para Pₙ)", 2, "clientes", "in", "0"),
        R("t", "t (para P(Wq > t))", 0.1, '={u}', "in", "0.####"),
        R("cw", "Costo de espera por cliente", 50, '="$ por "&{u}', "in", "#,##0.00"),
        R("cs", "Costo por servidor", 15, '="$ por "&{u}&" (cada uno)"', "in", "#,##0.00"),
        *_conv(),
        "Resultados",
        R("a", "λ/μ", "={lam}/{mu}", "", "calc", "0.0000"),
        R("rho", "Utilización ρ = λ/(sμ)", "={lam}/({s}*{mu})", "", "res", "0.0000",
          '=IF({rho}<1,"Cada servidor está ocupado el "&TEXT({rho},"0.00%")&" del tiempo","⚠ ρ ≥ 1: sistema INESTABLE, se necesitan más servidores")'),
        R("p0", "P₀", f"=1/(SUMPRODUCT(({T_N}<{{s}})*{T_T})+{{a}}^{{s}}/FACT({{s}})*1/(1-{{rho}}))", "", "res", "0.0000",
          '="Probabilidad de que el sistema esté vacío: "&TEXT({p0},"0.00%")'),
        R("Lq", "Lq = P₀(λ/μ)ˢρ / (s!(1−ρ)²)", "={p0}*{a}^{s}*{rho}/(FACT({s})*(1-{rho})^2)", "clientes", "res", "0.0000",
          '="En promedio hay "&ROUND({Lq},4)&" clientes en la fila"'),
        R("L", "L = Lq + λ/μ", "={Lq}+{a}", "clientes", "res", "0.0000",
          '="En promedio hay "&ROUND({L},4)&" clientes en el sistema"'),
        R("Wq", "Wq = Lq/λ", "={Lq}/{lam}", '={u}', "res", "0.0000",
          '="Espera promedio en fila: "&ROUND({Wq},4)&" "&{u}'),
        R("W", "W = Wq + 1/μ", "={Wq}+1/{mu}", '={u}', "res", "0.0000",
          '="Tiempo promedio en el sistema: "&ROUND({W},4)&" "&{u}'),
        R("Wqc", "Wq convertido", "={Wq}*{cf}", '={cn}', "calc", "0.0000"),
        R("Wc", "W convertido", "={W}*{cf}", '={cn}', "calc", "0.0000"),
        R("pw", "Pw = P(esperar) = (λ/μ)ˢ/s! · 1/(1−ρ) · P₀", "={a}^{s}/FACT({s})/(1-{rho})*{p0}", "", "res", "0.0000",
          '="Probabilidad de que un cliente que llega tenga que esperar: "&TEXT({pw},"0.00%")'),
        R("pn", "Pₙ", "=IF({n}<={s},{p0}*{a}^{n}/FACT({n}),{p0}*{a}^{n}/(FACT({s})*{s}^({n}-{s})))", "", "calc", "0.0000"),
        R("pwqt", "P(Wq > t) = Pw·e^(−(sμ−λ)t)", "={pw}*EXP(-({s}*{mu}-{lam})*{t})", "", "calc", "0.0000"),
        R("ocup", "Servidores ocupados en promedio = λ/μ", "={a}", "servidores", "calc", "0.0000"),
        "Costos",
        R("ctq", "Costo total = Cw·Lq + Cs·s", "={cw}*{Lq}+{cs}*{s}", '="$ por "&{u}', "res", "$#,##0.00"),
        R("ct", "Costo total = Cw·L + Cs·s", "={cw}*{L}+{cs}*{s}", '="$ por "&{u}', "res", "$#,##0.00"),
    ]
    rf = bloque(ws, 4, f)
    marcar_rojo(ws, rf["rho"].replace("$", ""), f'{rf["rho"]}>=1')
    # tabla auxiliar
    seccion(ws, f"{CL(tcol)}5", "Auxiliar")
    head(ws, 6, tcol, ["n", "(λ/μ)ⁿ/n!"])
    for k in range(60):
        r = 7 + k
        calc(ws, f"{CL(tcol)}{r}", k, "0", center=True)
        calc(ws, f"{CL(tcol + 1)}{r}", f"={rf['a']}^{CL(tcol)}{r}/FACT({CL(tcol)}{r})", "0.000000")
    p0, a, s = rf["p0"], rf["a"], rf["s"]
    seccion(ws, "F4", "Distribución del número de clientes")
    head(ws, 5, 6, ["n", "Pₙ", "P(N ≤ n)", "P(N > n)"])
    for k in range(26):
        r = 6 + k
        calc(ws, f"F{r}", k, "0", center=True)
        calc(ws, f"G{r}", f'=IF({rf["rho"]}<1,IF(F{r}<={s},{p0}*{a}^F{r}/FACT(F{r}),{p0}*{a}^F{r}/(FACT({s})*{s}^(F{r}-{s}))),"")', "0.0000")
        calc(ws, f"H{r}", f"=SUM(G$6:G{r})", "0.0000")
        calc(ws, f"I{r}", f"=1-H{r}", "0.0000")
    _anchos(ws)

    # ------------------------------------------------------------------ Capacidad finita
    ws = hoja(wb, "Capacidad finita", "Teoría de colas · M/M/s/K (capacidad máxima K en el sistema; incluye M/M/1/K con s = 1)",
              "Los clientes que llegan cuando hay K en el sistema se pierden. Funciona incluso si λ ≥ sμ.")
    f = _entradas_basicas(2, 3, extra=[
        R("s", "Número de servidores s", 1, "servidores", "in", "0"),
        R("K", "Capacidad máxima del sistema K (≤ 100)", 4, "clientes (en fila + en servicio)", "in", "0")]) + [
        R("cw", "Costo de espera por cliente", 50, '="$ por "&{u}', "in", "#,##0.00"),
        R("cs", "Costo por servidor", 15, '="$ por "&{u}', "in", "#,##0.00"),
        R("cp", "Costo por cliente perdido (opcional)", 0, "$ por cliente", "in", "#,##0.00"),
        "Resultados",
        R("a", "λ/μ", "={lam}/{mu}", "", "calc", "0.0000"),
        R("p0", "P₀", "=1/SUM($L$6:$L$106)", "", "res", "0.0000"),
        R("pk", "P_K (probabilidad de sistema lleno / cliente rechazado)", "=INDEX($M$6:$M$106,{K}+1)", "", "res", "0.0000",
          '="El "&TEXT({pk},"0.00%")&" de los clientes que llegan se pierde"'),
        R("le", "λ efectiva = λ(1 − P_K)", "={lam}*(1-{pk})", '="clientes por "&{u}', "res", "0.0000"),
        R("perd", "Clientes perdidos = λ·P_K", "={lam}*{pk}", '="clientes por "&{u}', "calc", "0.0000"),
        R("L", "L = Σ n·Pₙ", "=SUMPRODUCT($K$6:$K$106,$M$6:$M$106)", "clientes", "res", "0.0000"),
        R("Lq", "Lq = Σ (n − s)·Pₙ  (n > s)", "=SUMPRODUCT(($K$6:$K$106>{s})*($K$6:$K$106-{s}),$M$6:$M$106)", "clientes", "res", "0.0000"),
        R("W", "W = L / λef", "={L}/{le}", '={u}', "res", "0.0000"),
        R("Wq", "Wq = Lq / λef", "={Lq}/{le}", '={u}', "res", "0.0000"),
        R("ocu", "Servidores ocupados = L − Lq", "={L}-{Lq}", "servidores", "calc", "0.0000"),
        R("ut", "Utilización = (L − Lq)/s", "=({L}-{Lq})/{s}", "", "calc", "0.00%"),
        R("pw", "P(esperar) para quien sí entra", "=SUMPRODUCT(($K$6:$K$106>={s})*($K$6:$K$106<{K}),$M$6:$M$106)/(1-{pk})", "", "calc", "0.0000"),
        "Costos",
        R("ct", "Costo total = Cw·Lq + Cs·s + Cp·λ·P_K", "={cw}*{Lq}+{cs}*{s}+{cp}*{perd}", '="$ por "&{u}', "res", "$#,##0.00"),
    ]
    rf = bloque(ws, 4, f)
    seccion(ws, "K4", "Distribución Pₙ (n = 0..K)")
    head(ws, 5, 11, ["n", "Cₙ", "Pₙ", "P(N ≤ n)"])
    s, K, a = rf["s"], rf["K"], rf["a"]
    for k in range(NT):
        r = 6 + k
        calc(ws, f"K{r}", k, "0", center=True)
        calc(ws, f"L{r}", f"=IF(K{r}>{K},0,IF(K{r}<={s},{a}^K{r}/FACT(K{r}),{a}^K{r}/(FACT({s})*{s}^(K{r}-{s}))))", "0.000000")
        calc(ws, f"M{r}", f"=L{r}*{rf['p0']}", "0.0000")
        calc(ws, f"N{r}", f'=IF(K{r}>{K},"",SUM(M$6:M{r}))', "0.0000")
    ws.conditional_formatting.add("K6:N106", FormulaRule(formula=[f"$K6>{K}"], font=Font(color="D9D9D9")))
    _anchos(ws)
    ws.column_dimensions["N"].width = 12

    # ------------------------------------------------------------------ Población finita
    ws = hoja(wb, "Poblacion finita", "Teoría de colas · Población finita M/M/s/∞/N (fuente limitada de N clientes/máquinas)",
              "λ es la tasa de llegada POR CADA unidad de la población. Ejemplo (Render): 5 impresoras, λ = 0.05 fallas/día cada una, μ = 0.5 reparaciones/día.")
    f = [
        "Datos",
        R("u", "Unidad de tiempo", "día", "texto", "in", "@"),
        R("lam", "Tasa de llegada λ por unidad de la población", 0.05, '="por "&{u}&" (cada unidad)"', "in", "0.0000"),
        R("mu", "Tasa de servicio μ (por servidor)", 0.5, '="por "&{u}', "in", "0.0000"),
        R("s", "Número de servidores s", 1, "servidores", "in", "0"),
        R("N", "Tamaño de la población N (≤ 100)", 5, "unidades", "in", "0"),
        R("cw", "Costo por unidad en el sistema (descompuesta/esperando)", 120, '="$ por "&{u}', "in", "#,##0.00"),
        R("cs", "Costo por servidor", 25, '="$ por "&{u}', "in", "#,##0.00"),
        "Resultados",
        R("a", "λ/μ", "={lam}/{mu}", "", "calc", "0.0000"),
        R("p0", "P₀", "=1/SUM($L$6:$L$106)", "", "res", "0.0000",
          '="Probabilidad de que el sistema esté vacío: "&TEXT({p0},"0.00%")'),
        R("L", "L = Σ n·Pₙ", "=SUMPRODUCT($K$6:$K$106,$M$6:$M$106)", "unidades", "res", "0.0000",
          '="En promedio hay "&ROUND({L},4)&" unidades en el sistema (en fila o en servicio)"'),
        R("Lq", "Lq = Σ (n − s)·Pₙ", "=SUMPRODUCT(($K$6:$K$106>{s})*($K$6:$K$106-{s}),$M$6:$M$106)", "unidades", "res", "0.0000"),
        R("le", "λ efectiva = λ(N − L)", "={lam}*({N}-{L})", '="por "&{u}', "calc", "0.0000"),
        R("W", "W = L / λef", "={L}/{le}", '={u}', "res", "0.0000"),
        R("Wq", "Wq = Lq / λef", "={Lq}/{le}", '={u}', "res", "0.0000"),
        R("pw", "Probabilidad de esperar P(n ≥ s)", "=SUMPRODUCT(($K$6:$K$106>={s})*1,$M$6:$M$106)", "", "calc", "0.0000"),
        R("op", "Unidades operando = N − L", "={N}-{L}", "unidades", "calc", "0.0000"),
        R("ut", "Utilización de servidores = (L − Lq)/s", "=({L}-{Lq})/{s}", "", "calc", "0.00%"),
        "Costos",
        R("ct", "Costo total = Cw·L + Cs·s", "={cw}*{L}+{cs}*{s}", '="$ por "&{u}', "res", "$#,##0.00"),
    ]
    rf = bloque(ws, 4, f)
    seccion(ws, "K4", "Distribución Pₙ (n = 0..N)")
    head(ws, 5, 11, ["n", "Cₙ", "Pₙ", "P(N ≤ n)"])
    s, N, a = rf["s"], rf["N"], rf["a"]
    for k in range(NT):
        r = 6 + k
        calc(ws, f"K{r}", k, "0", center=True)
        calc(ws, f"L{r}", f"=IF(K{r}>{N},0,IF(K{r}<={s},COMBIN({N},K{r})*{a}^K{r},PERMUT({N},K{r})/(FACT({s})*{s}^(K{r}-{s}))*{a}^K{r}))", "0.000000")
        calc(ws, f"M{r}", f"=L{r}*{rf['p0']}", "0.0000")
        calc(ws, f"N{r}", f'=IF(K{r}>{N},"",SUM(M$6:M{r}))', "0.0000")
    ws.conditional_formatting.add("K6:N106", FormulaRule(formula=[f"$K6>{N}"], font=Font(color="D9D9D9")))
    _anchos(ws)
    ws.column_dimensions["N"].width = 12

    # ------------------------------------------------------------------ M/G/1 y M/D/1
    ws = hoja(wb, "MG1 y MD1", "Teoría de colas · M/G/1 (servicio con distribución general) y M/D/1 (servicio constante)",
              "Ejemplo (Anderson, Hartlage's Seafood): λ = 0.35 clientes/min, μ = 0.5 clientes/min, σ = 1.2 min. Para M/D/1 σ = 0.")
    f = [
        "Datos",
        R("u", "Unidad de tiempo", "minuto", "texto", "in", "@"),
        R("lam", "Tasa de llegadas λ", 0.35, '="clientes por "&{u}', "in", "0.0000"),
        R("mu", "Tasa de servicio μ", 0.5, '="clientes por "&{u}', "in", "0.0000"),
        R("sg", "Desviación estándar del tiempo de servicio σ", 1.2, '={u}', "in", "0.0000"),
        "Resultados M/G/1 (Pollaczek–Khinchine)",
        R("rho", "ρ = λ/μ", "={lam}/{mu}", "", "res", "0.0000",
          '=IF({rho}<1,"Utilización del servidor: "&TEXT({rho},"0.00%"),"⚠ ρ ≥ 1: sistema INESTABLE")'),
        R("p0", "P₀ = 1 − ρ", "=1-{rho}", "", "res", "0.0000"),
        R("Lq", "Lq = (λ²σ² + ρ²) / (2(1 − ρ))", "=({lam}^2*{sg}^2+{rho}^2)/(2*(1-{rho}))", "clientes", "res", "0.0000"),
        R("L", "L = Lq + ρ", "={Lq}+{rho}", "clientes", "res", "0.0000"),
        R("Wq", "Wq = Lq/λ", "={Lq}/{lam}", '={u}', "res", "0.0000"),
        R("W", "W = Wq + 1/μ", "={Wq}+1/{mu}", '={u}', "res", "0.0000"),
        R("pw", "Pw = ρ", "={rho}", "", "calc", "0.0000"),
        "Resultados M/D/1 (mismo λ y μ, σ = 0)",
        R("Lqd", "Lq = ρ² / (2(1 − ρ))", "={rho}^2/(2*(1-{rho}))", "clientes", "res", "0.0000",
          '="Con servicio constante la fila se reduce a "&ROUND({Lqd},4)&" clientes"'),
        R("Ld", "L = Lq + ρ", "={Lqd}+{rho}", "clientes", "res", "0.0000"),
        R("Wqd", "Wq = Lq/λ", "={Lqd}/{lam}", '={u}', "res", "0.0000"),
        R("Wd", "W = Wq + 1/μ", "={Wqd}+1/{mu}", '={u}', "res", "0.0000"),
        "Comparación con M/M/1 (servicio exponencial, σ = 1/μ)",
        R("Lqm", "Lq M/M/1", "={lam}^2/({mu}*({mu}-{lam}))", "clientes", "calc", "0.0000"),
        R("Wqm", "Wq M/M/1", "={Lqm}/{lam}", '={u}', "calc", "0.0000"),
    ]
    rf = bloque(ws, 4, f)
    marcar_rojo(ws, rf["rho"].replace("$", ""), f'{rf["rho"]}>=1')
    _anchos(ws)

    # ------------------------------------------------------------------ Comparador
    ws = hoja(wb, "Comparar servidores", "Teoría de colas · ¿Cuántos servidores conviene tener? (M/M/s, costo total mínimo)",
              "Costo total = Cs·s + Cw·(Lq o L). El renglón verde es el número de servidores con menor costo.")
    f = _entradas_basicas(2, 3) + [
        R("cw", "Costo de espera por cliente", 50, '="$ por "&{u}', "in", "#,##0.00"),
        R("cs", "Costo por servidor", 15, '="$ por "&{u}', "in", "#,##0.00"),
        R("base", "Costo de espera sobre: Lq (fila) o L (sistema)", "Lq", "escribe Lq o L", "in", "@"),
        R("a", "λ/μ", "={lam}/{mu}", "", "calc", "0.0000"),
        R("best", "Número óptimo de servidores", "=INDEX($A$17:$A$31,MATCH(MIN($J$17:$J$31),$J$17:$J$31,0))", "servidores", "res", "0",
          '="Conviene tener "&{best}&" servidor(es), costo total = $"&TEXT(MIN($J$17:$J$31),"#,##0.00")&" por "&{u}'),
    ]
    rf = bloque(ws, 4, f)
    lista(ws, rf["base"].replace("$", ""), ["Lq", "L"])
    head(ws, 16, 1, ["s", "ρ", "P₀", "Lq", "L", "Wq", "W", "Costo espera", "Costo servicio", "Costo total"])
    lam, mu, a = rf["lam"], rf["mu"], rf["a"]
    for k in range(15):
        r = 17 + k
        sref = f"$A{r}"
        calc(ws, f"A{r}", k + 1, "0", center=True)
        calc(ws, f"B{r}", f"={lam}/({sref}*{mu})", "0.0000")
        ok = f"B{r}<1"
        calc(ws, f"C{r}", f'=IF({ok},1/(SUMPRODUCT(($M$17:$M$76<{sref})*$N$17:$N$76)+{a}^{sref}/FACT({sref})/(1-B{r})),"Inestable")', "0.0000")
        calc(ws, f"D{r}", f'=IF({ok},C{r}*{a}^{sref}*B{r}/(FACT({sref})*(1-B{r})^2),"")', "0.0000")
        calc(ws, f"E{r}", f'=IF({ok},D{r}+{a},"")', "0.0000")
        calc(ws, f"F{r}", f'=IF({ok},D{r}/{lam},"")', "0.0000")
        calc(ws, f"G{r}", f'=IF({ok},F{r}+1/{mu},"")', "0.0000")
        calc(ws, f"H{r}", f'=IF({ok},{rf["cw"]}*IF({rf["base"]}="L",E{r},D{r}),"")', "$#,##0.00")
        calc(ws, f"I{r}", f"={rf['cs']}*{sref}", "$#,##0.00")
        calc(ws, f"J{r}", f'=IF({ok},H{r}+I{r},"")', "$#,##0.00")
    ws.conditional_formatting.add("A17:J31", FormulaRule(formula=["AND(ISNUMBER($J17),$J17=MIN($J$17:$J$31))"],
                                                          fill=F_RES, font=Font(name=FONT, bold=True)))
    seccion(ws, "M15", "Auxiliar")
    head(ws, 16, 13, ["n", "(λ/μ)ⁿ/n!"])
    for k in range(60):
        r = 17 + k
        calc(ws, f"M{r}", k, "0", center=True)
        calc(ws, f"N{r}", f"={a}^M{r}/FACT(M{r})", "0.000000")
    anchos(ws, {"A": 40, "B": 12, "C": 18, "D": 50, "E": 12, "F": 12, "G": 12, "H": 14, "I": 14, "J": 14, "M": 8, "N": 12})

    inicio(wb, "Solucionador · Teoría de colas (líneas de espera)",
           "Calcula las medidas de desempeño (ρ, P₀, L, Lq, W, Wq, Pw, Pₙ) y costos de los modelos de colas más usados. "
           "Notación de Kendall: llegadas/servicio/servidores/capacidad/población.",
           [("MM1", "Un servidor, llegadas Poisson, servicio exponencial. Tabla Pₙ, probabilidades de tiempo, costos."),
            ("MMs", "s servidores en paralelo (Erlang C). P₀, Lq, L, Wq, W, Pw, Pₙ, costos."),
            ("Capacidad finita", "M/M/s/K (y M/M/1/K): clientes perdidos, λ efectiva."),
            ("Poblacion finita", "M/M/s/∞/N: máquinas que se descomponen, fuente limitada."),
            ("MG1 y MD1", "Servicio general con σ (Pollaczek–Khinchine) y servicio constante."),
            ("Comparar servidores", "Tabla s = 1..15 con costo total y número óptimo de servidores."),
            ("Formulario", "Fórmulas del tema.")])
    formulario(wb, "Formulario · Teoría de colas", [
        ("Relaciones generales (Little)", [
            ("Ley de Little", "L = λ·W ;  Lq = λ·Wq ;  W = Wq + 1/μ ;  L = Lq + λ/μ"),
            ("Costo total", "CT = Cs·s + Cw·Lq   (o Cw·L si el costo es por tiempo en el sistema)"),
        ]),
        ("M/M/1", [
            ("Utilización", "ρ = λ/μ  (requiere λ < μ)"),
            ("Probabilidades", "P₀ = 1 − ρ ;  Pₙ = (1 − ρ)ρⁿ ;  P(N > k) = ρᵏ⁺¹"),
            ("Medidas", "L = λ/(μ−λ) ;  Lq = λ²/(μ(μ−λ)) ;  W = 1/(μ−λ) ;  Wq = λ/(μ(μ−λ))"),
            ("Tiempos", "P(W > t) = e^(−(μ−λ)t) ;  P(Wq > t) = ρ·e^(−(μ−λ)t)"),
        ]),
        ("M/M/s", [
            ("Utilización", "ρ = λ/(sμ)  (requiere ρ < 1)"),
            ("P₀", "P₀ = 1 / [ Σₙ₌₀ˢ⁻¹ (λ/μ)ⁿ/n!  +  (λ/μ)ˢ/s! · 1/(1−ρ) ]"),
            ("Lq", "Lq = P₀ (λ/μ)ˢ ρ / ( s! (1−ρ)² )"),
            ("Pw", "Pw = (λ/μ)ˢ/s! · 1/(1−ρ) · P₀"),
            ("Pₙ", "n ≤ s: P₀(λ/μ)ⁿ/n! ;   n > s: P₀(λ/μ)ⁿ/(s!·sⁿ⁻ˢ)"),
        ]),
        ("M/M/s/K (capacidad finita)", [
            ("Pₙ", "Igual que M/M/s para n ≤ K, normalizado para que Σₙ₌₀ᴷ Pₙ = 1 ; Pₙ = 0 si n > K"),
            ("M/M/1/K", "P₀ = (1−ρ)/(1−ρᴷ⁺¹) ;  Pₙ = ρⁿP₀"),
            ("λ efectiva", "λef = λ(1 − P_K) ;  W = L/λef ;  Wq = Lq/λef"),
        ]),
        ("Población finita (N)", [
            ("M/M/1/∞/N", "P₀ = 1 / Σₙ₌₀ᴺ [N!/(N−n)!] (λ/μ)ⁿ ;  Lq = N − (λ+μ)/λ · (1−P₀) ;  L = Lq + (1−P₀)"),
            ("λ efectiva", "λef = λ(N − L) ;  Wq = Lq/λef ;  W = Wq + 1/μ"),
        ]),
        ("M/G/1 y M/D/1", [
            ("M/G/1", "Lq = (λ²σ² + ρ²) / (2(1−ρ)) ;  L = Lq + ρ ;  Wq = Lq/λ ;  W = Wq + 1/μ"),
            ("M/D/1", "Lq = ρ² / (2(1−ρ))  (la mitad que en M/M/1)"),
        ]),
    ])
    wb.save(ruta)
