"""Conversión entre bases y apoyo para el taller de binarios."""

from __future__ import annotations

import math

from numerical_utils import evaluate_rounded_expression

from .errores import (
    cifras_significativas_desde_error_relativo,
    error_absoluto,
    error_relativo,
)


def entero_a_base(numero, base):
    if base < 2:
        raise ValueError("La base debe ser mayor o igual que 2")
    n = abs(int(numero))
    if n == 0:
        return "0"
    digitos = []
    while n > 0:
        digitos.append(str(n % base))
        n //= base
    return ("-" if numero < 0 else "") + "".join(reversed(digitos))


def fraccion_a_base(fraccion, base, max_digitos=10):
    if base < 2:
        raise ValueError("La base debe ser mayor o igual que 2")
    valor = abs(fraccion)
    digitos = []
    for _ in range(max_digitos):
        valor *= base
        digito = int(valor)
        digitos.append(str(digito))
        valor -= digito
        if valor == 0:
            break
    return "".join(digitos) or "0"


def decimal_a_base(numero, base=2, max_digitos_fraccion=10):
    numero = float(numero)
    parte_entera = int(abs(numero))
    parte_fraccion = abs(numero) - parte_entera
    entero = entero_a_base(parte_entera, base)
    if max_digitos_fraccion <= 0 or parte_fraccion == 0:
        return ("-" if numero < 0 else "") + entero
    fraccion = fraccion_a_base(parte_fraccion, base, max_digitos_fraccion)
    return ("-" if numero < 0 else "") + f"{entero}.{fraccion}"


def decimal_a_binario(numero, max_digitos_fraccion=10):
    return decimal_a_base(numero, 2, max_digitos_fraccion)


def binario_a_decimal(cadena):
    texto = str(cadena).strip().lower().replace("dos", "")
    texto = texto.replace("·", ".")
    sign = -1 if texto.startswith("-") else 1
    if texto[:1] in "+-":
        texto = texto[1:]
    if "." in texto:
        entero, fraccion = texto.split(".", 1)
    else:
        entero, fraccion = texto, ""
    valor = 0.0
    for caracter in entero:
        if caracter not in "01":
            continue
        valor = valor * 2 + int(caracter)
    for indice, caracter in enumerate(fraccion, start=1):
        if caracter not in "01":
            continue
        valor += int(caracter) * 2 ** (-indice)
    return sign * valor


def _leer_float(texto):
    return float(texto.replace("·", "."))


def _error_reporte(valor_real, aproximado):
    ea = error_absoluto(valor_real, aproximado)
    er = error_relativo(valor_real, aproximado)
    print(f"Valor exacto = {valor_real}")
    print(f"Aproximación  = {aproximado}")
    print(f"Error absoluto = {ea}")
    print(f"Error relativo = {er}")
    cifras = cifras_significativas_desde_error_relativo(er)
    print(f"Cifras significativas ≈ {cifras}")


