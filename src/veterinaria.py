class Veterinaria:
    """La clínica. Conoce a sus clientes.

    Protocolo:
      nombre()                   -> str
      registrar_cliente(cliente) -> None  (error si ya hay un cliente con ese DNI)
      clientes()                 -> list[Cliente]
      animales()                 -> list[Animal]
      animales_al_dia()          -> list[Animal]
      buscar_animal(nombre)      -> Animal | None
    """

    def __init__(self, nombre):
        self._nombre = nombre
        self._clientes = []

    def nombre(self):
        return self._nombre

    def registrar_cliente(self, cliente):
        if any(c.dni() == cliente.dni() for c in self._clientes):
            raise ValueError(f"Ya hay un cliente con DNI {cliente.dni()}")
        self._clientes.append(cliente)

    def clientes(self):
        return list(self._clientes)  # copia: no exponemos la lista interna

    def animales(self):
        """Los animales de todos los clientes.

        No guardamos una lista aparte: se arma cada vez recorriendo los clientes.
        Así un animal registrado despues de dar de alta al cliente aparece igual,
        y no hay dos lugares que puedan quedar desincronizados.
        """
        return [animal for cliente in self._clientes for animal in cliente.animales()]

    def animales_al_dia(self):
        """Los animales que no deben ninguna vacuna.

        Es un **select**: filtra la colección quedándose con los que cumplen la
        condición. El criterio vive en el animal (`esta_al_dia`), no acá: la
        veterinaria pregunta, no decide.
        """
        return [animal for animal in self.animales() if animal.esta_al_dia()]

    def buscar_animal(self, nombre):
        """El primer animal con ese nombre, o None si no hay ninguno.

        Es un **detect**: corta en cuanto encuentra uno y no sigue recorriendo.
        Devolver None en lugar de romper deja que el menú decida qué mostrar:
        no encontrar nada es un resultado posible, no un error.
        """
        return next(
            (animal for animal in self.animales() if animal.nombre() == nombre),
            None,
        )
