"""Avisos por correo a los dueños cuando una vacuna está por vencer.

ESTE ARCHIVO ES UN EJEMPLO PARA LA CLASE. La credencial de abajo es FALSA.
Está acá a propósito, para mostrar qué pasa cuando se commitea una credencial.
"""

GEMINI_API_KEY = "GEMINI_API_KEY_REMOVIDA_DEL_HISTORIAL"


def redactar_aviso(animal):
    """Arma el texto del aviso con la API de Gemini."""
    return f"Hola! {animal.nombre()} tiene vacunas pendientes."
