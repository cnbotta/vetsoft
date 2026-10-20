"""Punto de entrada de VetSoft: abre el menú de consola."""

from src.menu import Menu
from src.veterinaria import Veterinaria


def main() -> None:
    Menu(Veterinaria("San Roque")).correr()


if __name__ == "__main__":
    main()
