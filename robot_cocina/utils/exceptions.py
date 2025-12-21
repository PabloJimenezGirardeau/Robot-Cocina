"""
Excepciones personalizadas del sistema.
"""


class RobotException(Exception):
    """Excepción base para errores del robot."""
    pass


class RobotApagadoError(RobotException):
    """Se intenta operar con el robot apagado."""
    pass


class TareaInvalidaError(RobotException):
    """La tarea no puede ejecutarse en el estado actual."""
    pass


class RecetaNoEncontradaError(RobotException):
    """No se encuentra la receta solicitada."""
    pass


class DatabaseError(RobotException):
    """Error en operaciones de base de datos."""
    pass