def _menu_error_expresiones():
    while True:
        print("\nEjercicio 2 - Aritmética con redondeo de 3 cifras")
        print("1. Evaluar una expresión con redondeo a 3 cifras")
        print("2. Ejemplo guiado: 133 + 0.921")
        print("3. Ejemplo guiado: 133 - 0.499")
        print("4. Ejemplo guiado: (121 - 0.327) - 119")
        print("5. Ejemplo guiado: (121 - 199) - 0.327")
        print("0. Volver")

        opcion = input("Opción: ").strip()
        if opcion == "1":
            expr = input("Expresión usando x si quieres variables = ")
            texto = input(
                "Variables separadas por coma (ej: x=1,y=2) o Enter = "
            ).strip()
            variables = {}
            if texto:
                for parte in texto.split(","):
                    nombre, valor = parte.split("=")
                    variables[nombre.strip()] = _leer_float(valor.strip())
            resultado = evaluate_rounded_expression(
                expr, digits=3, variables=variables
            )
            print(f"Resultado con redondeo de 3 cifras = {resultado}")
        elif opcion == "2":
            resultado = evaluate_rounded_expression("133 + 0.921", digits=3)
            _error_reporte(133.921, resultado)
        elif opcion == "3":
            resultado = evaluate_rounded_expression("133 - 0.499", digits=3)
            _error_reporte(132.501, resultado)
        elif opcion == "4":
            resultado = evaluate_rounded_expression(
                "(121 - 0.327) - 119", digits=3
            )
            _error_reporte(1.673, resultado)
        elif opcion == "5":
            resultado = evaluate_rounded_expression(
                "(121 - 199) - 0.327", digits=3
            )
            _error_reporte(-78.327, resultado)
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def _menu_error_basico():
    while True:
        print("\nEjercicio 1 - Error absoluto y relativo")
        print("1. Ingresar valor exacto y aproximado")
        print("2. Mostrar casos del enunciado")
        print("0. Volver")

        opcion = input("Opción: ").strip()
        if opcion == "1":
            real = float(input("Valor exacto p = "))
            aprox = float(input("Aproximación p* = "))
            _error_reporte(real, aprox)
        elif opcion == "2":
            casos = [
                ("π", math.pi, 22 / 7),
                ("1/3", 1 / 3, 0.333),
                ("π/1000", math.pi / 1000, 0.0031),
                ("100/3", 100 / 3, 33.3),
                ("e", math.e, 2.718),
                ("e^10", math.e**10, 22000),
                ("8!", math.factorial(8), 39900),
                ("√2", math.sqrt(2), 1.414),
            ]
            for nombre, real, aprox in casos:
                print(f"\nCaso {nombre}")
                _error_reporte(real, aprox)
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def _menu_conversiones():
    while True:
        print("\nEjercicios 5-12 - Conversiones y bases")
        print("1. Binario a decimal")
        print("2. Decimal a binario/base")
        print("3. Base 3 de enteros")
        print("4. Base 3 de fracciones")
        print("5. Número racional como fracción binaria")
        print("0. Volver")

        opcion = input("Opción: ").strip()
        if opcion == "1":
            cadena = input("Número binario = ")
            print(f"Decimal = {binario_a_decimal(cadena)}")
        elif opcion == "2":
            numero = _leer_float(input("Número decimal = "))
            base = int(input("Base destino = "))
            digitos = int(input("Dígitos fraccionarios = "))
            print(f"Resultado = {decimal_a_base(numero, base, digitos)}")
        elif opcion == "3":
            numero = int(input("Entero a convertir a base 3 = "))
            print(f"Base 3 = {decimal_a_base(numero, 3, 0)}")
        elif opcion == "4":
            numero = _leer_float(input("Fracción a convertir a base 3 = "))
            print(f"Base 3 ≈ {decimal_a_base(numero, 3, 12)}")
        elif opcion == "5":
            numero = _leer_float(input("Número racional = "))
            print(f"Binario ≈ {decimal_a_binario(numero, 12)}")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def _menu_punto_flotante():
    while True:
        print("\nEjercicio 10 - Punto flotante normalizado")
        print("1. Mostrar tabla de la máquina de 4 bits")
        print("2. Aproximar un número real")
        print("3. Simular operación simple")
        print("0. Volver")

        opcion = input("Opción: ").strip()
        if opcion == "1":
            from .punto_flotante import tabla_flotante

            for mantisa, exp, valor in tabla_flotante():
                print(f"{mantisa} x 2^{exp:>2} = {valor}")
        elif opcion == "2":
            from .punto_flotante import aproximar_flotante

            valor = _leer_float(input("Número a aproximar = "))
            aprox, mantisa, exp = aproximar_flotante(valor)
            print(f"Aproximación = {aprox} usando {mantisa} x 2^{exp}")
        elif opcion == "3":
            from .punto_flotante import operar_en_punto_flotante

            a = _leer_float(input("a = "))
            oper = input("Operación (+, -, *, /) = ").strip()
            b = _leer_float(input("b = "))
            mapa = {
                "+": lambda x, y: x + y,
                "-": lambda x, y: x - y,
                "*": lambda x, y: x * y,
                "/": lambda x, y: x / y,
            }
            if oper not in mapa:
                print("Operación no válida.")
                continue
            exacto, aprox, mantisa, exp = operar_en_punto_flotante(
                a, b, mapa[oper]
            )
            print(f"Exacto = {exacto}")
            print(f"Aproximado = {aprox} usando {mantisa} x 2^{exp}")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def menu_binarios_y_errores():
    while True:
        print("\n" + "=" * 68)
        print("TALLER 2 - BINARIOS Y ANÁLISIS DEL ERROR")
        print("=" * 68)
        print("1. Ejercicio 1 - Error absoluto y relativo")
        print("2. Ejercicio 2 - Aritmética con redondeo")
        print("3. Ejercicios 5-12 - Conversiones")
        print("4. Ejercicio 10 - Punto flotante")
        print("0. Volver")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            _menu_error_basico()
        elif opcion == "2":
            _menu_error_expresiones()
        elif opcion == "3":
            _menu_conversiones()
        elif opcion == "4":
            _menu_punto_flotante()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
