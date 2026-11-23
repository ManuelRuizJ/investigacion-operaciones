# Reporte de pruebas de los solucionadores (23/11/2026)

Se resolvieron **67 ejercicios publicados** con una copia de los libros (carpeta `pruebas/copias/`) y se compararon **325 resultados** contra la respuesta de la fuente.

- ✅ Coinciden (dentro del redondeo con que los publica la fuente): **305**
- ≈ Diferencia menor a 1 % (la fuente usó valores redondeados, p. ej. Z de tabla): **19**
- ❌ No coinciden: **1**

Todas las diferencias (≈ y ❌) se revisaron a mano: vienen de redondeos o erratas de la fuente, no de las plantillas. La explicación está en la columna *Nota*.

Columnas: *Publicado* = respuesta de la fuente; *Solucionador* = lo que calculó la copia del libro.

## Markov

### ✅ MK1 — Ej. 5 Tiendas de abarrotes: π(1)

Fuente: R. Caballero, UTP Panamá, Lectura 3 Cadenas de Markov — academia.utp.ac.pa/sites/default/files/docente/541/03_cadenas_de_markov.pdf  
Libro / hoja: `1_Markov.xlsx` → `Matriz P` · copia: `copias/Markov/MK1.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| π1(1) | 0.41 | 0.41 | ✅ |  |
| π2(1) | 0.31 | 0.31 | ✅ |  |
| π3(1) | 0.28 | 0.28 | ✅ |  |

### ✅ MK2 — Ej. 6 Fresadora: π(1), π(2) y estado estable

Fuente: R. Caballero, UTP Panamá, Lectura 3 Cadenas de Markov — academia.utp.ac.pa/sites/default/files/docente/541/03_cadenas_de_markov.pdf  
Libro / hoja: `1_Markov.xlsx` → `Matriz P` · copia: `copias/Markov/MK2.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| π(1) funciona | 0.8 | 0.8 | ✅ |  |
| π(2) funciona | 0.66 | 0.66 | ✅ |  |
| π(2) no funciona | 0.34 | 0.34 | ✅ |  |
| π1 estable | 0.33333333 | 0.333333 | ✅ |  |
| π2 estable | 0.66666667 | 0.666667 | ✅ |  |

### ≈ MK3 — Ej. 7 Jardinero: π(n), estado estable, recurrencia, costo y primer paso

Fuente: R. Caballero, UTP Panamá, Lectura 3 Cadenas de Markov — academia.utp.ac.pa/sites/default/files/docente/541/03_cadenas_de_markov.pdf  
Libro / hoja: `1_Markov.xlsx` → `Matriz P` · copia: `copias/Markov/MK3.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| π(1) buena | 0.30 | 0.3 | ✅ |  |
| π(1) regular | 0.60 | 0.6 | ✅ |  |
| π(8) buena | 0.101753 | 0.101753 | ✅ |  |
| π(8) regular | 0.525514 | 0.525514 | ✅ |  |
| π(8) mala | 0.372733 | 0.372733 | ✅ |  |
| π(16) buena | 0.101659 | 0.101695 | ≈ | Errata de la fuente (dígitos invertidos): el valor exacto es 6/59 = 0.101695, igual que su propio estado estable 0.1017. |
| π(16) regular | 0.52454 | 0.525424 | ≈ | Errata de la fuente: el valor exacto es 31/59 = 0.525424 (su estado estable dice 0.5254). |
| π(16) mala | 0.372881 | 0.372881 | ✅ |  |
| π1 estable | 0.1017 | 0.101695 | ✅ |  |
| π2 estable | 0.5254 | 0.525424 | ✅ |  |
| π3 estable | 0.3729 | 0.372881 | ✅ |  |
| μ11 = 1/π1 | 9.83 | 9.83333 | ✅ |  |
| μ22 | 1.9 | 1.90323 | ✅ |  |
| μ33 | 2.68 | 2.68182 | ✅ |  |
| Costo esperado fertilizante | 135.51 | 135.508 | ✅ |  |
| Primer paso regular→buena μ21 | 12.50 | 12.5 | ✅ |  |
| Primer paso mala→buena μ31 | 13.34 | 13.3333 | ≈ | La fuente usa la inversa redondeada (6.67 + 6.67); el exacto es 13.333. |

### ≈ MK4 — Ej. 8 Cuentas por cobrar (absorbente)

Fuente: R. Caballero, UTP Panamá, Lectura 3 Cadenas de Markov — academia.utp.ac.pa/sites/default/files/docente/541/03_cadenas_de_markov.pdf  
Libro / hoja: `1_Markov.xlsx` → `Absorbente` · copia: `copias/Markov/MK4.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| F11 | 1.38 | 1.37931 | ✅ |  |
| F12 | 0.34 | 0.344828 | ✅ |  |
| F21 | 0.52 | 0.517241 | ✅ |  |
| F22 | 1.38 | 1.37931 | ✅ |  |
| FA <1 mes → pagada | 0.97 | 0.965517 | ✅ |  |
| FA <1 mes → incobrable | 0.03 | 0.0344828 | ✅ |  |
| FA 1-3 → pagada | 0.86 | 0.862069 | ✅ |  |
| FA 1-3 → incobrable | 0.14 | 0.137931 | ✅ |  |
| $ que se pagan | 6240 | 6,241.38 | ≈ | La fuente multiplica por FA redondeada a 2 decimales (0.97, 0.86). |
| $ incobrables | 760 | 758.621 | ≈ | Mismo redondeo de FA en la fuente. |

### ✅ MK5 — Tema 3 #1: compradores (100 de 1000) en 1 y 2 meses

