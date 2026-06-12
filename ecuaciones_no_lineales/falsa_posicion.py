"""Método de falsa posición."""

from __future__ import annotations


def falsa_posicion(f, a, b, tolerancia=1e-6, max_iter=100):
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos")

    iteraciones = []
    p = a
    for indice in range(1, max_iter + 1):
        denominador = fb - fa
        if denominador == 0:
            raise ZeroDivisionError(
                "La fórmula de falsa posición se indeterminó"
            )
        p = b - fb * (b - a) / denominador
        fp = f(p)
        iteraciones.append((indice, p, abs(fp)))
        if abs(fp) < tolerancia:
            return p, iteraciones
        if fa * fp < 0:
            b = p
            fb = fp
        else:
            a = p
            fa = fp
    return p, iteraciones
