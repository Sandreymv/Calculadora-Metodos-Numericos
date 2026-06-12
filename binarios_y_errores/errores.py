"""Cálculo de errores y redondeo."""

from __future__ import annotations

import math


def error_absoluto(valor_real, valor_aproximado):
    return abs(valor_real - valor_aproximado)


def error_relativo(valor_real, valor_aproximado):
    if valor_real == 0:
        return float("inf")
    return abs(error_absoluto(valor_real, valor_aproximado) / valor_real)


def redondear_cifras_significativas(valor, cifras):
    if cifras <= 0:
        raise ValueError("Las cifras significativas deben ser positivas")
    if valor == 0:
        return 0.0
    return float(f"{valor:.{cifras}g}")


def cifras_significativas_desde_error_relativo(error_rel):
    if error_rel == 0:
        return math.inf
    if not math.isfinite(error_rel):
        return 0
    return max(0, math.floor(-math.log10(2 * abs(error_rel))))
