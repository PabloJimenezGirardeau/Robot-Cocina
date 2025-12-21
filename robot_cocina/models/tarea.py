"""
Jerarquía de clases para tareas del robot.
Implementa herencia y polimorfismo para diferentes tipos de operaciones.
"""

from abc import ABC, abstractmethod
from typing import Dict
from enum import Enum


class TipoOperacion(Enum):
    """Tipos de operaciones que puede realizar el robot."""
    PICAR = "picar"
    TROCEAR = "trocear"
    AMASAR = "amasar"
    SOFREIR = "sofreir"
    VAPOR = "vapor"
    HERVIR = "hervir"


class Tarea(ABC):
    """Clase abstracta base para todas las tareas."""
    
    def __init__(self, nombre: str, duracion: int, descripcion: str = ""):
        """
        Inicializa una tarea genérica.
        
        Args:
            nombre: Nombre de la tarea
            duracion: Duración en segundos
            descripcion: Descripción opcional
        """
        self.nombre = nombre
        self.duracion = duracion
        self.descripcion = descripcion
        self._progreso = 0
    
    @abstractmethod
    def ejecutar(self) -> Dict:
        """Ejecuta la tarea y retorna información del proceso."""
        pass
    
    @abstractmethod
    def validar(self) -> tuple[bool, str]:
        """
        Valida si la tarea puede ejecutarse.
        
        Returns:
            (es_valida, mensaje_error)
        """
        pass
    
    @abstractmethod
    def get_parametros(self) -> Dict:
        """Obtiene los parámetros específicos de la tarea."""
        pass
    
    def actualizar_progreso(self, progreso: int):
        """Actualiza el progreso de la tarea."""
        self._progreso = min(100, max(0, progreso))
    
    @property
    def progreso(self) -> int:
        """Obtiene el progreso actual (0-100)."""
        return self._progreso


class TareaCorte(Tarea):
    """Tareas relacionadas con corte (picar, trocear)."""
    
    def __init__(
        self, 
        tipo: TipoOperacion,
        duracion: int, 
        velocidad: int,
        descripcion: str = ""
    ):
        """
        Inicializa una tarea de corte.
        
        Args:
            tipo: PICAR o TROCEAR
            duracion: Duración en segundos
            velocidad: Velocidad de las cuchillas (1-10)
            descripcion: Descripción opcional
        """
        super().__init__(tipo.value.capitalize(), duracion, descripcion)
        self.tipo = tipo
        self.velocidad = velocidad
    
    def ejecutar(self) -> Dict:
        """Ejecuta la operación de corte."""
        return {
            "tipo": "corte",
            "operacion": self.tipo.value,
            "velocidad": self.velocidad,
            "duracion": self.duracion,
            "temperatura": 0
        }
    
    def validar(self) -> tuple[bool, str]:
        """Valida los parámetros de corte."""
        if self.velocidad < 1 or self.velocidad > 10:
            return False, "La velocidad debe estar entre 1 y 10"
        if self.duracion < 1:
            return False, "La duración debe ser al menos 1 segundo"
        return True, ""
    
    def get_parametros(self) -> Dict:
        """Obtiene parámetros de la tarea de corte."""
        return {
            "velocidad": f"{self.velocidad}/10",
            "duracion": f"{self.duracion}s",
            "tipo": self.tipo.value
        }


