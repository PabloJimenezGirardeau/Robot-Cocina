"""
=================================================================
TAREAS DEL ROBOT DE COCINA
=================================================================
Implementa jerarquía de clases con herencia y polimorfismo.

HERENCIA:
- Tarea (clase base abstracta)
  ├── TareaCorte
  ├── TareaTemperatura
  └── TareaMecanica

POLIMORFISMO:
- Cada subclase implementa aplicar() de forma diferente
- Cada subclase genera mensajes específicos

=================================================================
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from models.robot import Robot


class TipoOperacion(Enum):
    """Tipos de operaciones disponibles."""
    # Operaciones de corte
    PICAR = "picar"
    TROCEAR = "trocear"
    TRITURAR = "triturar"
    RALLAR = "rallar"
    
    # Operaciones de temperatura
    SOFREIR = "sofreir"
    HERVIR = "hervir"
    VAPOR = "vapor"
    CALENTAR = "calentar"
    
    # Operaciones mecánicas
    AMASAR = "amasar"
    MEZCLAR = "mezclar"
    BATIR = "batir"
    REMOVER = "remover"


class Tarea(ABC):
    """
    CLASE BASE ABSTRACTA para todas las tareas.
    
    ABSTRACCIÓN:
    - Define la interfaz común para todas las tareas
    - Métodos abstractos que cada subclase debe implementar
    
    ENCAPSULAMIENTO:
    - Atributos protegidos con validación
    """
    
    def __init__(self, nombre: str, duracion: int, descripcion: str = ""):
        """
        Inicializa una tarea.
        
        Args:
            nombre: Nombre de la tarea
            duracion: Duración en segundos
            descripcion: Descripción opcional
        """
        self._nombre = nombre
        self._duracion = self._validar_duracion(duracion)
        self._descripcion = descripcion
    
    @staticmethod
    def _validar_duracion(duracion: int) -> int:
        """Valida y retorna la duración."""
        if duracion < 0:
            raise ValueError(f"La duración no puede ser negativa: {duracion}")
        return duracion
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def duracion(self) -> int:
        return self._duracion
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @abstractmethod
    def aplicar(self, robot: 'Robot') -> None:
        """
        MÉTODO ABSTRACTO - Aplica la tarea al robot.
        
        Cada subclase implementa esto de forma diferente:
        - TareaCorte: Configura velocidad
        - TareaTemperatura: Configura temperatura y velocidad
        - TareaMecanica: Configura velocidad
        
        Args:
            robot: Robot sobre el que aplicar la tarea
        """
        pass
    
    @abstractmethod
    def validar(self) -> Tuple[bool, str]:
        """
        MÉTODO ABSTRACTO - Valida que la tarea sea ejecutable.
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        pass
    
    def mensaje_inicio(self) -> str:
        """Mensaje al iniciar la tarea."""
        return f"▶️ Iniciando: {self._nombre}"
    
    def mensaje_fin(self) -> str:
        """Mensaje al finalizar la tarea."""
        return f"✓ {self._nombre} completado"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nombre='{self._nombre}', duracion={self._duracion}s)"


class TareaCorte(Tarea):
    """
    Tarea de corte/triturado.
    
    HERENCIA: Extiende Tarea
    POLIMORFISMO: Implementa aplicar() configurando velocidad
    """
    
    VELOCIDAD_MIN = 1
    VELOCIDAD_MAX = 10
    
    def __init__(
        self,
        operacion: TipoOperacion,
        duracion: int,
        velocidad: int,
        descripcion: str = ""
    ):
        """
        Args:
            operacion: Tipo de operación (picar, trocear, etc.)
            duracion: Duración en segundos
            velocidad: Velocidad de cuchillas (1-10)
            descripcion: Descripción opcional
        """
        super().__init__(operacion.value.title(), duracion, descripcion)
        self._operacion = operacion
        self._velocidad = self._validar_velocidad(velocidad)
    
    def _validar_velocidad(self, vel: int) -> int:
        """Valida la velocidad."""
        return max(self.VELOCIDAD_MIN, min(self.VELOCIDAD_MAX, vel))
    
    @property
    def operacion(self) -> TipoOperacion:
        return self._operacion
    
    @property
    def velocidad(self) -> int:
        return self._velocidad
    
    def aplicar(self, robot: 'Robot') -> None:
        """
        POLIMORFISMO: Aplica tarea de corte.
        Configura la velocidad de las cuchillas.
        """
        robot._velocidad = self._velocidad
        robot._temperatura = 0  # Corte no usa temperatura
    
    def validar(self) -> Tuple[bool, str]:
        """Valida la tarea de corte."""
        if self._duracion <= 0:
            return False, "La duración debe ser mayor a 0"
        if not self.VELOCIDAD_MIN <= self._velocidad <= self.VELOCIDAD_MAX:
            return False, f"Velocidad debe estar entre {self.VELOCIDAD_MIN} y {self.VELOCIDAD_MAX}"
        return True, ""
    
    def mensaje_inicio(self) -> str:
        return f"🔪 Iniciando {self._nombre} a velocidad {self._velocidad}"


