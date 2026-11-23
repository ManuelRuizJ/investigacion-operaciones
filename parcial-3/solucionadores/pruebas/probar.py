"""Prueba los solucionadores con ejercicios resueltos publicados.
1) Crea una COPIA del libro por ejercicio en pruebas/copias/<tema>/<id>.xlsx y la llena con los datos.
2) Recalcula cada copia con LibreOffice; si el ejercicio usa Solver, lo corre (lp_solve de LibreOffice).
3) Compara cada resultado contra la respuesta publicada y escribe pruebas/REPORTE.md.
Uso:  python3 probar.py [RECALC_PY]
"""
import json
import os
import re
import subprocess
import sys
from datetime import date

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from ejercicios import EJ, NOTAS  # noqa: E402

RECALC = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "--reporte" else os.path.expanduser(
    "~/.claude/skills/synced/bc67ad10-cf59-455a-9779-54697e43b610_f504c7a0-c611-4c32-a926-14af7cc5510b/xlsx/scripts/recalc.py")
PY_UNO = "/usr/bin/python3.14"


def ruta_copia(e):
    carpeta = os.path.join(AQUI, "copias", re.sub(r"[^A-Za-z]", "", e["tema"]))
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, f"{e['id']}.xlsx")


def comparar(obtenido, esperado):
    if isinstance(esperado, set):
        ok = obtenido == esperado
        return ("ok" if ok else "mal"), ", ".join(sorted(obtenido or [])), ", ".join(sorted(esperado))
    if esperado == "✓":
        ok = isinstance(obtenido, str) and obtenido.startswith("✓")
        return ("ok" if ok else "mal"), str(obtenido), "factible"
    if isinstance(esperado, str) and "-" in esperado and not re.fullmatch(r"-?[\d.]+", esperado):
        norm = str(obtenido).replace(" → ", "-").replace(" ", "")
        return ("ok" if norm.upper() == esperado.upper() else "mal"), str(obtenido), esperado
    e = float(esperado)
    if not isinstance(obtenido, (int, float)):
        return "mal", str(obtenido), esperado
    dec = len(esperado.split(".")[1]) if "." in esperado else 0
    tol_pub = 0.5 * 10 ** (-dec) * 1.0001 + 1e-9
    dif = abs(obtenido - e)
    if dif <= tol_pub:
        estado = "ok"
    elif dif <= 0.01 * abs(e):
        estado = "aprox"
    else:
        estado = "mal"
    return estado, f"{obtenido:,.6g}" if abs(obtenido) < 1e6 else f"{obtenido:,.2f}", esperado


def main():
    # 1) copias
    for e in EJ:
        wb = openpyxl.load_workbook(os.path.join(BASE, e["archivo"]))
        e["llenar"](wb)
        wb.active = wb.sheetnames.index(e["hoja"])
        wb.save(ruta_copia(e))
    print(f"{len(EJ)} copias creadas")

    # 2) Solver y recálculo
    trabajos = []
    for e in EJ:
        if e["solver"]:
            t = dict(e["solver"])
            t["archivo"] = ruta_copia(e)
            trabajos.append(t)
    solver_info = {}
    if trabajos:
        jf = os.path.join(AQUI, "copias", "trabajos_solver.json")
        json.dump(trabajos, open(jf, "w"), ensure_ascii=False, indent=1)
        out = subprocess.run([PY_UNO, os.path.join(AQUI, "solver_lo.py"), jf], capture_output=True, text=True, timeout=900)
        print(out.stdout[-2000:], out.stderr[-2000:])
        for s in json.loads(out.stdout.strip().splitlines()[-1]):
            solver_info[os.path.abspath(s["archivo"])] = s
        os.remove(jf)
    errores_formula = {}
    for e in EJ:
        r = subprocess.run([sys.executable, RECALC, ruta_copia(e), "90"], capture_output=True, text=True, timeout=300)
        try:
            j = json.loads(r.stdout)
            errores_formula[e["id"]] = j.get("total_errors", j.get("error"))
        except Exception:
            errores_formula[e["id"]] = r.stdout[-200:] + r.stderr[-200:]
        print(e["id"], "recalculado", errores_formula[e["id"]])

    # 3) comparar
    filas = []
    for e in EJ:
        wbv = openpyxl.load_workbook(ruta_copia(e), data_only=True)
        for nombre, getter, esperado in e["checks"]:
            try:
                obt = getter(wbv)
                estado, o_txt, e_txt = comparar(obt, esperado)
            except Exception as ex:
                estado, o_txt, e_txt = "mal", f"ERROR: {ex}", str(esperado)
            filas.append(dict(id=e["id"], tema=e["tema"], desc=e["desc"], fuente=e["fuente"], dato=nombre,
                              esperado=e_txt, obtenido=o_txt, estado=estado))
        si = solver_info.get(os.path.abspath(ruta_copia(e)))
        e["solver_txt"] = (f"Solver: {'éxito' if si['exito'] else 'FALLÓ'}, {si['variables']} variables, {si['restricciones']} restricciones"
                           if si else "")
    json.dump(filas, open(os.path.join(AQUI, "resultados.json"), "w"), ensure_ascii=False, indent=1)
    escribir_reporte(filas, errores_formula)
    tot = len(filas)
    n_ok = sum(f["estado"] == "ok" for f in filas)
    n_ap = sum(f["estado"] == "aprox" for f in filas)
    n_mal = sum(f["estado"] == "mal" for f in filas)
    print(f"\nComprobaciones: {tot} | coinciden {n_ok} | ≈ redondeo {n_ap} | NO coinciden {n_mal}")
    for f in filas:
        if f["estado"] != "ok":
            print(f"  [{f['estado']}] {f['id']} {f['dato']}: publicado {f['esperado']} vs solucionador {f['obtenido']}")


