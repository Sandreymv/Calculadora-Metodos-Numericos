"""
==============================================================
  SIMULACIÓN Y COMPUTACIÓN NUMÉRICA - Universidad del Valle
  Módulo 1: Polinomios de Taylor
==============================================================
  Funcionalidades:
    1. Calcular el polinomio de Taylor de grado n de cualquier función
       simbólica alrededor de un punto x0
    2. Evaluar el polinomio (forma directa y forma anidada de Horner)
    3. Calcular la cota del error de truncamiento (término del residuo)
    4. Calcular el error absoluto y relativo respecto al valor real
    5. Determinar cuántos términos se necesitan para una precisión dada
    6. Graficar la función original vs el polinomio de Taylor
==============================================================
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from math import factorial


# ─────────────────────────────────────────────
#  1. POLINOMIO DE TAYLOR (simbólico)
# ─────────────────────────────────────────────

def taylor_polynomial(f_expr, x, x0, n):
    """
    Calcula el polinomio de Taylor de grado n de f(x) alrededor de x0.

    Parámetros
    ----------
    f_expr : expresión sympy   → la función f(x)
    x      : símbolo sympy     → la variable independiente
    x0     : número            → punto de expansión
    n      : int               → grado del polinomio

    Retorna
    -------
    Pn     : expresión sympy   → polinomio de Taylor P_n(x)
    terms  : list              → lista de los términos individuales
    """
    Pn = sp.Integer(0)
    terms = []

    for k in range(n + 1):
        fk = sp.diff(f_expr, x, k)          # k-ésima derivada de f
        fk_at_x0 = fk.subs(x, x0)           # evaluada en x0
        term = (fk_at_x0 / factorial(k)) * (x - x0)**k
        term_simplified = sp.simplify(term)
        terms.append(term_simplified)
        Pn += term

    return sp.expand(Pn), terms


# ─────────────────────────────────────────────
#  2. EVALUACIÓN: FORMA DIRECTA vs HORNER
# ─────────────────────────────────────────────

def evaluar_directo(poly_expr, x, val):
    """Evalúa el polinomio sustituyendo directamente x = val."""
    return float(poly_expr.subs(x, val))


def horner(coeficientes, val):
    """
    Evalúa un polinomio usando el método de Horner (forma anidada).
    Reduce al mínimo las operaciones aritméticas y el error de redondeo.

    coeficientes : list  → [a_n, a_{n-1}, ..., a_1, a_0]  (mayor grado primero)
    val          : float → punto donde evaluar

    Retorna el valor numérico del polinomio en val.
    """
    resultado = coeficientes[0]
    for c in coeficientes[1:]:
        resultado = resultado * val + c
    return resultado


def obtener_coeficientes(poly_expr, x, n):
    """
    Extrae los coeficientes del polinomio en orden descendente de grado.
    Retorna lista [a_n, a_{n-1}, ..., a_0].
    """
    poly = sp.Poly(sp.expand(poly_expr), x)
    # Poly.all_coeffs() ya devuelve de mayor a menor grado
    coeffs = poly.all_coeffs()
    # Completar con ceros si el grado efectivo es menor que n
    while len(coeffs) < n + 1:
        coeffs.insert(0, sp.Integer(0))
    return [float(c) for c in coeffs]


# ─────────────────────────────────────────────
#  3. COTA DEL ERROR (término del residuo Rn)
# ─────────────────────────────────────────────

def cota_error(f_expr, x, x0, n, intervalo):
    """
    Calcula la cota superior del error de truncamiento |R_n(x)|.

    La fórmula del residuo de Taylor es:
        R_n(x) = f^{(n+1)}(c) / (n+1)!  *  (x - x0)^{n+1}
    donde c está entre x0 y x.

    Se estima tomando el máximo de |f^{(n+1)}| en el intervalo dado.

    Parámetros
    ----------
    intervalo : tuple (a, b)  → intervalo [a, b] donde se busca el máximo

    Retorna
    -------
    cota_expr : expresión de la cota en función de x (sympy)
    max_deriv : valor numérico máximo de |f^{(n+1)}| en el intervalo
    """
    deriv_n1 = sp.diff(f_expr, x, n + 1)          # derivada (n+1)-ésima

    # Máximo numérico de |f^{(n+1)}| en el intervalo
    f_num = sp.lambdify(x, sp.Abs(deriv_n1), 'numpy')
    xs = np.linspace(float(intervalo[0]), float(intervalo[1]), 1000)

    try:
        valores = f_num(xs)
        max_deriv = float(np.max(np.abs(valores)))
    except Exception:
        # Si hay singularidades, evaluar en puntos alejados de ellas
        max_deriv = float(sp.Maximum(sp.Abs(deriv_n1), x, sp.Interval(*intervalo)))

    # Cota simbólica: M / (n+1)! * |x - x0|^{n+1}
    M = sp.Symbol('M', positive=True)
    cota_expr = (sp.Abs(x - x0)**(n + 1)) / factorial(n + 1)

    return cota_expr, max_deriv, deriv_n1


# ─────────────────────────────────────────────
#  4. ERROR ABSOLUTO Y RELATIVO
# ─────────────────────────────────────────────

def calcular_errores(valor_real, valor_aprox):
    """
    Calcula el error absoluto y el error relativo.

    Error absoluto  = |valor_real - valor_aprox|
    Error relativo  = |error_absoluto / valor_real|  (si valor_real ≠ 0)
    """
    error_abs = abs(valor_real - valor_aprox)
    error_rel = abs(error_abs / valor_real) if valor_real != 0 else float('inf')
    return error_abs, error_rel


# ─────────────────────────────────────────────
#  5. TÉRMINOS NECESARIOS PARA UNA PRECISIÓN
# ─────────────────────────────────────────────

def terminos_necesarios(f_expr, x, x0, x_eval, tolerancia, max_terminos=50):
    """
    Determina cuántos términos del polinomio de Taylor se necesitan
    para aproximar f(x_eval) con un error menor que la tolerancia dada.

    Retorna
    -------
    n          : int   → número de términos necesarios (grado del polinomio)
    historial  : list  → [(n, aprox, error_abs)] para cada iteración
    """
    f_real = float(f_expr.subs(x, x_eval))
    historial = []

    for n in range(1, max_terminos + 1):
        Pn, _ = taylor_polynomial(f_expr, x, x0, n)
        aprox = float(Pn.subs(x, x_eval))
        error_abs, _ = calcular_errores(f_real, aprox)
        historial.append((n, aprox, error_abs))

        if error_abs < tolerancia:
            return n, historial

    return max_terminos, historial


# ─────────────────────────────────────────────
#  6. GRAFICAR f(x) vs P_n(x)
# ─────────────────────────────────────────────

def graficar_taylor(f_expr, x, x0, n, intervalo, titulo=None):
    """
    Grafica la función original f(x) y su polinomio de Taylor P_n(x)
    en el intervalo dado.
    """
    Pn, _ = taylor_polynomial(f_expr, x, x0, n)

    f_num  = sp.lambdify(x, f_expr, 'numpy')
    Pn_num = sp.lambdify(x, Pn,     'numpy')

    xs = np.linspace(float(intervalo[0]), float(intervalo[1]), 500)

    try:
        ys_f  = f_num(xs)
        ys_Pn = Pn_num(xs)
    except Exception as e:
        print(f"  [Advertencia al graficar]: {e}")
        return

    plt.figure(figsize=(9, 5))
    plt.plot(xs, ys_f,  'b-',  linewidth=2,   label=f'f(x) = {sp.latex(f_expr)}')
    plt.plot(xs, ys_Pn, 'r--', linewidth=2,   label=f'P_{n}(x)')
    plt.axvline(x=float(x0), color='gray', linestyle=':', alpha=0.7, label=f'x₀ = {x0}')
    plt.ylim(np.percentile(ys_f[np.isfinite(ys_f)], 1) - 1,
             np.percentile(ys_f[np.isfinite(ys_f)], 99) + 1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(titulo or f'Taylor P_{n}(x) alrededor de x₀ = {x0}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
#  MENÚ INTERACTIVO DEL MÓDULO
# ─────────────────────────────────────────────

def menu_taylor():
    x = sp.Symbol('x')

    print("\n" + "="*60)
    print("   MÓDULO 1 — POLINOMIOS DE TAYLOR")
    print("="*60)
    print("  1. Calcular polinomio de Taylor P_n(x)")
    print("  2. Evaluar P_n(x) — forma directa vs Horner")
    print("  3. Cota del error de truncamiento")
    print("  4. Términos necesarios para una tolerancia dada")
    print("  5. Graficar f(x) vs P_n(x)")
    print("  0. Volver al menú principal")
    print("="*60)

    while True:
        opcion = input("\n  Selecciona una opción: ").strip()

        # ── Opción 1: Calcular P_n ──────────────────────────────
        if opcion == '1':
            print("\n  Escribe la función usando sintaxis Python/SymPy.")
            print("  Ejemplos: sqrt(x)  |  cos(x)  |  exp(x)*cos(x)  |  (x-1)*ln(x)")
            expr_str = input("  f(x) = ").strip()
            try:
                f_expr = sp.sympify(expr_str, locals={'x': x,
                                                       'sqrt': sp.sqrt,
                                                       'sin': sp.sin,
                                                       'cos': sp.cos,
                                                       'exp': sp.exp,
                                                       'ln': sp.log,
                                                       'log': sp.log,
                                                       'cosh': sp.cosh,
                                                       'sinh': sp.sinh,
                                                       'pi': sp.pi,
                                                       'E': sp.E})
            except Exception as e:
                print(f"  ✗ Error al parsear la función: {e}")
                continue

            x0 = float(input("  Punto de expansión x₀ = "))
            n  = int(input("  Grado del polinomio n = "))

            Pn, terms = taylor_polynomial(f_expr, x, x0, n)

            print(f"\n  ── Polinomio de Taylor P_{n}(x) alrededor de x₀ = {x0} ──")
            print(f"\n  Términos individuales:")
            for k, t in enumerate(terms):
                print(f"    k={k}: {t}")
            print(f"\n  P_{n}(x) = {Pn}")
            print(f"\n  Forma simplificada:\n  P_{n}(x) = {sp.simplify(Pn)}")

        # ── Opción 2: Evaluación directa vs Horner ──────────────
        elif opcion == '2':
            expr_str = input("\n  f(x) = ").strip()
            try:
                f_expr = sp.sympify(expr_str, locals={'x': x, 'sqrt': sp.sqrt,
                                                       'sin': sp.sin, 'cos': sp.cos,
                                                       'exp': sp.exp, 'ln': sp.log,
                                                       'log': sp.log, 'cosh': sp.cosh,
                                                       'pi': sp.pi, 'E': sp.E})
            except Exception as e:
                print(f"  ✗ {e}"); continue

            x0    = float(input("  x₀ = "))
            n     = int(input("  Grado n = "))
            x_val = float(input("  Evaluar en x = "))

            Pn, _ = taylor_polynomial(f_expr, x, x0, n)

            # Evaluación directa
            val_directo = evaluar_directo(Pn, x, x_val)

            # Evaluación por Horner
            coeffs = obtener_coeficientes(Pn, x, n)
            val_horner = horner(coeffs, x_val)

            # Valor real
            val_real = float(f_expr.subs(x, x_val))

            err_abs_d, err_rel_d = calcular_errores(val_real, val_directo)
            err_abs_h, err_rel_h = calcular_errores(val_real, val_horner)

            print(f"\n  ── Evaluación de P_{n}({x_val}) ──")
            print(f"  Valor real f({x_val})          = {val_real:.10f}")
            print(f"  Forma directa                  = {val_directo:.10f}")
            print(f"    Error absoluto               = {err_abs_d:.2e}")
            print(f"    Error relativo               = {err_rel_d:.2e}")
            print(f"  Forma anidada (Horner)         = {val_horner:.10f}")
            print(f"    Error absoluto               = {err_abs_h:.2e}")
            print(f"    Error relativo               = {err_rel_h:.2e}")
            print(f"\n  Coeficientes (mayor→menor grado): {[round(c,6) for c in coeffs]}")

        # ── Opción 3: Cota del error ─────────────────────────────
        elif opcion == '3':
            expr_str = input("\n  f(x) = ").strip()
            try:
                f_expr = sp.sympify(expr_str, locals={'x': x, 'sqrt': sp.sqrt,
                                                       'sin': sp.sin, 'cos': sp.cos,
                                                       'exp': sp.exp, 'ln': sp.log,
                                                       'log': sp.log, 'pi': sp.pi,
                                                       'E': sp.E})
            except Exception as e:
                print(f"  ✗ {e}"); continue

            x0 = float(input("  x₀ = "))
            n  = int(input("  Grado n = "))
            a  = float(input("  Intervalo [a, b] — a = "))
            b  = float(input("                    b = "))

            cota_expr, M, deriv_n1 = cota_error(f_expr, x, x0, n, (a, b))

            print(f"\n  ── Cota del error de truncamiento R_{n}(x) ──")
            print(f"  Derivada de orden (n+1) = {n+1}:")
            print(f"    f^({n+1})(x) = {sp.simplify(deriv_n1)}")
            print(f"\n  Máximo de |f^({n+1})(x)| en [{a}, {b}]:")
            print(f"    M = {M:.6f}")
            print(f"\n  Fórmula de la cota:")
            print(f"    |R_{n}(x)| ≤  M / {factorial(n+1)}  ·  |x - {x0}|^{n+1}")
            print(f"    |R_{n}(x)| ≤  {M:.6f} / {factorial(n+1)}  ·  |x - {x0}|^{n+1}")

            # Si el usuario quiere evaluar la cota en un punto específico
            ev = input("\n  ¿Evaluar la cota en un punto específico? (s/n): ").strip().lower()
            if ev == 's':
                xp = float(input("  x = "))
                cota_val = M / factorial(n+1) * abs(xp - x0)**(n+1)
                print(f"\n  Cota numérica en x={xp}: |R_{n}({xp})| ≤ {cota_val:.6e}")

                # Comparar con error real
                Pn, _ = taylor_polynomial(f_expr, x, x0, n)
                aprox = float(Pn.subs(x, xp))
                real  = float(f_expr.subs(x, xp))
                err_real = abs(real - aprox)
                print(f"  Error real               |f({xp}) - P_{n}({xp})| = {err_real:.6e}")
                print(f"  ¿Cota válida? {'✓ Sí' if cota_val >= err_real else '✗ No (revisar intervalo)'}")

        # ── Opción 4: Términos necesarios ────────────────────────
        elif opcion == '4':
            expr_str = input("\n  f(x) = ").strip()
            try:
                f_expr = sp.sympify(expr_str, locals={'x': x, 'sqrt': sp.sqrt,
                                                       'sin': sp.sin, 'cos': sp.cos,
                                                       'exp': sp.exp, 'ln': sp.log,
                                                       'log': sp.log, 'pi': sp.pi,
                                                       'E': sp.E})
            except Exception as e:
                print(f"  ✗ {e}"); continue

            x0        = float(input("  x₀ = "))
            x_eval    = float(input("  Evaluar en x = "))
            tol_str   = input("  Tolerancia (ej: 1e-4 o 0.0001) = ").strip()
            tolerancia = float(tol_str)

            n, historial = terminos_necesarios(f_expr, x, x0, x_eval, tolerancia)

            print(f"\n  ── Convergencia hacia f({x_eval}) ──")
            print(f"  {'n':>4}  {'P_n(x)':>18}  {'Error abs':>14}")
            print(f"  {'-'*42}")
            for (ni, aprox, err) in historial:
                marca = " ← ✓" if ni == n and err < tolerancia else ""
                print(f"  {ni:>4}  {aprox:>18.10f}  {err:>14.6e}{marca}")

            f_real = float(f_expr.subs(x, x_eval))
            print(f"\n  Valor real f({x_eval}) = {f_real:.10f}")
            print(f"  Se necesitan {n} término(s) para error < {tolerancia:.2e}")

        # ── Opción 5: Gráfica ────────────────────────────────────
        elif opcion == '5':
            expr_str = input("\n  f(x) = ").strip()
            try:
                f_expr = sp.sympify(expr_str, locals={'x': x, 'sqrt': sp.sqrt,
                                                       'sin': sp.sin, 'cos': sp.cos,
                                                       'exp': sp.exp, 'ln': sp.log,
                                                       'log': sp.log, 'cosh': sp.cosh,
                                                       'pi': sp.pi, 'E': sp.E})
            except Exception as e:
                print(f"  ✗ {e}"); continue

            x0 = float(input("  x₀ = "))
            n  = int(input("  Grado n = "))
            a  = float(input("  Intervalo a graficar [a, b] — a = "))
            b  = float(input("                               b = "))

            graficar_taylor(f_expr, x, x0, n, (a, b))

        elif opcion == '0':
            break
        else:
            print("  Opción no válida.")


# ─────────────────────────────────────────────
#  Ejecución directa (prueba rápida)
# ─────────────────────────────────────────────
# Este módulo es importado por main.py
# Para pruebas directas puedes ejecutar: python -m taylor.taylor