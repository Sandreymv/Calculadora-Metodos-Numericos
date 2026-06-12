"""
Pruebas para el Taller 2: binarios y análisis del error.
Ejecutar con: pytest tests -v
"""

import math

import pytest

from binarios_y_errores.conversion_binaria import (
    binario_a_decimal,
    decimal_a_base,
    decimal_a_binario,
)
from binarios_y_errores.errores import (
    cifras_significativas_desde_error_relativo,
    error_absoluto,
    error_relativo,
    redondear_cifras_significativas,
)


class TestErrores:
    def test_error_absoluto(self):
        assert error_absoluto(math.pi, 22 / 7) == pytest.approx(
            abs(math.pi - 22 / 7)
        )

    def test_error_relativo(self):
        valor_real = math.e
        valor_aprox = 2.718
        esperado = abs(valor_real - valor_aprox) / valor_real
        assert error_relativo(valor_real, valor_aprox) == pytest.approx(
            esperado
        )

    def test_cifras_significativas(self):
        assert cifras_significativas_desde_error_relativo(1e-4) >= 3

    def test_redondeo_cifras_significativas(self):
        assert redondear_cifras_significativas(1234.567, 3) == pytest.approx(
            1230.0
        )


class TestConversiones:
    def test_binario_a_decimal_entero(self):
        assert binario_a_decimal("10101") == pytest.approx(21.0)

    def test_binario_a_decimal_fraccion(self):
        assert binario_a_decimal("0.11011") == pytest.approx(0.84375)

    def test_decimal_a_binario(self):
        assert decimal_a_binario(5.25, 4) == "101.01"

    def test_decimal_a_base_3(self):
        assert decimal_a_base(23, 3, 0) == "212"
