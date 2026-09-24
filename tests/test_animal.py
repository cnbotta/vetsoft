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


# --- registrar una vacuna aplicada ---
def test_al_aplicar_todas_las_vacunas_queda_al_dia(firulais):
    firulais.aplicar_vacuna("Quíntuple")
    firulais.aplicar_vacuna("Antirrábica")
    assert firulais.esta_al_dia() is True
    assert firulais.vacunas_pendientes() == []


def test_la_lista_de_vacunas_que_devuelve_es_una_copia(firulais):
    """Encapsulamiento: tocar la lista devuelta no altera el estado del animal."""
    firulais.aplicar_vacuna("Quíntuple")
    copia = firulais.vacunas_aplicadas()
    copia.append("Vacuna inventada")
    assert firulais.vacunas_aplicadas() == ["Quíntuple"]


def test_no_se_puede_aplicar_una_vacuna_de_otra_especie(firulais):
    with pytest.raises(ValueError, match="no corresponde"):
        firulais.aplicar_vacuna("Triple felina")


def test_no_se_puede_aplicar_dos_veces_la_misma_vacuna(michi):
    michi.aplicar_vacuna("Antirrábica")
    with pytest.raises(ValueError, match="ya tiene"):
        michi.aplicar_vacuna("Antirrábica")
