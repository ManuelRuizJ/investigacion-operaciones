"""Genera los 5 libros de solucionadores del parcial 3.
Uso:  python3 generar_solucionadores.py
"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "generador"))

import markov
MODULOS = [("1_Markov.xlsx", markov)]
for extra in [("2_Colas.xlsx", "colas"), ("3_Inventarios.xlsx", "inventarios"),
              ("4_Redes.xlsx", "redes"), ("5_PERT_CPM.xlsx", "pert")]:
    try:
        MODULOS.append((extra[0], __import__(extra[1])))
    except ModuleNotFoundError:
        pass

if __name__ == "__main__":
    solo = sys.argv[1:]
    for nombre, mod in MODULOS:
        if solo and not any(s in nombre for s in solo):
            continue
        ruta = os.path.join(AQUI, nombre)
        mod.generar(ruta)
        print("Generado:", ruta)
