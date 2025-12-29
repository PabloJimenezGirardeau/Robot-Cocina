"""
=================================================================
EXCEPCIONES PERSONALIZADAS
=================================================================
Jerarquía de excepciones para el Robot de Cocina.

HERENCIA en excepciones:
- RobotException (base)
  ├── RobotApagadoError
  ├── TareaInvalidaError
  ├── RecetaError
  └── DatabaseError

=================================================================
"""


class RobotException(Exception):
    """
    Excepción base para el Robot de Cocina.
    Todas las excepciones del sistema heredan de esta.
    """
    
    def __init__(self, mensaje: str, codigo: str = "ROBOT_ERROR"):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(self.mensaje)
    
    def __str__(self) -> str:
        return f"[{self.codigo}] {self.mensaje}"


class RobotApagadoError(RobotException):
    """
    Se lanza cuando se intenta operar con el robot apagado.
    """
    
    def __init__(self, mensaje: str = "El robot está apagado"):
        super().__init__(mensaje, "ROBOT_OFF")


class TareaInvalidaError(RobotException):
    """
    Se lanza cuando una tarea no es válida o no puede ejecutarse.
    """
    
    def __init__(self, mensaje: str = "Tarea inválida"):
        super().__init__(mensaje, "TAREA_INVALID")


class RecetaError(RobotException):
    """
    Se lanza cuando hay un problema con una receta.
    """
    
    def __init__(self, mensaje: str = "Error en la receta"):
        super().__init__(mensaje, "RECETA_ERROR")


class DatabaseError(RobotException):
    """
    Se lanza cuando hay un error de base de datos.
    """
    
    def __init__(self, mensaje: str = "Error de base de datos"):
        super().__init__(mensaje, "DB_ERROR")


class ConfiguracionError(RobotException):
    """
    Se lanza cuando hay un error de configuración.
    """
    
    def __init__(self, mensaje: str = "Error de configuración"):
        super().__init__(mensaje, "CONFIG_ERROR")
