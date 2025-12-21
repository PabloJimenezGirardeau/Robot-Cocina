"""
Utilidades para manejo de concurrencia.
Permite ejecutar tareas sin bloquear la UI.
"""

import asyncio
import time
from typing import Callable, Any, Optional
from concurrent.futures import ThreadPoolExecutor


class TaskExecutor:
    """Ejecutor de tareas en segundo plano."""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._running_tasks = {}
    
    async def run_async(self, func: Callable, *args, **kwargs) -> Any:
        """Ejecuta una función en un hilo separado."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            lambda: func(*args, **kwargs)
        )
    
    def shutdown(self):
        """Cierra el executor."""
        self.executor.shutdown(wait=True)


class CookingSimulator:
    """Simula el proceso de cocción en tiempo real."""
    
    def __init__(self):
        self._is_running = False
        self._is_paused = False
        self._should_stop = False
    
    async def simular_tarea(
        self, 
        duracion: int, 
        callback: Optional[Callable[[int, int], None]] = None
    ) -> bool:
        """
        Simula una tarea de cocina con progreso.
        
        Args:
            duracion: Duración en segundos
            callback: Función a llamar con (progreso, total)
        
        Returns:
            True si se completó, False si fue detenida
        """
        self._is_running = True
        self._should_stop = False
        
        for segundo in range(duracion + 1):
            if self._should_stop:
                self._is_running = False
                return False
            
            # Esperar mientras está pausado
            while self._is_paused and not self._should_stop:
                await asyncio.sleep(0.1)
            
            if self._should_stop:
                self._is_running = False
                return False
            
            # Llamar al callback con el progreso
            if callback:
                callback(segundo, duracion)
            
            # Esperar 1 segundo (simulación en tiempo real)
            if segundo < duracion:
                await asyncio.sleep(1)
        
        self._is_running = False
        return True
    
    def pausar(self):
        """Pausa la simulación."""
        self._is_paused = True
    
    def reanudar(self):
        """Reanuda la simulación."""
        self._is_paused = False
    
    def detener(self):
        """Detiene completamente la simulación."""
        self._should_stop = True
        self._is_paused = False
    
    @property
    def is_running(self) -> bool:
        """Verifica si hay una tarea ejecutándose."""
        return self._is_running
    
    @property
    def is_paused(self) -> bool:
        """Verifica si la tarea está pausada."""
        return self._is_paused