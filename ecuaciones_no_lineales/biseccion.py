"""Método de bisección."""

from __future__ import annotations


def biseccion(f, a, b, tolerancia=1e-6, max_iter=100):
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos")

    iteraciones = []
    p = a
    for indice in range(1, max_iter + 1):
        p = (a + b) / 2
        fp = f(p)
        error = abs(b - a) / 2
        iteraciones.append((indice, p, error))
        if error < tolerancia or fp == 0:
            return p, iteraciones
        if fa * fp < 0:
            b = p
            fb = fp
        else:
            a = p
            fa = fp
    return p, iteraciones
