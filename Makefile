# Atajos para no tener que recordar los comandos de Docker.
#
# Se usa `make <tarea>`, por ejemplo `make construir`. Sin argumentos muestra
# la lista de tareas disponibles.
#
# Cada tarea es uno de los comandos de la guía de Docker del campus: acá solo
# quedan los que se usan todos los días.

IMAGEN = vetsoft

# Le avisa a make que estos nombres son tareas y no archivos que tenga que crear.
.PHONY: ayuda construir correr imagenes contenedores limpiar

ayuda:
	@echo "Tareas disponibles:"
	@echo "  make construir     Construye la imagen $(IMAGEN)"
	@echo "  make correr        Abre el menú dentro del contenedor"
	@echo "  make imagenes      Lista las imágenes que hay en la máquina"
	@echo "  make contenedores  Lista los contenedores, incluso los apagados"
	@echo "  make limpiar       Borra lo que Docker dejó sin usar"

construir:
	docker build -t $(IMAGEN) .

# -it conecta la terminal, que el menú necesita para leer del teclado.
# --rm borra el contenedor al salir, así no quedan restos.
correr:
	docker run --rm -it $(IMAGEN)

imagenes:
	docker images

# -a incluye los que ya terminaron, no solo los que están corriendo.
contenedores:
	docker ps -a

limpiar:
	docker system prune