class TareaTemperatura(Tarea):
    """
    Tarea con control de temperatura.
    
    HERENCIA: Extiende Tarea
    POLIMORFISMO: Implementa aplicar() configurando temperatura y velocidad
    """
    
    TEMP_MIN = 0
    TEMP_MAX = 200
    
    def __init__(
        self,
        operacion: TipoOperacion,
        duracion: int,
        temperatura: int,
        velocidad: int = 1,
        descripcion: str = ""
    ):
        """
        Args:
            operacion: Tipo de operación (hervir, sofreir, etc.)
            duracion: Duración en segundos
            temperatura: Temperatura objetivo en °C
            velocidad: Velocidad de aspas (1-10)
            descripcion: Descripción opcional
        """
        super().__init__(operacion.value.title(), duracion, descripcion)
        self._operacion = operacion
        self._temperatura = self._validar_temperatura(temperatura)
        self._velocidad = max(0, min(10, velocidad))
    
    def _validar_temperatura(self, temp: int) -> int:
        """Valida la temperatura."""
        return max(self.TEMP_MIN, min(self.TEMP_MAX, temp))
    
    @property
    def operacion(self) -> TipoOperacion:
        return self._operacion
    
    @property
    def temperatura(self) -> int:
        return self._temperatura
    
    @property
    def velocidad(self) -> int:
        return self._velocidad
    
    def aplicar(self, robot: 'Robot') -> None:
        """
        POLIMORFISMO: Aplica tarea de temperatura.
        Configura temperatura y velocidad.
        """
        robot._temperatura = self._temperatura
        robot._velocidad = self._velocidad
    
    def validar(self) -> Tuple[bool, str]:
        """Valida la tarea de temperatura."""
        if self._duracion <= 0:
            return False, "La duración debe ser mayor a 0"
        if not self.TEMP_MIN <= self._temperatura <= self.TEMP_MAX:
            return False, f"Temperatura debe estar entre {self.TEMP_MIN} y {self.TEMP_MAX}°C"
        return True, ""
    
    def mensaje_inicio(self) -> str:
        return f"🌡️ Iniciando {self._nombre} a {self._temperatura}°C"


class TareaMecanica(Tarea):
    """
    Tarea mecánica (amasar, mezclar, etc.)
    
    HERENCIA: Extiende Tarea
    POLIMORFISMO: Implementa aplicar() configurando velocidad
    """
    
    def __init__(
        self,
        nombre: str,
        duracion: int,
        velocidad: int,
        descripcion: str = ""
    ):
        """
        Args:
            nombre: Nombre de la operación
            duracion: Duración en segundos
            velocidad: Velocidad (1-10)
            descripcion: Descripción opcional
        """
        super().__init__(nombre.title(), duracion, descripcion)
        self._velocidad = max(1, min(10, velocidad))
    
    @property
    def velocidad(self) -> int:
        return self._velocidad
    
    def aplicar(self, robot: 'Robot') -> None:
        """
        POLIMORFISMO: Aplica tarea mecánica.
        Configura velocidad sin temperatura.
        """
        robot._velocidad = self._velocidad
        robot._temperatura = 0
    
    def validar(self) -> Tuple[bool, str]:
        """Valida la tarea mecánica."""
        if self._duracion <= 0:
            return False, "La duración debe ser mayor a 0"
        return True, ""
    
    def mensaje_inicio(self) -> str:
        return f"⚙️ Iniciando {self._nombre} a velocidad {self._velocidad}"
