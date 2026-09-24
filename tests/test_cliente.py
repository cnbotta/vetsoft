import pytest

from src.cliente import Cliente


# --- caso normal ---
def test_un_cliente_nuevo_arranca_sin_animales():
    ana = Cliente("Ana Díaz", 30111222)
    assert ana.animales() == []


def test_un_cliente_responde_su_nombre_y_dni():
    ana = Cliente("Ana Díaz", 30111222)
    assert ana.nombre() == "Ana Díaz"
    assert ana.dni() == 30111222


# --- caso de error ---
@pytest.mark.parametrize("dni", [0, -30111222, None, "30111222"])
def test_no_se_puede_crear_un_cliente_sin_dni_valido(dni):
    with pytest.raises(ValueError, match="DNI"):
        Cliente("Ana Díaz", dni)