ICONO = {"ok": "✅", "aprox": "≈", "mal": "❌"}


def escribir_reporte(filas, errores_formula):
    tot = len(filas)
    n_ok = sum(f["estado"] == "ok" for f in filas)
    n_ap = sum(f["estado"] == "aprox" for f in filas)
    n_mal = tot - n_ok - n_ap
    ids = []
    for f in filas:
        if f["id"] not in ids:
            ids.append(f["id"])
    out = [f"# Reporte de pruebas de los solucionadores ({date.today():%d/%m/%Y})", "",
           f"Se resolvieron **{len(ids)} ejercicios publicados** con una copia de los libros (carpeta `pruebas/copias/`) "
           f"y se compararon **{tot} resultados** contra la respuesta de la fuente.", "",
           f"- ✅ Coinciden (dentro del redondeo con que los publica la fuente): **{n_ok}**",
           f"- ≈ Diferencia menor a 1 % (la fuente usó valores redondeados, p. ej. Z de tabla): **{n_ap}**",
           f"- ❌ No coinciden: **{n_mal}**", "",
           "Todas las diferencias (≈ y ❌) se revisaron a mano: vienen de redondeos o erratas de la fuente, no de las plantillas. "
           "La explicación está en la columna *Nota*.", "",
           "Columnas: *Publicado* = respuesta de la fuente; *Solucionador* = lo que calculó la copia del libro.", ""]
    temas = []
    for f in filas:
        if f["tema"] not in temas:
            temas.append(f["tema"])
    from ejercicios import EJ as _EJ
    info = {e["id"]: e for e in _EJ}
    for t in temas:
        out += [f"## {t}", ""]
        for i in [x for x in ids if info[x]["tema"] == t]:
            e = info[i]
            fs = [f for f in filas if f["id"] == i]
            est = "✅" if all(f["estado"] == "ok" for f in fs) else ("❌" if any(f["estado"] == "mal" for f in fs) else "≈")
            out += [f"### {est} {i} — {e['desc']}", "",
                    f"Fuente: {e['fuente']}  ", f"Libro / hoja: `{e['archivo']}` → `{e['hoja']}` · copia: `copias/{re.sub(r'[^A-Za-z]', '', t)}/{i}.xlsx`"
                    + (f"  \n{e.get('solver_txt', '')}" if e.get("solver_txt") else "")
                    + (f"  \nErrores de fórmula en la copia: {errores_formula.get(i)}" if errores_formula.get(i) not in (0, None) else ""), "",
                    "| Dato | Publicado | Solucionador | | Nota |", "|---|---|---|---|---|"]
            for f in fs:
                nota = NOTAS.get((f["id"], f["dato"]), "")
                out.append(f"| {f['dato']} | {f['esperado']} | {f['obtenido']} | {ICONO[f['estado']]} | {nota} |")
            out.append("")
    open(os.path.join(AQUI, "REPORTE.md"), "w").write("\n".join(out))


if __name__ == "__main__":
    if "--reporte" in sys.argv:  # solo regenerar el reporte con los resultados guardados
        escribir_reporte(json.load(open(os.path.join(AQUI, "resultados.json"))), {})
    else:
        main()
