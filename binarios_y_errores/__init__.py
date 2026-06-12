"""Herramientas para el taller de binarios y análisis del error."""
from . import conversion_binaria


def menu_binarios_y_errores():
    return conversion_binaria.menu_binarios_y_errores()


__all__ = ["menu_binarios_y_errores"]
