class Cliente:
    """El dueño de uno o más animales.

    Protocolo:
      nombre()                  -> str
      dni()                     -> int
      registrar_animal(animal)  -> None  (error si ya está registrado)
      animales()                -> list[Animal]
      cantidad_de_animales()    -> int
    """

    def __init__(self, nombre, dni):
        if not isinstance(dni, int) or isinstance(dni, bool) or dni <= 0:
            raise ValueError("El DNI tiene que ser un número entero positivo")
        self._nombre = nombre
        self._dni = dni
        self._animales = []

    def nombre(self):
        return self._nombre

    def dni(self):
        return self._dni

    def registrar_animal(self, animal):
        if animal in self._animales:
            raise ValueError(
                f"{animal.nombre()} ya está registrado a nombre de {self._nombre}"
            )
        self._animales.append(animal)

    def animales(self):
        return list(self._animales)  # copia: no exponemos la lista interna

    def cantidad_de_animales(self):
        return len(self._animales)
