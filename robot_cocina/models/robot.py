"""
Clase base Robot - Núcleo del sistema de control.
Implementa encapsulamiento de estados y operaciones básicas.
"""

from enum import Enum
from typing import Optional, Callable, List, Dict
import asyncio
from models.tarea import Tarea
from models.receta import Receta
from utils.exceptions import RobotApagadoError, TareaInvalidaError
from utils.threading_utils import CookingSimulator


class EstadoRobot(Enum):
    """Estados posibles del robot."""
    APAGADO = "apagado"
    ENCENDIDO = "encendido"
    COCINANDO = "cocinando"
    PAUSADO = "pausado"
    ERROR = "error"


class ModoOperacion(Enum):
    """Modos de operación del robot."""
    MANUAL = "manual"
    COCINA_GUIADA = "cocina_guiada"


class Robot:
    """Clase base que representa el robot de cocina."""
    
    def __init__(self):
        """Inicializa el robot en estado apagado."""
        self._estado = EstadoRobot.APAGADO
        self._modo = ModoOperacion.MANUAL
        self._temperatura = 0
        self._velocidad = 0
        self._tarea_actual: Optional[Tarea] = None
        self._receta_actual: Optional[Receta] = None
        self._paso_actual: int = 0
        self._progreso_actual: int = 0
        self._simulator = CookingSimulator()
        self._callback_progreso: Optional[Callable] = None
        self._callback_estado: Optional[Callable] = None
    
    # ==================== PROPIEDADES ====================
    
    @property
    def estado(self) -> EstadoRobot:
        """Obtiene el estado actual del robot."""
        return self._estado
    
    @property
    def modo(self) -> ModoOperacion:
        """Obtiene el modo de operación actual."""
        return self._modo
    
    @property
    def temperatura(self) -> int:
        """Obtiene la temperatura actual."""
        return self._temperatura
    
    @property
    def velocidad(self) -> int:
        """Obtiene la velocidad actual."""
        return self._velocidad
    
    @property
    def tarea_actual(self) -> Optional[Tarea]:
        """Obtiene la tarea en ejecución."""
        return self._tarea_actual
    
    @property
    def receta_actual(self) -> Optional[Receta]:
        """Obtiene la receta en ejecución."""
        return self._receta_actual
    
    @property
    def paso_actual(self) -> int:
        """Obtiene el paso actual de la receta."""
        return self._paso_actual
    
    @property
    def progreso_actual(self) -> int:
        """Obtiene el progreso actual (0-100)."""
        return self._progreso_actual
    
    @property
    def esta_ocupado(self) -> bool:
        """Verifica si el robot está ejecutando una tarea."""
        return self._estado == EstadoRobot.COCINANDO or self._estado == EstadoRobot.PAUSADO
    
    # ==================== CONTROL BÁSICO ====================
    
    def encender(self) -> bool:
        """
        Enciende el robot.
        
        Returns:
            True si se encendió correctamente
        """
        if self._estado == EstadoRobot.APAGADO:
            self._estado = EstadoRobot.ENCENDIDO
            self._temperatura = 0
            self._velocidad = 0
            self._tarea_actual = None
            self._notificar_cambio_estado()
            return True
        return False
    
    def apagar(self) -> bool:
        """
        Apaga el robot.
        
        Returns:
            True si se apagó correctamente
        
        Raises:
            TareaInvalidaError si hay una tarea en ejecución
        """
        if self.esta_ocupado:
            raise TareaInvalidaError(
                "No se puede apagar el robot mientras está cocinando. "
                "Use parada de emergencia primero."
            )
        
        if self._estado != EstadoRobot.APAGADO:
            self._estado = EstadoRobot.APAGADO
            self._temperatura = 0
            self._velocidad = 0
            self._modo = ModoOperacion.MANUAL
            self._tarea_actual = None
            self._receta_actual = None
            self._notificar_cambio_estado()
            return True
        return False
    
    def parada_emergencia(self):
        """Detiene inmediatamente todas las operaciones."""
        self._simulator.detener()
        self._estado = EstadoRobot.ENCENDIDO
        self._temperatura = 0
        self._velocidad = 0
        self._tarea_actual = None
        self._progreso_actual = 0
        self._notificar_cambio_estado()
    
    def pausar(self) -> bool:
        """
        Pausa la tarea actual.
        
        Returns:
            True si se pausó correctamente
        """
        if self._estado == EstadoRobot.COCINANDO:
            self._simulator.pausar()
            self._estado = EstadoRobot.PAUSADO
            self._notificar_cambio_estado()
            return True
        return False
    
    def reanudar(self) -> bool:
        """
        Reanuda la tarea pausada.
        
        Returns:
            True si se reanudó correctamente
        """
        if self._estado == EstadoRobot.PAUSADO:
            self._simulator.reanudar()
            self._estado = EstadoRobot.COCINANDO
            self._notificar_cambio_estado()
            return True
        return False
    
    def cambiar_modo(self, modo: ModoOperacion) -> bool:
        """
        Cambia el modo de operación.
        
        Args:
            modo: Nuevo modo de operación
        
        Returns:
            True si se cambió correctamente
        
        Raises:
            TareaInvalidaError si está ocupado
        """
        if self.esta_ocupado:
            raise TareaInvalidaError("No se puede cambiar de modo mientras se cocina")
        
        self._modo = modo
        self._notificar_cambio_estado()
        return True
    
    # ==================== EJECUCIÓN DE TAREAS ====================
    
    async def ejecutar_tarea(self, tarea: Tarea) -> bool:
        """
        Ejecuta una tarea individual (modo manual).
        
        Args:
            tarea: Tarea a ejecutar
        
        Returns:
            True si se completó, False si fue detenida
        
        Raises:
            RobotApagadoError si el robot está apagado
            TareaInvalidaError si la tarea no es válida
        """
        if self._estado == EstadoRobot.APAGADO:
            raise RobotApagadoError("El robot debe estar encendido para ejecutar tareas")
        
        if self.esta_ocupado:
            raise TareaInvalidaError("Ya hay una tarea en ejecución")
        
        # Validar la tarea
        es_valida, mensaje = tarea.validar()
        if not es_valida:
            raise TareaInvalidaError(f"Tarea inválida: {mensaje}")
        
        # Configurar tarea
        self._tarea_actual = tarea
        self._estado = EstadoRobot.COCINANDO
        self._progreso_actual = 0
        self._notificar_cambio_estado()
        
        # Obtener parámetros y aplicarlos
        params = tarea.ejecutar()
        self._temperatura = params.get("temperatura", 0)
        self._velocidad = params.get("velocidad", 0)
        
        # Ejecutar simulación
        resultado = await self._simulator.simular_tarea(
            tarea.duracion,
            self._actualizar_progreso_tarea
        )
        
        # Limpiar después de ejecutar
        if resultado:
            self._progreso_actual = 100
            self._notificar_progreso()
        
        self._estado = EstadoRobot.ENCENDIDO
        self._tarea_actual = None
        self._temperatura = 0
        self._velocidad = 0
        self._progreso_actual = 0
        self._notificar_cambio_estado()
        
        return resultado
    
    async def ejecutar_receta(self, receta: Receta) -> bool:
        """
        Ejecuta una receta completa (modo cocina guiada).
        
        Args:
            receta: Receta a ejecutar
        
        Returns:
            True si se completó, False si fue detenida
        
        Raises:
            RobotApagadoError si el robot está apagado
        """
        if self._estado == EstadoRobot.APAGADO:
            raise RobotApagadoError("El robot debe estar encendido para cocinar recetas")
        
        if self.esta_ocupado:
            raise TareaInvalidaError("Ya hay una tarea en ejecución")
        
        # Configurar receta
        self._receta_actual = receta
        self._paso_actual = 0
        self._modo = ModoOperacion.COCINA_GUIADA
        self._notificar_cambio_estado()
        
        # Ejecutar cada paso
        for i, paso in enumerate(receta.pasos):
            self._paso_actual = i
            
            # Crear tarea desde el paso
            tarea = self._crear_tarea_desde_paso(paso)
            
            # Ejecutar tarea
            resultado = await self.ejecutar_tarea(tarea)
            
            if not resultado:
                # Tarea detenida
                self._receta_actual = None
                self._paso_actual = 0
                return False
        
        # Receta completada
        self._receta_actual = None
        self._paso_actual = 0
        self._modo = ModoOperacion.MANUAL
        self._notificar_cambio_estado()
        
        return True
    
    def _crear_tarea_desde_paso(self, paso: Dict) -> Tarea:
        """Crea una instancia de Tarea desde un diccionario de paso."""
        # Importar aquí para evitar circular imports
        from models.tarea import (
            TareaCorte, TareaTemperatura, TareaMecanica, TipoOperacion
        )
        
        tipo = paso.get("tipo")
        
        if tipo == "corte":
            return TareaCorte(
                TipoOperacion(paso["operacion"]),
                paso["duracion"],
                paso["velocidad"],
                paso.get("descripcion", "")
            )
        elif tipo == "temperatura":
            return TareaTemperatura(
                TipoOperacion(paso["operacion"]),
                paso["duracion"],
                paso["temperatura"],
                paso.get("velocidad", 1),
                paso.get("descripcion", "")
            )
        elif tipo == "mecanica":
            return TareaMecanica(
                paso.get("nombre", "Amasar"),
                paso["duracion"],
                paso["velocidad"],
                paso.get("descripcion", "")
            )
        else:
            raise TareaInvalidaError(f"Tipo de tarea desconocido: {tipo}")
    
    # ==================== CALLBACKS Y NOTIFICACIONES ====================
    
    def _actualizar_progreso_tarea(self, actual: int, total: int):
        """Callback interno para actualizar progreso."""
        self._progreso_actual = int((actual / total) * 100)
        if self._tarea_actual:
            self._tarea_actual.actualizar_progreso(self._progreso_actual)
        self._notificar_progreso()
    
    def registrar_callback_progreso(self, callback: Callable[[int], None]):
        """Registra callback para notificaciones de progreso."""
        self._callback_progreso = callback
    
    def registrar_callback_estado(self, callback: Callable[[EstadoRobot], None]):
        """Registra callback para cambios de estado."""
        self._callback_estado = callback
    
    def _notificar_progreso(self):
        """Notifica el progreso actual."""
        if self._callback_progreso:
            self._callback_progreso(self._progreso_actual)
    
    def _notificar_cambio_estado(self):
        """Notifica cambio de estado."""
        if self._callback_estado:
            self._callback_estado(self._estado)
    
    # ==================== INFORMACIÓN DE ESTADO ====================
    
    def get_estado_completo(self) -> dict:
        """Obtiene toda la información del estado actual."""
        return {
            "estado": self._estado.value,
            "modo": self._modo.value,
            "temperatura": self._temperatura,
            "velocidad": self._velocidad,
            "progreso": self._progreso_actual,
            "tarea_actual": self._tarea_actual.nombre if self._tarea_actual else None,
            "receta_actual": self._receta_actual.nombre if self._receta_actual else None,
            "paso_actual": self._paso_actual if self._receta_actual else None,
            "total_pasos": len(self._receta_actual.pasos) if self._receta_actual else None
        }