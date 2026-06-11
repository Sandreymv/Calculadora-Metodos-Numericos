"""
==============================================================
  PRUEBAS — Módulo 1: Polinomios de Taylor
  Ejecutar con:  pytest tests/ -v
==============================================================
"""

import pytest
import math
import sympy as sp
from taylor.taylor import (
    taylor_polynomial,
    evaluar_directo,
    horner,
    obtener_coeficientes,
    cota_error,
    calcular_errores,
    terminos_necesarios,
)

# ── Símbolo compartido ──────────────────────────────────────
x = sp.Symbol('x')
TOL = 1e-6  # tolerancia general para comparaciones flotantes


# ==============================================================
# 1. taylor_polynomial
# ==============================================================

class TestTaylorPolynomial:

    def test_exp_grado1_alrededor_de_0(self):
        """e^x ≈ 1 + x  (P1 en x0=0)"""
        f = sp.exp(x)
        Pn, terms = taylor_polynomial(f, x, 0, 1)
        assert Pn == sp.sympify("1 + x")

    def test_exp_grado4_alrededor_de_0(self):
        """e^x P4 evaluado en x=1 debe estar cerca de e"""
        f = sp.exp(x)
        Pn, _ = taylor_polynomial(f, x, 0, 4)
        aprox = float(Pn.subs(x, 1))
        # 1 + 1 + 1/2 + 1/6 + 1/24 = 2.708...
        assert abs(aprox - math.e) < 0.01

    def test_sin_grado3_alrededor_de_0(self):
        """sen(x) P3 = x - x³/6"""
        f = sp.sin(x)
        Pn, _ = taylor_polynomial(f, x, 0, 3)
        esperado = sp.sympify("x - x**3/6")
        assert sp.simplify(Pn - esperado) == 0

    def test_cos_termino_par_en_x0_0(self):
        """cos(x) solo tiene términos pares: P4 = 1 - x²/2 + x⁴/24"""
        f = sp.cos(x)
        Pn, _ = taylor_polynomial(f, x, 0, 4)
        esperado = sp.sympify("1 - x**2/2 + x**4/24")
        assert sp.simplify(Pn - esperado) == 0

    def test_polinomio_grado_0_es_constante(self):
        """P0 de cualquier función es simplemente f(x0)"""
        f = sp.exp(x)
        Pn, terms = taylor_polynomial(f, x, 0, 0)
        assert float(Pn) == pytest.approx(1.0)
        assert len(terms) == 1

    def test_numero_de_terminos_correcto(self):
        """Para grado n, deben retornarse n+1 términos"""
        f = sp.sin(x)
        for n in [0, 1, 3, 5]:
            _, terms = taylor_polynomial(f, x, 0, n)
            assert len(terms) == n + 1

    def test_expansion_alrededor_de_punto_no_cero(self):
        """ln(x) alrededor de x0=1: P1 = (x-1)"""
        f = sp.log(x)
        Pn, _ = taylor_polynomial(f, x, 1, 1)
        esperado = sp.sympify("x - 1")
        assert sp.simplify(Pn - esperado) == 0

    def test_funcion_constante(self):
        """f(x)=5  → P_n = 5 para cualquier n"""
        f = sp.Integer(5)
        for n in [0, 2, 4]:
            Pn, _ = taylor_polynomial(f, x, 0, n)
            assert float(Pn) == pytest.approx(5.0)


# ==============================================================
# 2. evaluar_directo
# ==============================================================

class TestEvaluarDirecto:

    def test_evalua_polinomio_simple(self):
        """P(x) = x² evaluado en x=3 → 9"""
        poly = x**2
        assert evaluar_directo(poly, x, 3) == pytest.approx(9.0)

    def test_evalua_constante(self):
        poly = sp.Integer(7)
        assert evaluar_directo(poly, x, 100) == pytest.approx(7.0)

    def test_coincide_con_valor_real_exp(self):
        """P4 de e^x evaluado en 0.5 debe estar muy cerca de e^0.5"""
        f = sp.exp(x)
        Pn, _ = taylor_polynomial(f, x, 0, 10)
        val = evaluar_directo(Pn, x, 0.5)
        assert abs(val - math.exp(0.5)) < 1e-7


# ==============================================================
# 3. horner
# ==============================================================

class TestHorner:

    def test_polinomio_lineal(self):
        """2x + 3 en x=4 → 11"""
        # coefs de mayor a menor: [2, 3]
        assert horner([2, 3], 4) == pytest.approx(11.0)

    def test_polinomio_cuadratico(self):
        """x² - x + 1 en x=2 → 3"""
        assert horner([1, -1, 1], 2) == pytest.approx(3.0)

    def test_polinomio_constante(self):
        assert horner([5.0], 99) == pytest.approx(5.0)

    def test_equivalente_a_evaluar_directo(self):
        """Horner y forma directa deben dar el mismo resultado"""
        f = sp.cos(x)
        Pn, _ = taylor_polynomial(f, x, 0, 6)
        coeffs = obtener_coeficientes(Pn, x, 6)
        val_horner  = horner(coeffs, 1.0)
        val_directo = evaluar_directo(Pn, x, 1.0)
        assert abs(val_horner - val_directo) < TOL

    def test_horner_en_cero(self):
        """Cualquier polinomio evaluado en 0 da el término independiente"""
        assert horner([3, 7, -2, 5], 0) == pytest.approx(5.0)


