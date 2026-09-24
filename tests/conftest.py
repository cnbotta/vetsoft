from datetime import date

import pytest

from src.animal import crear_animal

# Los tests nunca llaman al constructor directo: pasan por la fábrica.
# Así, si mañana cambia cómo se construye un animal, los asserts no cambian.


@pytest.fixture
def firulais():
    return crear_animal("Firulais", "perro", date(2020, 5, 10))


@pytest.fixture
def michi():
    return crear_animal("Michi", "gato", date(2022, 1, 3))
