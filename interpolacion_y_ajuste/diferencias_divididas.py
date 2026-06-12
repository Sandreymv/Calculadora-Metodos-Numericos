"""Diferencias divididas de Newton."""

from __future__ import annotations

import sympy as sp


def diferencias_divididas(xs, ys):
    if len(xs) != len(ys):
        raise ValueError("xs e ys deben tener la misma longitud")
    tabla = [list(ys)]
    for orden in range(1, len(xs)):
        columna = []
        for i in range(len(xs) - orden):
            numerador = tabla[orden - 1][i + 1] - tabla[orden - 1][i]
            denominador = xs[i + orden] - xs[i]
            valor = numerador / denominador
            columna.append(valor)
        tabla.append(columna)
    return tabla


def polinomio_newton(xs, ys, symbol=None):
    x = symbol or sp.Symbol("x")
    tabla = diferencias_divididas(xs, ys)
    polinomio = sp.Float(tabla[0][0])
    termino = sp.Integer(1)
    for orden in range(1, len(xs)):
        termino *= x - xs[orden - 1]
        polinomio += sp.Float(tabla[orden][0]) * termino
    return sp.expand(sp.simplify(polinomio))
