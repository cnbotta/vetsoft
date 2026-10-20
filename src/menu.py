"""Menú de consola de VetSoft.

La clase recibe de afuera cómo leer y cómo escribir (`leer` y `escribir`). En la vida
real son `input` y `print`; en las pruebas son funciones de mentira que devuelven
respuestas preparadas y guardan lo que se mostró. Así el menú se puede probar entero
sin que nadie teclee nada.

Cada opción está en su propio método y el bucle principal solo despacha. Agregar una
opción nueva es sumar una entrada al diccionario `_opciones()`, sin tocar el bucle.
"""

from datetime import date

from src.animal import crear_animal
from src.cliente import Cliente
from src.veterinaria import Veterinaria

# El alta por consola no pregunta la fecha de nacimiento: hoy ninguna regla del
# negocio depende de ella (el esquema de vacunación sale de la especie). Queda una
# fecha fija y explícita en vez de `date.today()`, que daría a entender que el
# animal nació el día que se lo registró.
FECHA_SIN_DATO = date(1900, 1, 1)


class Menu:
    """El menú de la aplicación.

    Protocolo:
      correr()  -> None  (muestra el menú hasta que eligen salir)
    """

    def __init__(self, veterinaria, leer=None, escribir=None):
        self._vet = veterinaria
        # Se resuelven al usarse, no acá: si se guardara `input` en el constructor,
        # un reemplazo posterior (como el de las pruebas) ya no tendría efecto.
        self._leer = leer if leer is not None else (lambda mensaje="": input(mensaje))
        self._escribir = (
            escribir if escribir is not None else (lambda texto="": print(texto))
        )

    # ---------------------------------------------------------------- bucle

    def correr(self):
        """Muestra el menú y atiende opciones hasta que eligen salir."""
        while True:
            self._mostrar_menu()
            elegida = self._leer("Opción: ").strip()

            if elegida == "0":
                self._escribir("Hasta luego.")
                return

            accion = self._opciones().get(elegida)
            if accion is None:
                self._escribir(f"La opción {elegida} no existe.")
                continue

            # Los errores del dominio (DNI repetido, vacuna que no corresponde,
            # especie que no atendemos) se avisan y el menú sigue vivo.
            try:
                accion()
            except ValueError as error:
                self._escribir(f"No se pudo: {error}")

    def _opciones(self):
        return {
            "1": self._cargar_datos_de_ejemplo,
            "2": self._registrar_cliente,
            "3": self._registrar_animal,
            "4": self._aplicar_vacuna,
            "5": self._listar_animales_al_dia,
            "6": self._listar_nombres,
            "7": self._contar_por_especie,
            "8": self._buscar_animal,
            "9": self._mostrar_agenda,
        }

    def _mostrar_menu(self):
        self._escribir()
        self._escribir(f"=== VetSoft · {self._vet.nombre()} ===")
        self._escribir("1 · Cargar datos de ejemplo")
        self._escribir("2 · Registrar un cliente")
        self._escribir("3 · Registrar un animal")
        self._escribir("4 · Aplicar una vacuna")
        self._escribir("5 · Animales al día")
        self._escribir("6 · Nombres de todos los animales")
        self._escribir("7 · Cuántos animales hay por especie")
        self._escribir("8 · Buscar un animal por nombre")
        self._escribir("9 · Agenda de llamados")
        self._escribir("0 · Salir")

    # ---------------------------------------------------------------- altas

    def _cargar_datos_de_ejemplo(self):
        cargados = datos_de_ejemplo()
        for cliente in cargados.clientes():
            self._vet.registrar_cliente(cliente)
        self._escribir(
            f"Cargados {len(cargados.clientes())} clientes "
            f"y {len(cargados.animales())} animales de ejemplo."
        )

    def _registrar_cliente(self):
        nombre = self._leer("Nombre del cliente: ").strip()
        dni = self._pedir_dni()
        if dni is None:
            return
        self._vet.registrar_cliente(Cliente(nombre, dni))
        self._escribir(f"{nombre} quedó registrado.")

    def _registrar_animal(self):
        dni = self._pedir_dni()
        if dni is None:
            return

        dueño = self._buscar_cliente(dni)
        if dueño is None:
            self._escribir(f"No encontré ningún cliente con el DNI {dni}.")
            return

        nombre = self._leer("Nombre del animal: ").strip()
        especie = self._leer("Especie (perro o gato): ").strip().lower()
        animal = crear_animal(nombre, especie, FECHA_SIN_DATO)
        dueño.registrar_animal(animal)
        self._escribir(f"{nombre} quedó registrado a nombre de {dueño.nombre()}.")

    def _aplicar_vacuna(self):
        nombre = self._leer("Nombre del animal: ").strip()
        animal = self._vet.buscar_animal(nombre)
        if animal is None:
            self._escribir(f"No encontré ningún animal llamado {nombre}.")
            return

        self._escribir(
            f"Le faltan: {', '.join(animal.vacunas_pendientes()) or 'ninguna'}"
        )
        vacuna = self._leer("Vacuna a aplicar: ").strip()
        animal.aplicar_vacuna(vacuna)
        self._escribir(f"Se registró la {vacuna} de {nombre}.")

    # ------------------------------------------------------------ consultas

    def _listar_animales_al_dia(self):
        al_dia = self._vet.animales_al_dia()
        self._escribir(f"Animales al día ({len(al_dia)}):")
        self._listar(animal.nombre() for animal in al_dia)

    def _listar_nombres(self):
        nombres = self._vet.nombres_de_los_animales()
        self._escribir(f"Nombres de los animales ({len(nombres)}):")
        self._listar(nombres)

    def _contar_por_especie(self):
        self._escribir("Animales por especie:")
        conteo = self._vet.animales_por_especie()
        if not conteo:
            self._escribir("  (todavía no hay animales)")
            return
        for especie, cuantos in sorted(conteo.items()):
            self._escribir(f"  {especie}: {cuantos}")

    def _buscar_animal(self):
        nombre = self._leer("Nombre a buscar: ").strip()
        animal = self._vet.buscar_animal(nombre)
        if animal is None:
            self._escribir(f"No encontré ningún animal llamado {nombre}.")
            return
        pendientes = ", ".join(animal.vacunas_pendientes()) or "ninguna"
        self._escribir(
            f"{animal.nombre()} · {animal.especie()} · le faltan: {pendientes}"
        )

    def _mostrar_agenda(self):
        agenda = self._vet.agenda_de_llamados()
        self._escribir(f"Agenda de llamados, los más urgentes primero ({len(agenda)}):")
        if not agenda:
            self._escribir("  (no hay llamados pendientes)")
            return
        for animal in agenda:
            faltan = ", ".join(animal.vacunas_pendientes())
            self._escribir(
                f"  {animal.nombre()} ({animal.especie()}) · le faltan: {faltan}"
            )

    # ---------------------------------------------------------- auxiliares

    def _pedir_dni(self):
        """Convierte el DNI tecleado a entero. Devuelve None si no es un número."""
        tecleado = self._leer("DNI: ").strip()
        try:
            return int(tecleado)
        except ValueError:
            self._escribir(f"El DNI tiene que ser un número y '{tecleado}' no lo es.")
            return None

    def _buscar_cliente(self, dni):
        """El cliente con ese DNI, o None. Es un detect sobre los clientes."""
        for cliente in self._vet.clientes():
            if cliente.dni() == dni:
                return cliente
        return None

    def _listar(self, textos):
        textos = list(textos)
        if not textos:
            self._escribir("  (ninguno)")
            return
        for texto in textos:
            self._escribir(f"  {texto}")


