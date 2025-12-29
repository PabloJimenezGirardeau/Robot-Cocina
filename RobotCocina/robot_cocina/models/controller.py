"""
=================================================================
CONTROLADOR DEL ROBOT
=================================================================
Implementa el patrón MVC - Controlador.
Actúa como intermediario entre la UI (Vista) y el Robot (Modelo).
=================================================================
"""

from models.robot import Robot, EstadoRobot
from models.receta import Receta
from utils.exceptions import RobotApagadoError, TareaInvalidaError


class RobotController:
    """
    Controlador para el Robot de Cocina.
    
    PATRÓN MVC:
    - Recibe acciones de la Vista (UI)
    - Actualiza el Modelo (Robot)
    - Maneja excepciones y valida operaciones
    """
    
    def __init__(self, robot: Robot):
        """
        Args:
            robot: Instancia del robot a controlar
        """
        self._robot = robot
    
    @property
    def robot(self) -> Robot:
        """Acceso al robot (solo lectura)."""
        return self._robot
    
    def encender(self) -> bool:
        """Enciende el robot."""
        return self._robot.encender()
    
    def apagar(self) -> bool:
        """Apaga el robot."""
        return self._robot.apagar()
    
    def pausar(self) -> bool:
        """Pausa la ejecución actual."""
        return self._robot.pausar()
    
    def reanudar(self) -> bool:
        """Reanuda la ejecución pausada."""
        return self._robot.reanudar()
    
    def parada_emergencia(self) -> None:
        """Ejecuta parada de emergencia."""
        self._robot.parada_emergencia()
    
    def preparar_receta(self, receta: Receta) -> bool:
        """
        Prepara una receta para ejecución.
        
        Args:
            receta: Receta a preparar
            
        Returns:
            True si se preparó correctamente
        """
        return self._robot.preparar_receta(receta)
    
    async def ejecutar_receta(self) -> bool:
        """
        Ejecuta la receta preparada.
        
        Returns:
            True si se completó correctamente
        """
        return await self._robot.comenzar_receta()
    
    def get_estado(self) -> EstadoRobot:
        """Obtiene el estado actual."""
        return self._robot.estado
    
    def get_info_completa(self) -> dict:
        """Obtiene información completa del robot."""
        return self._robot.get_estado_completo()
