class Veterinaria:
    """La clínica. Conoce a sus clientes.

    Protocolo:
      nombre()                   -> str
      registrar_cliente(cliente) -> None  (error si ya hay un cliente con ese DNI)
      clientes()                 -> list[Cliente]
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
