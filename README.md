# VetSoft — Veterinaria Patitas

Control de vacunación de los pacientes de una veterinaria.
Proyecto demostración de Metodologías de Programación II (UNAJ, 2026).

## Cómo levantarlo

```bash
uv sync               # instala las dependencias en un entorno aislado
uv run pytest         # corre las pruebas
uv run python -m src  # ejecuta el programa
```

El modelo del dominio está en [`docs/modelo.md`](docs/modelo.md).

## Cómo levantarlo con Docker

Sin tener Python ni `uv` instalados:

```bash
docker build -t vetsoft .      # construye la imagen
docker run --rm -it vetsoft    # abre el menú
```

El `-it` es necesario porque el menú lee del teclado. El `--rm` borra el contenedor
al salir. Si cambiás el código, hay que volver a hacer `docker build`: la imagen es
una foto del momento en que se construyó.
