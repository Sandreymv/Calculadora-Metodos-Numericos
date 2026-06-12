"""
Pruebas para el Taller 3: solución de ecuaciones no lineales.
Ejecutar con: pytest tests -v
"""

import math

import pytest

from ecuaciones_no_lineales.biseccion import biseccion
from ecuaciones_no_lineales.falsa_posicion import falsa_posicion
from ecuaciones_no_lineales.newton import newton
from ecuaciones_no_lineales.punto_fijo import punto_fijo
from ecuaciones_no_lineales.secante import secante


def f_x2_menos_2(x):
    return x * x - 2


def df_x2_menos_2(x):
    return 2 * x


class TestBiseccion:
    def test_raiz_de_x2_menos_2(self):
        raiz, iteraciones = biseccion(f_x2_menos_2, 1, 2, 1e-8, 100)
        assert raiz == pytest.approx(math.sqrt(2), rel=1e-8)
        assert len(iteraciones) > 0


class TestFalsaPosicion:
    def test_raiz_de_x2_menos_2(self):
        raiz, iteraciones = falsa_posicion(f_x2_menos_2, 1, 2, 1e-8, 100)
        assert raiz == pytest.approx(math.sqrt(2), rel=1e-8)
        assert len(iteraciones) > 0


class TestNewton:
    def test_raiz_de_x2_menos_2(self):
        raiz, iteraciones = newton(
            f_x2_menos_2, df_x2_menos_2, 1.5, 1e-10, 100
        )
        assert raiz == pytest.approx(math.sqrt(2), rel=1e-10)
        assert len(iteraciones) > 0


class TestSecante:
    def test_raiz_de_x2_menos_2(self):
        raiz, iteraciones = secante(f_x2_menos_2, 1, 2, 1e-10, 100)
        assert raiz == pytest.approx(math.sqrt(2), rel=1e-10)
        assert len(iteraciones) > 0


class TestPuntoFijo:
    def test_raiz_de_cos_x(self):
        def g(x):
            return math.cos(x)

        raiz, iteraciones = punto_fijo(g, 0.5, 1e-8, 100)
        assert raiz == pytest.approx(0.7390851332, rel=1e-8)
        assert len(iteraciones) > 0
