"""
Componentes reutilizables de UI.
"""

from nicegui import ui
from typing import Callable, Optional
from models.robot import EstadoRobot, ModoOperacion
from models.receta import Receta


class StatusIndicator:
    """Indicador de estado del robot."""
    
    # Mapeo de estados a colores y emojis
    ESTADO_CONFIG = {
        EstadoRobot.APAGADO: {"color": "red-7", "icon": "power_settings_new", "texto": "Apagado"},
        EstadoRobot.ENCENDIDO: {"color": "green-6", "icon": "check_circle", "texto": "Encendido"},
        EstadoRobot.COCINANDO: {"color": "blue-6", "icon": "restaurant", "texto": "Cocinando"},
        EstadoRobot.PAUSADO: {"color": "orange-6", "icon": "pause_circle", "texto": "Pausado"},
        EstadoRobot.ERROR: {"color": "red-9", "icon": "error", "texto": "Error"},
    }
    
    def __init__(self, estado_inicial: EstadoRobot = EstadoRobot.APAGADO):
        """Inicializa el indicador de estado."""
        self.estado_actual = estado_inicial
        self._crear_componente()
    
    def _crear_componente(self):
        """Crea el componente visual."""
        config = self.ESTADO_CONFIG[self.estado_actual]
        
        with ui.card().classes('w-full'):
            with ui.row().classes('items-center w-full'):
                self.icon = ui.icon(config["icon"], size="lg").classes(f'text-{config["color"]}')
                with ui.column().classes('flex-grow'):
                    ui.label("Estado del Robot").classes('text-caption text-grey-7')
                    self.label = ui.label(config["texto"]).classes(f'text-h6 text-{config["color"]} font-bold')
    
    def actualizar(self, nuevo_estado: EstadoRobot):
        """Actualiza el estado mostrado."""
        self.estado_actual = nuevo_estado
        config = self.ESTADO_CONFIG[nuevo_estado]
        
        self.icon.props(f'name={config["icon"]} color={config["color"]}')
        self.label.text = config["texto"]
        self.label.classes(f'text-h6 text-{config["color"]} font-bold', remove='text-red-7 text-green-6 text-blue-6 text-orange-6 text-red-9')


class ProgressBar:
    """Barra de progreso para tareas."""
    
    def __init__(self, label: str = "Progreso", mostrar_tiempo: bool = True):
        """
        Inicializa la barra de progreso.
        
        Args:
            label: Etiqueta a mostrar
            mostrar_tiempo: Si mostrar tiempo estimado
        """
        self.label_text = label
        self.mostrar_tiempo = mostrar_tiempo
        self.progreso_actual = 0
        self.tiempo_restante = 0
        self._crear_componente()
    
    def _crear_componente(self):
        """Crea el componente visual."""
        with ui.card().classes('w-full'):
            with ui.row().classes('items-center justify-between w-full'):
                self.label = ui.label(self.label_text).classes('text-subtitle2')
                if self.mostrar_tiempo:
                    self.tiempo_label = ui.label("0s restantes").classes('text-caption text-grey-7')
            
            self.progress = ui.linear_progress(
                value=0,
                show_value=True,
                size='20px'
            ).classes('w-full')
    
    def actualizar(self, progreso: int, tiempo_restante: int = 0):
        """
        Actualiza la barra de progreso.
        
        Args:
            progreso: Progreso actual (0-100)
            tiempo_restante: Tiempo restante en segundos
        """
        self.progreso_actual = progreso
        self.tiempo_restante = tiempo_restante
        
        self.progress.value = progreso / 100
        
        if self.mostrar_tiempo and tiempo_restante > 0:
            mins, secs = divmod(tiempo_restante, 60)
            if mins > 0:
                self.tiempo_label.text = f"{mins}m {secs}s restantes"
            else:
                self.tiempo_label.text = f"{secs}s restantes"
    
    def reiniciar(self):
        """Reinicia la barra de progreso."""
        self.actualizar(0, 0)