Fuente: Presentaciones/problemas-resueltos-de-investigación-de-operaciones.pdf (tu carpeta)  
Libro / hoja: `1_Markov.xlsx` → `Matriz P` · copia: `copias/Markov/MK5.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P²11 | 0.7 | 0.7 | ✅ |  |
| P²21 | 0.45 | 0.45 | ✅ |  |
| Compran mes 1 (de 1000) | 350 | 350 | ✅ |  |
| Compran mes 2 (de 1000) | 475 | 475 | ✅ |  |

### ✅ MK6 — Tema 3 #2: fumadores en 10,000 habitantes

Fuente: Presentaciones/problemas-resueltos-de-investigación-de-operaciones.pdf (tu carpeta)  
Libro / hoja: `1_Markov.xlsx` → `Matriz P` · copia: `copias/Markov/MK6.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| No fuman | 5025 | 5,025 | ✅ |  |
| ≤1 paquete | 2500 | 2,500 | ✅ |  |
| >1 paquete | 2475 | 2,475 | ✅ |  |

### ✅ MK7 — Problema resuelto 15-1 Bradley School

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `1_Markov.xlsx` → `Matriz P` · copia: `copias/Markov/MK7.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Bradley año siguiente | 0.303 | 0.3025 | ✅ |  |
| Career año siguiente | 0.420 | 0.42 | ✅ |  |
| International año siguiente | 0.278 | 0.2775 | ✅ |  |
| Bradley equilibrio | 0.158 | 0.157895 | ✅ |  |
| Career equilibrio | 0.579 | 0.578947 | ✅ |  |
| International equilibrio | 0.263 | 0.263158 | ✅ |  |

### ✅ MK8 — Problema resuelto 15-2 Central State University (absorbente)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `1_Markov.xlsx` → `Absorbente` · copia: `copias/Markov/MK8.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| F11 | 1.176 | 1.17647 | ✅ |  |
| F12 | 0.147 | 0.147059 | ✅ |  |
| F21 | 0.588 | 0.588235 | ✅ |  |
| F22 | 1.324 | 1.32353 | ✅ |  |
| FA11 | 0.971 | 0.970588 | ✅ |  |
| FA12 | 0.029 | 0.0294118 | ✅ |  |
| FA21 | 0.735 | 0.735294 | ✅ |  |
| FA22 | 0.265 | 0.264706 | ✅ |  |
| Estudiantes exentos | 231 | 230.882 | ✅ |  |
| Toman el curso | 19 | 19.1176 | ✅ |  |

## Colas

### ✅ Q1 — Ej. 7.4 Transmisión de mensajes (M/M/1, λ=5/min, servicio 10 s)

Fuente: Universidad de Alcalá, Sistemas de colas (Baron cap. 7) — hilera.web.uah.es/estadistica/teoria/t5/t52.pdf  
Libro / hoja: `2_Colas.xlsx` → `MM1` · copia: `copias/Colas/Q1.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| ρ | 0.83 | 0.833333 | ✅ |  |
| L | 5 | 5 | ✅ |  |
| Lq | 4.17 | 4.16667 | ✅ |  |
| Wq (min) | 0.83 | 0.833333 | ✅ |  |
| W (min) | 1 | 1 | ✅ |  |

### ✅ Q2 — Ej. 7.5 Mensajes con 10% más llegadas (λ=5.5/min)

Fuente: Universidad de Alcalá, Sistemas de colas (Baron cap. 7) — hilera.web.uah.es/estadistica/teoria/t5/t52.pdf  
Libro / hoja: `2_Colas.xlsx` → `MM1` · copia: `copias/Colas/Q2.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| ρ | 0.92 | 0.916667 | ✅ |  |
| L | 11 | 11 | ✅ |  |
| Lq | 10.08 | 10.0833 | ✅ |  |
| Wq (s) | 110 | 110 | ✅ |  |
| W (min) | 2 | 2 | ✅ |  |

### ✅ Q3 — Taller de silenciadores Arnold (M/M/1) con costos

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `MM1` · copia: `copias/Colas/Q3.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| L | 2 | 2 | ✅ |  |
| W (h) | 1 | 1 | ✅ |  |
| Lq | 1.33 | 1.33333 | ✅ |  |
| Wq (min) | 40 | 40 | ✅ |  |
| ρ | 0.67 | 0.666667 | ✅ |  |
| P0 | 0.33 | 0.333333 | ✅ |  |
| Costo diario (8 h) = 8·(Cw·Lq + Cs) | 653.33 | 653.333 | ✅ |  |

### ✅ Q4 — Arnold con el mecánico rápido J. Smith (μ=4, $20/h)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `MM1` · copia: `copias/Colas/Q4.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| L | 1 | 1 | ✅ |  |
| W (h) | 0.5 | 0.5 | ✅ |  |
| Wq (min) | 15 | 15 | ✅ |  |
| ρ | 0.5 | 0.5 | ✅ |  |
| P0 | 0.5 | 0.5 | ✅ |  |
| Costo diario | 360 | 360 | ✅ |  |

### ≈ Q5 — Arnold con dos mecánicos (M/M/2)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `MMs` · copia: `copias/Colas/Q5.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P0 | 0.5 | 0.5 | ✅ |  |
| L | 0.75 | 0.75 | ✅ |  |
| W (min) | 22.5 | 22.5 | ✅ |  |
| Lq | 0.083 | 0.0833333 | ✅ |  |
| Wq (h) | 0.0415 | 0.0416667 | ≈ | El libro redondea 1/24 h = 0.041667 a 0.0415. |
| Wq (min) | 2.5 | 2.5 | ✅ |  |
| Costo diario | 273.20 | 273.333 | ≈ | El libro usa Wq = 0.0415 redondeado; con el valor exacto es $273.33. |

