from datetime import UTC, date, datetime

from src.animal import ESPECIES_ATENDIDAS, crear_animal
from src.cliente import Cliente
from src.veterinaria import Veterinaria


def cargar_datos_ejemplo(vet: Veterinaria) -> None:
    """Carga clientes y animales iniciales para probar el sistema."""
    ana = Cliente("Ana Díaz", 30111222)
    carlos = Cliente("Carlos Gómez", 28333444)

    firulais = crear_animal("Firulais", "perro", date(2020, 5, 10))
    michi = crear_animal("Michi", "gato", date(2022, 1, 3))
    luna = crear_animal("Luna", "perro", date(2021, 8, 15))

    # Firulais tiene una vacuna aplicada, Michi ninguna, Luna al día
    firulais.aplicar_vacuna("Quíntuple")
    luna.aplicar_vacuna("Quíntuple")
    luna.aplicar_vacuna("Antirrábica")

    ana.registrar_animal(firulais)
    ana.registrar_animal(michi)
    carlos.registrar_animal(luna)

    vet.registrar_cliente(ana)
    vet.registrar_cliente(carlos)


def menu_interactivo(vet: Veterinaria) -> None:
    while True:
        print("\n" + "=" * 45)
        print(f"       {vet.nombre()} — Menú Principal")
        print("=" * 45)
        print("1. Listar animales y estado de vacunación")
        print("2. Registrar nuevo cliente")
        print("3. Registrar nuevo animal a un cliente")
        print("4. Aplicar vacuna a un animal")
        print("5. Ver agenda de llamados (por urgencia)")
        print("6. Ver estadísticas por especie")
        print("7. Cargar datos de ejemplo")
        print("0. Salir")
        print("-" * 45)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            animales = vet.animales()
            if not animales:
                print("No hay animales registrados aún.")
                continue

            print("\n--- Animales Registrados ---")
            for a in animales:
                estado = "AL DÍA" if a.esta_al_dia() else "PENDIENTE"
                pendientes = a.vacunas_pendientes()
                pendientes_str = ", ".join(pendientes) if pendientes else "Ninguna"
                print(
                    f"• {a.nombre()} ({a.especie()}): [{estado}] "
                    f"- Pendientes: {pendientes_str}"
                )

        elif opcion == "2":
            nombre = input("Nombre del cliente: ").strip()
            dni_raw = input("DNI (número entero): ").strip()
            try:
                dni = int(dni_raw)
                cliente = Cliente(nombre, dni)
                vet.registrar_cliente(cliente)
                print(f"Cliente '{nombre}' (DNI: {dni}) registrado con éxito.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "3":
            if not vet.clientes():
                print("Primero debe registrar al menos un cliente.")
                continue

            dni_raw = input("DNI del dueño: ").strip()
            try:
                dni = int(dni_raw)
            except ValueError:
                print("El DNI debe ser numérico.")
                continue

            cliente = next((c for c in vet.clientes() if c.dni() == dni), None)
            if not cliente:
                print(f"No se encontró ningún cliente con DNI {dni}.")
                continue

            nombre = input("Nombre del animal: ").strip()
            especies_disponibles = ", ".join(ESPECIES_ATENDIDAS)
            especie = (
                input(f"Especie ({especies_disponibles}): ").strip().lower()
            )

            try:
                nuevo_animal = crear_animal(
                    nombre, especie, datetime.now(UTC).date()
                )
                cliente.registrar_animal(nuevo_animal)
                print(
                    f"Animal '{nombre}' registrado a nombre de {cliente.nombre()}."
                )
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "4":
            nombre = input("Nombre del animal a vacunar: ").strip()
            animal = vet.buscar_animal(nombre)
            if not animal:
                print(f"No se encontró ningún animal llamado '{nombre}'.")
                continue

            print(f"Esquema de {animal.nombre()}: {animal.esquema_de_vacunacion()}")
            print(f"Vacunas pendientes: {animal.vacunas_pendientes()}")
            if animal.esta_al_dia():
                print(f"{animal.nombre()} ya tiene todas sus vacunas al día.")
                continue

            vacuna = input("Nombre de la vacuna a aplicar: ").strip()
            try:
                animal.aplicar_vacuna(vacuna)
                print(f"Vacuna '{vacuna}' aplicada exitosamente a {animal.nombre()}.")
            except ValueError as e:
                print(f"Error al aplicar vacuna: {e}")

        elif opcion == "5":
            agenda = vet.agenda_de_llamados()
            if not agenda:
                print("Todos los animales están al día. No hay llamados pendientes.")
            else:
                print("\n--- Agenda de Llamados (Ordenada por Urgencia) ---")
                for pos, a in enumerate(agenda, start=1):
                    debe = len(a.vacunas_pendientes())
                    print(
                        f"{pos}. {a.nombre()} ({a.especie()}) "
                        f"- Debe {debe} vacuna(s): {', '.join(a.vacunas_pendientes())}"
                    )

        elif opcion == "6":
            conteo = vet.animales_por_especie()
            if not conteo:
                print("No hay animales para contabilizar.")
            else:
                print("\n--- Conteo de Animales por Especie ---")
                for esp, cant in conteo.items():
                    print(f"• {esp.capitalize()}: {cant}")

        elif opcion == "7":
            try:
                cargar_datos_ejemplo(vet)
                print("Datos de ejemplo cargados correctamente.")
            except ValueError as e:
                print(f"Aviso: {e}")

        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Ingrese un número del 0 al 7.")


def main(interactivo: bool = False) -> None:
    print("VetSoft — Veterinaria Patitas")
    if interactivo:
        vet = Veterinaria("Veterinaria Patitas")
        menu_interactivo(vet)


if __name__ == "__main__":
    main(interactivo=True)
