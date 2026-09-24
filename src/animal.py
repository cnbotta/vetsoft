ESPECIES_ATENDIDAS = ("perro", "gato")


class Animal:
    """Un animal atendido en la veterinaria.

    Protocolo:
      nombre()                 -> str
      especie()                -> str
      esquema_de_vacunacion()  -> list[str]
      vacunas_pendientes()     -> list[str]
    """

    def __init__(self, nombre, especie, fecha_nacimiento):
        if especie not in ESPECIES_ATENDIDAS:
            raise ValueError(f"No atendemos {especie}")
        self._nombre = nombre
        self._especie = especie
        self._fecha_nacimiento = fecha_nacimiento
        self._vacunas_aplicadas = []

    def nombre(self):
        return self._nombre

    def especie(self):
        return self._especie

    def esquema_de_vacunacion(self):
        if self._especie == "perro":
            return ["Quíntuple", "Antirrábica"]
        elif self._especie == "gato":
            return ["Triple felina", "Antirrábica"]
        return []

    def vacunas_pendientes(self):
        aplicadas = self._vacunas_aplicadas
        return [v for v in self.esquema_de_vacunacion() if v not in aplicadas]


def crear_animal(nombre, especie, fecha_nacimiento):
    """Fábrica de animales: el único punto por donde se crean."""
    return Animal(nombre, especie, fecha_nacimiento)
