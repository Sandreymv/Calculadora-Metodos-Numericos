"""Método de punto fijo."""

from __future__ import annotations


def punto_fijo(g, p0, tolerancia=1e-6, max_iter=100):
    iteraciones = []
    p = p0
    for indice in range(1, max_iter + 1):
        p_siguiente = g(p)
        error = abs(p_siguiente - p)
        iteraciones.append((indice, p_siguiente, error))
        if error < tolerancia:
            return p_siguiente, iteraciones
        p = p_siguiente
    return p, iteraciones
