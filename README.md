# 🍳 Robot de Cocina - Simulador v13.0

Simulador completo de un robot de cocina inteligente con interfaz web moderna desarrollado en Python.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![NiceGUI](https://img.shields.io/badge/NiceGUI-1.4+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Índice

- [Descripción](#-descripción)
- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Arquitectura](#-arquitectura)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Base de Datos](#-base-de-datos)
- [Tecnologías](#-tecnologías)

---

## 📖 Descripción

Este proyecto simula el funcionamiento completo de un robot de cocina tipo Thermomix o similar. Permite gestionar recetas, ejecutar procesos de cocción simulados, y llevar un registro completo de la actividad culinaria.

El simulador reproduce fielmente las operaciones de un robot real:
- **Operaciones de corte**: picar, trocear, rallar, triturar, laminar, dados, rodajas
- **Operaciones de temperatura**: sofreír, hervir, vapor, calentar, freír, hornear, gratinar, escaldar, confitar, flamear
- **Operaciones mecánicas**: amasar, mezclar, batir, remover, emulsionar, montar, incorporar, tamizar

---

## ✨ Características

### Gestión de Recetas
- 📚 **24 recetas de fábrica** incluidas (sopas, arroces, carnes, pescados, postres...)
- ➕ **Crear recetas personalizadas** con ingredientes y pasos detallados
- ✏️ **Editar y duplicar** recetas existentes
- ⭐ **Sistema de favoritos** para acceso rápido
- 🔍 **Búsqueda y filtros** por categoría, dificultad y tiempo

### Ejecución de Recetas
- ▶️ **Simulación en tiempo real** de cada paso de cocción
- ⏸️ **Pausar y reanudar** en cualquier momento
- 🛑 **Parada de emergencia** con confirmación
- 📊 **Progreso visual** con barras y porcentajes
- ⚡ **Velocidad ajustable** (lento, normal, rápido, ultra)

### Información Nutricional
- 🥗 **Cálculo automático** de calorías, proteínas, carbohidratos y grasas
- 📏 **Gramos por porción** calculados automáticamente
- 🔄 **Escalado por porciones** que recalcula ingredientes y nutrición

### Sistema de Alérgenos
- ⚠️ **Detección automática** de 10 tipos de alérgenos:
  - 🌾 Gluten | 🥛 Lácteos | 🥚 Huevo | 🥜 Frutos secos | 🐟 Pescado
  - 🦐 Marisco | 🫘 Soja | 🥬 Apio | 🟡 Mostaza | ⚪ Sésamo
- ✅ **Selector de alérgenos** al crear recetas personalizadas

### Historial y Estadísticas
- 📜 **Historial completo** de ejecuciones
- 📈 **Estadísticas** de uso (recetas cocinadas, tasa de éxito, tiempo total)
- 📝 **Notas por receta** para guardar observaciones

### Interfaz
- 🌓 **Modo claro/oscuro** con transición suave
- 📱 **Diseño responsive** adaptable a diferentes pantallas
- 🎨 **Interfaz moderna** y profesional

---

## 📦 Requisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Dependencias
```
nicegui>=1.4.0
```

---

## 🚀 Instalación

### 1. Clonar o descargar el proyecto
```bash
unzip robot_cocina_v13.zip
cd robot_cocina
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install nicegui
```

### 4. Ejecutar la aplicación
```bash
python app.py
```

### 5. Abrir en el navegador
La aplicación se abrirá automáticamente en `http://localhost:8080`

---

## 🎮 Uso

### Flujo básico de uso

1. **Encender el robot** - Click en "Encender"
2. **Seleccionar receta** - Navegar por las recetas y hacer click en una
3. **Ajustar porciones** - Modificar el número de porciones si es necesario
4. **Preparar receta** - Click en "Preparar" en el diálogo de la receta
5. **Iniciar cocción** - Click en "Iniciar Receta"
6. **Monitorizar** - Observar el progreso de cada paso
7. **Finalizar** - Al completar, añadir notas opcionales

### Controles durante la ejecución

| Botón | Función |
|-------|---------|
| Pausar | Detiene temporalmente la ejecución |
| Reanudar | Continúa desde donde se pausó |
| Cancelar | Aborta la receta actual |
| Parada Emergencia | Detiene inmediatamente (con confirmación) |

### Crear una receta personalizada

1. Ir a la pestaña "Nueva Receta"
2. Rellenar información básica (nombre, descripción, porciones, dificultad)
3. Marcar los alérgenos presentes
4. Añadir ingredientes con cantidad y unidad
5. Definir los pasos de cocción (tipo, operación, duración, temperatura, velocidad)
6. Guardar la receta

---

## 🏗️ Arquitectura

El proyecto sigue el patrón **MVC (Modelo-Vista-Controlador)**:
```
┌─────────────────────────────────────────────────────────┐
│                      VISTA (UI)                         │
│                  main_interface.py                      │
│         NiceGUI - Interfaz web responsive               │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                   CONTROLADOR                           │
│                  controller.py                          │
│        Lógica de negocio y coordinación                 │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                     MODELO                              │
│     robot.py │ receta.py │ tarea.py │ simulator.py     │
│         Entidades y lógica de dominio                   │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  BASE DE DATOS                          │
│                  db_handler.py                          │
│              SQLite - Persistencia                      │
└─────────────────────────────────────────────────────────┘
```

### Patrón de Estados

El robot implementa una máquina de estados:
```
APAGADO ──► IDLE ──► PREPARADO ──► EJECUTANDO ──► FINALIZADO
              ▲          │              │              │
              │          │              ▼              │
              │          │          PAUSADO            │
              │          │              │              │
              └──────────┴──────────────┴──────────────┘
```

---

## 📁 Estructura del Proyecto
```
robot_cocina/
│
├── app.py                    # Punto de entrada principal
├── README.md                 # Este archivo
│
├── models/                   # Capa de modelo
│   ├── __init__.py
│   ├── robot.py             # Clase Robot (máquina de estados)
│   ├── receta.py            # Clases Receta e Ingrediente
│   ├── tarea.py             # Clases de tareas (corte, temp, mecánica)
│   └── controller.py        # Controlador del robot
│
├── database/                 # Capa de persistencia
│   ├── __init__.py
│   ├── db_handler.py        # Manejador de base de datos
│   └── init_db.py           # Inicialización y recetas de fábrica
│
├── ui/                       # Capa de presentación
│   ├── __init__.py
│   └── main_interface.py    # Interfaz principal (NiceGUI)
│
├── utils/                    # Utilidades
│   ├── __init__.py
│   ├── exceptions.py        # Excepciones personalizadas
│   └── simulator.py         # Simulador de tiempo
│
└── data/                     # Datos persistentes
    └── robot_cocina.db      # Base de datos SQLite (generada)
```

---

## 🗄️ Base de Datos

### Esquema de tablas

#### `recetas`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria |
| nombre | TEXT | Nombre de la receta |
| descripcion | TEXT | Descripción breve |
| ingredientes | TEXT | JSON con lista de ingredientes |
| pasos | TEXT | JSON con pasos de cocción |
| tiempo_total | INTEGER | Tiempo en segundos |
| porciones | INTEGER | Número de porciones |
| dificultad | TEXT | Fácil, Media, Difícil |
| es_fabrica | INTEGER | 1 si es receta de fábrica |

#### `favoritos`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria |
| receta_id | INTEGER | FK a recetas |
| fecha | TIMESTAMP | Fecha de agregado |

#### `historial_ejecuciones`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria |
| receta_id | INTEGER | FK a recetas |
| fecha_inicio | TIMESTAMP | Inicio de ejecución |
| fecha_fin | TIMESTAMP | Fin de ejecución |
| completada | INTEGER | 1 si se completó |
| duracion_real | INTEGER | Duración en segundos |
| porciones | INTEGER | Porciones preparadas |

#### `notas_recetas`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria |
| receta_id | INTEGER | FK a recetas |
| nota | TEXT | Contenido de la nota |
| fecha | TIMESTAMP | Fecha de creación |

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|------------|-----|
| **Python 3.10+** | Lenguaje principal |
| **NiceGUI** | Framework de interfaz web |
| **SQLite** | Base de datos embebida |
| **AsyncIO** | Programación asíncrona |
| **CSS Variables** | Temas claro/oscuro |

