# Modelo

Diagramas del dominio de VetSoft, en Mermaid. GitHub los dibuja al abrir este archivo.

El diagrama modela el negocio completo; el código implementa solo el alcance comprometido.
Que el modelo sea más grande que la implementación no es un error: es la diferencia entre
entender el dominio y entregar un incremento.

## Diagrama de clases

| Clase | ¿Se implementa? | Por qué está |
|---|---|---|
| `Veterinaria` | Sí | Agregado raíz. Donde viven los recorridos de colección. |
| `Cliente` | Sí | Dueño de los animales. Asociación uno a muchos. |
| `Animal` | Sí | Clase base. |
| `Perro` | Sí | Subclase: esquema de vacunación propio. |
| `Gato` | Sí | Subclase: esquema de vacunación propio. |
| `HistoriaClinica` | No | Composición con `Animal`: no tiene sentido sin su animal. |
| `Atencion` | No | Una visita a la clínica. |
| `Tratamiento` | No | Lo indicado en una atención. |
| `Vacuna` | No | Registro de aplicación con fecha. |
| `Turno` | No | Agenda de la clínica. |

Tres decisiones del modelo:

- `Veterinaria o-- Cliente`: **agregación**, porque un cliente existe aunque cierre la veterinaria.
- `Animal *-- HistoriaClinica`: **composición**, porque la historia clínica no existe sin su animal.
- `Animal <|-- Perro`: **herencia**, justificada porque cada especie tiene un esquema de vacunación distinto.

```mermaid
classDiagram
    class Veterinaria {
        -nombre
        +registrarCliente(cliente)
        +animales()
        +animalesAlDia()
        +animalesConVacunasPendientes()
        +nombresDeAnimales()
        +buscarAnimal(nombre)
        +conteoPorEspecie()
        +agendaDeVacunacion()
    }
    class Cliente {
        -nombre
        -dni
        +registrarAnimal(animal)
        +animales()
        +cantidadDeAnimales()
    }
    class Animal {
        -nombre
        -fechaNacimiento
        +edadEnAnios(hoy)
        +especie()
        +esquemaDeVacunacion()
        +aplicarVacuna(vacuna)
        +vacunasPendientes()
        +estaAlDia()
    }
    class Perro {
        +especie()
        +esquemaDeVacunacion()
    }
    class Gato {
        +especie()
        +esquemaDeVacunacion()
    }
    class HistoriaClinica {
        +agregarAtencion(atencion)
        +atenciones()
    }
    class Atencion {
        -fecha
        -diagnostico
        +registrarTratamiento(t)
    }
    class Tratamiento {
        -enfermedad
        -medicamento
        -dosis
        -duracionDias
    }
    class Vacuna {
        -nombre
        -fechaAplicacion
    }
    class Turno {
        -fecha
        -motivo
        -estado
        +confirmar()
        +cancelar()
    }
    Veterinaria "1" o-- "*" Cliente : clientes
    Cliente "1" o-- "*" Animal : animales
    Animal <|-- Perro
    Animal <|-- Gato
    Animal "1" *-- "1" HistoriaClinica : historia
    HistoriaClinica "1" o-- "*" Atencion : atenciones
    Atencion "1" o-- "*" Tratamiento : tratamientos
    Animal "1" o-- "*" Vacuna : aplicadas
    Veterinaria "1" o-- "*" Turno : agenda
    Turno "*" --> "1" Animal : paciente
```

## Diagrama de secuencia: vacunar a un animal

Incluye **autodelegación** (`esquemaDeVacunacion()` sale y vuelve al mismo objeto) y una
**condición** con `alt`.

```mermaid
sequenceDiagram
    actor R as Recepcion
    participant V as vet:Veterinaria
    participant C as ana:Cliente
    participant A as firulais:Perro
    R->>V: buscarAnimal("Firulais")
    V->>C: animales()
    C-->>V: [firulais, michi]
    V-->>R: firulais
    R->>A: vacunasPendientes()
    A->>A: esquemaDeVacunacion()
    A-->>R: ["Antirrabica"]
    R->>A: aplicarVacuna("Antirrabica")
    alt la vacuna no corresponde a la especie
        A-->>R: error
    else corresponde y no la tenia
        A->>A: registra la vacuna
        A-->>R: ok
    end
```
