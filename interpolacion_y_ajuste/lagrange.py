"""Interpolación de Lagrange."""

from __future__ import annotations

import sympy as sp


def lagrange_polynomial(xs, ys, symbol=None):
    if len(xs) != len(ys):
        raise ValueError("xs e ys deben tener la misma longitud")
    x = symbol or sp.Symbol("x")
    polinomio = sp.Integer(0)
    for i, xi in enumerate(xs):
        base = sp.Integer(1)
        for j, xj in enumerate(xs):
            if i != j:
                base *= (x - xj) / (xi - xj)
        polinomio += ys[i] * base
    return sp.expand(sp.simplify(polinomio))
