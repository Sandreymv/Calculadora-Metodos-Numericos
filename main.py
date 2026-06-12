"""Punto de entrada de la calculadora de métodos numéricos."""

from binarios_y_errores import menu_binarios_y_errores
from ecuaciones_no_lineales import menu_ecuaciones_no_lineales
from interpolacion_y_ajuste import menu_interpolacion_y_ajuste
from taylor import menu_taylor


def menu_principal():
    while True:
        print("\n" + "=" * 68)
        print("CALCULADORA DE MÉTODOS NUMÉRICOS")
        print("=" * 68)
        print("1. Taller 1 - Introducción y Polinomios de Taylor")
        print("2. Taller 2 - Binarios y análisis del error")
        print("3. Taller 3 - Solución de ecuaciones no lineales")
        print("4. Taller 4 - Interpolación y ajuste de curvas")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            menu_taylor()
        elif opcion == "2":
            menu_binarios_y_errores()
        elif opcion == "3":
            menu_ecuaciones_no_lineales()
        elif opcion == "4":
            menu_interpolacion_y_ajuste()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu_principal()
