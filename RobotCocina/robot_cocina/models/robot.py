"""
=================================================================
ROBOT DE COCINA - NÚCLEO DEL SISTEMA
=================================================================
Implementa el patrón State Machine para gestión de estados.
Demuestra: Encapsulamiento, Abstracción, Polimorfismo.

Autor: Estudiante
Versión: 4.0
=================================================================
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Callable, Dict, List, Any, TYPE_CHECKING
import asyncio

from models.tarea import Tarea, TareaCorte, TareaTemperatura, TareaMecanica, TipoOperacion
from utils.exceptions import RobotApagadoError, TareaInvalidaError, RecetaError
from utils.simulator import CookingSimulator

if TYPE_CHECKING:
    from models.receta import Receta


class EstadoRobot(Enum):
    """
    Estados posibles del robot.
    Implementa el patrón State para gestión de estados.
    """
    APAGADO = "apagado"
    IDLE = "idle"
    PREPARADO = "preparado"
    EJECUTANDO = "ejecutando"
    PAUSADO = "pausado"
    FINALIZADO = "finalizado"
    ERROR = "error"


class ObservadorRobot(ABC):
    """
    Interfaz Observer para notificaciones del robot.
    ABSTRACCIÓN: Define contrato sin implementación.
    """
    
    @abstractmethod
    def on_estado_changed(self, estado: EstadoRobot) -> None:
        """Notifica cambio de estado."""
        pass
    
    @abstractmethod
    def on_progreso_changed(self, progreso: int) -> None:
        """Notifica cambio de progreso (0-100)."""
        pass
    
    @abstractmethod
    def on_evento(self, mensaje: str) -> None:
        """Notifica un evento."""
        pass


class Robot:
    """
    Clase principal del Robot de Cocina.
    
    ENCAPSULAMIENTO: 
    - Atributos privados con underscore
    - Acceso controlado mediante properties
    - Validación en setters
    
    PATRÓN OBSERVER:
    - Notifica a observadores sobre cambios de estado
    
    PATRÓN STATE MACHINE:
    - Gestiona transiciones de estado válidas
    """

    # Transiciones válidas de estado
    _TRANSICIONES_VALIDAS = {
        EstadoRobot.APAGADO: [EstadoRobot.IDLE],
        EstadoRobot.IDLE: [EstadoRobot.APAGADO, EstadoRobot.PREPARADO],
        EstadoRobot.PREPARADO: [EstadoRobot.IDLE, EstadoRobot.EJECUTANDO],
        EstadoRobot.EJECUTANDO: [EstadoRobot.PAUSADO, EstadoRobot.FINALIZADO, EstadoRobot.IDLE, EstadoRobot.ERROR],
        EstadoRobot.PAUSADO: [EstadoRobot.EJECUTANDO, EstadoRobot.IDLE],
        EstadoRobot.FINALIZADO: [EstadoRobot.IDLE, EstadoRobot.PREPARADO],
        EstadoRobot.ERROR: [EstadoRobot.IDLE],
    }

    def __init__(self) -> None:
        """Inicializa el robot en estado apagado."""
        # ===== ESTADO INTERNO (ENCAPSULADO) =====
        self._estado: EstadoRobot = EstadoRobot.APAGADO
        
        # ===== PARÁMETROS FÍSICOS =====
        self._temperatura: int = 0
        self._velocidad: int = 0
        
        # ===== EJECUCIÓN =====
        self._tarea_actual: Optional[Tarea] = None
        self._receta_actual: Optional[Receta] = None
        self._paso_actual: int = 0
        self._total_pasos: int = 0
        
        # ===== PROGRESO =====
        self._progreso_actual: int = 0
        self._progreso_receta: int = 0
        self._duracion_paso_actual: int = 0
        self._tiempo_restante_paso: int = 0
        self._tiempo_restante_receta: int = 0
        
        # ===== CONTROL =====
        self._cancelado: bool = False
        
        # ===== SIMULADOR (Composición) =====
        self._simulator = CookingSimulator(velocidad_multiplicador=0.01)
        
        # ===== OBSERVADORES (Patrón Observer) =====
        self._observadores: List[ObservadorRobot] = []
        
        # ===== CALLBACKS LEGACY =====
        self._callback_progreso: Optional[Callable[[int], None]] = None
        self._callback_estado: Optional[Callable[[EstadoRobot], None]] = None
        self._callback_evento: Optional[Callable[[str], None]] = None

    # ==========================================================
    # PROPERTIES (Encapsulamiento con acceso controlado)
    # ==========================================================

    @property
    def estado(self) -> EstadoRobot:
        """Estado actual del robot (solo lectura)."""
        return self._estado

    @property
    def temperatura(self) -> int:
        """Temperatura actual en °C."""
        return self._temperatura
    
    @temperatura.setter
    def temperatura(self, valor: int) -> None:
        """Establece temperatura con validación."""
        if not 0 <= valor <= 200:
            raise ValueError(f"Temperatura debe estar entre 0 y 200°C, recibido: {valor}")
        self._temperatura = valor

    @property
    def velocidad(self) -> int:
        """Velocidad actual (1-10)."""
        return self._velocidad
    
    @velocidad.setter
    def velocidad(self, valor: int) -> None:
        """Establece velocidad con validación."""
        if not 0 <= valor <= 10:
            raise ValueError(f"Velocidad debe estar entre 0 y 10, recibido: {valor}")
        self._velocidad = valor

    @property
    def tarea_actual(self) -> Optional[Tarea]:
        return self._tarea_actual

    @property
    def receta_actual(self) -> Optional[Receta]:
        return self._receta_actual

    @property
    def paso_actual(self) -> int:
        return self._paso_actual

    @property
    def total_pasos(self) -> int:
        return self._total_pasos

    @property
    def progreso_actual(self) -> int:
        return self._progreso_actual

    @property
    def esta_ocupado(self) -> bool:
        """Indica si el robot está ejecutando algo."""
        return self._estado in (EstadoRobot.EJECUTANDO, EstadoRobot.PAUSADO)

    # ==========================================================
    # GESTIÓN DE OBSERVADORES (Patrón Observer)
    # ==========================================================

    def agregar_observador(self, observador: ObservadorRobot) -> None:
        """Registra un observador."""
        if observador not in self._observadores:
            self._observadores.append(observador)

    def eliminar_observador(self, observador: ObservadorRobot) -> None:
        """Elimina un observador."""
        if observador in self._observadores:
            self._observadores.remove(observador)

    # ==========================================================
    # CALLBACKS LEGACY (compatibilidad)
    # ==========================================================

    def registrar_callback_progreso(self, callback: Callable[[int], None]) -> None:
        self._callback_progreso = callback

    def registrar_callback_estado(self, callback: Callable[[EstadoRobot], None]) -> None:
        self._callback_estado = callback

    def registrar_callback_evento(self, callback: Callable[[str], None]) -> None:
        self._callback_evento = callback

    # ==========================================================
    # NOTIFICACIONES
    # ==========================================================

    def _notificar_cambio_estado(self) -> None:
        """Notifica a todos los observadores sobre cambio de estado."""
        for obs in self._observadores:
            try:
                obs.on_estado_changed(self._estado)
            except Exception as e:
                print(f"[ROBOT] Error notificando observador: {e}")
        
        if self._callback_estado:
            try:
                self._callback_estado(self._estado)
            except Exception as e:
                print(f"[ROBOT] Error en callback estado: {e}")

    def _notificar_progreso(self, progreso: int) -> None:
        """Notifica progreso a observadores."""
        for obs in self._observadores:
            try:
                obs.on_progreso_changed(progreso)
            except Exception as e:
                print(f"[ROBOT] Error notificando progreso: {e}")
        
        if self._callback_progreso:
            try:
                self._callback_progreso(progreso)
            except Exception as e:
                print(f"[ROBOT] Error en callback progreso: {e}")

    def _notificar_evento(self, mensaje: str) -> None:
        """Notifica un evento."""
        print(f"[ROBOT EVENTO] {mensaje}")
        
        for obs in self._observadores:
            try:
                obs.on_evento(mensaje)
            except Exception as e:
                print(f"[ROBOT] Error notificando evento: {e}")
        
        if self._callback_evento:
            try:
                self._callback_evento(mensaje)
            except Exception as e:
                print(f"[ROBOT] Error en callback evento: {e}")

    # ==========================================================
    # GESTIÓN DE ESTADOS (State Machine)
    # ==========================================================

    def _cambiar_estado(self, nuevo_estado: EstadoRobot) -> bool:
        """
        Cambia el estado validando la transición.
        Implementa el patrón State Machine.
        """
        if nuevo_estado == self._estado:
            return True
        
        transiciones_permitidas = self._TRANSICIONES_VALIDAS.get(self._estado, [])
        
        if nuevo_estado not in transiciones_permitidas:
            print(f"[ROBOT] Transición inválida: {self._estado.value} -> {nuevo_estado.value}")
            return False
        
        print(f"[ROBOT] Estado: {self._estado.value} -> {nuevo_estado.value}")
        self._estado = nuevo_estado
        self._notificar_cambio_estado()
        return True

    # ==========================================================
    # CONTROL BÁSICO
    # ==========================================================

    def encender(self) -> bool:
        """Enciende el robot."""
        if self._estado != EstadoRobot.APAGADO:
            return False
        
        self._reset_parametros()
        if self._cambiar_estado(EstadoRobot.IDLE):
            self._notificar_evento("🔌 Robot encendido y listo")
            return True
        return False

    def apagar(self) -> bool:
        """Apaga el robot."""
        if self.esta_ocupado:
            raise TareaInvalidaError("No se puede apagar mientras ejecuta una receta")
        
        if self._estado == EstadoRobot.APAGADO:
            return False
        
        self._reset_todo()
        self._estado = EstadoRobot.APAGADO
        self._notificar_cambio_estado()
        self._notificar_evento("Robot apagado")
        return True

    def parada_emergencia(self) -> None:
        """Detiene inmediatamente toda operación."""
        print("[ROBOT] ⚠️ PARADA DE EMERGENCIA")
        self._cancelado = True
        self._simulator.detener()
        self._reset_todo()
        self._estado = EstadoRobot.IDLE
        self._notificar_cambio_estado()
        self._notificar_evento("⚠️ PARADA DE EMERGENCIA ACTIVADA")

    def pausar(self) -> bool:
        """Pausa la ejecución actual."""
        if self._estado != EstadoRobot.EJECUTANDO:
            raise TareaInvalidaError("No hay receta en ejecución para pausar")
        
        self._simulator.pausar()
        if self._cambiar_estado(EstadoRobot.PAUSADO):
            self._notificar_evento("⏸️ Receta pausada")
            return True
        return False

    def reanudar(self) -> bool:
        """Reanuda la ejecución pausada."""
        if self._estado != EstadoRobot.PAUSADO:
            raise TareaInvalidaError("No hay receta pausada para reanudar")
        
        self._simulator.reanudar()
        if self._cambiar_estado(EstadoRobot.EJECUTANDO):
            self._notificar_evento("▶️ Receta reanudada")
            return True
        return False

    # ==========================================================
    # PREPARACIÓN Y EJECUCIÓN DE RECETAS
    # ==========================================================

    def preparar_receta(self, receta: Receta) -> bool:
        """
        Prepara una receta para ejecución.
        
        Args:
            receta: Receta a preparar
            
        Returns:
            True si se preparó correctamente
            
        Raises:
            RobotApagadoError: Si el robot está apagado
            TareaInvalidaError: Si no se puede preparar en el estado actual
        """
        if self._estado == EstadoRobot.APAGADO:
            raise RobotApagadoError("El robot está apagado")
        
        if self._estado not in (EstadoRobot.IDLE, EstadoRobot.FINALIZADO):
            raise TareaInvalidaError(f"No se puede preparar receta en estado: {self._estado.value}")
        
        if not receta.pasos:
            raise RecetaError("La receta no tiene pasos definidos")
        
        # Configurar receta
        self._receta_actual = receta
        self._tarea_actual = None
        self._paso_actual = 0
        self._total_pasos = len(receta.pasos)
        self._progreso_actual = 0
        self._progreso_receta = 0
        self._cancelado = False
        
        # Reset simulador
        self._simulator.reset()
        
        # Calcular tiempo total
        self._tiempo_restante_receta = sum(
            int(p.get("duracion", 0)) for p in receta.pasos
        )
        
        # Cambiar estado
        if self._cambiar_estado(EstadoRobot.PREPARADO):
            self._notificar_evento(
                f'📋 Receta "{receta.nombre}" preparada ({self._total_pasos} pasos)'
            )
            return True
        return False

    async def comenzar_receta(self) -> bool:
        """
        Ejecuta la receta preparada paso a paso.
        
        IMPORTANTE: Método asíncrono para no bloquear la UI.
        
        Returns:
            True si se completó, False si fue cancelada/error
        """
        if self._estado == EstadoRobot.APAGADO:
            raise RobotApagadoError("El robot está apagado")
        
        if self._estado != EstadoRobot.PREPARADO:
            raise TareaInvalidaError("No hay receta preparada")
        
        if not self._receta_actual:
            raise RecetaError("No hay receta cargada")
        
        pasos = self._receta_actual.pasos
        total = len(pasos)
        
        # Iniciar ejecución
        self._cancelado = False
        self._cambiar_estado(EstadoRobot.EJECUTANDO)
        self._notificar_evento(f"🚀 Iniciando receta: {self._receta_actual.nombre}")
        
        print(f"[ROBOT] Ejecutando {total} pasos")
        
        # ========== BUCLE PRINCIPAL DE PASOS ==========
        for i, paso in enumerate(pasos):
            # Verificar cancelación
            if self._cancelado:
                print(f"[ROBOT] Cancelado antes del paso {i+1}")
                self._finalizar(EstadoRobot.IDLE, "Receta cancelada")
                return False
            
            # Actualizar estado del paso
            self._paso_actual = i
            self._progreso_actual = 0
            self._progreso_receta = int((i / total) * 100)
            
            # Tiempo restante
            self._tiempo_restante_receta = sum(
                int(p.get("duracion", 0)) for p in pasos[i:]
            )
            
            # Notificar cambio de paso
            self._notificar_progreso(0)
            
            print(f"[ROBOT] === Paso {i+1}/{total}: {paso.get('operacion', paso.get('nombre', '?'))} ===")
            
            # Crear y ejecutar tarea
            try:
                tarea = self._crear_tarea(paso)
                resultado = await self._ejecutar_tarea(tarea)
                
                if not resultado:
                    if self._cancelado:
                        self._finalizar(EstadoRobot.IDLE, "Receta cancelada")
                    else:
                        self._finalizar(EstadoRobot.ERROR, "Error en ejecución")
                    return False
                
                print(f"[ROBOT] Paso {i+1} completado ✓")
                
                # CRÍTICO: Pequeña pausa entre pasos para que la UI se actualice
                await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f"[ROBOT ERROR] Paso {i+1}: {e}")
                self._finalizar(EstadoRobot.ERROR, f"Error: {e}")
                return False
        
        # ========== RECETA COMPLETADA ==========
        self._progreso_receta = 100
        self._progreso_actual = 100
        self._tiempo_restante_receta = 0
        self._tiempo_restante_paso = 0
        
        self._cambiar_estado(EstadoRobot.FINALIZADO)
        self._notificar_progreso(100)
        self._notificar_evento("🎉 ¡Receta completada con éxito!")
        
        return True

    async def _ejecutar_tarea(self, tarea: Tarea) -> bool:
        """Ejecuta una tarea individual."""
        # Validar
        valido, msg = tarea.validar()
        if not valido:
            raise TareaInvalidaError(msg)
        
        # Configurar
        self._tarea_actual = tarea
        self._progreso_actual = 0
        self._duracion_paso_actual = tarea.duracion
        self._tiempo_restante_paso = tarea.duracion
        
        # Aplicar parámetros (POLIMORFISMO - cada tarea aplica diferente)
        tarea.aplicar(self)
        
        # Notificar inicio
        self._notificar_evento(tarea.mensaje_inicio())
        self._notificar_progreso(0)
        
        # Simular
        resultado = await self._simulator.simular_tarea(
            tarea.duracion,
            self._callback_simulador
        )
        
        # Notificar fin
        if resultado:
            self._notificar_evento(tarea.mensaje_fin())
        
        return resultado

    def _callback_simulador(self, actual: int, total: int) -> None:
        """Callback del simulador para actualizar progreso."""
        if total <= 0:
            self._progreso_actual = 100
            self._tiempo_restante_paso = 0
        else:
            self._progreso_actual = int((actual / total) * 100)
            self._tiempo_restante_paso = max(0, total - actual)
        
        # Progreso global
        if self._receta_actual and self._total_pasos > 0:
            progreso_paso = actual / total if total > 0 else 1
            self._progreso_receta = int(
                ((self._paso_actual + progreso_paso) / self._total_pasos) * 100
            )
            
            # Tiempo restante total
            pasos_futuros = sum(
                int(p.get("duracion", 0))
                for p in self._receta_actual.pasos[self._paso_actual + 1:]
            )
            self._tiempo_restante_receta = self._tiempo_restante_paso + pasos_futuros
        
        self._notificar_progreso(self._progreso_actual)

    # ==========================================================
    # UTILIDADES
    # ==========================================================

    def _crear_tarea(self, paso: Dict[str, Any]) -> Tarea:
        """
        Factory Method para crear tareas desde definición de paso.
        POLIMORFISMO: Retorna diferentes tipos de Tarea.
        """
        tipo = paso.get("tipo", "").lower()
        
        if tipo == "corte":
            return TareaCorte(
                operacion=TipoOperacion(paso.get("operacion", "picar")),
                duracion=int(paso.get("duracion", 30)),
                velocidad=int(paso.get("velocidad", 5)),
                descripcion=paso.get("descripcion", "")
            )
        
        elif tipo == "temperatura":
            return TareaTemperatura(
                operacion=TipoOperacion(paso.get("operacion", "hervir")),
                duracion=int(paso.get("duracion", 60)),
                temperatura=int(paso.get("temperatura", 100)),
                velocidad=int(paso.get("velocidad", 1)),
                descripcion=paso.get("descripcion", "")
            )
        
        elif tipo == "mecanica":
            return TareaMecanica(
                nombre=paso.get("nombre", paso.get("operacion", "Mezclar")),
                duracion=int(paso.get("duracion", 30)),
                velocidad=int(paso.get("velocidad", 5)),
                descripcion=paso.get("descripcion", "")
            )
        
        else:
            raise TareaInvalidaError(f"Tipo de tarea desconocido: {tipo}")

    def _finalizar(self, estado: EstadoRobot, mensaje: str) -> None:
        """Finaliza la ejecución con un estado y mensaje."""
        self._reset_parametros()
        self._cambiar_estado(estado)
        self._notificar_evento(mensaje)

    def _reset_parametros(self) -> None:
        """Resetea parámetros físicos."""
        self._tarea_actual = None
        self._temperatura = 0
        self._velocidad = 0
        self._progreso_actual = 0

    def _reset_todo(self) -> None:
        """Resetea todo el estado."""
        self._reset_parametros()
        self._receta_actual = None
        self._paso_actual = 0
        self._total_pasos = 0
        self._progreso_receta = 0
        self._duracion_paso_actual = 0
        self._tiempo_restante_paso = 0
        self._tiempo_restante_receta = 0
        self._cancelado = False

    # ==========================================================
    # INFORMACIÓN
    # ==========================================================

    def get_estado_completo(self) -> Dict[str, Any]:
        """Retorna el estado completo del robot."""
        return {
            "estado": self._estado.value,
            "temperatura": self._temperatura,
            "velocidad": self._velocidad,
            "progreso_paso": self._progreso_actual,
            "progreso_receta": self._progreso_receta,
            "tarea_actual": self._tarea_actual.nombre if self._tarea_actual else None,
            "receta_actual": self._receta_actual.nombre if self._receta_actual else None,
            "paso_actual": self._paso_actual,
            "total_pasos": self._total_pasos,
        }

    def get_parametros_activos(self) -> Dict[str, Any]:
        """Retorna los parámetros físicos activos."""
        return {
            "operacion": self._tarea_actual.nombre if self._tarea_actual else None,
            "temperatura": self._temperatura,
            "velocidad": self._velocidad,
        }

    def get_tiempos_restantes(self) -> Dict[str, int]:
        """Retorna los tiempos restantes."""
        return {
            "paso": self._tiempo_restante_paso,
            "receta": self._tiempo_restante_receta,
        }

    def __repr__(self) -> str:
        return f"Robot(estado={self._estado.value}, temp={self._temperatura}°C, vel={self._velocidad})"
