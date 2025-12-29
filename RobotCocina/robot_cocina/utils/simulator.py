"""
=================================================================
SIMULADOR DE COCCIÓN
=================================================================
Simula la ejecución temporal de tareas de cocina.

USO DE ASYNC/AWAIT:
- Permite ejecución no bloqueante
- La UI permanece responsive durante la simulación
- Compatible con el event loop de NiceGUI

=================================================================
"""

import asyncio
from typing import Callable, Optional
from threading import Lock


class CookingSimulator:
    """
    Simulador de tiempo de cocción.
    
    Características:
    - Simula el paso del tiempo de forma acelerada
    - Soporta pausa y reanudación
    - Callbacks para actualización de progreso
    - Thread-safe
    """
    
    def __init__(self, velocidad_multiplicador: float = 0.01):
        """
        Args:
            velocidad_multiplicador: Factor de velocidad.
                0.01 = 100x más rápido (1 minuto real = 0.6 segundos simulados)
                0.1 = 10x más rápido
                1.0 = tiempo real
        """
        self._velocidad = velocidad_multiplicador
        self._pausado = False
        self._detenido = False
        self._lock = Lock()  # Thread safety
    
    @property
    def velocidad(self) -> float:
        return self._velocidad
    
    @velocidad.setter
    def velocidad(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La velocidad debe ser positiva")
        self._velocidad = valor
    
    async def simular_tarea(
        self,
        duracion: int,
        callback_progreso: Callable[[int, int], None]
    ) -> bool:
        """
        Simula una tarea de cocción.
        
        ASYNC: Este método es asíncrono para no bloquear el event loop.
        
        Args:
            duracion: Duración en segundos (tiempo de receta)
            callback_progreso: Función callback(tiempo_actual, tiempo_total)
        
        Returns:
            True si completó, False si fue detenido
        """
        with self._lock:
            self._detenido = False
            self._pausado = False
        
        # Validar duración
        if duracion <= 0:
            callback_progreso(0, 0)
            return True
        
        # Calcular tiempo real de simulación
        # Mínimo 2 segundos para que dé tiempo a leer cada paso
        duracion_real = max(2.0, duracion * self._velocidad)
        
        # Número de actualizaciones (más = animación más suave)
        num_pasos = min(duracion, 100)
        num_pasos = max(num_pasos, 10)  # Mínimo 10 actualizaciones
        
        intervalo = duracion_real / num_pasos
        
        print(f"[SIMULATOR] Iniciando: {duracion}s -> {duracion_real:.2f}s real ({num_pasos} pasos)")
        
        # Callback inicial
        self._safe_callback(callback_progreso, 0, duracion)
        
        # Bucle de simulación
        for i in range(1, num_pasos + 1):
            # Verificar detención
            if self._detenido:
                print("[SIMULATOR] Detenido")
                return False
            
            # Manejar pausa
            while self._pausado and not self._detenido:
                await asyncio.sleep(0.05)
            
            if self._detenido:
                return False
            
            # Esperar intervalo
            await asyncio.sleep(intervalo)
            
            # Calcular progreso
            tiempo_simulado = int((i / num_pasos) * duracion)
            
            # Notificar progreso
            self._safe_callback(callback_progreso, tiempo_simulado, duracion)
        
        # Asegurar 100%
        self._safe_callback(callback_progreso, duracion, duracion)
        
        print("[SIMULATOR] Completado ✓")
        return True
    
    def _safe_callback(
        self,
        callback: Callable[[int, int], None],
        actual: int,
        total: int
    ) -> None:
        """Ejecuta callback de forma segura."""
        try:
            callback(actual, total)
        except Exception as e:
            print(f"[SIMULATOR] Error en callback: {e}")
    
    def pausar(self) -> None:
        """Pausa la simulación."""
        with self._lock:
            self._pausado = True
        print("[SIMULATOR] Pausado")
    
    def reanudar(self) -> None:
        """Reanuda la simulación."""
        with self._lock:
            self._pausado = False
        print("[SIMULATOR] Reanudado")
    
    def detener(self) -> None:
        """Detiene la simulación completamente."""
        with self._lock:
            self._detenido = True
            self._pausado = False
        print("[SIMULATOR] Detenido")
    
    def reset(self) -> None:
        """Reinicia el estado del simulador."""
        with self._lock:
            self._detenido = False
            self._pausado = False
    
    @property
    def esta_pausado(self) -> bool:
        return self._pausado
    
    @property
    def esta_detenido(self) -> bool:
        return self._detenido