def datos_de_ejemplo():
    """Una veterinaria con clientes y animales ya cargados, para probar el menú.

    Deja a propósito animales al día y animales con vacunas pendientes, así las
    opciones de consulta tienen algo que mostrar desde el arranque.
    """
    vet = Veterinaria("San Roque")

    ana = Cliente("Ana Gómez", 30111222)
    pelusa = crear_animal("Pelusa", "gato", date(2021, 5, 10))
    pelusa.aplicar_vacuna("Triple felina")
    pelusa.aplicar_vacuna("Antirrábica")  # queda al día
    rocky = crear_animal("Rocky", "perro", date(2019, 3, 2))
    rocky.aplicar_vacuna("Quíntuple")  # le falta la antirrábica
    ana.registrar_animal(pelusa)
    ana.registrar_animal(rocky)

    luis = Cliente("Luis Paredes", 27888444)
    nina = crear_animal("Nina", "perro", date(2022, 8, 21))  # le faltan las dos
    michi = crear_animal("Michi", "gato", date(2020, 1, 15))
    michi.aplicar_vacuna("Antirrábica")  # le falta la triple felina
    luis.registrar_animal(nina)
    luis.registrar_animal(michi)

    vet.registrar_cliente(ana)
    vet.registrar_cliente(luis)
    return vet
