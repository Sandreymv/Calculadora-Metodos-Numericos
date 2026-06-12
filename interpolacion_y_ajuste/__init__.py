"""Interpolación y ajuste de curvas."""

from __future__ import annotations

import sympy as sp

from .diferencias_divididas import diferencias_divididas, polinomio_newton
from .lagrange import lagrange_polynomial
from .minimos_cuadrados import (
    ajuste_exponencial,
    ajuste_potencia,
    ajuste_senoidal,
    ajuste_suma_exponenciales,
    minimos_cuadrados_polinomio,
)


def _leer_lista(texto):
    partes = texto.replace(";", ",").split(",")
    return [float(parte.strip()) for parte in partes if parte.strip()]


def _mostrar_polinomio_y_valor(titulo, polinomio, x, x_eval):
    print(f"\n{titulo}")
    print(f"P(x) = {sp.expand(polinomio)}")
    print(f"P({x_eval}) = {float(polinomio.subs(x, x_eval))}")


def _menu_lagrange():
    while True:
        print("\nLagrange")
        print("1. Interpolar una tabla de datos")
        print("2. Ejercicio guiado: cos(x), ln(x+1) o tan(x)")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            xs = _leer_lista(input("x separados por coma = "))
            ys = _leer_lista(input("y separados por coma = "))
            x_eval = float(input("Evaluar en x = "))
            x = sp.Symbol("x")
            polinomio = lagrange_polynomial(xs, ys, x)
            _mostrar_polinomio_y_valor(
                "Polinomio de Lagrange", polinomio, x, x_eval
            )
        elif opcion == "2":
            print("a. cos(x) con x0=0, x1=0.6, x2=0.9")
            print("b. ln(x+1) con x0=0, x1=0.6, x2=0.9")
            print("c. tan(x) con x0=0, x1=0.6, x2=0.9")
            funcion = input("Elige a/b/c: ").strip().lower()
            x = sp.Symbol("x")
            xs = [0.0, 0.6, 0.9]
            if funcion == "a":
                ys = [float(sp.cos(valor)) for valor in xs]
                x_eval = 0.45
            elif funcion == "b":
                ys = [float(sp.log(valor + 1)) for valor in xs]
                x_eval = 0.45
            elif funcion == "c":
                ys = [float(sp.tan(valor)) for valor in xs]
                x_eval = 0.45
            else:
                print("Opción no válida.")
                continue
            polinomio = lagrange_polynomial(xs, ys, x)
            _mostrar_polinomio_y_valor(
                "Polinomio guiado", polinomio, x, x_eval
            )
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def _menu_diferencias_divididas():
    while True:
        print("\nDiferencias divididas")
        print("1. Construir tabla y polinomio")
        print("2. Ejercicio guiado con datos del taller")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            xs = _leer_lista(input("x separados por coma = "))
            ys = _leer_lista(input("y separados por coma = "))
            x_eval = float(input("Evaluar en x = "))
            x = sp.Symbol("x")
            tabla = diferencias_divididas(xs, ys)
            polinomio = polinomio_newton(xs, ys, x)
            print("Tabla de diferencias divididas:")
            for fila in tabla:
                print(fila)
            _mostrar_polinomio_y_valor(
                "Polinomio de Newton", polinomio, x, x_eval
            )
        elif opcion == "2":
            print("a. f(8.4) con tabla 8.1, 8.3, 8.6, 8.7")
            print("b. f(0.9) con tabla 0.6, 0.7, 0.8, 1.0")
            funcion = input("Elige a/b: ").strip().lower()
            x = sp.Symbol("x")
            if funcion == "a":
                xs = [8.1, 8.3, 8.6, 8.7]
                ys = [16.94410, 17.56492, 18.50515, 18.82091]
                x_eval = 8.4
            elif funcion == "b":
                xs = [0.6, 0.7, 0.8, 1.0]
                ys = [-0.17694460, 0.01375227, 0.22363362, 0.65809197]
                x_eval = 0.9
            else:
                print("Opción no válida.")
                continue
            tabla = diferencias_divididas(xs, ys)
            polinomio = polinomio_newton(xs, ys, x)
            print("Tabla de diferencias divididas:")
            for fila in tabla:
                print(fila)
            _mostrar_polinomio_y_valor(
                "Polinomio guiado", polinomio, x, x_eval
            )
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def _menu_minimos_cuadrados():
    while True:
        print("\nMínimos cuadrados")
        print("1. Ajuste polinómico general")
        print("2. Ajuste exponencial a e^(bx)")
        print("3. Ajuste de potencia a x^b")
        print("4. Ajuste b + a sin(t)")
        print("5. Ajuste a e^-3t + b e^-2t")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            xs = _leer_lista(input("x separados por coma = "))
            ys = _leer_lista(input("y separados por coma = "))
            grado = int(input("Grado del polinomio = "))
            polinomio, error = minimos_cuadrados_polinomio(xs, ys, grado)
            print(f"P(x) = {sp.expand(polinomio)}")
            print(f"Error cuadrático total = {error}")
        elif opcion == "2":
            xs = _leer_lista(input("x separados por coma = "))
            ys = _leer_lista(input("y separados por coma = "))
            a, b = ajuste_exponencial(xs, ys)
            print(f"y ≈ {a} e^({b}x)")
        elif opcion == "3":
            xs = _leer_lista(input("x separados por coma = "))
            ys = _leer_lista(input("y separados por coma = "))
            a, b = ajuste_potencia(xs, ys)
            print(f"y ≈ {a} x^{b}")
        elif opcion == "4":
            xs = _leer_lista(input("t separados por coma = "))
            ys = _leer_lista(input("y separados por coma = "))
            b, a = ajuste_senoidal(xs, ys)
            print(f"y ≈ {b} + {a} sin(t)")
        elif opcion == "5":
            xs = _leer_lista(input("t separados por coma = "))
            ys = _leer_lista(input("f(t) separados por coma = "))
            a, b = ajuste_suma_exponenciales(xs, ys)
            print(f"f(t) ≈ {a} e^-3t + {b} e^-2t")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def menu_interpolacion_y_ajuste():
    while True:
        print("\n" + "=" * 68)
        print("TALLER 4 - INTERPOLACIÓN Y AJUSTE")
        print("=" * 68)
        print("1. Lagrange")
        print("2. Diferencias divididas / Newton")
        print("3. Mínimos cuadrados")
        print("0. Volver")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            _menu_lagrange()
        elif opcion == "2":
            _menu_diferencias_divididas()
        elif opcion == "3":
            _menu_minimos_cuadrados()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
