"""
INTERFAZ PRINCIPAL DEL ROBOT DE COCINA - v11.0
Paleta de colores optimizada y diálogo final funcional
"""

from nicegui import ui
from database.db_handler import DatabaseHandler
from models.robot import Robot, EstadoRobot
from models.receta import Receta, Ingrediente
from utils.exceptions import TareaInvalidaError
from models.controller import RobotController
import asyncio
import time


class MainInterface:
    OPERACIONES = {
        'corte': ['picar', 'trocear', 'rallar', 'triturar', 'laminar', 'dados', 'rodajas'],
        'temperatura': ['sofreir', 'hervir', 'vapor', 'calentar', 'freir', 'hornear', 'gratinar', 'escaldar', 'confitar', 'flamear'],
        'mecanica': ['amasar', 'mezclar', 'batir', 'remover', 'emulsionar', 'montar', 'incorporar', 'tamizar']
    }
    
    ICONOS_OPERACION = {
        'picar': '🔪', 'trocear': '🔪', 'rallar': '🧀', 'triturar': '🔪', 'laminar': '🔪',
        'dados': '🎲', 'rodajas': '⭕', 'sofreir': '🍳', 'hervir': '🫕', 'vapor': '💨',
        'calentar': '🔥', 'freir': '🍳', 'hornear': '🔥', 'gratinar': '🧀', 'escaldar': '♨️',
        'confitar': '🍯', 'flamear': '🔥', 'amasar': '🫓', 'mezclar': '🥄', 'batir': '🥚',
        'remover': '🥄', 'emulsionar': '🫗', 'montar': '🍦', 'incorporar': '➕', 'tamizar': '🕳️'
    }
    
    # Sistema de alérgenos
    ALERGENOS = {
        'gluten': {'icono': '🌾', 'nombre': 'Gluten', 'color': '#d97706',
                   'ingredientes': ['harina', 'pan', 'pasta', 'trigo', 'cebada', 'centeno', 'avena', 'sémola', 'cuscús']},
        'lactosa': {'icono': '🥛', 'nombre': 'Lácteos', 'color': '#0ea5e9',
                    'ingredientes': ['leche', 'nata', 'queso', 'mantequilla', 'yogur', 'crema', 'bechamel']},
        'huevo': {'icono': '🥚', 'nombre': 'Huevo', 'color': '#eab308',
                  'ingredientes': ['huevo', 'yema', 'clara', 'mayonesa']},
        'frutos_secos': {'icono': '🥜', 'nombre': 'Frutos Secos', 'color': '#92400e',
                         'ingredientes': ['almendra', 'nuez', 'avellana', 'pistacho', 'anacardo', 'cacahuete', 'piñon']},
        'pescado': {'icono': '🐟', 'nombre': 'Pescado', 'color': '#0284c7',
                    'ingredientes': ['merluza', 'salmon', 'bacalao', 'atun', 'anchoa', 'sardina', 'pescado']},
        'marisco': {'icono': '🦐', 'nombre': 'Marisco', 'color': '#dc2626',
                    'ingredientes': ['gamba', 'langostino', 'mejillon', 'almeja', 'calamar', 'pulpo', 'marisco']},
        'soja': {'icono': '🫘', 'nombre': 'Soja', 'color': '#65a30d',
                 'ingredientes': ['soja', 'tofu', 'edamame', 'salsa de soja']},
        'apio': {'icono': '🥬', 'nombre': 'Apio', 'color': '#16a34a',
                 'ingredientes': ['apio']},
        'mostaza': {'icono': '🟡', 'nombre': 'Mostaza', 'color': '#ca8a04',
                    'ingredientes': ['mostaza']},
        'sesamo': {'icono': '⚪', 'nombre': 'Sésamo', 'color': '#a3a3a3',
                   'ingredientes': ['sesamo', 'ajonjoli']},
    }
    
    INFO_NUTRICIONAL = {
        'tomate': {'calorias': 18, 'proteinas': 0.9, 'carbohidratos': 3.9, 'grasas': 0.2},
        'cebolla': {'calorias': 40, 'proteinas': 1.1, 'carbohidratos': 9, 'grasas': 0.1},
        'ajo': {'calorias': 149, 'proteinas': 6.4, 'carbohidratos': 33, 'grasas': 0.5},
        'zanahoria': {'calorias': 41, 'proteinas': 0.9, 'carbohidratos': 10, 'grasas': 0.2},
        'patata': {'calorias': 77, 'proteinas': 2, 'carbohidratos': 17, 'grasas': 0.1},
        'calabacín': {'calorias': 17, 'proteinas': 1.2, 'carbohidratos': 3.1, 'grasas': 0.3},
        'calabaza': {'calorias': 26, 'proteinas': 1, 'carbohidratos': 6.5, 'grasas': 0.1},
        'pimiento': {'calorias': 20, 'proteinas': 0.9, 'carbohidratos': 4.6, 'grasas': 0.2},
        'pepino': {'calorias': 16, 'proteinas': 0.7, 'carbohidratos': 3.6, 'grasas': 0.1},
        'berenjena': {'calorias': 25, 'proteinas': 1, 'carbohidratos': 6, 'grasas': 0.2},
        'puerro': {'calorias': 61, 'proteinas': 1.5, 'carbohidratos': 14, 'grasas': 0.3},
        'champiñon': {'calorias': 22, 'proteinas': 3.1, 'carbohidratos': 3.3, 'grasas': 0.3},
        'espinaca': {'calorias': 23, 'proteinas': 2.9, 'carbohidratos': 3.6, 'grasas': 0.4},
        'brocoli': {'calorias': 34, 'proteinas': 2.8, 'carbohidratos': 7, 'grasas': 0.4},
        'coliflor': {'calorias': 25, 'proteinas': 1.9, 'carbohidratos': 5, 'grasas': 0.3},
        'judias': {'calorias': 31, 'proteinas': 1.8, 'carbohidratos': 7, 'grasas': 0.1},
        'manzana': {'calorias': 52, 'proteinas': 0.3, 'carbohidratos': 14, 'grasas': 0.2},
        'limon': {'calorias': 29, 'proteinas': 1.1, 'carbohidratos': 9, 'grasas': 0.3},
        'pollo': {'calorias': 239, 'proteinas': 27, 'carbohidratos': 0, 'grasas': 14},
        'ternera': {'calorias': 250, 'proteinas': 26, 'carbohidratos': 0, 'grasas': 15},
        'cerdo': {'calorias': 242, 'proteinas': 27, 'carbohidratos': 0, 'grasas': 14},
        'carne': {'calorias': 250, 'proteinas': 26, 'carbohidratos': 0, 'grasas': 15},
        'merluza': {'calorias': 89, 'proteinas': 17, 'carbohidratos': 0, 'grasas': 2},
        'salmon': {'calorias': 208, 'proteinas': 20, 'carbohidratos': 0, 'grasas': 13},
        'pescado': {'calorias': 100, 'proteinas': 18, 'carbohidratos': 0, 'grasas': 3},
        'leche': {'calorias': 42, 'proteinas': 3.4, 'carbohidratos': 5, 'grasas': 1},
        'nata': {'calorias': 340, 'proteinas': 2, 'carbohidratos': 3, 'grasas': 35},
        'mantequilla': {'calorias': 717, 'proteinas': 0.9, 'carbohidratos': 0.1, 'grasas': 81},
        'queso': {'calorias': 402, 'proteinas': 25, 'carbohidratos': 1.3, 'grasas': 33},
        'huevo': {'calorias': 155, 'proteinas': 13, 'carbohidratos': 1.1, 'grasas': 11},
        'arroz': {'calorias': 130, 'proteinas': 2.7, 'carbohidratos': 28, 'grasas': 0.3},
        'pasta': {'calorias': 131, 'proteinas': 5, 'carbohidratos': 25, 'grasas': 1.1},
        'pan': {'calorias': 265, 'proteinas': 9, 'carbohidratos': 49, 'grasas': 3.2},
        'harina': {'calorias': 364, 'proteinas': 10, 'carbohidratos': 76, 'grasas': 1},
        'aceite': {'calorias': 884, 'proteinas': 0, 'carbohidratos': 0, 'grasas': 100},
        'azucar': {'calorias': 387, 'proteinas': 0, 'carbohidratos': 100, 'grasas': 0},
        'caldo': {'calorias': 10, 'proteinas': 1, 'carbohidratos': 1, 'grasas': 0.2},
        'vino': {'calorias': 85, 'proteinas': 0.1, 'carbohidratos': 2.6, 'grasas': 0},
        'agua': {'calorias': 0, 'proteinas': 0, 'carbohidratos': 0, 'grasas': 0},
    }
    
    CATEGORIAS = {
        'Todas': None, '⭐ Favoritas': 'favoritas',
        '🥣 Sopas y Cremas': ['Gazpacho', 'Sopa', 'Crema', 'Vichyssoise'],
        '🍝 Arroces y Pastas': ['Arroz', 'Risotto', 'Pasta'],
        '🍖 Carnes': ['Pollo', 'Ternera', 'Albóndigas'],
        '🐟 Pescados': ['Merluza', 'Salmón'],
        '🥖 Masas': ['Pan', 'Pizza', 'Bizcocho'],
        '🥗 Guarniciones': ['Puré', 'Verduras', 'Pisto'],
        '🍮 Postres': ['Natillas', 'Compota'],
    }

    def __init__(self, db: DatabaseHandler):
        self.db = db
        self.robot = Robot()
        self.controller = RobotController(self.robot)
        self._ejecutando = False
        self._velocidad_simulacion = 0.01
        self._tiempo_inicio = None
        self._exec_id = None
        self._porciones_actuales = 4
        self._modo_oscuro = False
        self._ultima_receta = None
        self._receta_completada_id = None
        self.robot.registrar_callback_estado(self._on_estado_changed)
        self.robot.registrar_callback_progreso(self._on_progreso_changed)
        self.robot.registrar_callback_evento(self._on_evento)

    def _calcular_nutricion(self, ingredientes, porciones_base, porciones_calc):
        factor = porciones_calc / porciones_base
        total = {'calorias': 0, 'proteinas': 0, 'carbohidratos': 0, 'grasas': 0}
        for ing in ingredientes:
            nombre_lower = ing.nombre.lower()
            for key, value in self.INFO_NUTRICIONAL.items():
                if key in nombre_lower:
                    cantidad_g = ing.cantidad
                    if ing.unidad == 'kg': cantidad_g *= 1000
                    elif ing.unidad in ('ml', 'l'): cantidad_g = ing.cantidad * (1000 if ing.unidad == 'l' else 1)
                    elif ing.unidad == 'unidad': cantidad_g = 100
                    elif ing.unidad in ('cucharada', 'cda'): cantidad_g = 15
                    elif ing.unidad == 'pizca': cantidad_g = 1
                    for k in total: total[k] += (value[k] / 100) * cantidad_g * factor
                    break
        for k in total: total[k] = round(total[k] / porciones_calc, 1)
        return total

    def _detectar_alergenos(self, ingredientes):
        """Detecta alérgenos presentes en una lista de ingredientes"""
        alergenos_detectados = []
        for ing in ingredientes:
            nombre_lower = ing.nombre.lower()
            for alergeno_key, alergeno_info in self.ALERGENOS.items():
                if alergeno_key not in [a['key'] for a in alergenos_detectados]:
                    for ingrediente_alergeno in alergeno_info['ingredientes']:
                        if ingrediente_alergeno in nombre_lower:
                            alergenos_detectados.append({
                                'key': alergeno_key,
                                'icono': alergeno_info['icono'],
                                'nombre': alergeno_info['nombre'],
                                'color': alergeno_info['color'],
                                'encontrado_en': ing.nombre
                            })
                            break
        return alergenos_detectados

    def create_ui(self):
        # CSS con paleta de colores optimizada
        ui.add_head_html('''<style>
            :root {
                --bg-body: #f0f2f5;
                --bg-card: #ffffff;
                --bg-card-alt: #f8f9fa;
                --bg-input: #ffffff;
                --text-primary: #212529;
                --text-secondary: #6c757d;
                --border-color: #dee2e6;
                --shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            body.dark-mode {
                --bg-body: #121212;
                --bg-card: #1e1e1e;
                --bg-card-alt: #2d2d2d;
                --bg-input: #2d2d2d;
                --text-primary: #e0e0e0;
                --text-secondary: #a0a0a0;
                --border-color: #404040;
                --shadow: 0 1px 3px rgba(0,0,0,0.3);
            }
            body { 
                background: var(--bg-body) !important; 
                color: var(--text-primary) !important;
                transition: background 0.3s, color 0.3s;
            }
            .nicegui-content { background: var(--bg-body) !important; }
            
            /* Cards */
            .q-card, .card-custom { 
                background: var(--bg-card) !important; 
                color: var(--text-primary) !important;
                border: 1px solid var(--border-color) !important;
                box-shadow: var(--shadow) !important;
            }
            
            /* Inputs y selects */
            .q-field__control { background: var(--bg-input) !important; }
            .q-field__native, .q-field__input, .q-select__dropdown-icon { color: var(--text-primary) !important; }
            .q-field__label { color: var(--text-secondary) !important; }
            .q-field--outlined .q-field__control:before { border-color: var(--border-color) !important; }
            .q-menu { background: var(--bg-card) !important; }
            .q-item { color: var(--text-primary) !important; }
            .q-item__label { color: var(--text-primary) !important; }
            
            /* Tabs */
            .q-tab__label { color: var(--text-primary) !important; }
            .q-tab-panels { background: var(--bg-card) !important; }
            
            /* Recipe cards */
            .recipe-card {
                background: var(--bg-card) !important;
                border: 1px solid var(--border-color) !important;
                transition: transform 0.2s, box-shadow 0.2s;
                cursor: pointer;
            }
            .recipe-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
            }
            
            /* Textos */
            .text-primary { color: var(--text-primary) !important; }
            .text-secondary { color: var(--text-secondary) !important; }
            
            /* Paso actual */
            .paso-actual { 
                background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; 
                border: none !important;
            }
            .paso-actual * { color: white !important; }
            .paso-completado { opacity: 0.5; }
            
            /* Dialogs */
            .q-dialog .q-card { 
                background: var(--bg-card) !important; 
                color: var(--text-primary) !important;
            }
            
            /* Botones profesionales */
            .btn-pro { 
                text-transform: none !important; 
                font-weight: 500 !important; 
                letter-spacing: 0 !important;
                border-radius: 6px !important;
            }
        </style>''')
        
        # Header
        with ui.header().style('background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);'):
            with ui.row().classes('w-full items-center justify-between px-4'):
                with ui.row().classes('items-center gap-3'):
                    ui.icon('precision_manufacturing', size='28px').style('color: #60a5fa;')
                    ui.label('Robot de Cocina').style('color: white; font-size: 1.2rem; font-weight: 600;')
                with ui.row().classes('items-center gap-2'):
                    ui.button(icon='history', on_click=self._mostrar_historial).props('flat round size=sm').style('color: white;').tooltip('Historial')
                    self.dark_toggle = ui.button(icon='dark_mode', on_click=self._toggle_modo_oscuro).props('flat round size=sm').style('color: white;')
                    ui.element('div').style('width: 1px; height: 20px; background: rgba(255,255,255,0.3); margin: 0 8px;')
                    ui.label('Velocidad:').style('color: rgba(255,255,255,0.7); font-size: 0.85rem;')
                    self.velocidad_select = ui.select(
                        {0.005: 'Lento', 0.01: 'Normal', 0.02: 'Rápido', 0.05: 'Ultra'}, 
                        value=0.01, 
                        on_change=self._cambiar_velocidad
                    ).props('dense dark outlined').style('width: 100px;')
                    ui.element('div').style('width: 1px; height: 20px; background: rgba(255,255,255,0.3); margin: 0 8px;')
                    self.header_icon = ui.icon('power_settings_new', size='20px').style('color: #ef4444;')
                    self.header_status = ui.label('Apagado').style('color: rgba(255,255,255,0.8); font-size: 0.85rem;')

        # Contenido principal
        with ui.column().classes('w-full p-4').style('max-width: 1600px; margin: 0 auto;'):
            # Dashboard
            with ui.row().classes('w-full gap-3 mb-4'):
                self._crear_dashboard_card('Estado', 'APAGADO', 'power_settings_new', '#6366f1')
                self._crear_dashboard_card('Receta', 'Ninguna', 'restaurant_menu', '#10b981')
                self._crear_dashboard_card('Progreso', '0%', 'donut_large', '#f59e0b')
                self._crear_dashboard_card('Tiempo', '--:--', 'schedule', '#8b5cf6')
            
            with ui.row().classes('w-full gap-4'):
                # Panel izquierdo - Control
                with ui.column().classes('gap-3').style('width: 280px;'):
                    self._crear_panel_control()
                    self.receta_activa_container = ui.column().classes('w-full')
                    self._crear_lista_pasos()
                
                # Panel central - Ejecución
                with ui.column().classes('gap-3').style('flex: 1; min-width: 400px;'):
                    self._crear_panel_ejecucion()
                
                # Panel derecho - Parámetros
                with ui.column().classes('gap-3').style('width: 250px;'):
                    self._crear_panel_parametros()
            
            # Tabs de recetas
            with ui.card().classes('w-full mt-4 card-custom'):
                with ui.tabs().classes('w-full') as tabs:
                    ui.tab('recetas', label='Recetas', icon='menu_book')
                    ui.tab('crear', label='Nueva Receta', icon='add_circle')
                with ui.tab_panels(tabs, value='recetas').classes('w-full'):
                    with ui.tab_panel('recetas'):
                        self._crear_explorador_recetas()
                    with ui.tab_panel('crear'):
                        self._crear_formulario_receta()
        
        self._actualizar_botones()

    def _toggle_modo_oscuro(self):
        self._modo_oscuro = not self._modo_oscuro
        if self._modo_oscuro:
            ui.run_javascript("document.body.classList.add('dark-mode')")
            self.dark_toggle.props('icon=light_mode')
        else:
            ui.run_javascript("document.body.classList.remove('dark-mode')")
            self.dark_toggle.props('icon=dark_mode')

    def _crear_dashboard_card(self, titulo, valor, icono, color):
        with ui.card().classes('flex-1 p-4').style(f'background: linear-gradient(135deg, {color}, {color}cc) !important; border: none !important; min-width: 140px;'):
            with ui.row().classes('w-full items-center justify-between'):
                with ui.column().classes('gap-0'):
                    ui.label(titulo).style('color: rgba(255,255,255,0.8); font-size: 0.75rem;')
                    label = ui.label(valor).style('color: white; font-size: 1.2rem; font-weight: 600;')
                ui.icon(icono, size='28px').style('color: rgba(255,255,255,0.4);')
        setattr(self, f'dash_{titulo.lower()}', label)

    def _crear_panel_control(self):
        with ui.card().classes('w-full p-4 card-custom'):
            ui.label('Control').classes('text-primary').style('font-weight: 600; margin-bottom: 12px;')
            with ui.row().classes('w-full gap-2 mb-3'):
                self.btn_encender = ui.button('Encender', on_click=self._encender_robot).classes('flex-1 btn-pro').props('color=positive no-caps')
                self.btn_apagar = ui.button('Apagar', on_click=self._apagar_robot).classes('flex-1 btn-pro').props('color=negative no-caps')
            ui.separator().style('background: var(--border-color);')
            self.btn_comenzar = ui.button('Iniciar Receta', icon='play_arrow', on_click=self._comenzar_receta).classes('w-full btn-pro mt-3').props('color=primary no-caps')
            with ui.row().classes('w-full gap-2 mt-2'):
                self.btn_pausar = ui.button('Pausar', on_click=self._pausar_robot).classes('flex-1 btn-pro').props('color=warning no-caps outline')
                self.btn_reanudar = ui.button('Reanudar', on_click=self._reanudar_robot).classes('flex-1 btn-pro').props('color=positive no-caps outline')
            self.btn_cancelar = ui.button('Cancelar', on_click=self._cancelar_receta).classes('w-full btn-pro mt-2').props('no-caps flat')
            ui.separator().style('background: var(--border-color);').classes('my-2')
            self.btn_emergencia = ui.button('Parada de Emergencia', icon='warning', on_click=self._confirmar_emergencia).classes('w-full btn-pro').props('color=negative no-caps outline')

    def _crear_lista_pasos(self):
        with ui.card().classes('w-full p-4 card-custom'):
            ui.label('Pasos').classes('text-primary').style('font-weight: 600; margin-bottom: 12px;')
            self.lista_pasos_container = ui.column().classes('w-full gap-2')
            with self.lista_pasos_container:
                ui.label('Selecciona una receta').classes('text-secondary').style('font-size: 0.85rem;')

    def _actualizar_lista_pasos(self):
        self.lista_pasos_container.clear()
        if not self.robot.receta_actual:
            with self.lista_pasos_container:
                ui.label('Selecciona una receta').classes('text-secondary').style('font-size: 0.85rem;')
            return
        pasos = self.robot.receta_actual.pasos
        pa = self.robot.paso_actual
        estado = self.robot.estado
        with self.lista_pasos_container:
            for i, paso in enumerate(pasos):
                op = paso.get('operacion', paso.get('nombre', 'Paso'))
                icono = self.ICONOS_OPERACION.get(op.lower(), '📌')
                duracion = paso.get('duracion', 0)
                m, s = divmod(duracion, 60)
                tiempo_str = f'{m}:{s:02d}' if m else f'{s}s'
                
                if estado in (EstadoRobot.EJECUTANDO, EstadoRobot.PAUSADO):
                    if i < pa:
                        clase, indicador = 'paso-completado', '✓'
                    elif i == pa:
                        clase, indicador = 'paso-actual', '▶' if estado == EstadoRobot.EJECUTANDO else '❚❚'
                    else:
                        clase, indicador = '', str(i + 1)
                elif estado == EstadoRobot.FINALIZADO:
                    clase, indicador = 'paso-completado', '✓'
                else:
                    clase, indicador = '', str(i + 1)
                
                with ui.card().classes(f'w-full p-2 card-custom {clase}'):
                    with ui.row().classes('items-center gap-2 w-full'):
                        ui.badge(indicador).props('color=grey' if clase != 'paso-actual' else 'color=white')
                        ui.label(f'{icono} {op.title()}').classes('text-primary').style('flex: 1; font-size: 0.85rem;')
                        ui.label(tiempo_str).classes('text-secondary').style('font-size: 0.75rem;')

    def _crear_panel_ejecucion(self):
        with ui.card().classes('w-full p-4 card-custom'):
            ui.label('Paso Actual').classes('text-primary').style('font-weight: 600; margin-bottom: 12px;')
            self.paso_container = ui.column().classes('w-full')
            with self.paso_container:
                self._mostrar_esperando()
        
        with ui.card().classes('w-full p-4 card-custom'):
            ui.label('Progreso General').classes('text-primary').style('font-weight: 600; margin-bottom: 12px;')
            with ui.row().classes('w-full items-center justify-between'):
                self.progreso_texto = ui.label('0 de 0 pasos').classes('text-secondary')
                self.recipe_progress_label = ui.label('0%').style('font-size: 1.1rem; font-weight: 600; color: #10b981;')
            self.recipe_progress = ui.linear_progress(value=0, show_value=False).props('color=positive').classes('w-full')
            with ui.row().classes('w-full items-center justify-between mt-3'):
                self.tiempo_transcurrido = ui.label('Transcurrido: --:--').classes('text-secondary').style('font-size: 0.8rem;')
                self.tiempo_restante_label = ui.label('Restante: --:--').classes('text-secondary').style('font-size: 0.8rem;')

    def _mostrar_esperando(self):
        with ui.column().classes('items-center justify-center w-full p-8').style('background: var(--bg-card-alt); border-radius: 8px;'):
            ui.icon('hourglass_empty', size='40px').style('color: var(--text-secondary);')
            ui.label('En espera').classes('text-secondary').style('margin-top: 8px;')

    def _crear_panel_parametros(self):
        with ui.card().classes('w-full p-4 card-custom'):
            ui.label('Parámetros').classes('text-primary').style('font-weight: 600; margin-bottom: 12px;')
            
            with ui.card().classes('w-full p-3 card-custom mb-2'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('thermostat', size='20px').style('color: #ef4444;')
                        ui.label('Temperatura').classes('text-primary').style('font-size: 0.85rem;')
                    self.temp_display = ui.label('0°C').style('font-size: 1.1rem; font-weight: 600; color: #ef4444;')
            
            with ui.card().classes('w-full p-3 card-custom mb-2'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('speed', size='20px').style('color: #3b82f6;')
                        ui.label('Velocidad').classes('text-primary').style('font-size: 0.85rem;')
                    self.vel_display = ui.label('0').style('font-size: 1.1rem; font-weight: 600; color: #3b82f6;')
            
            with ui.card().classes('w-full p-3 card-custom'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('timer', size='20px').style('color: #10b981;')
                        ui.label('Tiempo Paso').classes('text-primary').style('font-size: 0.85rem;')
                    self.time_display = ui.label('--:--').style('font-size: 1.1rem; font-weight: 600; color: #10b981;')
                self.paso_progress = ui.linear_progress(value=0, show_value=False).props('color=teal').classes('w-full mt-2')

    def _actualizar_indicadores(self, temp, vel):
        self.temp_display.set_text(f'{temp}°C')
        self.vel_display.set_text(str(vel))

    # ==================== EXPLORADOR DE RECETAS ====================
    
    def _crear_explorador_recetas(self):
        with ui.column().classes('w-full gap-4 p-2'):
            with ui.row().classes('w-full items-center gap-3 flex-wrap'):
                self.search_input = ui.input(placeholder='Buscar recetas...').props('outlined dense').style('flex: 1; min-width: 200px;')
                self.search_input.on('keyup', self._filtrar_recetas)
                self.filtro_categoria = ui.select(list(self.CATEGORIAS.keys()), value='Todas', label='Categoría', on_change=self._filtrar_recetas).props('outlined dense').style('width: 150px;')
                self.filtro_dificultad = ui.select(['Todas', 'Fácil', 'Media', 'Difícil'], value='Todas', label='Dificultad', on_change=self._filtrar_recetas).props('outlined dense').style('width: 120px;')
                self.filtro_tiempo = ui.select(['Todos', '< 15 min', '15-30 min', '> 30 min'], value='Todos', label='Tiempo', on_change=self._filtrar_recetas).props('outlined dense').style('width: 120px;')
            self.recipe_grid = ui.row().classes('w-full gap-3').style('flex-wrap: wrap;')
            self._cargar_recetas()

    def _cargar_recetas(self):
        self.recipe_grid.clear()
        self._favoritos_ids = self.db.get_favorite_ids()
        with self.recipe_grid:
            for r in self.db.get_all_recipes():
                self._crear_card_receta(r)

    def _filtrar_recetas(self, e=None):
        self.recipe_grid.clear()
        self._favoritos_ids = self.db.get_favorite_ids()
        cat = self.filtro_categoria.value
        if cat == '⭐ Favoritas':
            recetas = self.db.get_favorites()
        else:
            recetas = self.db.get_all_recipes()
            if cat != 'Todas':
                kw = self.CATEGORIAS.get(cat, [])
                if kw:
                    recetas = [r for r in recetas if any(k.lower() in r.nombre.lower() for k in kw)]
        busq = (self.search_input.value or '').lower()
        if busq:
            recetas = [r for r in recetas if busq in r.nombre.lower() or busq in r.descripcion.lower()]
        dif = self.filtro_dificultad.value
        if dif != 'Todas':
            recetas = [r for r in recetas if r.dificultad == dif]
        tiempo = self.filtro_tiempo.value
        if tiempo == '< 15 min':
            recetas = [r for r in recetas if r.tiempo_total < 900]
        elif tiempo == '15-30 min':
            recetas = [r for r in recetas if 900 <= r.tiempo_total <= 1800]
        elif tiempo == '> 30 min':
            recetas = [r for r in recetas if r.tiempo_total > 1800]
        with self.recipe_grid:
            if not recetas:
                ui.label('No se encontraron recetas').classes('text-secondary')
            else:
                for r in recetas:
                    self._crear_card_receta(r)

    def _crear_card_receta(self, receta):
        colores = {'Fácil': '#10b981', 'Media': '#f59e0b', 'Difícil': '#ef4444'}
        color = colores.get(receta.dificultad, '#6366f1')
        n = receta.nombre.lower()
        if any(x in n for x in ['sopa', 'crema', 'gazpacho', 'vichyssoise']): icono = '🥣'
        elif any(x in n for x in ['arroz', 'risotto', 'pasta']): icono = '🍝'
        elif any(x in n for x in ['pollo', 'ternera', 'albóndigas']): icono = '🍖'
        elif any(x in n for x in ['merluza', 'salmón']): icono = '🐟'
        elif any(x in n for x in ['pan', 'pizza', 'bizcocho']): icono = '🥖'
        elif any(x in n for x in ['natillas', 'compota']): icono = '🍮'
        elif any(x in n for x in ['puré', 'verduras', 'pisto']): icono = '🥗'
        else: icono = '🍽️'
        
        es_fav = receta.id in self._favoritos_ids
        notas = self.db.get_notes(receta.id)
        
        with ui.card().classes('p-3 recipe-card').style(f'width: 250px; border-left: 3px solid {color} !important;').on('click', lambda r=receta: self._mostrar_detalle_receta(r)):
            with ui.row().classes('w-full items-center gap-2 mb-2'):
                ui.label(icono).style('font-size: 1.2rem;')
                ui.label(receta.nombre).classes('text-primary').style('font-weight: 600; flex: 1; font-size: 0.9rem;')
                if len(notas) > 0:
                    ui.icon('note', size='14px').style('color: var(--text-secondary);')
                if es_fav:
                    ui.icon('star', size='14px').style('color: #f59e0b;')
            desc = receta.descripcion[:40] + '...' if len(receta.descripcion) > 40 else receta.descripcion
            ui.label(desc).classes('text-secondary').style('font-size: 0.8rem; min-height: 24px;')
            with ui.row().classes('w-full items-center justify-between mt-2'):
                ui.label(f'{receta.tiempo_str} · {receta.num_pasos} pasos').classes('text-secondary').style('font-size: 0.75rem;')
                ui.badge(receta.dificultad).style(f'background: {color}; color: white; font-size: 0.65rem;')

    def _mostrar_detalle_receta(self, receta):
        es_fav = self.db.is_favorite(receta.id)
        notas = self.db.get_notes(receta.id)
        alergenos = self._detectar_alergenos(receta.ingredientes)
        
        with ui.dialog() as dialog, ui.card().classes('p-0').style('width: 600px; max-width: 95vw; max-height: 90vh; overflow-y: auto;'):
            # Header
            with ui.row().classes('w-full items-center justify-between p-4').style('background: linear-gradient(135deg, #1e3a5f, #0d1b2a);'):
                with ui.column().classes('gap-0'):
                    with ui.row().classes('items-center gap-2'):
                        ui.label(receta.nombre).style('font-size: 1.1rem; font-weight: 600; color: white;')
                        if es_fav:
                            ui.icon('star', size='18px').style('color: #f59e0b;')
                    ui.label(f'{receta.dificultad} · {receta.tiempo_str} · {receta.porciones} porciones').style('color: rgba(255,255,255,0.7); font-size: 0.8rem;')
                ui.button(icon='close', on_click=dialog.close).props('flat round size=sm').style('color: white;')
            
            with ui.column().classes('p-4 gap-3'):
                ui.label(receta.descripcion).classes('text-secondary')
                
                # Alérgenos detectados
                if alergenos:
                    with ui.card().classes('w-full p-3 card-custom').style('border: 1px solid #f59e0b !important;'):
                        ui.label('⚠️ Alérgenos detectados').classes('text-primary').style('font-weight: 600; font-size: 0.85rem; margin-bottom: 8px;')
                        with ui.row().classes('gap-2 flex-wrap'):
                            for a in alergenos:
                                with ui.row().classes('items-center gap-1 p-1 px-2').style(f'background: {a["color"]}22; border-radius: 4px; border: 1px solid {a["color"]};'):
                                    ui.label(a['icono']).style('font-size: 0.9rem;')
                                    ui.label(a['nombre']).style(f'font-size: 0.75rem; color: {a["color"]}; font-weight: 500;')
                
                # Notas existentes
                if notas:
                    with ui.card().classes('w-full p-3 card-custom'):
                        ui.label(f'📝 Notas ({len(notas)})').classes('text-primary').style('font-weight: 600; font-size: 0.85rem; margin-bottom: 8px;')
                        for nota in notas:
                            with ui.row().classes('w-full items-start gap-2 p-2').style('background: var(--bg-card-alt); border-radius: 4px; margin-bottom: 4px;'):
                                with ui.column().classes('flex-1 gap-0'):
                                    ui.label(nota['nota']).classes('text-primary').style('font-size: 0.85rem;')
                                    fecha = nota['fecha'][:10] if nota.get('fecha') else ''
                                    ui.label(fecha).classes('text-secondary').style('font-size: 0.7rem;')
                                ui.button(icon='delete', on_click=lambda n=nota: (self.db.delete_note(n['id']), dialog.close(), self._mostrar_detalle_receta(self.db.get_recipe_by_id(receta.id)))).props('flat round size=xs color=negative')
                
                # Porciones
                with ui.card().classes('w-full p-3 card-custom'):
                    with ui.row().classes('w-full items-center gap-3'):
                        ui.label('🍽️ Porciones:').classes('text-primary').style('font-weight: 500;')
                        porciones_input = ui.number(value=receta.porciones, min=1, max=20).props('outlined dense').style('width: 80px;')
                
                # Ingredientes
                with ui.card().classes('w-full p-3 card-custom'):
                    ui.label('🥗 Ingredientes').classes('text-primary').style('font-weight: 600; font-size: 0.85rem; margin-bottom: 8px;')
                    ingredientes_container = ui.row().classes('gap-2 flex-wrap')
                    
                    def actualizar_ingredientes():
                        factor = (porciones_input.value or receta.porciones) / receta.porciones
                        ingredientes_container.clear()
                        with ingredientes_container:
                            for ing in receta.ingredientes:
                                nc = ing.cantidad * factor
                                cs = str(int(nc)) if nc == int(nc) else f'{nc:.1f}'
                                ui.badge(f'{cs} {ing.unidad} {ing.nombre}').props('outline color=grey')
                    
                    actualizar_ingredientes()
                    porciones_input.on('change', actualizar_ingredientes)
                    
                    # Info nutricional toggle
                    nutricion_container = ui.column().classes('w-full mt-2')
                    nutricion_visible = [False]
                    
                    def toggle_nutricion():
                        nutricion_visible[0] = not nutricion_visible[0]
                        nutricion_container.clear()
                        if nutricion_visible[0]:
                            porc = int(porciones_input.value or receta.porciones)
                            info = self._calcular_nutricion(receta.ingredientes, receta.porciones, porc)
                            with nutricion_container:
                                with ui.row().classes('w-full gap-4 p-3').style('background: var(--bg-card-alt); border-radius: 4px;'):
                                    for val, label, color in [(info["calorias"], 'kcal', '#ef4444'), (f'{info["proteinas"]}g', 'prot', '#3b82f6'), (f'{info["carbohidratos"]}g', 'carbs', '#f59e0b'), (f'{info["grasas"]}g', 'grasas', '#8b5cf6')]:
                                        with ui.column().classes('items-center'):
                                            ui.label(str(val)).style(f'font-size: 1rem; font-weight: 600; color: {color};')
                                            ui.label(label).classes('text-secondary').style('font-size: 0.7rem;')
                    
                    ui.button('Ver info nutricional', icon='analytics', on_click=toggle_nutricion).props('flat dense no-caps').classes('mt-2')
                
                # Pasos
                with ui.card().classes('w-full p-3 card-custom'):
                    ui.label('📋 Pasos').classes('text-primary').style('font-weight: 600; font-size: 0.85rem; margin-bottom: 8px;')
                    for i, p in enumerate(receta.pasos, 1):
                        op = p.get('operacion', p.get('nombre', 'Paso'))
                        ic = self.ICONOS_OPERACION.get(op.lower(), '📌')
                        with ui.row().classes('items-start gap-2 mb-2 p-2').style('background: var(--bg-card-alt); border-radius: 4px;'):
                            ui.badge(str(i)).props('color=primary')
                            with ui.column().classes('gap-0 flex-1'):
                                ui.label(f'{ic} {op.title()}').classes('text-primary').style('font-weight: 500; font-size: 0.9rem;')
                                if p.get('descripcion'):
                                    ui.label(p['descripcion']).classes('text-secondary').style('font-size: 0.8rem;')
                                info_parts = []
                                if p.get('duracion'):
                                    m, s = divmod(p['duracion'], 60)
                                    info_parts.append(f"{m}:{s:02d}" if m else f"{s}s")
                                if p.get('temperatura'):
                                    info_parts.append(f"{p['temperatura']}°C")
                                if p.get('velocidad'):
                                    info_parts.append(f"Vel.{p['velocidad']}")
                                if info_parts:
                                    ui.label(' · '.join(info_parts)).classes('text-secondary').style('font-size: 0.75rem;')
                
                # Añadir nota
                with ui.card().classes('w-full p-3 card-custom'):
                    ui.label('📝 Añadir Nota').classes('text-primary').style('font-weight: 600; font-size: 0.85rem; margin-bottom: 8px;')
                    nueva_nota = ui.input(placeholder='Escribe una nota...').props('outlined dense').classes('w-full')
                    
                    def guardar_nota():
                        if nueva_nota.value and nueva_nota.value.strip():
                            self.db.add_note(receta.id, nueva_nota.value.strip())
                            ui.notify('Nota guardada', type='positive')
                            dialog.close()
                            self._mostrar_detalle_receta(self.db.get_recipe_by_id(receta.id))
                            self._cargar_recetas()
                    
                    ui.button('Guardar Nota', icon='save', on_click=guardar_nota).props('flat dense no-caps color=primary').classes('mt-2')
                
                # Acciones
                with ui.row().classes('w-full justify-between mt-2'):
                    with ui.row().classes('gap-1'):
                        ui.button(icon='star' if es_fav else 'star_border', on_click=lambda: (self._toggle_favorito(receta), dialog.close())).props('flat round')
                        if receta.es_fabrica:
                            ui.button(icon='content_copy', on_click=lambda: self._duplicar_receta(receta, dialog)).props('flat round')
                        if not receta.es_fabrica:
                            ui.button(icon='edit', on_click=lambda: (dialog.close(), self._editar_receta(receta))).props('flat round')
                            ui.button(icon='delete', on_click=lambda: self._eliminar_receta(receta, dialog)).props('flat round color=negative')
                    with ui.row().classes('gap-2'):
                        ui.button('Cerrar', on_click=dialog.close).props('flat no-caps')
                        
                        def preparar():
                            self._porciones_actuales = int(porciones_input.value or receta.porciones)
                            dialog.close()
                            self._preparar_receta(receta)
                        
                        ui.button('Preparar', icon='play_arrow', on_click=preparar).props('color=positive no-caps')
        dialog.open()

    def _toggle_favorito(self, receta):
        if receta.id in self._favoritos_ids:
            self.db.remove_favorite(receta.id)
            ui.notify('Quitada de favoritos', type='info')
        else:
            self.db.add_favorite(receta.id)
            ui.notify('Añadida a favoritos', type='positive')
        self._cargar_recetas()

    def _duplicar_receta(self, receta, parent):
        with ui.dialog() as d, ui.card().classes('p-4 card-custom'):
            ui.label('Duplicar Receta').classes('text-primary').style('font-weight: 600;')
            nombre_input = ui.input(label='Nombre', value=f'{receta.nombre} (copia)').props('outlined dense').classes('w-full mt-2')
            with ui.row().classes('justify-end gap-2 mt-3'):
                ui.button('Cancelar', on_click=d.close).props('flat no-caps')
                def dup():
                    self.db.duplicate_recipe(receta.id, nombre_input.value)
                    ui.notify('Receta duplicada', type='positive')
                    d.close()
                    parent.close()
                    self._cargar_recetas()
                ui.button('Duplicar', on_click=dup).props('color=primary no-caps')
        d.open()

    def _eliminar_receta(self, receta, parent):
        with ui.dialog() as d, ui.card().classes('p-4 card-custom'):
            ui.label(f'¿Eliminar "{receta.nombre}"?').classes('text-primary').style('font-weight: 600;')
            ui.label('Esta acción no se puede deshacer.').classes('text-secondary').style('font-size: 0.85rem;')
            with ui.row().classes('justify-end gap-2 mt-3'):
                ui.button('Cancelar', on_click=d.close).props('flat no-caps')
                def si():
                    self.db.delete_user_recipe(receta.id)
                    ui.notify('Receta eliminada', type='warning')
                    d.close()
                    parent.close()
                    self._cargar_recetas()
                ui.button('Eliminar', on_click=si).props('color=negative no-caps')
        d.open()

    def _editar_receta(self, receta):
        with ui.dialog() as dialog, ui.card().classes('p-4 card-custom').style('width: 800px; max-width: 95vw; max-height: 90vh; overflow-y: auto;'):
            ui.label(f'Editar: {receta.nombre}').classes('text-primary').style('font-size: 1.1rem; font-weight: 600;')
            with ui.row().classes('w-full gap-4 mt-3'):
                with ui.column().classes('gap-3').style('flex: 1;'):
                    edit_nombre = ui.input(label='Nombre', value=receta.nombre).props('outlined dense').classes('w-full')
                    edit_desc = ui.textarea(label='Descripción', value=receta.descripcion).props('outlined dense').classes('w-full')
                    with ui.row().classes('gap-3'):
                        edit_porc = ui.number(label='Porciones', value=receta.porciones, min=1).props('outlined dense').style('flex: 1;')
                        edit_dif = ui.select(['Fácil', 'Media', 'Difícil'], value=receta.dificultad, label='Dificultad').props('outlined dense').style('flex: 1;')
                    ui.label('Ingredientes').classes('text-primary').style('font-weight: 600; font-size: 0.85rem;')
                    edit_ings = ui.column().classes('w-full gap-1')
                    
                    def add_ing(n='', c=0, u='g'):
                        with edit_ings:
                            with ui.row().classes('w-full gap-2 items-center') as r:
                                r.nombre = ui.input(value=n).props('outlined dense').style('flex: 1;')
                                r.cantidad = ui.number(value=c, min=0).props('outlined dense').style('width: 70px;')
                                r.unidad = ui.select(['g', 'kg', 'ml', 'l', 'unidad', 'cda', 'pizca'], value=u).props('outlined dense').style('width: 90px;')
                                ui.button(icon='delete', on_click=lambda x=r: x.delete()).props('flat round size=sm color=negative')
                    
                    for ing in receta.ingredientes:
                        add_ing(ing.nombre, ing.cantidad, ing.unidad)
                    ui.button('+ Ingrediente', on_click=lambda: add_ing()).props('flat dense no-caps color=primary')
                
                with ui.column().classes('gap-3').style('flex: 1;'):
                    ui.label('Pasos').classes('text-primary').style('font-weight: 600; font-size: 0.85rem;')
                    edit_pasos = ui.column().classes('w-full gap-2')
                    
                    def add_paso(t='corte', op='picar', dur=60, temp=0, vel=5, desc=''):
                        with edit_pasos:
                            with ui.card().classes('w-full p-2 card-custom') as c:
                                with ui.row().classes('justify-between items-center'):
                                    ui.label('Paso').classes('text-primary').style('font-weight: 500; font-size: 0.85rem;')
                                    ui.button(icon='delete', on_click=lambda x=c: x.delete()).props('flat round size=sm color=negative')
                                with ui.row().classes('gap-2'):
                                    c.tipo = ui.select(['corte', 'temperatura', 'mecanica'], value=t).props('outlined dense').style('width: 100px;')
                                    todas_ops = self.OPERACIONES['corte'] + self.OPERACIONES['temperatura'] + self.OPERACIONES['mecanica']
                                    c.operacion = ui.select(todas_ops, value=op).props('outlined dense').style('flex: 1;')
                                with ui.row().classes('gap-2'):
                                    c.duracion = ui.number(label='Seg', value=dur, min=1).props('outlined dense').style('flex: 1;')
                                    c.temperatura = ui.number(label='°C', value=temp).props('outlined dense').style('flex: 1;')
                                    c.velocidad = ui.number(label='Vel', value=vel, min=1, max=10).props('outlined dense').style('flex: 1;')
                                c.descripcion = ui.input(value=desc, placeholder='Descripción').props('outlined dense').classes('w-full')
                    
                    for p in receta.pasos:
                        add_paso(p.get('tipo', 'corte'), p.get('operacion', 'picar'), p.get('duracion', 60), p.get('temperatura', 0), p.get('velocidad', 5), p.get('descripcion', ''))
                    ui.button('+ Paso', on_click=lambda: add_paso()).props('flat dense no-caps color=primary')
            
            with ui.row().classes('w-full justify-end gap-2 mt-4'):
                ui.button('Cancelar', on_click=dialog.close).props('flat no-caps')
                
                def guardar():
                    ings = [Ingrediente(r.nombre.value, float(r.cantidad.value or 0), r.unidad.value) for r in edit_ings.default_slot.children if hasattr(r, 'nombre') and r.nombre.value]
                    pasos, tiempo = [], 0
                    for c in edit_pasos.default_slot.children:
                        if hasattr(c, 'tipo'):
                            p = {'tipo': c.tipo.value, 'operacion': c.operacion.value, 'duracion': int(c.duracion.value or 60), 'temperatura': int(c.temperatura.value or 0), 'velocidad': int(c.velocidad.value or 5), 'descripcion': c.descripcion.value or ''}
                            if p['tipo'] == 'mecanica':
                                p['nombre'] = p['operacion'].title()
                            pasos.append(p)
                            tiempo += p['duracion']
                    if not edit_nombre.value or not ings or not pasos:
                        ui.notify('Completa todos los campos', type='negative')
                        return
                    receta.nombre = edit_nombre.value
                    receta.descripcion = edit_desc.value
                    receta.porciones = int(edit_porc.value or 4)
                    receta.dificultad = edit_dif.value
                    receta.ingredientes = ings
                    receta.pasos = pasos
                    receta.tiempo_total = tiempo
                    self.db.update_recipe(receta)
                    ui.notify('Receta actualizada', type='positive')
                    dialog.close()
                    self._cargar_recetas()
                
                ui.button('Guardar', icon='save', on_click=guardar).props('color=primary no-caps')
        dialog.open()

    # ==================== HISTORIAL Y ESTADÍSTICAS ====================
    
    def _mostrar_historial(self):
        historial = self.db.get_history(limit=30)
        with ui.dialog() as dialog, ui.card().classes('p-4 card-custom').style('width: 450px; max-width: 95vw;'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Historial de Recetas').classes('text-primary').style('font-size: 1.1rem; font-weight: 600;')
                ui.button(icon='close', on_click=dialog.close).props('flat round size=sm')
            if not historial:
                ui.label('No hay ejecuciones registradas').classes('text-secondary').style('padding: 20px;')
            else:
                with ui.column().classes('w-full gap-2').style('max-height: 60vh; overflow-y: auto;'):
                    for h in historial:
                        col = '#10b981' if h['completada'] else '#ef4444'
                        ic = 'check_circle' if h['completada'] else 'cancel'
                        with ui.row().classes('w-full items-center p-2').style(f'border-left: 3px solid {col}; background: var(--bg-card-alt); border-radius: 4px;'):
                            ui.icon(ic, size='18px').style(f'color: {col};')
                            with ui.column().classes('flex-1 gap-0 ml-2'):
                                ui.label(h['receta_nombre']).classes('text-primary').style('font-weight: 500; font-size: 0.9rem;')
                                fecha = h['fecha_inicio'][:16].replace('T', ' ') if h['fecha_inicio'] else ''
                                ui.label(fecha).classes('text-secondary').style('font-size: 0.7rem;')
            with ui.row().classes('w-full justify-between mt-4'):
                ui.button('Limpiar', icon='delete', on_click=lambda: (self.db.clear_history(), ui.notify('Historial limpiado'), dialog.close())).props('flat no-caps color=negative')
                ui.button('Cerrar', on_click=dialog.close).props('flat no-caps')
        dialog.open()

    def _mostrar_estadisticas(self):
        stats = self.db.get_stats()
        with ui.dialog() as dialog, ui.card().classes('p-4 card-custom').style('width: 400px;'):
            ui.label('Estadísticas').classes('text-primary').style('font-size: 1.1rem; font-weight: 600; margin-bottom: 16px;')
            with ui.row().classes('w-full gap-3'):
                for bg, val, label in [('#6366f1', stats['total_ejecuciones'], 'Ejecuciones'), ('#10b981', f'{stats["tasa_exito"]}%', 'Éxito'), ('#3b82f6', stats['recetas_unicas'], 'Recetas')]:
                    with ui.card().classes('flex-1 p-3').style(f'background: {bg} !important; border: none !important;'):
                        ui.label(str(val)).style('font-size: 1.4rem; font-weight: 600; color: white;')
                        ui.label(label).style('font-size: 0.7rem; color: rgba(255,255,255,0.7);')
            t = stats['tiempo_total_segundos']
            h, r = divmod(t, 3600)
            m = r // 60
            with ui.card().classes('w-full p-3 mt-3 card-custom'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('timer', size='20px').style('color: var(--text-secondary);')
                    ui.label(f'Tiempo total: {h}h {m}m' if h else f'Tiempo total: {m} min').classes('text-primary')
            if stats['receta_favorita']:
                with ui.card().classes('w-full p-3 mt-2 card-custom'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('emoji_events', size='20px').style('color: #f59e0b;')
                        ui.label(f'Más cocinada: {stats["receta_favorita"]["receta_nombre"]} ({stats["receta_favorita"]["veces"]}x)').classes('text-primary')
            ui.button('Cerrar', on_click=dialog.close).props('flat no-caps').classes('w-full mt-4')
        dialog.open()

    # ==================== CREAR RECETA ====================
    
    def _crear_formulario_receta(self):
        with ui.column().classes('w-full gap-4 p-2'):
            ui.label('Nueva Receta').classes('text-primary').style('font-size: 1.1rem; font-weight: 600;')
            with ui.row().classes('w-full gap-4'):
                with ui.column().classes('gap-3').style('flex: 1;'):
                    with ui.card().classes('w-full p-4 card-custom'):
                        ui.label('Información').classes('text-primary').style('font-weight: 600; font-size: 0.85rem; margin-bottom: 8px;')
                        self.new_nombre = ui.input(label='Nombre').props('outlined dense').classes('w-full')
                        self.new_descripcion = ui.textarea(label='Descripción').props('outlined dense').classes('w-full')
                        with ui.row().classes('gap-3'):
                            self.new_porciones = ui.number(label='Porciones', value=4, min=1).props('outlined dense').style('flex: 1;')
                            self.new_dificultad = ui.select(['Fácil', 'Media', 'Difícil'], value='Media', label='Dificultad').props('outlined dense').style('flex: 1;')
                    
                    # Selector de alérgenos
                    with ui.card().classes('w-full p-4 card-custom'):
                        ui.label('Alérgenos').classes('text-primary').style('font-weight: 600; font-size: 0.85rem; margin-bottom: 8px;')
                        ui.label('Marca los alérgenos presentes en la receta:').classes('text-secondary').style('font-size: 0.75rem; margin-bottom: 8px;')
                        self.alergenos_checkboxes = {}
                        with ui.row().classes('gap-2 flex-wrap'):
                            for key, info in self.ALERGENOS.items():
                                with ui.row().classes('items-center gap-1'):
                                    cb = ui.checkbox(f'{info["icono"]} {info["nombre"]}').props('dense')
                                    self.alergenos_checkboxes[key] = cb
                    
                    with ui.card().classes('w-full p-4 card-custom'):
                        with ui.row().classes('justify-between items-center mb-2'):
                            ui.label('Ingredientes').classes('text-primary').style('font-weight: 600; font-size: 0.85rem;')
                            ui.button(icon='add', on_click=self._add_ingrediente).props('flat round size=sm color=primary')
                        self.ingredientes_container = ui.column().classes('w-full gap-2')
                        for _ in range(3):
                            self._add_ingrediente()
                with ui.column().classes('gap-3').style('flex: 1;'):
                    with ui.card().classes('w-full p-4 card-custom'):
                        with ui.row().classes('justify-between items-center mb-2'):
                            ui.label('Pasos').classes('text-primary').style('font-weight: 600; font-size: 0.85rem;')
                            ui.button(icon='add', on_click=self._add_paso).props('flat round size=sm color=primary')
                        self.pasos_container = ui.column().classes('w-full gap-2')
                        self._add_paso()
            with ui.row().classes('justify-end gap-2'):
                ui.button('Limpiar', on_click=self._limpiar_formulario).props('flat no-caps')
                ui.button('Guardar Receta', icon='save', on_click=self._guardar_receta).props('color=primary no-caps')

    def _add_ingrediente(self):
        with self.ingredientes_container:
            with ui.row().classes('w-full gap-2 items-center') as r:
                r.nombre = ui.input(placeholder='Ingrediente').props('outlined dense').style('flex: 1;')
                r.cantidad = ui.number(placeholder='Cant', min=0).props('outlined dense').style('width: 70px;')
                r.unidad = ui.select(['g', 'kg', 'ml', 'l', 'unidad', 'cda', 'pizca'], value='g').props('outlined dense').style('width: 90px;')
                ui.button(icon='delete', on_click=lambda x=r: x.delete()).props('flat round size=sm color=negative')

    def _add_paso(self):
        n = len(self.pasos_container.default_slot.children) + 1
        with self.pasos_container:
            with ui.card().classes('w-full p-3 card-custom') as c:
                with ui.row().classes('justify-between items-center mb-2'):
                    ui.badge(f'Paso {n}').props('color=primary')
                    ui.button(icon='delete', on_click=lambda x=c: x.delete()).props('flat round size=sm color=negative')
                with ui.row().classes('gap-2'):
                    c.tipo = ui.select(['corte', 'temperatura', 'mecanica'], value='corte', label='Tipo').props('outlined dense').style('width: 100px;')
                    todas_ops = self.OPERACIONES['corte'] + self.OPERACIONES['temperatura'] + self.OPERACIONES['mecanica']
                    c.operacion = ui.select(todas_ops, value='picar', label='Operación').props('outlined dense').style('flex: 1;')
                with ui.row().classes('gap-2 mt-2'):
                    c.duracion = ui.number(label='Seg', value=60, min=1).props('outlined dense').style('flex: 1;')
                    c.temperatura = ui.number(label='°C', value=0).props('outlined dense').style('flex: 1;')
                    c.velocidad = ui.number(label='Vel', value=5, min=1, max=10).props('outlined dense').style('flex: 1;')
                c.descripcion = ui.input(placeholder='Descripción...').props('outlined dense').classes('w-full mt-2')

    def _limpiar_formulario(self):
        self.new_nombre.value = ''
        self.new_descripcion.value = ''
        # Resetear checkboxes de alérgenos
        if hasattr(self, 'alergenos_checkboxes'):
            for cb in self.alergenos_checkboxes.values():
                cb.value = False
        self.ingredientes_container.clear()
        self.pasos_container.clear()
        for _ in range(3):
            self._add_ingrediente()
        self._add_paso()

    def _guardar_receta(self):
        nombre = (self.new_nombre.value or '').strip()
        if not nombre:
            ui.notify('Nombre requerido', type='negative')
            return
        ings = [Ingrediente(r.nombre.value, float(r.cantidad.value or 0), r.unidad.value) for r in self.ingredientes_container.default_slot.children if hasattr(r, 'nombre') and r.nombre.value]
        if not ings:
            ui.notify('Añade ingredientes', type='negative')
            return
        pasos, tiempo = [], 0
        for c in self.pasos_container.default_slot.children:
            if hasattr(c, 'tipo'):
                p = {'tipo': c.tipo.value, 'operacion': c.operacion.value, 'duracion': int(c.duracion.value or 60), 'temperatura': int(c.temperatura.value or 0), 'velocidad': int(c.velocidad.value or 5), 'descripcion': c.descripcion.value or ''}
                if p['tipo'] == 'mecanica':
                    p['nombre'] = p['operacion'].title()
                pasos.append(p)
                tiempo += p['duracion']
        if not pasos:
            ui.notify('Añade pasos', type='negative')
            return
        receta = Receta(nombre=nombre, descripcion=self.new_descripcion.value or nombre, ingredientes=ings, pasos=pasos, tiempo_total=tiempo, porciones=int(self.new_porciones.value or 4), dificultad=self.new_dificultad.value)
        self.db.add_recipe(receta)
        ui.notify(f'Receta "{nombre}" guardada', type='positive')
        self._limpiar_formulario()
        self._cargar_recetas()
    # ==================== EJECUCIÓN ====================
    
    def _preparar_receta(self, receta):
        try:
            self._ultima_receta = receta
            self._receta_completada_id = receta.id
            self.robot.preparar_receta(receta)
            nombre_corto = receta.nombre[:18] + '...' if len(receta.nombre) > 18 else receta.nombre
            self.dash_receta.set_text(nombre_corto)
            m, s = divmod(receta.tiempo_total, 60)
            self.dash_tiempo.set_text(f'{m:02d}:{s:02d}')
            self._mostrar_receta_activa(receta)
            self._actualizar_lista_pasos()
            self._reset_displays()
            ui.notify(f'Receta preparada: {receta.nombre}', type='positive')
            self._actualizar_botones()
        except Exception as e:
            ui.notify(str(e), type='negative')

    def _mostrar_receta_activa(self, receta):
        self.receta_activa_container.clear()
        with self.receta_activa_container:
            with ui.card().classes('w-full p-3 card-custom').style('border-left: 3px solid #10b981 !important;'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('check_circle', size='18px').style('color: #10b981;')
                    ui.label('Listo para cocinar').style('font-size: 0.8rem; color: #10b981; font-weight: 500;')
                ui.label(receta.nombre).classes('text-primary').style('font-weight: 600;')
                ui.label(f'{receta.tiempo_str} · {receta.num_pasos} pasos · {self._porciones_actuales} porc.').classes('text-secondary').style('font-size: 0.8rem;')

    async def _comenzar_receta(self):
        if self._ejecutando or self.robot.estado != EstadoRobot.PREPARADO:
            return
        self._ejecutando = True
        self._tiempo_inicio = time.time()
        self.robot._simulator.velocidad = self._velocidad_simulacion
        if self.robot.receta_actual:
            self._exec_id = self.db.start_execution(self.robot.receta_actual, self._porciones_actuales)
        
        try:
            completada = await self.robot.comenzar_receta()
            duracion = int(time.time() - self._tiempo_inicio) if self._tiempo_inicio else 0
            if self._exec_id:
                self.db.finish_execution(self._exec_id, completada=completada, duracion_real=duracion)
            if completada:
                # Pequeña pausa para asegurar que la UI se actualiza
                await asyncio.sleep(0.2)
                self._mostrar_dialogo_completado(duracion)
        except Exception as e:
            ui.notify(str(e), type='negative')
            if self._exec_id:
                self.db.finish_execution(self._exec_id, completada=False, duracion_real=0)
        finally:
            self._ejecutando = False
            self._exec_id = None

    def _mostrar_dialogo_completado(self, duracion_segundos):
        receta = self._ultima_receta
        if not receta:
            return
        
        # Calcular tiempo REAL de la receta
        tiempo_real = receta.tiempo_total
        m, s = divmod(tiempo_real, 60)
        tiempo_str = f'{m} min' if not s else f'{m}m {s}s'
        
        # Calcular nutrición
        nutricion = self._calcular_nutricion(receta.ingredientes, receta.porciones, self._porciones_actuales)
        
        # Calcular gramos SÓLIDOS por porción (excluir líquidos como agua, caldo, vino)
        factor = self._porciones_actuales / receta.porciones
        gramos_total = 0
        liquidos = ['agua', 'caldo', 'vino', 'aceite', 'vinagre']
        for ing in receta.ingredientes:
            nombre_lower = ing.nombre.lower()
            # Saltar líquidos que no aportan peso significativo al plato final
            if any(liq in nombre_lower for liq in liquidos):
                continue
            cantidad = ing.cantidad * factor
            if ing.unidad == 'g':
                gramos_total += cantidad
            elif ing.unidad == 'kg':
                gramos_total += cantidad * 1000
            elif ing.unidad == 'unidad':
                gramos_total += cantidad * 80  # Peso promedio más realista
            elif ing.unidad == 'cda':
                gramos_total += cantidad * 12
        gramos_porcion = int(gramos_total / self._porciones_actuales) if self._porciones_actuales > 0 else 0
        
        dialog = ui.dialog().props('persistent')
        with dialog, ui.card().classes('p-0').style('width: 340px; max-width: 95vw;'):
            # Header verde
            with ui.column().classes('w-full items-center').style('background: linear-gradient(135deg, #10b981, #059669); padding: 24px 16px;'):
                ui.icon('check_circle', size='40px').style('color: white;')
                ui.label('¡Receta Completada!').style('font-size: 1.15rem; font-weight: 600; color: white; margin-top: 8px;')
                ui.label(receta.nombre).style('color: rgba(255,255,255,0.9); font-size: 0.85rem; text-align: center;')
            
            with ui.column().style('padding: 16px; gap: 12px;'):
                # Resumen - 3 columnas iguales
                with ui.row().classes('w-full justify-center').style('gap: 8px;'):
                    for icono, valor, etiqueta in [('schedule', tiempo_str, 'Tiempo'), ('restaurant', str(self._porciones_actuales), 'Porciones'), ('scale', f'{gramos_porcion}g', 'Porción')]:
                        with ui.card().classes('card-custom').style('width: 95px; padding: 12px 8px; text-align: center;'):
                            ui.icon(icono, size='18px').style('color: var(--text-secondary); display: block; margin: 0 auto;')
                            ui.label(valor).classes('text-primary').style('font-size: 0.9rem; font-weight: 600; margin-top: 4px; display: block;')
                            ui.label(etiqueta).classes('text-secondary').style('font-size: 0.6rem; display: block;')
                
                # Info nutricional - 4 columnas iguales
                with ui.card().classes('w-full card-custom').style('padding: 12px;'):
                    ui.label('Información Nutricional').classes('text-primary').style('font-weight: 500; font-size: 0.75rem; margin-bottom: 10px; text-align: center; display: block;')
                    with ui.row().classes('w-full justify-center').style('gap: 12px;'):
                        for valor, etiqueta, color in [(f'{nutricion["calorias"]}', 'kcal', '#ef4444'), (f'{nutricion["proteinas"]}g', 'prot', '#3b82f6'), (f'{nutricion["carbohidratos"]}g', 'carbs', '#f59e0b'), (f'{nutricion["grasas"]}g', 'grasas', '#8b5cf6')]:
                            with ui.column().classes('items-center').style('min-width: 50px;'):
                                ui.label(str(valor)).style(f'font-size: 0.85rem; font-weight: 600; color: {color};')
                                ui.label(etiqueta).classes('text-secondary').style('font-size: 0.55rem;')
                
                # Nota opcional
                with ui.card().classes('w-full card-custom').style('padding: 12px;'):
                    ui.label('Añadir nota (opcional)').classes('text-primary').style('font-weight: 500; font-size: 0.75rem; margin-bottom: 6px;')
                    nota_input = ui.textarea(placeholder='Ej: Quedó muy bueno...').props('outlined dense').classes('w-full').style('min-height: 40px;')
                
                def cerrar_dialogo():
                    if nota_input.value and nota_input.value.strip():
                        self.db.add_note(self._receta_completada_id, nota_input.value.strip())
                        ui.notify('Nota guardada', type='positive')
                    dialog.close()
                    # Resetear el robot a estado IDLE para poder seguir usándolo
                    self.robot._estado = EstadoRobot.IDLE
                    self.robot._reset_todo()
                    self.receta_activa_container.clear()
                    self._limpiar_paso()
                    self._reset_displays()
                    self._actualizar_lista_pasos()
                    self._actualizar_botones()
                    self._cargar_recetas()
                
                ui.button('Cerrar', on_click=cerrar_dialogo).props('color=positive no-caps unelevated').classes('w-full')
        
        dialog.open()

    def _cancelar_receta(self):
        if self.robot.estado == EstadoRobot.PREPARADO:
            self.robot._estado = EstadoRobot.IDLE
            self.robot._reset_todo()
            self.receta_activa_container.clear()
            self._limpiar_paso()
            self._reset_displays()
            self._actualizar_lista_pasos()
            self._actualizar_botones()
            ui.notify('Receta cancelada', type='warning')
        elif self.robot.estado in (EstadoRobot.EJECUTANDO, EstadoRobot.PAUSADO):
            if self._exec_id:
                dur = int(time.time() - self._tiempo_inicio) if self._tiempo_inicio else 0
                self.db.finish_execution(self._exec_id, completada=False, duracion_real=dur)
                self._exec_id = None
            self.robot.parada_emergencia()
            self._ejecutando = False

    def _confirmar_emergencia(self):
        if self.robot.estado not in (EstadoRobot.EJECUTANDO, EstadoRobot.PAUSADO):
            ui.notify('No hay receta en ejecución', type='info')
            return
        with ui.dialog() as d, ui.card().classes('p-4 card-custom'):
            ui.label('⚠️ Parada de Emergencia').style('font-weight: 600; color: #ef4444;')
            ui.label('¿Detener la receta inmediatamente?').classes('text-secondary')
            with ui.row().classes('justify-end gap-2 mt-3'):
                ui.button('Cancelar', on_click=d.close).props('flat no-caps')
                ui.button('Detener', on_click=lambda: (d.close(), self._parada_emergencia())).props('color=negative no-caps')
        d.open()

    def _limpiar_paso(self):
        self.paso_container.clear()
        with self.paso_container:
            self._mostrar_esperando()

    def _reset_displays(self):
        self.dash_progreso.set_text('0%')
        self.recipe_progress.set_value(0)
        self.recipe_progress_label.set_text('0%')
        self.progreso_texto.set_text('0 de 0 pasos')
        self.tiempo_transcurrido.set_text('Transcurrido: --:--')
        self.tiempo_restante_label.set_text('Restante: --:--')
        self._actualizar_indicadores(0, 0)
        self.time_display.set_text('--:--')
        self.paso_progress.set_value(0)

    def _cambiar_velocidad(self, e):
        self._velocidad_simulacion = e.value
        if hasattr(self.robot, '_simulator'):
            self.robot._simulator.velocidad = e.value

    def _on_estado_changed(self, estado):
        config = {
            EstadoRobot.APAGADO: ('power_settings_new', '#ef4444', 'Apagado', 'APAGADO'),
            EstadoRobot.IDLE: ('check_circle', '#10b981', 'Listo', 'LISTO'),
            EstadoRobot.PREPARADO: ('schedule', '#3b82f6', 'Preparado', 'PREPARADO'),
            EstadoRobot.EJECUTANDO: ('restaurant', '#8b5cf6', 'Cocinando', 'COCINANDO'),
            EstadoRobot.PAUSADO: ('pause_circle', '#f59e0b', 'Pausado', 'PAUSADO'),
            EstadoRobot.FINALIZADO: ('check_circle', '#10b981', 'Completado', 'COMPLETADO'),
        }
        icono, color, texto, dash = config.get(estado, ('help', '#888', '?', '?'))
        self.header_icon.props(f'name={icono}').style(f'color: {color};')
        self.header_status.set_text(texto)
        self.dash_estado.set_text(dash)
        
        if estado == EstadoRobot.EJECUTANDO:
            self._mostrar_paso_actual()
            self._actualizar_lista_pasos()
        elif estado == EstadoRobot.FINALIZADO:
            self._mostrar_completado()
            self._actualizar_lista_pasos()
            self._ejecutando = False
        elif estado == EstadoRobot.PAUSADO:
            self._actualizar_lista_pasos()
        elif estado in (EstadoRobot.IDLE, EstadoRobot.APAGADO):
            self._limpiar_paso()
            self._actualizar_lista_pasos()
            if not self.robot.receta_actual:
                self.receta_activa_container.clear()
                self.dash_receta.set_text('Ninguna')
                self.dash_tiempo.set_text('--:--')
        self._actualizar_botones()

    def _on_progreso_changed(self, progreso):
        tiempos = self.robot.get_tiempos_restantes()
        estado = self.robot.get_estado_completo()
        pr = estado.get('progreso_receta', 0)
        pa = self.robot.paso_actual
        total = self.robot.total_pasos
        
        self.recipe_progress.set_value(pr / 100)
        self.recipe_progress_label.set_text(f'{pr}%')
        self.dash_progreso.set_text(f'{pr}%')
        self.progreso_texto.set_text(f'{pa} de {total} pasos')
        
        m, s = divmod(tiempos.get('receta', 0), 60)
        self.dash_tiempo.set_text(f'{m:02d}:{s:02d}')
        self.tiempo_restante_label.set_text(f'Restante: {m:02d}:{s:02d}')
        
        if self._tiempo_inicio:
            t = int(time.time() - self._tiempo_inicio)
            mt, st = divmod(t, 60)
            self.tiempo_transcurrido.set_text(f'Transcurrido: {mt:02d}:{st:02d}')
        
        tp = tiempos.get('paso', 0)
        mp, sp = divmod(tp, 60)
        self.time_display.set_text(f'{mp}:{sp:02d}')
        
        if self.robot.receta_actual and pa < len(self.robot.receta_actual.pasos):
            dur = self.robot.receta_actual.pasos[pa].get('duracion', 1)
            pp = 1 - (tp / dur) if dur > 0 else 1
            self.paso_progress.set_value(max(0, min(1, pp)))
        
        params = self.robot.get_parametros_activos()
        self._actualizar_indicadores(params.get('temperatura', 0), params.get('velocidad', 0))
        self._mostrar_paso_actual()

    def _on_evento(self, msg):
        pass

    def _mostrar_paso_actual(self):
        if not self.robot.receta_actual:
            return
        idx = self.robot.paso_actual
        pasos = self.robot.receta_actual.pasos
        if idx >= len(pasos):
            return
        paso = pasos[idx]
        op = paso.get('operacion', paso.get('nombre', 'Paso'))
        icono = self.ICONOS_OPERACION.get(op.lower(), '📌')
        
        self.paso_container.clear()
        with self.paso_container:
            with ui.card().classes('w-full p-5').style('background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; border: none !important;'):
                with ui.row().classes('justify-between items-center mb-3'):
                    ui.label(f'Paso {idx + 1} de {len(pasos)}').style('color: rgba(255,255,255,0.7); font-size: 0.85rem;')
                    tipo = paso.get('tipo', '').upper()
                    tc = {'CORTE': '#fbbf24', 'TEMPERATURA': '#ef4444', 'MECANICA': '#60a5fa'}.get(tipo, '#fff')
                    ui.badge(tipo).style(f'background: {tc};')
                with ui.row().classes('items-center gap-3 mb-3'):
                    ui.label(icono).style('font-size: 2.5rem;')
                    ui.label(op.upper()).style('font-size: 1.4rem; font-weight: 600; color: white;')
                if paso.get('descripcion'):
                    ui.label(paso['descripcion']).style('color: rgba(255,255,255,0.8); margin-bottom: 12px;')
                with ui.row().classes('gap-6'):
                    if paso.get('duracion'):
                        mm, ss = divmod(paso['duracion'], 60)
                        with ui.column().classes('items-center'):
                            ui.icon('timer', size='24px').style('color: rgba(255,255,255,0.7);')
                            ui.label(f'{mm}:{ss:02d}' if mm else f'{ss}s').style('font-weight: 600; color: white;')
                    if paso.get('temperatura'):
                        with ui.column().classes('items-center'):
                            ui.icon('thermostat', size='24px').style('color: rgba(255,255,255,0.7);')
                            ui.label(f'{paso["temperatura"]}°C').style('font-weight: 600; color: white;')
                    if paso.get('velocidad'):
                        with ui.column().classes('items-center'):
                            ui.icon('speed', size='24px').style('color: rgba(255,255,255,0.7);')
                            ui.label(f'Vel. {paso["velocidad"]}').style('font-weight: 600; color: white;')

    def _mostrar_completado(self):
        self.paso_container.clear()
        with self.paso_container:
            with ui.card().classes('w-full p-8 items-center').style('background: linear-gradient(135deg, #10b981, #059669) !important; border: none !important;'):
                ui.icon('check_circle', size='48px').style('color: white;')
                ui.label('Receta Completada').style('font-size: 1.3rem; font-weight: 600; color: white; margin-top: 8px;')
                if self.robot.receta_actual:
                    ui.label(self.robot.receta_actual.nombre).style('color: rgba(255,255,255,0.8);')

    def _actualizar_botones(self):
        e = self.robot.estado
        self.btn_encender.set_enabled(e == EstadoRobot.APAGADO)
        self.btn_apagar.set_enabled(e in [EstadoRobot.IDLE, EstadoRobot.FINALIZADO])
        self.btn_comenzar.set_enabled(e == EstadoRobot.PREPARADO and not self._ejecutando)
        self.btn_pausar.set_enabled(e == EstadoRobot.EJECUTANDO)
        self.btn_reanudar.set_enabled(e == EstadoRobot.PAUSADO)
        self.btn_cancelar.set_enabled(e in [EstadoRobot.PREPARADO, EstadoRobot.PAUSADO, EstadoRobot.FINALIZADO])
        self.btn_emergencia.set_enabled(e in [EstadoRobot.EJECUTANDO, EstadoRobot.PAUSADO])

    def _encender_robot(self):
        if self.controller.encender():
            ui.notify('Robot encendido', type='positive')

    def _apagar_robot(self):
        try:
            if self.controller.apagar():
                self.receta_activa_container.clear()
                self._limpiar_paso()
                self._reset_displays()
                self._actualizar_lista_pasos()
                ui.notify('Robot apagado', type='info')
        except TareaInvalidaError as e:
            ui.notify(str(e), type='negative')

    def _pausar_robot(self):
        try:
            self.controller.pausar()
            ui.notify('Receta pausada', type='warning')
        except TareaInvalidaError as e:
            ui.notify(str(e), type='negative')

    def _reanudar_robot(self):
        try:
            self.controller.reanudar()
            ui.notify('Receta reanudada', type='positive')
        except TareaInvalidaError as e:
            ui.notify(str(e), type='negative')

    def _parada_emergencia(self):
        if self._exec_id:
            dur = int(time.time() - self._tiempo_inicio) if self._tiempo_inicio else 0
            self.db.finish_execution(self._exec_id, completada=False, duracion_real=dur)
            self._exec_id = None
        self.controller.parada_emergencia()
        self._ejecutando = False
        self.receta_activa_container.clear()
        self._limpiar_paso()
        self._reset_displays()
        self._actualizar_lista_pasos()
        ui.notify('Parada de emergencia activada', type='negative')
