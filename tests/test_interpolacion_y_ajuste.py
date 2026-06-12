"""
Pruebas para el Taller 4: interpolación y ajuste de curvas.
Ejecutar con: pytest tests/ -v
"""

import math

import pytest
import sympy as sp

from interpolacion_y_ajuste.diferencias_divididas import (
    diferencias_divididas,
    polinomio_newton,
)
from interpolacion_y_ajuste.lagrange import lagrange_polynomial
from interpolacion_y_ajuste.minimos_cuadrados import (
    ajuste_exponencial,
    ajuste_potencia,
    ajuste_senoidal,
    ajuste_suma_exponenciales,
    minimos_cuadrados_polinomio,
)

x = sp.Symbol("x")


class TestLagrange:
    def test_polinomio_cuadratico_simple(self):
        xs = [0, 1, 2]
        ys = [1, 3, 7]
        polinomio = lagrange_polynomial(xs, ys, x)
        esperado = sp.expand(x**2 + x + 1)
        assert sp.simplify(polinomio - esperado) == 0

    def test_interpolacion_reproduce_nodos(self):
        xs = [0.0, 0.6, 0.9]
        ys = [math.cos(v) for v in xs]
        polinomio = lagrange_polynomial(xs, ys, x)
        for xi, yi in zip(xs, ys):
            assert float(polinomio.subs(x, xi)) == pytest.approx(yi)


class TestDiferenciasDivididas:
    def test_tabla_de_diferencias(self):
        xs = [0, 1, 2]
        ys = [1, 3, 7]
        tabla = diferencias_divididas(xs, ys)
        assert tabla[0] == [1, 3, 7]
        assert tabla[1] == [2.0, 4.0]
        assert tabla[2] == [1.0]

    def test_polinomio_newton_equivale_a_lagrange(self):
        xs = [0, 1, 2]
        ys = [1, 3, 7]
        pn = polinomio_newton(xs, ys, x)
        esperado = sp.expand(x**2 + x + 1)
        assert sp.simplify(pn - esperado) == 0


class TestMinimosCuadrados:
    def test_ajuste_polinomico_lineal_exacto(self):
        xs = [0, 1, 2, 3]
        ys = [1, 3, 5, 7]
        polinomio, error = minimos_cuadrados_polinomio(xs, ys, 1)
        esperado = sp.expand(2 * x + 1)
        assert sp.simplify(polinomio - esperado) == 0
        assert error == pytest.approx(0.0)

    def test_ajuste_exponencial(self):
        xs = [0, 1, 2]
        ys = [2 * math.exp(3 * xi) for xi in xs]
        a, b = ajuste_exponencial(xs, ys)
        assert a == pytest.approx(2.0, rel=1e-8)
        assert b == pytest.approx(3.0, rel=1e-8)

    def test_ajuste_potencia(self):
        xs = [1, 2, 4]
        ys = [3 * (xi**2) for xi in xs]
        a, b = ajuste_potencia(xs, ys)
        assert a == pytest.approx(3.0, rel=1e-8)
        assert b == pytest.approx(2.0, rel=1e-8)

    def test_ajuste_senoidal(self):
        xs = [0.0, math.pi / 6, math.pi / 3, math.pi / 2]
        ys = [1.0 + 2.0 * math.sin(xi) for xi in xs]
        b, a = ajuste_senoidal(xs, ys)
        assert b == pytest.approx(1.0, rel=1e-8)
        assert a == pytest.approx(2.0, rel=1e-8)

    def test_ajuste_suma_exponenciales(self):
        xs = [0.1, 0.2, 0.3, 0.4]
        ys = [2 * math.exp(-3 * t) + 5 * math.exp(-2 * t) for t in xs]
        a, b = ajuste_suma_exponenciales(xs, ys)
        assert a == pytest.approx(2.0, rel=1e-8)
        assert b == pytest.approx(5.0, rel=1e-8)
