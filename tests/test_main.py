from src.__main__ import main


def test_el_programa_arranca_el_menu_y_se_puede_salir(capsys, monkeypatch):
    # el usuario elige salir apenas ve el menú
    monkeypatch.setattr("builtins.input", lambda _mensaje="": "0")

    main()

    salida = capsys.readouterr().out
    assert "VetSoft" in salida
    assert "Salir" in salida
