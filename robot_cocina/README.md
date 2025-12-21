# Sistema de Control para Robot de Cocina

## Descripción
Aplicación web para controlar un robot de cocina mediante interfaz moderna desarrollada con NiceGUI y SQLite.

**Asignatura:** Desarrollo Orientado a Objetos  
**Framework:** NiceGUI + SQLite  
**Paradigma:** Programación Orientada a Objetos (POO)

## Características

### Operaciones del Robot
- **Corte:** Picar, trocear
- **Mecánicas:** Amasar
- **Temperatura:** Sofreír, vapor, hervir

### Modos de Operación
- **Manual:** Control directo de operaciones individuales
- **Cocina Guiada:** Ejecución de recetas preprogramadas

### Gestión de Recetas
- Recetas de fábrica (no eliminables)
- Recetas de usuario (gestionables)
- Factory Reset (mantiene recetas de fábrica)

## Estructura del Proyecto

```
robot_cocina/
├── app.py                  # Punto de entrada principal
├── database/
│   ├── db_handler.py      # Gestor de base de datos
│   └── init_db.py         # Inicialización de BD
├── models/
│   ├── robot.py           # Clase base Robot
│   ├── tarea.py           # Jerarquía de tareas
│   └── receta.py          # Modelo de recetas
├── ui/
│   ├── main_interface.py  # Interfaz principal
│   └── components.py      # Componentes reutilizables
├── utils/
│   ├── exceptions.py      # Excepciones personalizadas
│   └── threading_utils.py # Utilidades de concurrencia
└── data/
    └── robot_cocina.db    # Base de datos SQLite
```

## Instalación

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install nicegui

# Inicializar base de datos
python database/init_db.py
```

## Ejecución

```bash
python app.py
```

La aplicación estará disponible en: http://localhost:8080

## Principios POO Implementados

1. **Abstracción:** Clase abstracta `Tarea` define interfaz común
2. **Encapsulamiento:** Estado interno del `Robot` protegido
3. **Herencia:** `TareaCorte`, `TareaTemperatura`, `TareaMecanica` extienden `Tarea`
4. **Polimorfismo:** Método `ejecutar()` implementado de forma específica en cada tipo de tarea

## Características Técnicas

- ✅ Arquitectura modular y escalable
- ✅ Manejo robusto de excepciones
- ✅ Ejecución asíncrona de tareas
- ✅ Persistencia con SQLite
- ✅ Interfaz moderna y responsiva
- ✅ Separación de concerns (MVC)

## Autor
[Tu Nombre]  
Desarrollo Orientado a Objetos - [Año Académico]
