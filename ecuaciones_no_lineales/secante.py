"""Método de la secante."""

from __future__ import annotations


def secante(f, p0, p1, tolerancia=1e-6, max_iter=100):
    iteraciones = []
    q0 = f(p0)
    q1 = f(p1)
    p = p1
    for indice in range(1, max_iter + 1):
        denominador = q1 - q0
        if denominador == 0:
            raise ZeroDivisionError("La secante se indeterminó")
        p = p1 - q1 * (p1 - p0) / denominador
        error = abs(p - p1)
        iteraciones.append((indice, p, error))
        if error < tolerancia:
            return p, iteraciones
        p0, q0 = p1, q1
        p1, q1 = p, f(p)
    return p, iteraciones
