from datetime import date

import pytest

from src.animal import crear_animal


# --- caso normal ---
def test_un_perro_responde_su_esquema(firulais):
    assert firulais.esquema_de_vacunacion() == ["Quíntuple", "Antirrábica"]


def test_un_gato_responde_su_esquema(michi):
    assert michi.esquema_de_vacunacion() == ["Triple felina", "Antirrábica"]


# --- caso borde ---
def test_un_animal_recien_registrado_tiene_todas_sus_vacunas_pendientes(firulais):
    assert firulais.vacunas_pendientes() == firulais.esquema_de_vacunacion()


# --- caso de error ---
def test_no_se_puede_crear_un_animal_de_una_especie_que_no_atendemos():
    with pytest.raises(ValueError, match="No atendemos"):
        crear_animal("Nemo", "pez", date(2023, 1, 1))
