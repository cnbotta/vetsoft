import pytest

from src.cliente import Cliente


# --- caso normal ---
def test_un_cliente_nuevo_arranca_sin_animales():
    ana = Cliente("Ana Díaz", 30111222)
    assert ana.animales() == []


def test_un_cliente_responde_su_nombre_y_dni():
    ana = Cliente("Ana Díaz", 30111222)
    assert ana.nombre() == "Ana Díaz"
    assert ana.dni() == 30111222


# --- caso de error ---
@pytest.mark.parametrize("dni", [0, -30111222, None, "30111222"])
def test_no_se_puede_crear_un_cliente_sin_dni_valido(dni):
    with pytest.raises(ValueError, match="DNI"):
        Cliente("Ana Díaz", dni)


# --- registrar una mascota a nombre del cliente ---
def test_un_cliente_puede_tener_varios_animales(firulais, michi):
    ana = Cliente("Ana Díaz", 30111222)
    ana.registrar_animal(firulais)
    ana.registrar_animal(michi)
    assert ana.animales() == [firulais, michi]
    assert ana.cantidad_de_animales() == 2


def test_la_lista_de_animales_que_devuelve_es_una_copia(firulais):
    ana = Cliente("Ana Díaz", 30111222)
    ana.animales().append(firulais)
    assert ana.cantidad_de_animales() == 0


def test_no_se_puede_registrar_dos_veces_el_mismo_animal(firulais):
    ana = Cliente("Ana Díaz", 30111222)
    ana.registrar_animal(firulais)
    with pytest.raises(ValueError, match="ya está registrado"):
        ana.registrar_animal(firulais)
