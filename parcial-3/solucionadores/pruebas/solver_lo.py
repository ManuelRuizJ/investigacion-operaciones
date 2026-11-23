"""Ejecuta el Solver lineal de LibreOffice (lp_solve) sobre copias de los libros.
Se corre con el Python que trae pyuno:  /usr/bin/python3.14 solver_lo.py trabajos.json
trabajos.json: lista de {archivo, hoja, objetivo, maximizar, variables:[rangos], restricciones:[[izq, op, der]]}
op: "<=", ">=", "="; der puede ser rango del mismo tamaño, una celda o un número."""
import json
import os
import subprocess
import sys
import tempfile
import time

import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.table import CellAddress
from com.sun.star.sheet import SolverConstraint
from com.sun.star.sheet.SolverConstraintOperator import LESS_EQUAL, GREATER_EQUAL, EQUAL

OPS = {"<=": LESS_EQUAL, ">=": GREATER_EQUAL, "=": EQUAL}


def celdas(rng):
    """'H9:I38' -> lista de (col, fila) base 0, recorriendo por filas."""
    from re import match
    def one(a):
        m = match(r"\$?([A-Z]+)\$?(\d+)", a)
        col = 0
        for ch in m.group(1):
            col = col * 26 + ord(ch) - 64
        return col - 1, int(m.group(2)) - 1
    if ":" in rng:
        a, b = rng.split(":")
        (c1, r1), (c2, r2) = one(a), one(b)
        return [(c, r) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]
    return [one(rng)]


def prop(n, v):
    p = PropertyValue()
    p.Name, p.Value = n, v
    return p


def main(path_json):
    trabajos = json.load(open(path_json))
    prof = tempfile.mkdtemp(prefix="lo_solver_")
    proc = subprocess.Popen(["soffice", f"-env:UserInstallation=file://{prof}", "--headless", "--invisible",
                             "--norestore", "--accept=pipe,name=solverio;urp;"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    ctx = None
    for _ in range(120):
        try:
            ctx = resolver.resolve("uno:pipe,name=solverio;urp;StarOffice.ComponentContext")
            break
        except Exception:
            time.sleep(0.5)
    smgr = ctx.ServiceManager
    desk = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    salida = []
    for t in trabajos:
        url = uno.systemPathToFileUrl(os.path.abspath(t["archivo"]))
        doc = desk.loadComponentFromURL(url, "_blank", 0, (prop("Hidden", True),))
        sheets = doc.Sheets
        idx = [sheets.getByIndex(i).Name for i in range(sheets.Count)].index(t["hoja"])
        sh = sheets.getByIndex(idx)

        def addr(c, r):
            a = CellAddress()
            a.Sheet, a.Column, a.Row = idx, c, r
            return a

        variables = [addr(c, r) for rng in t["variables"] for c, r in celdas(rng)]
        for v in variables:  # empezar de cero para que Solver realmente resuelva
            sh.getCellByPosition(v.Column, v.Row).setValue(0)
        doc.calculateAll()
        cons = []
        for izq, op, der in t["restricciones"]:
            L = celdas(izq)
            if isinstance(der, (int, float)):
                Rr = [float(der)] * len(L)
            else:
                Rc = celdas(der)
                Rr = [addr(*Rc[0])] * len(L) if len(Rc) == 1 else [addr(*x) for x in Rc]
            for (c, r), rv in zip(L, Rr):
                sc = SolverConstraint()
                sc.Left = addr(c, r)
                sc.Operator = OPS[op]
                sc.Right = rv
                cons.append(sc)
        solver = smgr.createInstanceWithContext("com.sun.star.comp.Calc.LpsolveSolver", ctx)
        solver.Document = doc
        oc, orow = celdas(t["objetivo"])[0]
        solver.Objective = addr(oc, orow)
        solver.Variables = tuple(variables)
        solver.Constraints = tuple(cons)
        solver.Maximize = bool(t["maximizar"])
        try:
            solver.setPropertyValue("NonNegative", True)
        except Exception:
            pass
        solver.solve()
        ok = solver.Success
        if ok:
            for v, val in zip(variables, solver.Solution):
                sh.getCellByPosition(v.Column, v.Row).setValue(round(val, 9))
        doc.calculateAll()
        doc.storeToURL(url, (prop("FilterName", "Calc MS Excel 2007 XML"),))
        doc.close(True)
        salida.append({"archivo": t["archivo"], "exito": bool(ok), "objetivo": solver.ResultValue if ok else None,
                       "restricciones": len(cons), "variables": len(variables)})
    try:
        desk.terminate()
    except Exception:
        pass
    proc.wait(timeout=30)
    print(json.dumps(salida, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
