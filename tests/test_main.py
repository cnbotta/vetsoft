from src.__main__ import main


def test_el_programa_arranca_y_saluda(capsys):
    main()

    salida = capsys.readouterr()
    assert "VetSoft" in salida.out
