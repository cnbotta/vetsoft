class Cliente:
    """El dueño de uno o más animales.

    Protocolo:
      nombre()   -> str
      dni()      -> int
      animales() -> list[Animal]
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

    def animales(self):
        return list(self._animales)  # copia: no exponemos la lista interna