class RecipeCard:
    """Tarjeta para mostrar una receta."""
    
    def __init__(self, receta: Receta, on_select: Callable, on_delete: Optional[Callable] = None):
        """
        Inicializa la tarjeta de receta.
        
        Args:
            receta: Receta a mostrar
            on_select: Callback al seleccionar
            on_delete: Callback al eliminar (opcional)
        """
        self.receta = receta
        self.on_select = on_select
        self.on_delete = on_delete
        self._crear_componente()
    
    def _crear_componente(self):
        """Crea el componente visual."""
        with ui.card().classes('w-full cursor-pointer hover:shadow-lg transition-shadow').on('click', lambda: self.on_select(self.receta)):
            # Header con nombre y badge de fábrica
            with ui.row().classes('items-center justify-between w-full'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('restaurant_menu', size='sm').classes('text-primary')
                    ui.label(self.receta.nombre).classes('text-h6 font-bold')
                
                if self.receta.es_fabrica:
                    ui.badge('Fábrica', color='blue').classes('text-xs')
            
            # Descripción
            ui.label(self.receta.descripcion).classes('text-caption text-grey-7 line-clamp-2')
            
            ui.separator()
            
            # Información de la receta
            with ui.row().classes('items-center gap-4 w-full text-sm'):
                with ui.row().classes('items-center gap-1'):
                    ui.icon('schedule', size='sm').classes('text-grey-6')
                    ui.label(self.receta.tiempo_str).classes('text-grey-8')
                
                with ui.row().classes('items-center gap-1'):
                    ui.icon('people', size='sm').classes('text-grey-6')
                    ui.label(f"{self.receta.porciones} porciones").classes('text-grey-8')
                
                with ui.row().classes('items-center gap-1'):
                    ui.icon('bar_chart', size='sm').classes('text-grey-6')
                    ui.label(self.receta.dificultad).classes('text-grey-8')
            
            # Botón de eliminar (solo para recetas de usuario)
            if not self.receta.es_fabrica and self.on_delete:
                ui.separator()
                with ui.row().classes('w-full justify-end'):
                    ui.button(
                        'Eliminar',
                        icon='delete',
                        color='red',
                        on_click=lambda e: self._confirmar_eliminar(e)
                    ).props('flat dense').classes('text-xs')
    
    def _confirmar_eliminar(self, event):
        """Muestra diálogo de confirmación para eliminar."""
        event.stopPropagation()
        
        with ui.dialog() as dialog, ui.card():
            ui.label('¿Eliminar receta?').classes('text-h6')
            ui.label(f'¿Está seguro de eliminar "{self.receta.nombre}"?').classes('text-body2')
            
            with ui.row().classes('w-full justify-end gap-2 mt-4'):
                ui.button('Cancelar', on_click=dialog.close).props('flat')
                ui.button(
                    'Eliminar',
                    color='red',
                    on_click=lambda: (self.on_delete(self.receta), dialog.close())
                )
        
        dialog.open()


class ParameterPanel:
    """Panel para mostrar parámetros de operación."""
    
    def __init__(self):
        """Inicializa el panel de parámetros."""
        self._crear_componente()
    
    def _crear_componente(self):
        """Crea el componente visual."""
        with ui.card().classes('w-full'):
            ui.label('Parámetros de Operación').classes('text-subtitle1 font-bold mb-2')
            
            with ui.grid(columns=2).classes('w-full gap-4'):
                # Temperatura
                with ui.column():
                    ui.label('Temperatura').classes('text-caption text-grey-7')
                    self.temp_label = ui.label('0°C').classes('text-h6 text-primary font-bold')
                
                # Velocidad
                with ui.column():
                    ui.label('Velocidad').classes('text-caption text-grey-7')
                    self.vel_label = ui.label('0/10').classes('text-h6 text-primary font-bold')
    
    def actualizar(self, temperatura: int, velocidad: int):
        """
        Actualiza los parámetros mostrados.
        
        Args:
            temperatura: Temperatura en °C
            velocidad: Velocidad (0-10)
        """
        self.temp_label.text = f'{temperatura}°C'
        self.vel_label.text = f'{velocidad}/10'


class TaskInfoCard:
    """Tarjeta de información de tarea actual."""
    
    def __init__(self):
        """Inicializa la tarjeta de información."""
        self._crear_componente()
    
    def _crear_componente(self):
        """Crea el componente visual."""
        with ui.card().classes('w-full'):
            ui.label('Tarea Actual').classes('text-subtitle1 font-bold mb-2')
            
            self.nombre_label = ui.label('Ninguna').classes('text-body1 text-grey-7')
            self.descripcion_label = ui.label('').classes('text-caption text-grey-6 mt-1')
    
    def actualizar(self, nombre: str, descripcion: str = ""):
        """
        Actualiza la información de la tarea.
        
        Args:
            nombre: Nombre de la tarea
            descripcion: Descripción de la tarea
        """
        self.nombre_label.text = nombre
        self.nombre_label.classes('text-body1 text-grey-9 font-medium', remove='text-grey-7')
        self.descripcion_label.text = descripcion
    
    def limpiar(self):
        """Limpia la información."""
        self.nombre_label.text = 'Ninguna'
        self.nombre_label.classes('text-body1 text-grey-7', remove='text-grey-9 font-medium')
        self.descripcion_label.text = ''


class RecipeStepIndicator:
    """Indicador de pasos de receta."""
    
    def __init__(self, total_pasos: int = 0):
        """
        Inicializa el indicador de pasos.
        
        Args:
            total_pasos: Total de pasos en la receta
        """
        self.total_pasos = total_pasos
        self.paso_actual = 0
        self._crear_componente()
    
    def _crear_componente(self):
        """Crea el componente visual."""
        self.container = ui.card().classes('w-full')
        with self.container:
            ui.label('Progreso de Receta').classes('text-subtitle1 font-bold mb-2')
            self.paso_label = ui.label('No hay receta en curso').classes('text-body2 text-grey-7')
    
    def actualizar(self, paso_actual: int, nombre_receta: str):
        """
        Actualiza el indicador.
        
        Args:
            paso_actual: Paso actual (0-indexed)
            nombre_receta: Nombre de la receta
        """
        self.paso_actual = paso_actual
        self.paso_label.text = f'{nombre_receta}: Paso {paso_actual + 1} de {self.total_pasos}'
        self.paso_label.classes('text-body2 text-primary font-medium', remove='text-grey-7')
    
    def establecer_total_pasos(self, total: int):
        """Establece el total de pasos."""
        self.total_pasos = total
    
    def limpiar(self):
        """Limpia el indicador."""
        self.paso_actual = 0
        self.paso_label.text = 'No hay receta en curso'
        self.paso_label.classes('text-body2 text-grey-7', remove='text-primary font-medium')