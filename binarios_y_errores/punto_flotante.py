"""Simulación de aritmética de punto flotante binario normalizado."""

from __future__ import annotations

from itertools import product
from operator import add, mul, sub, truediv


def mantisas_normalizadas(total_bits=4):
    if total_bits < 1:
        raise ValueError("El número de bits debe ser positivo")
    valores = []
    for bits in product("01", repeat=total_bits - 1):
        cadena = "1" + "".join(bits)
        valor = int(cadena, 2) / (2 ** total_bits)
        valores.append((f"0.{cadena}", valor))
    return valores


def tabla_flotante(mantisa_bits=4, exp_min=-3, exp_max=4):
    mantisas = mantisas_normalizadas(mantisa_bits)
    tabla = []
    for exp in range(exp_min, exp_max + 1):
        for etiqueta, q in mantisas:
            tabla.append((etiqueta, exp, q * (2 ** exp)))
    return tabla


def aproximar_flotante(valor, mantisa_bits=4, exp_min=-3, exp_max=4):
    if valor == 0:
        return 0.0, "0", 0
    signo = -1 if valor < 0 else 1
    objetivo = abs(valor)
    mejor = None
    for etiqueta, exp, aproximado in tabla_flotante(
        mantisa_bits, exp_min, exp_max
    ):
        diff = abs(objetivo - aproximado)
        if mejor is None or diff < mejor[0]:
            mejor = (diff, signo * aproximado, etiqueta, exp)
    return mejor[1], mejor[2], mejor[3]


def operar_en_punto_flotante(
    a, b, operacion, mantisa_bits=4, exp_min=-3, exp_max=4
):
    exacto = operacion(a, b)
    aprox, mantisa, exp = aproximar_flotante(
        exacto, mantisa_bits, exp_min, exp_max
    )
    return exacto, aprox, mantisa, exp


def menu_punto_flotante():
    while True:
        print("\n" + "=" * 68)
        print("SIMULADOR DE PUNTO FLOTANTE")
        print("=" * 68)
        print("1. Mostrar tabla de aproximaciones")
        print("2. Aproximar un número real")
        print("3. Simular una operación +, -, *, /")
        print("0. Volver")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            for mantisa, exp, valor in tabla_flotante():
                print(f"{mantisa} x 2^{exp:>2} = {valor}")
        elif opcion == "2":
            valor = float(input("Número a aproximar = "))
            aprox, mantisa, exp = aproximar_flotante(valor)
            print(f"Aproximación = {aprox} usando {mantisa} x 2^{exp}")
        elif opcion == "3":
            a = float(input("a = "))
            oper = input("Operación (+, -, *, /) = ").strip()
            b = float(input("b = "))
            mapa = {"+": add, "-": sub, "*": mul, "/": truediv}
            if oper not in mapa:
                print("Operación no válida.")
                continue
            exacto, aprox, mantisa, exp = operar_en_punto_flotante(
                a, b, mapa[oper]
            )
            print(f"Resultado exacto = {exacto}")
            print(
                f"Aproximación flotante = {aprox} usando {mantisa} x 2^{exp}"
            )
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
