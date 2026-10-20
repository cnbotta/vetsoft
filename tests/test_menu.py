from src.cliente import Cliente
from src.menu import Menu, datos_de_ejemplo
from src.veterinaria import Veterinaria


class PantallaFalsa:
    """Guarda lo que se escribiría en pantalla, para poder revisarlo en los tests."""

    def __init__(self):
        self.lineas = []

    def escribir(self, texto=""):
        self.lineas.append(str(texto))

    def texto(self):
        return "\n".join(self.lineas)


def correr(opciones, vet=None):
    """Corre el menú con una lista de respuestas ya preparadas."""
    pantalla = PantallaFalsa()
    pendientes = list(opciones)
    menu = Menu(
        vet if vet is not None else Veterinaria("San Roque"),
        leer=lambda _mensaje="": pendientes.pop(0) if pendientes else "0",
        escribir=pantalla.escribir,
    )
    menu.correr()
    return pantalla.texto()


# --- el menú se muestra y se puede salir ---
def test_el_menu_se_muestra_y_termina_con_la_opcion_de_salir():
    salida = correr(["0"])

    assert "VetSoft" in salida
    assert "0" in salida and "Salir" in salida


def test_despues_de_una_opcion_vuelve_al_menu():
    salida = correr(["7", "0"])  # 7 = conteo por especie

    # el encabezado aparece dos veces: una por cada vuelta al menú
    assert salida.count("VetSoft") == 2


def test_una_opcion_que_no_existe_avisa_y_no_corta_el_programa():
    salida = correr(["99", "0"])

    assert "no existe" in salida.lower()
    assert salida.count("VetSoft") == 2


# --- datos de ejemplo ---
def test_la_opcion_de_datos_de_ejemplo_carga_clientes_y_animales():
    vet = Veterinaria("San Roque")
    correr(["1", "0"], vet)

    assert len(vet.clientes()) > 0
    assert len(vet.animales()) > 0


def test_los_datos_de_ejemplo_traen_animales_al_dia_y_con_pendientes():
    vet = datos_de_ejemplo()

    assert len(vet.animales_al_dia()) > 0
    assert len(vet.animales_con_vacunas_pendientes()) > 0


# --- altas desde el menú ---
def test_registrar_un_cliente_desde_el_menu():
    vet = Veterinaria("San Roque")
    correr(["2", "Ana", "30111222", "0"], vet)

    assert [c.nombre() for c in vet.clientes()] == ["Ana"]


def test_registrar_un_animal_a_nombre_de_un_cliente():
    vet = Veterinaria("San Roque")
    correr(["2", "Ana", "30111222", "3", "30111222", "Firulais", "perro", "0"], vet)

    assert vet.buscar_animal("Firulais") is not None
    assert vet.clientes()[0].cantidad_de_animales() == 1


def test_aplicar_una_vacuna_desde_el_menu():
    vet = Veterinaria("San Roque")
    correr(
        [
            "2",
            "Ana",
            "30111222",
            "3",
            "30111222",
            "Firulais",
            "perro",
            "4",
            "Firulais",
            "Quíntuple",
            "0",
        ],
        vet,
    )

    assert vet.buscar_animal("Firulais").vacunas_aplicadas() == ["Quíntuple"]


# --- los recorridos se ven en el menú ---
def test_el_menu_muestra_los_animales_al_dia_select():
    salida = correr(["1", "5", "0"])

    assert "al día" in salida.lower()


def test_el_menu_muestra_los_nombres_collect():
    salida = correr(["1", "6", "0"])

    assert "Pelusa" in salida or "Rocky" in salida


def test_el_menu_muestra_el_conteo_por_especie_diccionario():
    salida = correr(["1", "7", "0"])

    assert "perro" in salida.lower() and "gato" in salida.lower()


def test_el_menu_busca_un_animal_por_nombre_detect():
    vet = datos_de_ejemplo()
    nombre = vet.animales()[0].nombre()
    salida = correr(["1", "8", nombre, "0"])

    assert nombre in salida


def test_buscar_un_animal_que_no_existe_avisa_sin_cortar():
    salida = correr(["1", "8", "Inexistente", "0"])

    assert "no encontr" in salida.lower()
    assert salida.count("VetSoft") == 3


def test_el_menu_muestra_la_agenda_ordenada_por_urgencia():
    salida = correr(["1", "9", "0"])

    assert "agenda" in salida.lower()


# --- los errores no cortan el programa ---
def test_un_dni_repetido_muestra_el_error_y_vuelve_al_menu():
    vet = Veterinaria("San Roque")
    salida = correr(["2", "Ana", "30111222", "2", "Otro", "30111222", "0"], vet)

    assert "ya" in salida.lower()
    assert len(vet.clientes()) == 1


def test_un_dni_que_no_es_numero_avisa_y_vuelve_al_menu():
    vet = Veterinaria("San Roque")
    salida = correr(["2", "Ana", "no-es-un-dni", "0"], vet)

    assert "número" in salida.lower() or "numero" in salida.lower()
    assert vet.clientes() == []


def test_una_vacuna_que_no_corresponde_muestra_el_error():
    vet = Veterinaria("San Roque")
    salida = correr(
        [
            "2",
            "Ana",
            "30111222",
            "3",
            "30111222",
            "Michi",
            "gato",
            "4",
            "Michi",
            "Quíntuple",
            "0",
        ],
        vet,
    )

    assert "no corresponde" in salida.lower()
    assert vet.buscar_animal("Michi").vacunas_aplicadas() == []


def test_una_especie_que_no_atendemos_avisa_sin_cortar():
    vet = Veterinaria("San Roque")
    salida = correr(["2", "Ana", "30111222", "3", "30111222", "Nemo", "pez", "0"], vet)

    assert "no atendemos" in salida.lower()
    assert vet.animales() == []


def test_registrar_un_animal_a_un_dni_inexistente_avisa():
    vet = Veterinaria("San Roque")
    salida = correr(["3", "99999999", "Firulais", "perro", "0"], vet)

    assert "no encontr" in salida.lower() or "no existe" in salida.lower()
    assert vet.animales() == []


def test_aplicar_una_vacuna_a_un_animal_inexistente_avisa():
    salida = correr(["4", "Fantasma", "Quíntuple", "0"])

    assert "no encontr" in salida.lower()


# --- la fábrica sigue siendo el único punto de creación ---
def test_el_cliente_registrado_desde_el_menu_es_un_cliente_de_verdad():
    vet = Veterinaria("San Roque")
    correr(["2", "Ana", "30111222", "0"], vet)

    assert isinstance(vet.clientes()[0], Cliente)


def test_los_animales_de_ejemplo_se_crean_con_la_fabrica():
    vet = datos_de_ejemplo()
    uno = vet.animales()[0]

    assert uno.especie() in ("perro", "gato")
    assert uno.esquema_de_vacunacion() != []
