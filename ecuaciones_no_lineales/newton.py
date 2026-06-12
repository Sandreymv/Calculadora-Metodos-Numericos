"""Método de Newton."""

from __future__ import annotations


def newton(f, df, p0, tolerancia=1e-6, max_iter=100):
    iteraciones = []
    p = p0
    for indice in range(1, max_iter + 1):
        fp = f(p)
        dfp = df(p)
        if dfp == 0:
            raise ZeroDivisionError("La derivada se anuló durante Newton")
        p_siguiente = p - fp / dfp
        error = abs(p_siguiente - p)
        iteraciones.append((indice, p_siguiente, error))
        if error < tolerancia:
            return p_siguiente, iteraciones
        p = p_siguiente
    return p, iteraciones