### ✅ Q6 — Problema resuelto 13-2 Marty (M/M/1, λ=20, μ=30)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `MM1` · copia: `copias/Colas/Q6.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| L | 2 | 2 | ✅ |  |
| W (h) | 0.1 | 0.1 | ✅ |  |
| Lq | 1.33 | 1.33333 | ✅ |  |
| Wq (min) | 4 | 4 | ✅ |  |
| ρ | 0.67 | 0.666667 | ✅ |  |
| P0 | 0.33 | 0.333333 | ✅ |  |
| P(n>0) | 0.667 | 0.666667 | ✅ |  |
| P(n>1) | 0.444 | 0.444444 | ✅ |  |
| P(n>2) | 0.296 | 0.296296 | ✅ |  |
| P(n>3) | 0.198 | 0.197531 | ✅ |  |
| Costo de espera diario 12 h a $0.10/min | 96 | 96 | ✅ |  |

### ✅ Q7 — Problema resuelto 13-3 Marty con dos empleados (M/M/2)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `MMs` · copia: `copias/Colas/Q7.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P0 | 0.5 | 0.5 | ✅ |  |
| L | 0.75 | 0.75 | ✅ |  |
| W (h) | 0.0375 | 0.0375 | ✅ |  |
| Lq | 0.083 | 0.0833333 | ✅ |  |
| Wq (min) | 0.25 | 0.25 | ✅ |  |
| ρ | 0.33 | 0.333333 | ✅ |  |

### ✅ Q8 — García-Golding Recycling (M/D/1, λ=8, μ=12)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `MG1 y MD1` · copia: `copias/Colas/Q8.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Wq (h) M/D/1 | 0.08333 | 0.0833333 | ✅ |  |
| Costo de espera por viaje ($60/h) | 5 | 5 | ✅ |  |

### ✅ Q9 — Hartlage's Seafood (M/G/1, λ=0.35, μ=0.5, σ=1.2 min)