class TareaTemperatura(Tarea):
    """Tareas con temperatura (sofreír, hervir, vapor)."""
    
    def __init__(
        self, 
        tipo: TipoOperacion,
        duracion: int, 
        temperatura: int,
        velocidad: int = 1,
        descripcion: str = ""
    ):
        """
        Inicializa una tarea con temperatura.
        
        Args:
            tipo: SOFREIR, HERVIR o VAPOR
            duracion: Duración en segundos
            temperatura: Temperatura en grados Celsius
            velocidad: Velocidad de mezclado (1-10)
            descripcion: Descripción opcional
        """
        super().__init__(tipo.value.capitalize(), duracion, descripcion)
        self.tipo = tipo
        self.temperatura = temperatura
        self.velocidad = velocidad
    
    def ejecutar(self) -> Dict:
        """Ejecuta la operación con temperatura."""
        return {
            "tipo": "temperatura",
            "operacion": self.tipo.value,
            "temperatura": self.temperatura,
            "velocidad": self.velocidad,
            "duracion": self.duracion
        }
    
    def validar(self) -> tuple[bool, str]:
        """Valida los parámetros de temperatura."""
        if self.temperatura < 0 or self.temperatura > 200:
            return False, "La temperatura debe estar entre 0 y 200°C"
        if self.velocidad < 1 or self.velocidad > 10:
            return False, "La velocidad debe estar entre 1 y 10"
        if self.duracion < 1:
            return False, "La duración debe ser al menos 1 segundo"
        
        # Validaciones específicas por tipo
        if self.tipo == TipoOperacion.VAPOR and self.temperatura != 100:
            return False, "El vapor requiere 100°C"
        if self.tipo == TipoOperacion.HERVIR and self.temperatura < 90:
            return False, "Hervir requiere al menos 90°C"
        
        return True, ""
    
    def get_parametros(self) -> Dict:
        """Obtiene parámetros de la tarea con temperatura."""
        return {
            "temperatura": f"{self.temperatura}°C",
            "velocidad": f"{self.velocidad}/10",
            "duracion": f"{self.duracion}s",
            "tipo": self.tipo.value
        }


class TareaMecanica(Tarea):
    """Tareas mecánicas (amasar)."""
    
    def __init__(
        self, 
        nombre: str,
        duracion: int, 
        velocidad: int,
        descripcion: str = ""
    ):
        """
        Inicializa una tarea mecánica.
        
        Args:
            nombre: Nombre de la operación
            duracion: Duración en segundos
            velocidad: Velocidad del motor (1-10)
            descripcion: Descripción opcional
        """
        super().__init__(nombre, duracion, descripcion)
        self.velocidad = velocidad
    
    def ejecutar(self) -> Dict:
        """Ejecuta la operación mecánica."""
        return {
            "tipo": "mecanica",
            "operacion": "amasar",
            "velocidad": self.velocidad,
            "duracion": self.duracion,
            "temperatura": 0
        }
    
    def validar(self) -> tuple[bool, str]:
        """Valida los parámetros mecánicos."""
        if self.velocidad < 1 or self.velocidad > 10:
            return False, "La velocidad debe estar entre 1 y 10"
        if self.duracion < 1:
            return False, "La duración debe ser al menos 1 segundo"
        return True, ""
    
    def get_parametros(self) -> Dict:
        """Obtiene parámetros de la tarea mecánica."""
        return {
            "velocidad": f"{self.velocidad}/10",
            "duracion": f"{self.duracion}s",
            "tipo": "amasar"
        }


# Funciones helper para crear tareas rápidamente
def crear_picar(duracion: int = 10, velocidad: int = 7) -> TareaCorte:
    """Crea una tarea de picar."""
    return TareaCorte(
        TipoOperacion.PICAR,
        duracion,
        velocidad,
        "Picar ingredientes finamente"
    )


def crear_trocear(duracion: int = 8, velocidad: int = 5) -> TareaCorte:
    """Crea una tarea de trocear."""
    return TareaCorte(
        TipoOperacion.TROCEAR,
        duracion,
        velocidad,
        "Trocear en cubos medianos"
    )


def crear_amasar(duracion: int = 300, velocidad: int = 4) -> TareaMecanica:
    """Crea una tarea de amasar."""
    return TareaMecanica(
        "Amasar",
        duracion,
        velocidad,
        "Amasar hasta obtener textura homogénea"
    )


def crear_sofreir(duracion: int = 180, temperatura: int = 120) -> TareaTemperatura:
    """Crea una tarea de sofreír."""
    return TareaTemperatura(
        TipoOperacion.SOFREIR,
        duracion,
        temperatura,
        3,
        "Sofreír hasta dorar"
    )


def crear_hervir(duracion: int = 600, temperatura: int = 100) -> TareaTemperatura:
    """Crea una tarea de hervir."""
    return TareaTemperatura(
        TipoOperacion.HERVIR,
        duracion,
        temperatura,
        1,
        "Hervir hasta cocción completa"
    )


def crear_vapor(duracion: int = 900, velocidad: int = 1) -> TareaTemperatura:
    """Crea una tarea al vapor."""
    return TareaTemperatura(
        TipoOperacion.VAPOR,
        duracion,
        100,  # El vapor siempre es a 100°C
        velocidad,
        "Cocinar al vapor"
    )