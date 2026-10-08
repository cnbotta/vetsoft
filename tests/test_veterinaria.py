import pytest

from src.cliente import Cliente
from src.veterinaria import Veterinaria


# --- caso normal ---
def test_registrar_un_cliente_nuevo():
    vet = Veterinaria("Patitas")
    ana = Cliente("Ana Díaz", 30111222)
    vet.registrar_cliente(ana)
    assert vet.clientes() == [ana]


# --- caso borde ---
def test_una_veterinaria_nueva_no_tiene_clientes():
    assert Veterinaria("Patitas").clientes() == []


def test_la_lista_de_clientes_que_devuelve_es_una_copia():
    """Encapsulamiento: nadie registra clientes salteándose la validación del DNI."""
    vet = Veterinaria("Patitas")
    vet.clientes().append(Cliente("Colado", 11222333))
    assert vet.clientes() == []


# --- caso de error ---
def test_no_se_pueden_registrar_dos_clientes_con_el_mismo_dni():
    vet = Veterinaria("Patitas")
    vet.registrar_cliente(Cliente("Ana Díaz", 30111222))
    with pytest.raises(ValueError, match="Ya hay un cliente"):
        vet.registrar_cliente(Cliente("Otra Ana", 30111222))


# --- la veterinaria llega a los animales a través de sus clientes ---
def test_la_veterinaria_ve_los_animales_de_todos_sus_clientes(firulais, michi):
    vet = Veterinaria("Patitas")
    ana, beto = Cliente("Ana Díaz", 30111222), Cliente("Beto Ruiz", 28999111)
    ana.registrar_animal(firulais)
    beto.registrar_animal(michi)
    vet.registrar_cliente(ana)
    vet.registrar_cliente(beto)
    assert vet.animales() == [firulais, michi]


def test_no_guarda_una_lista_aparte_de_animales(firulais):
    """Un animal registrado al cliente DESPUÉS de darlo de alta aparece igual."""
    vet = Veterinaria("Patitas")
    ana = Cliente("Ana Díaz", 30111222)
    vet.registrar_cliente(ana)
    ana.registrar_animal(firulais)
    assert vet.animales() == [firulais]


def test_una_veterinaria_sin_clientes_no_tiene_animales():
    assert Veterinaria("Patitas").animales() == []


# --- animales al día (select) ---
def test_los_animales_al_dia_son_los_que_no_deben_vacunas(firulais, michi):
    vet = Veterinaria("Patitas")
    ana = Cliente("Ana Díaz", 30111222)
    for vacuna in firulais.esquema_de_vacunacion():
        firulais.aplicar_vacuna(vacuna)
    ana.registrar_animal(firulais)
    ana.registrar_animal(michi)
    vet.registrar_cliente(ana)
    assert vet.animales_al_dia() == [firulais]


def test_una_veterinaria_sin_clientes_no_tiene_animales_al_dia():
    assert Veterinaria("Patitas").animales_al_dia() == []


def test_un_animal_con_una_sola_vacuna_pendiente_no_esta_al_dia(firulais):
    vet = Veterinaria("Patitas")
    ana = Cliente("Ana Díaz", 30111222)
    firulais.aplicar_vacuna(firulais.esquema_de_vacunacion()[0])
    ana.registrar_animal(firulais)
    vet.registrar_cliente(ana)
    assert vet.animales_al_dia() == []


# --- buscar por nombre (detect) ---
def test_buscar_un_animal_por_nombre(firulais, michi):
    vet = Veterinaria("Patitas")
    ana = Cliente("Ana Díaz", 30111222)
    ana.registrar_animal(firulais)
    ana.registrar_animal(michi)
    vet.registrar_cliente(ana)
    assert vet.buscar_animal("Michi") is michi


def test_buscar_un_animal_que_no_existe_devuelve_none(firulais):
    vet = Veterinaria("Patitas")
    ana = Cliente("Ana Díaz", 30111222)
    ana.registrar_animal(firulais)
    vet.registrar_cliente(ana)
    assert vet.buscar_animal("Pelusa") is None


def test_buscar_devuelve_el_primero_cuando_hay_nombres_repetidos():
    from datetime import date

    from src.animal import crear_animal

    vet = Veterinaria("Patitas")
    ana = Cliente("Ana Díaz", 30111222)
    primero = crear_animal("Negro", "perro", date(2019, 1, 1))
    segundo = crear_animal("Negro", "gato", date(2021, 1, 1))
    ana.registrar_animal(primero)
    ana.registrar_animal(segundo)
    vet.registrar_cliente(ana)
    assert vet.buscar_animal("Negro") is primero