Fuente: Anderson, Sweeney & Williams, Métodos cuantitativos para los negocios 11a ed. (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `MG1 y MD1` · copia: `copias/Colas/Q9.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P0 | 0.30 | 0.3 | ✅ |  |
| Lq | 1.1107 | 1.11067 | ✅ |  |
| L | 1.8107 | 1.81067 | ✅ |  |
| Wq (min) | 3.1733 | 3.17333 | ✅ |  |
| Pw | 0.70 | 0.7 | ✅ |  |

### ❌ Q10 — Departamento de Comercio: 5 impresoras (población finita)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `Poblacion finita` · copia: `copias/Colas/Q10.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P0 | 0.564 | 0.563952 | ✅ |  |
| Lq | 0.2 | 0.203474 | ✅ |  |
| L | 0.64 | 0.639522 | ✅ |  |
| Wq (h) | 0.91 | 0.933264 | ❌ | El libro redondea Lq = 0.2035 a 0.2 antes de dividir (0.2/0.218 = 0.917 → 0.91). Con Lq exacto: 0.2035/0.218 = 0.933. La hoja es correcta. |
| W (h) | 2.91 | 2.93326 | ≈ | Arrastra el redondeo de Wq del libro. |
| Costo total por hora | 101.80 | 101.743 | ≈ | El libro usa L = 0.64 redondeado (exacto 0.6395). |

### ✅ Q11 — Kolkmeyer: 6 máquinas, 1 mecánico

Fuente: Anderson, Sweeney & Williams, Métodos cuantitativos para los negocios 11a ed. (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `Poblacion finita` · copia: `copias/Colas/Q11.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P0 | 0.4845 | 0.484515 | ✅ |  |
| Lq | 0.3297 | 0.329664 | ✅ |  |
| L | 0.8451 | 0.845149 | ✅ |  |
| Wq (h) | 1.279 | 1.27904 | ✅ |  |
| W (h) | 3.279 | 3.27904 | ✅ |  |
| Pw | 0.5155 | 0.515485 | ✅ |  |

### ✅ Q12 — Kolkmeyer con 2 mecánicos

Fuente: Anderson, Sweeney & Williams, Métodos cuantitativos para los negocios 11a ed. (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `Poblacion finita` · copia: `copias/Colas/Q12.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Lq | 0.0227 | 0.0226558 | ✅ |  |
| Wq (h) | 0.0834 | 0.0833862 | ✅ |  |
| Pw | 0.1036 | 0.103628 | ✅ |  |

### ✅ Q13 — Burger Dome, un canal (λ=0.75, μ=1 por min), costos Cw=$10, Cs=$7

Fuente: Anderson, Sweeney & Williams, Métodos cuantitativos para los negocios 11a ed. (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `MM1` · copia: `copias/Colas/Q13.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P0 | 0.25 | 0.25 | ✅ |  |
| Lq | 2.25 | 2.25 | ✅ |  |
| L | 3 | 3 | ✅ |  |
| Wq (min) | 3 | 3 | ✅ |  |
| W (min) | 4 | 4 | ✅ |  |
| Pw | 0.75 | 0.75 | ✅ |  |
| Costo/h = Cw·L + Cs | 37.00 | 37 | ✅ |  |

### ✅ Q14 — Burger Dome con servicio mejorado (μ=1.25/min)

Fuente: Anderson, Sweeney & Williams, Métodos cuantitativos para los negocios 11a ed. (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `MM1` · copia: `copias/Colas/Q14.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P0 | 0.400 | 0.4 | ✅ |  |
| Lq | 0.900 | 0.9 | ✅ |  |
| L | 1.500 | 1.5 | ✅ |  |
| P(7 o más) = P(N>6) | 0.028 | 0.0279936 | ✅ |  |

### ✅ Q15 — Burger Dome con dos canales (M/M/2)

Fuente: Anderson, Sweeney & Williams, Métodos cuantitativos para los negocios 11a ed. (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `MMs` · copia: `copias/Colas/Q15.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P0 | 0.4545 | 0.454545 | ✅ |  |
| Lq | 0.1227 | 0.122727 | ✅ |  |
| L | 0.8727 | 0.872727 | ✅ |  |
| Wq (min) | 0.1636 | 0.163636 | ✅ |  |
| Pw | 0.2045 | 0.204545 | ✅ |  |
| Costo/h = Cw·L + Cs·s | 22.73 | 22.7273 | ✅ |  |

### ✅ Q16 — Microdata: 3 líneas sin espera (M/M/3/3)

Fuente: Anderson, Sweeney & Williams, Métodos cuantitativos para los negocios 11a ed. (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `Capacidad finita` · copia: `copias/Colas/Q16.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P3 (llamadas bloqueadas) | 0.2105 | 0.210526 | ✅ |  |

### ✅ Q17 — Microdata con 4 líneas (M/M/4/4)

Fuente: Anderson, Sweeney & Williams, Métodos cuantitativos para los negocios 11a ed. (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `Capacidad finita` · copia: `copias/Colas/Q17.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| P4 (bloqueadas) | 0.0952 | 0.0952381 | ✅ |  |
| L (líneas ocupadas) | 1.8095 | 1.80952 | ✅ |  |
| P0 | 0.1429 | 0.142857 | ✅ |  |
| P1 | 0.2857 | 0.285714 | ✅ |  |
| P2 | 0.2857 | 0.285714 | ✅ |  |
| P3 | 0.1905 | 0.190476 | ✅ |  |

### ≈ Q18 — Arnold: ¿1 o 2 mecánicos? (costo con Lq)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `Comparar servidores` · copia: `copias/Colas/Q18.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Óptimo | 2 | 2 | ✅ |  |
| Costo diario s=1 | 653.33 | 653.333 | ✅ |  |
| Costo diario s=2 | 273.20 | 273.333 | ≈ | Mismo redondeo de Wq que en Q5. |

### ✅ Q19 — Burger Dome: 1 vs 2 canales (costo con L)

Fuente: Anderson, Sweeney & Williams, Métodos cuantitativos para los negocios 11a ed. (libros/ de tu carpeta)  
Libro / hoja: `2_Colas.xlsx` → `Comparar servidores` · copia: `copias/Colas/Q19.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Óptimo | 2 | 2 | ✅ |  |
| Costo s=1 | 37.00 | 37 | ✅ |  |
| Costo s=2 | 22.73 | 22.7273 | ✅ |  |

## Inventarios

### ✅ I1 — Ej. 2 Bebidas Nacionales (EOQ, H = 25% de $8)

Fuente: R. Caballero, UTP Panamá, Lectura 4 Inventarios determinísticos — academia.utp.ac.pa/sites/default/files/docente/541/l4_modelos_de_inventario_deterministico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `EOQ` · copia: `copias/Inventarios/I1.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Q* | 1824 | 1,824.28 | ✅ |  |
| Costo total (ordenar + mantener) | 3648.56 | 3,648.56 | ✅ |  |
| Punto de reorden | 832 | 832 | ✅ |  |
| Pedidos por año | 57 | 57.0088 | ✅ |  |
| Tiempo entre pedidos (días) | 4.39 | 4.38529 | ✅ |  |

### ✅ I2 — Ej. 3 Carcasas para bomba (EOQ)

Fuente: R. Caballero, UTP Panamá, Lectura 4 Inventarios determinísticos — academia.utp.ac.pa/sites/default/files/docente/541/l4_modelos_de_inventario_deterministico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `EOQ` · copia: `copias/Inventarios/I2.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Q* | 200 | 200 | ✅ |  |
| N | 5 | 5 | ✅ |  |
| T (días) | 50 | 50 | ✅ |  |
| Inventario promedio | 100 | 100 | ✅ |  |
| Costo total | 100 | 100 | ✅ |  |

### ✅ I3 — Problema resuelto 6-1 Patterson Electronics (EOQ)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `3_Inventarios.xlsx` → `EOQ` · copia: `copias/Inventarios/I3.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Q* | 100 | 100 | ✅ |  |
| Órdenes por año | 2.5 | 2.5 | ✅ |  |
| Inventario promedio (el libro imprime 500 por errata: Q/2 = 100/2 = 50) | 50 | 50 | ✅ |  |

### ✅ I4 — Problema resuelto 6-4 F.W. Harris: punto de reorden (d=25/día, L=20)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `3_Inventarios.xlsx` → `EOQ` · copia: `copias/Inventarios/I4.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Punto de reorden | 500 | 500 | ✅ |  |

### ≈ I5 — Ej. 6 Compañía de radio con faltantes planeados

Fuente: R. Caballero, UTP Panamá, Lectura 4 Inventarios determinísticos — academia.utp.ac.pa/sites/default/files/docente/541/l4_modelos_de_inventario_deterministico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `EOQ faltantes` · copia: `copias/Inventarios/I5.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Q* | 115 | 115.47 | ✅ |  |
| Faltantes planeados | 29 | 28.8675 | ✅ |  |
| Inventario máximo | 86 | 86.6025 | ≈ | La fuente redondea Q = 115 y B = 29 antes de restar (exacto 115.47 − 28.87 = 86.60). |
| Tiempo de ciclo (días) | 14 | 14.4338 | ✅ |  |
| Costo total | 867 | 866.025 | ≈ | La fuente calcula con Q = 115 redondeado; con Q* exacto el costo es $866.03. |

### ✅ I6 — Ej. 7 Autos de juguete (Brass Department Store)

Fuente: R. Caballero, UTP Panamá, Lectura 4 Inventarios determinísticos — academia.utp.ac.pa/sites/default/files/docente/541/l4_modelos_de_inventario_deterministico.pdf / Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `3_Inventarios.xlsx` → `Descuentos` · copia: `copias/Inventarios/I6.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Q* precio $5 | 700 | 700 | ✅ |  |
| Q* precio $4.80 | 714 | 714.435 | ✅ |  |
| Q* precio $4.75 | 718 | 718.185 | ✅ |  |
| Q ajustada 2 | 1000 | 1,000 | ✅ |  |
| Q ajustada 3 | 2000 | 2,000 | ✅ |  |
| CT rango 1 | 25700 | 25,700 | ✅ |  |
| CT rango 2 | 24725 | 24,725 | ✅ |  |
| CT rango 3 | 24822.50 | 24,822.5 | ✅ |  |
| Cantidad elegida | 1000 | 1,000 | ✅ |  |

### ✅ I7 — Problema resuelto 6-3 Distribuidores Dorsey (5% de descuento desde 300)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `3_Inventarios.xlsx` → `Descuentos` · copia: `copias/Inventarios/I7.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| EOQ sin descuento | 29.6 | 29.5804 | ✅ |  |
| EOQ con descuento | 30.3 | 30.3488 | ✅ |  |
| CT sin descuento | 562366 | 562,366 | ✅ |  |
| CT con descuento | 543517 | 543,517 | ✅ |  |
| Cantidad elegida | 300 | 300 | ✅ |  |

### ✅ I8 — Ej. 4 Jabón de tocador (POQ, capacidad 60,000/año)

Fuente: R. Caballero, UTP Panamá, Lectura 4 Inventarios determinísticos — academia.utp.ac.pa/sites/default/files/docente/541/l4_modelos_de_inventario_deterministico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `POQ` · copia: `copias/Inventarios/I8.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Q* | 3387 | 3,386.83 | ✅ |  |
| Punto de reorden | 520 | 520 | ✅ |  |
| Tiempo de ciclo (días) | 33 | 32.5656 | ✅ |  |

### ✅ I9 — Ej. 5 Brown Manufacturing (POQ, d=60, p=80)

Fuente: R. Caballero, UTP Panamá, Lectura 4 Inventarios determinísticos — academia.utp.ac.pa/sites/default/files/docente/541/l4_modelos_de_inventario_deterministico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `POQ` · copia: `copias/Inventarios/I9.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Q* | 4000 | 4,000 | ✅ |  |
| Duración de la producción (días) | 50 | 50 | ✅ |  |
| Corridas por año | 2.5 | 2.5 | ✅ |  |

### ✅ I10 — Problema resuelto 6-2 Flemming Accessories (POQ)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `3_Inventarios.xlsx` → `POQ` · copia: `copias/Inventarios/I10.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Q* | 1632 | 1,632.32 | ✅ |  |

### ≈ I11 — Ej. 1 Hospital Regional: equipos código azul (5% de faltantes)

Fuente: R. Caballero, UTP Panamá, Lectura 5 Inventarios probabilísticos — academia.utp.ac.pa/sites/default/files/docente/541/05_modelos_de_inventario_probabilistico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `Revision continua` · copia: `copias/Inventarios/I11.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Inventario de seguridad (Z tabla = 1.65) | 16.5 | 16.4485 | ≈ | La fuente usa Z = 1.65 de tabla; Excel usa Z = 1.6449 exacto. |
| Punto de reorden | 366.5 | 366.449 | ≈ | Misma Z de tabla. |

### ≈ I12 — Problema resuelto 6-5 Thayer & Thaht (96% de servicio)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `3_Inventarios.xlsx` → `Revision continua` · copia: `copias/Inventarios/I12.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Inventario de seguridad (Z tabla = 1.75; el libro imprime 375 por errata, sus cuentas usan 350) | 350 | 350.137 | ✅ |  |
| Punto de reorden | 1350 | 1,350.14 | ✅ |  |
| Costo de mantener el inventario de seguridad (parte de los $11,400) | 1400 | 1,400.55 | ≈ | El libro usa Z = 1.75 de tabla (exacto 1.7507). |

### ✅ I13 — Ej. 4 Revisión periódica: nivel de reposición con 1% de agotamiento

Fuente: R. Caballero, UTP Panamá, Lectura 5 Inventarios probabilísticos — academia.utp.ac.pa/sites/default/files/docente/541/05_modelos_de_inventario_probabilistico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `Revision periodica` · copia: `copias/Inventarios/I13.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Nivel de reposición M (Z tabla = 2.33) | 355 | 354.686 | ✅ |  |

### ✅ I14 — Ej. 3 Car Rental: autos grandes para el fin de semana

Fuente: R. Caballero, UTP Panamá, Lectura 5 Inventarios probabilísticos — academia.utp.ac.pa/sites/default/files/docente/541/05_modelos_de_inventario_probabilistico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `Un periodo` · copia: `copias/Inventarios/I14.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Razón crítica | 0.7143 | 0.714286 | ✅ |  |
| Autos a tener (Z tabla = 0.57) | 158 | 157.923 | ✅ |  |

### ≈ I15a — Ej. 4 Limonada de Don (Lunes-Viernes)

Fuente: R. Caballero, UTP Panamá, Lectura 5 Inventarios probabilísticos — academia.utp.ac.pa/sites/default/files/docente/541/05_modelos_de_inventario_probabilistico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `Un periodo` · copia: `copias/Inventarios/I15a.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Nivel de servicio | 0.75 | 0.75 | ✅ |  |
| Galones (Z tabla = 0.68) | 467.56 | 467.191 | ≈ | La fuente usa Z = 0.68 de tabla; exacto 0.6745. |

### ≈ I15b — Ej. 4 Limonada de Don (Sábado)

Fuente: R. Caballero, UTP Panamá, Lectura 5 Inventarios probabilísticos — academia.utp.ac.pa/sites/default/files/docente/541/05_modelos_de_inventario_probabilistico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `Un periodo` · copia: `copias/Inventarios/I15b.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Nivel de servicio | 0.75 | 0.75 | ✅ |  |
| Galones (Z tabla = 0.68) | 795.84 | 795.217 | ≈ | La fuente usa Z = 0.68 de tabla; exacto 0.6745. |

### ≈ I15c — Ej. 4 Limonada de Don (Domingo)

Fuente: R. Caballero, UTP Panamá, Lectura 5 Inventarios probabilísticos — academia.utp.ac.pa/sites/default/files/docente/541/05_modelos_de_inventario_probabilistico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `Un periodo` · copia: `copias/Inventarios/I15c.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Nivel de servicio | 0.75 | 0.75 | ✅ |  |
| Galones (Z tabla = 0.68) | 585.80 | 585.332 | ≈ | La fuente usa Z = 0.68 de tabla; exacto 0.6745. |

### ✅ I16 — Ej. 5 Zapatería con demanda uniforme 350–650

Fuente: R. Caballero, UTP Panamá, Lectura 5 Inventarios probabilísticos — academia.utp.ac.pa/sites/default/files/docente/541/05_modelos_de_inventario_probabilistico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `Un periodo` · copia: `copias/Inventarios/I16.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Q (uniforme) | 550 | 550 | ✅ |  |

### ✅ I17 — Ej. 6 Muffins (uniforme 30–50 y normal μ=40, σ=5)

Fuente: R. Caballero, UTP Panamá, Lectura 5 Inventarios probabilísticos — academia.utp.ac.pa/sites/default/files/docente/541/05_modelos_de_inventario_probabilistico.pdf  
Libro / hoja: `3_Inventarios.xlsx` → `Un periodo` · copia: `copias/Inventarios/I17.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Nivel de servicio | 0.75 | 0.75 | ✅ |  |
| Q uniforme | 45 | 45 | ✅ |  |
| Q normal (Z tabla = 0.68) | 43.4 | 43.3724 | ✅ |  |

## Redes

### ✅ N1 — Tema 1 #1: ruta más corta de O a T (11 nodos)

Fuente: Presentaciones/problemas-resueltos-de-investigación-de-operaciones.pdf (tu carpeta)  
Libro / hoja: `4_Redes.xlsx` → `Ruta mas corta` · copia: `copias/Redes/N1.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Distancia mínima | 17 | 17 | ✅ |  |
| Ruta | O-C-F-G-T | O → C → F → G → T | ✅ |  |
| Distancia a A | 4 | 4 | ✅ |  |
| a B | 3 | 3 | ✅ |  |
| a C | 6 | 6 | ✅ |  |
| a D | 7 | 7 | ✅ |  |
| a E | 9 | 9 | ✅ |  |
| a F | 8 | 8 | ✅ |  |
| a G | 10 | 10 | ✅ |  |
| a H | 11 | 11 | ✅ |  |
| a I | 14 | 14 | ✅ |  |

### ✅ N2 — Problema resuelto 11-3 Leadville → Dillon

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `4_Redes.xlsx` → `Ruta mas corta` · copia: `copias/Redes/N2.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Distancia mínima | 32 | 32 | ✅ |  |
| Ruta | 1-2-3-6-7 | 1 → 2 → 3 → 6 → 7 | ✅ |  |
| Distancia a 2 | 8 | 8 | ✅ |  |
| a 3 | 14 | 14 | ✅ |  |
| a 4 | 18 | 18 | ✅ |  |
| a 5 | 22 | 22 | ✅ |  |
| a 6 | 26 | 26 | ✅ |  |

### ✅ N3 — Tema 1 #3: líneas telefónicas en 5 subdivisiones

Fuente: Presentaciones/problemas-resueltos-de-investigación-de-operaciones.pdf (tu carpeta)  
Libro / hoja: `4_Redes.xlsx` → `Arbol expansion minima` · copia: `copias/Redes/N3.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Longitud mínima (km) | 15 | 15 | ✅ |  |

### ✅ N4 — Problema resuelto 11-1 Granja de Roxie LaMothe

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `4_Redes.xlsx` → `Arbol expansion minima` · copia: `copias/Redes/N4.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Distancia total | 67 | 67 | ✅ |  |
| Arcos elegidos | 1-2, 1-3, 1-4, 4-7, 5-6, 6-7, 6-8 | 1-2, 1-3, 1-4, 4-7, 5-6, 6-7, 6-8 | ✅ |  |

### ✅ N5 — Tema 1 #2: flujo máximo de AI a GT (Solver)

Fuente: Presentaciones/problemas-resueltos-de-investigación-de-operaciones.pdf (tu carpeta)  
Libro / hoja: `4_Redes.xlsx` → `Flujo maximo` · copia: `copias/Redes/N5.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Flujo máximo | 9 | 9 | ✅ |  |
| Verificación | factible | ✓ Flujo factible: el flujo máximo es 9 | ✅ |  |

### ✅ N6 — Problema resuelto 11-2 PetroChem (Solver; capacidades por sentido según la figura 11.17)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `4_Redes.xlsx` → `Flujo maximo` · copia: `copias/Redes/N6.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Flujo máximo (miles de galones) | 10 | 10 | ✅ |  |
| Verificación | factible | ✓ Flujo factible: el flujo máximo es 10 | ✅ |  |

### ✅ N7 — Tema 1 #1 resuelto como PL con Solver

Fuente: Presentaciones/problemas-resueltos-de-investigación-de-operaciones.pdf (tu carpeta)  
Libro / hoja: `4_Redes.xlsx` → `Ruta corta PL` · copia: `copias/Redes/N7.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Distancia mínima | 17 | 17 | ✅ |  |
| Verificación | factible | ✓ Balance correcto. Arcos usados: los que tienen x = 1. Distancia = 17 | ✅ |  |

### ✅ N8 — Problema resuelto 11-3 resuelto como PL con Solver

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `4_Redes.xlsx` → `Ruta corta PL` · copia: `copias/Redes/N8.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Distancia mínima | 32 | 32 | ✅ |  |
| Verificación | factible | ✓ Balance correcto. Arcos usados: los que tienen x = 1. Distancia = 32 | ✅ |  |

## PERT/CPM

### ✅ P1 — Ejercicio 1: auditoría (3 rutas críticas)

Fuente: Plan de Mejora, Ruta crítica: ejercicios resueltos PERT/CPM — ejloorc.github.io/Portafolio-An-lisisyE-Loor.E/RUTA_CRITICA.pdf  
Libro / hoja: `5_PERT_CPM.xlsx` → `CPM` · copia: `copias/PERTCPM/P1.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Duración | 12 | 12 | ✅ |  |
| Actividades críticas (a-e-g, a-b-d-g, c-d-g) | A, B, C, D, E, G | A, B, C, D, E, G | ✅ |  |

### ✅ P2 — Ejercicio 2: arranque de planta

Fuente: Plan de Mejora, Ruta crítica: ejercicios resueltos PERT/CPM — ejloorc.github.io/Portafolio-An-lisisyE-Loor.E/RUTA_CRITICA.pdf  
Libro / hoja: `5_PERT_CPM.xlsx` → `CPM` · copia: `copias/PERTCPM/P2.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Duración | 14 | 14 | ✅ |  |
| Ruta crítica b-g | B, G | B, G | ✅ |  |

### ✅ P3 — Ejercicio 3: preparación de un curso

Fuente: Plan de Mejora, Ruta crítica: ejercicios resueltos PERT/CPM — ejloorc.github.io/Portafolio-An-lisisyE-Loor.E/RUTA_CRITICA.pdf  
Libro / hoja: `5_PERT_CPM.xlsx` → `CPM` · copia: `copias/PERTCPM/P3.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Duración | 9 | 9 | ✅ |  |
| Ruta crítica b-d-g | B, D, G | B, D, G | ✅ |  |

### ✅ P4 — Ejercicio 4: proyecto en semanas, holgura de B

Fuente: Plan de Mejora, Ruta crítica: ejercicios resueltos PERT/CPM — ejloorc.github.io/Portafolio-An-lisisyE-Loor.E/RUTA_CRITICA.pdf  
Libro / hoja: `5_PERT_CPM.xlsx` → `CPM` · copia: `copias/PERTCPM/P4.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Duración | 23 | 23 | ✅ |  |
| Ruta crítica A-C-D-E-G | A, C, D, E, G | A, C, D, E, G | ✅ |  |
| Holgura de B | 6 | 6 | ✅ |  |

### ✅ P5 — Ejercicio 5: sistema de comunicación (dos rutas críticas)

Fuente: Plan de Mejora, Ruta crítica: ejercicios resueltos PERT/CPM — ejloorc.github.io/Portafolio-An-lisisyE-Loor.E/RUTA_CRITICA.pdf  
Libro / hoja: `5_PERT_CPM.xlsx` → `CPM` · copia: `copias/PERTCPM/P5.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Rutas críticas A-C-F-G-I y A-D-F-G-I | A, C, D, F, G, I | A, C, D, F, G, I | ✅ |  |

### ✅ P5b — Ejercicio 5c-d: acortar C, D y G una semana

Fuente: Plan de Mejora, Ruta crítica: ejercicios resueltos PERT/CPM — ejloorc.github.io/Portafolio-An-lisisyE-Loor.E/RUTA_CRITICA.pdf  
Libro / hoja: `5_PERT_CPM.xlsx` → `CPM` · copia: `copias/PERTCPM/P5b.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Nueva duración | 16 | 16 | ✅ |  |
| Rutas críticas A-C-F-G-I y A-D-F-G-I | A, C, D, F, G, I | A, C, D, F, G, I | ✅ |  |

### ✅ P6 — Ejercicio 6: Duplaga Corporation

Fuente: Plan de Mejora, Ruta crítica: ejercicios resueltos PERT/CPM — ejloorc.github.io/Portafolio-An-lisisyE-Loor.E/RUTA_CRITICA.pdf  
Libro / hoja: `5_PERT_CPM.xlsx` → `CPM` · copia: `copias/PERTCPM/P6.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Duración | 34 | 34 | ✅ |  |
| Ruta crítica A-B-E-G-I | A, B, E, G, I | A, B, E, G, I | ✅ |  |

### ✅ P7 — Ejercicio 7: Charlie Cook Corp. (holguras)

Fuente: Plan de Mejora, Ruta crítica: ejercicios resueltos PERT/CPM — ejloorc.github.io/Portafolio-An-lisisyE-Loor.E/RUTA_CRITICA.pdf  
Libro / hoja: `5_PERT_CPM.xlsx` → `CPM` · copia: `copias/PERTCPM/P7.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Duración | 21 | 21 | ✅ |  |
| Ruta crítica B-E-G | B, E, G | B, E, G | ✅ |  |
| Holgura A | 2 | 2 | ✅ |  |
| Holgura C | 2 | 2 | ✅ |  |
| Holgura D | 6 | 6 | ✅ |  |
| Holgura F | 1 | 1 | ✅ |  |
| Holgura H | 1 | 1 | ✅ |  |

### ✅ P8 — Ejercicio 8: proyecto PERT de 25 actividades

Fuente: Plan de Mejora, Ruta crítica: ejercicios resueltos PERT/CPM — ejloorc.github.io/Portafolio-An-lisisyE-Loor.E/RUTA_CRITICA.pdf  
Libro / hoja: `5_PERT_CPM.xlsx` → `PERT` · copia: `copias/PERTCPM/P8.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Duración esperada (20.(3)) | 20.3333 | 20.3333 | ✅ |  |
| Varianza del proyecto (4.(3)) | 4.3333 | 4.33333 | ✅ |  |
| Ruta crítica O-P-S-T-W-Y | O, P, S, T, W, Y | O, P, S, T, W, Y | ✅ |  |

### ✅ P9 — Problemas resueltos 12-1 y 12-2 Ensamble del ala (Scott DeWitte)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `5_PERT_CPM.xlsx` → `PERT` · copia: `copias/PERTCPM/P9.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Duración esperada | 19 | 19 | ✅ |  |
| Varianza ruta crítica | 1.333 | 1.33333 | ✅ |  |
| Desviación estándar | 1.155 | 1.1547 | ✅ |  |
| Ruta crítica B-D-E-G | B, D, E, G | B, D, E, G | ✅ |  |
| A t | 2 | 2 | ✅ |  |
| A IC | 0 | 0 | ✅ |  |
| A TC | 2 | 2 | ✅ |  |
| A IL | 5 | 5 | ✅ |  |
| A TL | 7 | 7 | ✅ |  |
| A Holgura | 5 | 5 | ✅ |  |
| B t | 3 | 3 | ✅ |  |
| B IC | 0 | 0 | ✅ |  |
| B TC | 3 | 3 | ✅ |  |
| B IL | 0 | 0 | ✅ |  |
| B TL | 3 | 3 | ✅ |  |
| B Holgura | 0 | 0 | ✅ |  |
| C t | 5 | 5 | ✅ |  |
| C IC | 2 | 2 | ✅ |  |
| C TC | 7 | 7 | ✅ |  |
| C IL | 7 | 7 | ✅ |  |
| C TL | 12 | 12 | ✅ |  |
| C Holgura | 5 | 5 | ✅ |  |
| D t | 9 | 9 | ✅ |  |
| D IC | 3 | 3 | ✅ |  |
| D TC | 12 | 12 | ✅ |  |
| D IL | 3 | 3 | ✅ |  |
| D TL | 12 | 12 | ✅ |  |
| D Holgura | 0 | 0 | ✅ |  |
| E t | 5 | 5 | ✅ |  |
| E IC | 12 | 12 | ✅ |  |
| E TC | 17 | 17 | ✅ |  |
| E IL | 12 | 12 | ✅ |  |
| E TL | 17 | 17 | ✅ |  |
| E Holgura | 0 | 0 | ✅ |  |
| F t | 5 | 5 | ✅ |  |
| F IC | 3 | 3 | ✅ |  |
| F TC | 8 | 8 | ✅ |  |
| F IL | 14 | 14 | ✅ |  |
| F TL | 19 | 19 | ✅ |  |
| F Holgura | 11 | 11 | ✅ |  |
| G t | 2 | 2 | ✅ |  |
| G IC | 17 | 17 | ✅ |  |
| G TC | 19 | 19 | ✅ |  |
| G IL | 17 | 17 | ✅ |  |
| G TL | 19 | 19 | ✅ |  |
| G Holgura | 0 | 0 | ✅ |  |

### ≈ P10 — General Foundry: probabilidad de terminar en 16 semanas

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `5_PERT_CPM.xlsx` → `PERT` · copia: `copias/PERTCPM/P10.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Duración esperada | 15 | 15 | ✅ |  |
| Varianza del proyecto | 3.111 | 3.11111 | ✅ |  |
| Desviación estándar | 1.76 | 1.76383 | ✅ |  |
| Z | 0.57 | 0.566947 | ✅ |  |
| P(T ≤ 16) (tabla con Z = 0.57) | 0.71566 | 0.714625 | ≈ | El libro redondea Z = 0.567 a 0.57 antes de buscar en la tabla. |

### ✅ P11 — General Foundry: acelerar a 14 semanas (Solver)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `5_PERT_CPM.xlsx` → `Compresion` · copia: `copias/PERTCPM/P11.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Costo de aceleración | 1000 | 1,000 | ✅ |  |
| Costo por semana de B | 2000 | 2,000 | ✅ |  |
| Duración lograda | 14 | 14 | ✅ |  |

### ✅ P12 — General Foundry: acelerar a 12 semanas (Solver)

Fuente: Render, Stair & Hanna, Métodos cuantitativos para los negocios (libros/ de tu carpeta)  
Libro / hoja: `5_PERT_CPM.xlsx` → `Compresion` · copia: `copias/PERTCPM/P12.xlsx`

| Dato | Publicado | Solucionador | | Nota |
|---|---|---|---|---|
| Costo de aceleración | 5000 | 5,000 | ✅ |  |
| Duración lograda | 12 | 12 | ✅ |  |
| Factible | factible | ✓ Factible | ✅ |  |
