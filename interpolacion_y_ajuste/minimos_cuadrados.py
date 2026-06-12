"""Ajuste por mínimos cuadrados."""

from __future__ import annotations

import math

import numpy as np
import sympy as sp


def minimos_cuadrados_polinomio(xs, ys, grado):
    if len(xs) != len(ys):
        raise ValueError("xs e ys deben tener la misma longitud")
    x = sp.Symbol("x")
    A = np.vander(np.asarray(xs, dtype=float), grado + 1, increasing=True)
    coeficientes, *_ = np.linalg.lstsq(
        A, np.asarray(ys, dtype=float), rcond=None
    )
    polinomio = sum(sp.Float(coeficientes[i]) * x**i for i in range(grado + 1))
    ajuste = A @ coeficientes
    error = float(np.sum((np.asarray(ys, dtype=float) - ajuste) ** 2))
    return sp.expand(sp.simplify(polinomio)), error


def ajuste_lineal_bases(xs, ys, bases):
    if len(xs) != len(ys):
        raise ValueError("xs e ys deben tener la misma longitud")
    matriz = np.column_stack(
        [[base(xi) for xi in xs] for base in bases]
    ).astype(float)
    coeficientes, *_ = np.linalg.lstsq(
        matriz, np.asarray(ys, dtype=float), rcond=None
    )
    return coeficientes


def ajuste_exponencial(xs, ys):
    if any(y <= 0 for y in ys):
        raise ValueError("El ajuste exponencial requiere y > 0")
    y_log = np.log(np.asarray(ys, dtype=float))
    A = np.column_stack([np.ones(len(xs)), np.asarray(xs, dtype=float)])
    coeficientes, *_ = np.linalg.lstsq(A, y_log, rcond=None)
    a = float(np.exp(coeficientes[0]))
    b = float(coeficientes[1])
    return a, b


def ajuste_potencia(xs, ys):
    if any(x <= 0 for x in xs) or any(y <= 0 for y in ys):
        raise ValueError("El ajuste de potencia requiere x > 0 e y > 0")
    X = np.log(np.asarray(xs, dtype=float))
    Y = np.log(np.asarray(ys, dtype=float))
    A = np.column_stack([np.ones(len(xs)), X])
    coeficientes, *_ = np.linalg.lstsq(A, Y, rcond=None)
    a = float(np.exp(coeficientes[0]))
    b = float(coeficientes[1])
    return a, b


def ajuste_senoidal(xs, ys):
    def base_constante(_):
        return 1.0

    def base_seno(x):
        return math.sin(x)

    b, a = ajuste_lineal_bases(xs, ys, [base_constante, base_seno])
    return float(b), float(a)


def ajuste_suma_exponenciales(xs, ys):
    def base_1(t):
        return math.exp(-3 * t)

    def base_2(t):
        return math.exp(-2 * t)

    a, b = ajuste_lineal_bases(xs, ys, [base_1, base_2])
    return float(a), float(b)