# ==============================================================
# 4. obtener_coeficientes
# ==============================================================

class TestObtenerCoeficientes:

    def test_longitud_igual_a_n_mas_1(self):
        f = sp.sin(x)
        Pn, _ = taylor_polynomial(f, x, 0, 5)
        coeffs = obtener_coeficientes(Pn, x, 5)
        assert len(coeffs) == 6

    def test_coeficientes_de_x_cuadrado(self):
        """x² → coefs deben ser [1, 0, 0]"""
        poly = x**2
        coeffs = obtener_coeficientes(poly, x, 2)
        assert coeffs == pytest.approx([1.0, 0.0, 0.0])

    def test_coeficientes_polinomio_conocido(self):
        """2x³ - x + 4 → [2, 0, -1, 4]"""
        poly = 2*x**3 - x + 4
        coeffs = obtener_coeficientes(poly, x, 3)
        assert coeffs == pytest.approx([2.0, 0.0, -1.0, 4.0])


# ==============================================================
# 5. calcular_errores
# ==============================================================

class TestCalcularErrores:

    def test_sin_error(self):
        err_abs, err_rel = calcular_errores(10.0, 10.0)
        assert err_abs == pytest.approx(0.0)
        assert err_rel == pytest.approx(0.0)

    def test_error_absoluto(self):
        err_abs, _ = calcular_errores(5.0, 4.0)
        assert err_abs == pytest.approx(1.0)

    def test_error_relativo(self):
        _, err_rel = calcular_errores(5.0, 4.0)
        assert err_rel == pytest.approx(0.2)

    def test_valor_real_cero_da_inf(self):
        _, err_rel = calcular_errores(0.0, 1.0)
        assert err_rel == float('inf')

    def test_error_negativo_se_toma_absoluto(self):
        """El error siempre es positivo aunque aprox > real"""
        err_abs, err_rel = calcular_errores(3.0, 5.0)
        assert err_abs == pytest.approx(2.0)
        assert err_rel == pytest.approx(2/3)


# ==============================================================
# 6. cota_error
# ==============================================================

class TestCotaError:

    def test_cota_es_mayor_que_error_real_sin(self):
        """La cota del residuo debe ser >= error real para sen(x)"""
        f = sp.sin(x)
        _, M, _ = cota_error(f, x, 0, 3, (-1, 1))
        Pn, _ = taylor_polynomial(f, x, 0, 3)
        x_test = 0.5
        real  = math.sin(x_test)
        aprox = float(Pn.subs(x, x_test))
        cota_val = M / math.factorial(4) * abs(x_test - 0)**4
        assert cota_val >= abs(real - aprox)

    def test_cota_es_mayor_que_error_real_exp(self):
        """La cota del residuo debe ser >= error real para e^x"""
        f = sp.exp(x)
        _, M, _ = cota_error(f, x, 0, 4, (0, 1))
        Pn, _ = taylor_polynomial(f, x, 0, 4)
        x_test = 0.8
        real  = math.exp(x_test)
        aprox = float(Pn.subs(x, x_test))
        cota_val = M / math.factorial(5) * abs(x_test)**5
        assert cota_val >= abs(real - aprox)

    def test_retorna_tres_valores(self):
        f = sp.cos(x)
        resultado = cota_error(f, x, 0, 2, (-1, 1))
        assert len(resultado) == 3

    def test_M_es_positivo(self):
        f = sp.exp(x)
        _, M, _ = cota_error(f, x, 0, 3, (0, 2))
        assert M > 0


# ==============================================================
# 7. terminos_necesarios
# ==============================================================

class TestTerminosNecesarios:

    def test_convergencia_exp(self):
        """e^x en x=1 con tol=1e-4 debe converger en pocos términos"""
        f = sp.exp(x)
        n, historial = terminos_necesarios(f, x, 0, 1, 1e-4)
        assert n <= 10
        # El error final debe cumplir la tolerancia
        _, _, err_final = historial[n - 1]
        assert err_final < 1e-4

    def test_convergencia_sin(self):
        """sen(x) en x=0.5 con tol=1e-6"""
        f = sp.sin(x)
        n, historial = terminos_necesarios(f, x, 0, 0.5, 1e-6)
        assert n <= 15
        _, _, err_final = historial[n - 1]
        assert err_final < 1e-6

    def test_historial_tiene_n_entradas(self):
        f = sp.exp(x)
        n, historial = terminos_necesarios(f, x, 0, 0.5, 1e-3)
        assert len(historial) == n

    def test_errores_decrecientes_en_general(self):
        """Los errores deben tender a decrecer conforme aumenta n"""
        f = sp.cos(x)
        _, historial = terminos_necesarios(f, x, 0, 0.3, 1e-8)
        errores = [h[2] for h in historial]
        # El último error debe ser menor que el primero
        assert errores[-1] < errores[0]

    def test_tolerancia_alta_necesita_menos_terminos(self):
        """Con tolerancia más laxa se necesitan menos términos"""
        f = sp.exp(x)
        n_holgado, _ = terminos_necesarios(f, x, 0, 1, 1e-2)
        n_estricto, _ = terminos_necesarios(f, x, 0, 1, 1e-8)
        assert n_holgado <= n_estricto