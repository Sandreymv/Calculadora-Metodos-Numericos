"""Métodos para resolver ecuaciones no lineales."""

from __future__ import annotations

import sympy as sp

from .biseccion import biseccion
from .falsa_posicion import falsa_posicion
from .newton import newton
from .punto_fijo import punto_fijo
from .secante import secante


def _construir_expresion(texto):
    x = sp.Symbol("x")
    expr = sp.sympify(
        texto,
        locals={
            "x": x,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "exp": sp.exp,
            "ln": sp.log,
            "log": sp.log,
            "sqrt": sp.sqrt,
            "pi": sp.pi,
            "E": sp.E,
        },
    )
    return x, expr, sp.lambdify(x, expr, "math")


def _mostrar_iteraciones(nombre, iteraciones):
    print(f"\n{nombre}")
    print("iteración | aproximación | error")
    for indice, aproximacion, error in iteraciones:
        print(f"{indice:>9} | {aproximacion:>12.10f} | {error:.3e}")


def menu_ecuaciones_no_lineales():
    while True:
        print("\n" + "=" * 68)
        print("TALLER 3 - ECUACIONES NO LINEALES")
        print("=" * 68)
        print("1. Sección de bisección")
        print("2. Sección de Newton")
        print("3. Sección de secante")
        print("4. Sección de falsa posición")
        print("5. Sección de punto fijo")
        print("0. Volver")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion in {"1", "2", "3", "4"}:
            texto = input("f(x) = ")
            _, _, funcion = _construir_expresion(texto)
            tol = float(input("Tolerancia = "))
            max_iter = int(input("Máximo de iteraciones = "))

            if opcion == "1":
                a = float(input("a = "))
                b = float(input("b = "))
                raiz, iteraciones = biseccion(funcion, a, b, tol, max_iter)
                _mostrar_iteraciones("Bisección", iteraciones)
                print(f"Raíz aproximada = {raiz}")
            elif opcion == "2":
                a = float(input("a = "))
                b = float(input("b = "))
                raiz, iteraciones = falsa_posicion(
                    funcion, a, b, tol, max_iter
                )
                _mostrar_iteraciones("Falsa posición", iteraciones)
                print(f"Raíz aproximada = {raiz}")
            elif opcion == "3":
                dtexto = input("f'(x) = ")
                _, _, derivada = _construir_expresion(dtexto)
                p0 = float(input("p0 = "))
                raiz, iteraciones = newton(
                    funcion, derivada, p0, tol, max_iter
                )
                _mostrar_iteraciones("Newton", iteraciones)
                print(f"Raíz aproximada = {raiz}")
            elif opcion == "4":
                p0 = float(input("p0 = "))
                p1 = float(input("p1 = "))
                raiz, iteraciones = secante(
                    funcion, p0, p1, tol, max_iter
                )
                _mostrar_iteraciones("Secante", iteraciones)
                print(f"Raíz aproximada = {raiz}")
        elif opcion == "5":
            texto = input("g(x) = ")
            _, _, funcion = _construir_expresion(texto)
            p0 = float(input("p0 = "))
            tol = float(input("Tolerancia = "))
            max_iter = int(input("Máximo de iteraciones = "))
            raiz, iteraciones = punto_fijo(funcion, p0, tol, max_iter)
            _mostrar_iteraciones("Punto fijo", iteraciones)
            print(f"Punto fijo aproximado = {raiz}")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
