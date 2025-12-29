"""
Gestor de base de datos SQLite para el robot de cocina.
Maneja recetas de fábrica y de usuario - VERSIÓN AMPLIADA.
"""

import sqlite3
from pathlib import Path
from typing import List, Optional
from models.receta import Receta, Ingrediente
from utils.exceptions import DatabaseError


class DatabaseHandler:
    """Maneja todas las operaciones de base de datos."""
    
    def __init__(self, db_path: str = "data/robot_cocina.db"):
        self.db_path = db_path
        Path("data").mkdir(exist_ok=True)
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_database(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Tabla de recetas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recetas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    ingredientes TEXT NOT NULL,
                    pasos TEXT NOT NULL,
                    tiempo_total INTEGER NOT NULL,
                    porciones INTEGER DEFAULT 4,
                    dificultad TEXT DEFAULT 'Media',
                    es_fabrica INTEGER DEFAULT 0,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de favoritos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS favoritos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    receta_id INTEGER NOT NULL,
                    fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
                    UNIQUE(receta_id)
                )
            ''')
            
            # Tabla de historial de ejecuciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historial (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    receta_id INTEGER NOT NULL,
                    receta_nombre TEXT NOT NULL,
                    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_fin TIMESTAMP,
                    duracion_real INTEGER,
                    porciones_cocinadas INTEGER,
                    completada INTEGER DEFAULT 0,
                    cancelada INTEGER DEFAULT 0,
                    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE SET NULL
                )
            ''')
            
            # Tabla de notas de recetas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notas_recetas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    receta_id INTEGER NOT NULL,
                    nota TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
            conn.close()
            if self.get_recipe_count(solo_fabrica=True) == 0:
                self.load_factory_recipes()
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al inicializar la base de datos: {e}")
    
    def load_factory_recipes(self):
        """Carga recetas de fábrica ampliadas."""
        recetas = [
            # SOPAS Y CREMAS
            self._receta_gazpacho(),
            self._receta_sopa_verduras(),
            self._receta_crema_calabaza(),
            self._receta_crema_champinones(),
            self._receta_sopa_tomate(),
            self._receta_vichyssoise(),
            # ARROCES Y PASTAS
            self._receta_risotto(),
            self._receta_arroz_cubana(),
            self._receta_pasta_carbonara(),
            self._receta_pasta_bolonesa(),
            # CARNES
            self._receta_pollo_curry(),
            self._receta_estofado_ternera(),
            self._receta_albondigas(),
            self._receta_pollo_limon(),
            # PESCADOS
            self._receta_merluza_verde(),
            self._receta_salmon_vapor(),
            # MASAS Y PANES
            self._receta_pan(),
            self._receta_masa_pizza(),
            self._receta_bizcocho(),
            # GUARNICIONES
            self._receta_pure_patatas(),
            self._receta_verduras_vapor(),
            self._receta_pisto(),
            # POSTRES
            self._receta_natillas(),
            self._receta_compota_manzana(),
        ]
        for r in recetas:
            self.add_recipe(r, es_fabrica=True)

    # ==================== SOPAS Y CREMAS ====================

    def _receta_gazpacho(self) -> Receta:
        return Receta(
            nombre="Gazpacho Andaluz",
            descripcion="Refrescante sopa fría tradicional española perfecta para el verano",
            ingredientes=[
                Ingrediente("tomates maduros", 1, "kg"),
                Ingrediente("pepino", 1, "unidad"),
                Ingrediente("pimiento verde", 1, "unidad"),
                Ingrediente("ajo", 2, "diente"),
                Ingrediente("aceite de oliva", 100, "ml"),
                Ingrediente("vinagre de Jerez", 30, "ml"),
                Ingrediente("sal", 1, "cucharada"),
                Ingrediente("pan del día anterior", 100, "g"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 20, "velocidad": 5, "descripcion": "Trocear todos los vegetales en trozos grandes"},
                {"tipo": "corte", "operacion": "picar", "duracion": 60, "velocidad": 9, "descripcion": "Triturar hasta obtener textura fina y homogénea"},
            ],
            tiempo_total=80, porciones=6, dificultad="Fácil", es_fabrica=True
        )

    def _receta_sopa_verduras(self) -> Receta:
        return Receta(
            nombre="Sopa de Verduras",
            descripcion="Sopa casera nutritiva y reconfortante con verduras de temporada",
            ingredientes=[
                Ingrediente("zanahoria", 3, "unidad"),
                Ingrediente("calabacín", 1, "unidad"),
                Ingrediente("puerro", 2, "unidad"),
                Ingrediente("patata", 2, "unidad"),
                Ingrediente("judías verdes", 150, "g"),
                Ingrediente("caldo de verduras", 1.5, "l"),
                Ingrediente("aceite de oliva", 30, "ml"),
                Ingrediente("sal y pimienta", 1, "al gusto"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 25, "velocidad": 6, "descripcion": "Trocear todas las verduras en cubos medianos"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 180, "temperatura": 120, "velocidad": 2, "descripcion": "Sofreír las verduras con aceite"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 600, "temperatura": 100, "velocidad": 1, "descripcion": "Cocinar a fuego lento con el caldo"},
            ],
            tiempo_total=805, porciones=6, dificultad="Fácil", es_fabrica=True
        )

    def _receta_crema_calabaza(self) -> Receta:
        return Receta(
            nombre="Crema de Calabaza",
            descripcion="Crema suave y aromática con un toque de nuez moscada",
            ingredientes=[
                Ingrediente("calabaza", 800, "g"),
                Ingrediente("cebolla", 1, "unidad"),
                Ingrediente("patata", 1, "unidad"),
                Ingrediente("nata líquida", 200, "ml"),
                Ingrediente("caldo de pollo", 500, "ml"),
                Ingrediente("nuez moscada", 1, "pizca"),
                Ingrediente("mantequilla", 30, "g"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 20, "velocidad": 5, "descripcion": "Trocear la calabaza, cebolla y patata"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 120, "temperatura": 100, "velocidad": 2, "descripcion": "Pochar la cebolla con mantequilla"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 480, "temperatura": 100, "velocidad": 1, "descripcion": "Cocer con el caldo hasta que esté tierna"},
                {"tipo": "corte", "operacion": "picar", "duracion": 60, "velocidad": 10, "descripcion": "Triturar hasta obtener crema fina"},
            ],
            tiempo_total=680, porciones=4, dificultad="Fácil", es_fabrica=True
        )

    def _receta_crema_champinones(self) -> Receta:
        return Receta(
            nombre="Crema de Champiñones",
            descripcion="Deliciosa crema con champiñones frescos y un toque de tomillo",
            ingredientes=[
                Ingrediente("champiñones", 500, "g"),
                Ingrediente("cebolla", 1, "unidad"),
                Ingrediente("ajo", 2, "diente"),
                Ingrediente("nata para cocinar", 250, "ml"),
                Ingrediente("caldo de pollo", 400, "ml"),
                Ingrediente("tomillo fresco", 1, "cucharada"),
                Ingrediente("mantequilla", 40, "g"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "picar", "duracion": 15, "velocidad": 5, "descripcion": "Picar la cebolla y el ajo"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 120, "temperatura": 110, "velocidad": 2, "descripcion": "Sofreír la cebolla y ajo"},
                {"tipo": "corte", "operacion": "trocear", "duracion": 10, "velocidad": 4, "descripcion": "Añadir champiñones troceados"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 180, "temperatura": 120, "velocidad": 2, "descripcion": "Cocinar los champiñones"},
                {"tipo": "corte", "operacion": "picar", "duracion": 45, "velocidad": 9, "descripcion": "Triturar con nata y caldo"},
            ],
            tiempo_total=370, porciones=4, dificultad="Fácil", es_fabrica=True
        )

    def _receta_sopa_tomate(self) -> Receta:
        return Receta(
            nombre="Sopa de Tomate",
            descripcion="Sopa clásica de tomate con albahaca fresca",
            ingredientes=[
                Ingrediente("tomates maduros", 1, "kg"),
                Ingrediente("cebolla", 1, "unidad"),
                Ingrediente("ajo", 3, "diente"),
                Ingrediente("caldo de verduras", 500, "ml"),
                Ingrediente("albahaca fresca", 10, "g"),
                Ingrediente("azúcar", 1, "cucharada"),
                Ingrediente("aceite de oliva", 50, "ml"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 15, "velocidad": 5, "descripcion": "Trocear tomates, cebolla y ajo"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 180, "temperatura": 110, "velocidad": 2, "descripcion": "Sofreír hasta caramelizar"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 300, "temperatura": 100, "velocidad": 1, "descripcion": "Cocinar con caldo"},
                {"tipo": "corte", "operacion": "picar", "duracion": 30, "velocidad": 8, "descripcion": "Triturar hasta textura suave"},
            ],
            tiempo_total=525, porciones=4, dificultad="Fácil", es_fabrica=True
        )

    def _receta_vichyssoise(self) -> Receta:
        return Receta(
            nombre="Vichyssoise",
            descripcion="Elegante crema fría de puerros y patata de origen francés",
            ingredientes=[
                Ingrediente("puerros", 4, "unidad"),
                Ingrediente("patata", 2, "unidad"),
                Ingrediente("cebolla", 1, "unidad"),
                Ingrediente("nata líquida", 200, "ml"),
                Ingrediente("caldo de pollo", 750, "ml"),
                Ingrediente("cebollino", 1, "cucharada"),
                Ingrediente("mantequilla", 50, "g"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "picar", "duracion": 20, "velocidad": 5, "descripcion": "Picar puerros, patata y cebolla"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 180, "temperatura": 100, "velocidad": 2, "descripcion": "Pochar los puerros con mantequilla"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 480, "temperatura": 100, "velocidad": 1, "descripcion": "Cocer con caldo hasta que la patata esté tierna"},
                {"tipo": "corte", "operacion": "picar", "duracion": 60, "velocidad": 10, "descripcion": "Triturar y añadir nata"},
            ],
            tiempo_total=740, porciones=6, dificultad="Media", es_fabrica=True
        )

    # ==================== ARROCES Y PASTAS ====================

    def _receta_risotto(self) -> Receta:
        return Receta(
            nombre="Risotto de Setas",
            descripcion="Cremoso risotto italiano con variedad de setas y parmesano",
            ingredientes=[
                Ingrediente("arroz arborio", 350, "g"),
                Ingrediente("setas variadas", 300, "g"),
                Ingrediente("cebolla", 1, "unidad"),
                Ingrediente("vino blanco", 150, "ml"),
                Ingrediente("caldo de pollo", 1, "l"),
                Ingrediente("parmesano rallado", 80, "g"),
                Ingrediente("mantequilla", 50, "g"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "picar", "duracion": 15, "velocidad": 5, "descripcion": "Picar la cebolla finamente"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 120, "temperatura": 110, "velocidad": 2, "descripcion": "Sofreír cebolla con mantequilla"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 60, "temperatura": 120, "velocidad": 2, "descripcion": "Tostar el arroz"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 1080, "temperatura": 100, "velocidad": 1, "descripcion": "Cocinar añadiendo caldo poco a poco"},
            ],
            tiempo_total=1275, porciones=4, dificultad="Media", es_fabrica=True
        )

    def _receta_arroz_cubana(self) -> Receta:
        return Receta(
            nombre="Arroz a la Cubana",
            descripcion="Clásico arroz con tomate, huevo frito y plátano",
            ingredientes=[
                Ingrediente("arroz", 300, "g"),
                Ingrediente("tomate frito", 400, "g"),
                Ingrediente("huevos", 4, "unidad"),
                Ingrediente("plátano macho", 2, "unidad"),
                Ingrediente("agua", 600, "ml"),
                Ingrediente("aceite de oliva", 50, "ml"),
                Ingrediente("sal", 1, "cucharada"),
            ],
            pasos=[
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 900, "temperatura": 100, "velocidad": 1, "descripcion": "Cocer el arroz con agua y sal"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 180, "temperatura": 80, "velocidad": 1, "descripcion": "Calentar el tomate frito"},
            ],
            tiempo_total=1080, porciones=4, dificultad="Fácil", es_fabrica=True
        )

    def _receta_pasta_carbonara(self) -> Receta:
        return Receta(
            nombre="Pasta Carbonara",
            descripcion="Auténtica carbonara italiana con guanciale y pecorino",
            ingredientes=[
                Ingrediente("espaguetis", 400, "g"),
                Ingrediente("guanciale o panceta", 200, "g"),
                Ingrediente("huevos", 4, "unidad"),
                Ingrediente("pecorino romano", 100, "g"),
                Ingrediente("pimienta negra", 1, "cucharada"),
                Ingrediente("agua", 3, "l"),
                Ingrediente("sal", 2, "cucharada"),
            ],
            pasos=[
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 600, "temperatura": 100, "velocidad": 1, "descripcion": "Cocer la pasta al dente"},
                {"tipo": "corte", "operacion": "trocear", "duracion": 15, "velocidad": 4, "descripcion": "Cortar el guanciale en dados"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 180, "temperatura": 130, "velocidad": 1, "descripcion": "Dorar el guanciale"},
                {"tipo": "mecanica", "nombre": "Mezclar", "duracion": 60, "velocidad": 3, "descripcion": "Mezclar con la salsa de huevo"},
            ],
            tiempo_total=855, porciones=4, dificultad="Media", es_fabrica=True
        )

    def _receta_pasta_bolonesa(self) -> Receta:
        return Receta(
            nombre="Pasta Boloñesa",
            descripcion="Ragú de carne tradicional de Bolonia con tagliatelle",
            ingredientes=[
                Ingrediente("carne picada mixta", 500, "g"),
                Ingrediente("tomate triturado", 400, "g"),
                Ingrediente("cebolla", 1, "unidad"),
                Ingrediente("zanahoria", 1, "unidad"),
                Ingrediente("apio", 1, "unidad"),
                Ingrediente("vino tinto", 150, "ml"),
                Ingrediente("pasta tagliatelle", 400, "g"),
                Ingrediente("aceite de oliva", 40, "ml"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "picar", "duracion": 20, "velocidad": 6, "descripcion": "Picar el sofrito (cebolla, zanahoria, apio)"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 180, "temperatura": 120, "velocidad": 2, "descripcion": "Sofreír el sofrito"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 300, "temperatura": 140, "velocidad": 2, "descripcion": "Dorar la carne picada"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 1800, "temperatura": 90, "velocidad": 1, "descripcion": "Cocinar a fuego lento con tomate y vino"},
            ],
            tiempo_total=2300, porciones=6, dificultad="Media", es_fabrica=True
        )

    # ==================== CARNES ====================

    def _receta_pollo_curry(self) -> Receta:
        return Receta(
            nombre="Pollo al Curry",
            descripcion="Aromático curry de pollo con leche de coco y especias",
            ingredientes=[
                Ingrediente("pechuga de pollo", 600, "g"),
                Ingrediente("leche de coco", 400, "ml"),
                Ingrediente("cebolla", 2, "unidad"),
                Ingrediente("ajo", 3, "diente"),
                Ingrediente("jengibre fresco", 30, "g"),
                Ingrediente("curry en polvo", 2, "cucharada"),
                Ingrediente("tomate triturado", 200, "g"),
                Ingrediente("cilantro fresco", 1, "al gusto"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 20, "velocidad": 5, "descripcion": "Trocear el pollo en cubos"},
                {"tipo": "corte", "operacion": "picar", "duracion": 15, "velocidad": 6, "descripcion": "Picar cebolla, ajo y jengibre"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 180, "temperatura": 130, "velocidad": 2, "descripcion": "Sellar el pollo"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 900, "temperatura": 100, "velocidad": 1, "descripcion": "Cocinar con las especias y leche de coco"},
            ],
            tiempo_total=1115, porciones=4, dificultad="Media", es_fabrica=True
        )

    def _receta_estofado_ternera(self) -> Receta:
        return Receta(
            nombre="Estofado de Ternera",
            descripcion="Tierno estofado tradicional con verduras y vino tinto",
            ingredientes=[
                Ingrediente("ternera para guisar", 800, "g"),
                Ingrediente("patatas", 4, "unidad"),
                Ingrediente("zanahoria", 3, "unidad"),
                Ingrediente("cebolla", 2, "unidad"),
                Ingrediente("vino tinto", 250, "ml"),
                Ingrediente("caldo de carne", 500, "ml"),
                Ingrediente("laurel", 2, "unidad"),
                Ingrediente("aceite de oliva", 50, "ml"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 25, "velocidad": 5, "descripcion": "Trocear la carne y verduras"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 300, "temperatura": 140, "velocidad": 2, "descripcion": "Sellar la carne hasta dorar"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 180, "temperatura": 120, "velocidad": 2, "descripcion": "Sofreír las verduras"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 3600, "temperatura": 90, "velocidad": 1, "descripcion": "Guisar a fuego lento hasta que esté tierna"},
            ],
            tiempo_total=4105, porciones=6, dificultad="Difícil", es_fabrica=True
        )

    def _receta_albondigas(self) -> Receta:
        return Receta(
            nombre="Albóndigas en Salsa",
            descripcion="Jugosas albóndigas caseras en salsa de tomate",
            ingredientes=[
                Ingrediente("carne picada mixta", 500, "g"),
                Ingrediente("pan rallado", 50, "g"),
                Ingrediente("huevo", 1, "unidad"),
                Ingrediente("ajo", 2, "diente"),
                Ingrediente("perejil", 1, "cucharada"),
                Ingrediente("tomate frito", 500, "g"),
                Ingrediente("caldo de carne", 200, "ml"),
                Ingrediente("aceite de oliva", 100, "ml"),
            ],
            pasos=[
                {"tipo": "mecanica", "nombre": "Mezclar", "duracion": 60, "velocidad": 4, "descripcion": "Mezclar carne, pan rallado, huevo y especias"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 480, "temperatura": 140, "velocidad": 1, "descripcion": "Freír las albóndigas hasta dorar"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 900, "temperatura": 90, "velocidad": 1, "descripcion": "Cocinar en la salsa de tomate"},
            ],
            tiempo_total=1440, porciones=4, dificultad="Media", es_fabrica=True
        )

    def _receta_pollo_limon(self) -> Receta:
        return Receta(
            nombre="Pollo al Limón",
            descripcion="Pollo jugoso con salsa de limón al estilo asiático",
            ingredientes=[
                Ingrediente("pechuga de pollo", 600, "g"),
                Ingrediente("limones", 3, "unidad"),
                Ingrediente("miel", 3, "cucharada"),
                Ingrediente("salsa de soja", 2, "cucharada"),
                Ingrediente("ajo", 2, "diente"),
                Ingrediente("maicena", 2, "cucharada"),
                Ingrediente("aceite de sésamo", 1, "cucharada"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 15, "velocidad": 5, "descripcion": "Cortar el pollo en tiras"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 300, "temperatura": 150, "velocidad": 2, "descripcion": "Saltear el pollo hasta dorar"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 180, "temperatura": 100, "velocidad": 2, "descripcion": "Añadir salsa de limón y reducir"},
            ],
            tiempo_total=495, porciones=4, dificultad="Fácil", es_fabrica=True
        )

    # ==================== PESCADOS ====================

    def _receta_merluza_verde(self) -> Receta:
        return Receta(
            nombre="Merluza en Salsa Verde",
            descripcion="Clásico plato vasco de merluza con salsa de perejil",
            ingredientes=[
                Ingrediente("lomos de merluza", 600, "g"),
                Ingrediente("ajo", 4, "diente"),
                Ingrediente("perejil fresco", 30, "g"),
                Ingrediente("harina", 2, "cucharada"),
                Ingrediente("vino blanco", 150, "ml"),
                Ingrediente("caldo de pescado", 300, "ml"),
                Ingrediente("aceite de oliva", 100, "ml"),
                Ingrediente("guisantes", 100, "g"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "picar", "duracion": 15, "velocidad": 6, "descripcion": "Picar el ajo y perejil"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 120, "temperatura": 100, "velocidad": 2, "descripcion": "Hacer el sofrito de ajo"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 480, "temperatura": 90, "velocidad": 1, "descripcion": "Cocinar la merluza en la salsa"},
            ],
            tiempo_total=615, porciones=4, dificultad="Media", es_fabrica=True
        )

    def _receta_salmon_vapor(self) -> Receta:
        return Receta(
            nombre="Salmón al Vapor",
            descripcion="Salmón cocinado al vapor con verduras y limón",
            ingredientes=[
                Ingrediente("lomos de salmón", 600, "g"),
                Ingrediente("brócoli", 200, "g"),
                Ingrediente("zanahoria", 2, "unidad"),
                Ingrediente("limón", 1, "unidad"),
                Ingrediente("eneldo fresco", 1, "cucharada"),
                Ingrediente("sal y pimienta", 1, "al gusto"),
                Ingrediente("agua", 500, "ml"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 15, "velocidad": 4, "descripcion": "Cortar las verduras"},
                {"tipo": "temperatura", "operacion": "vapor", "duracion": 900, "temperatura": 100, "velocidad": 1, "descripcion": "Cocinar al vapor el salmón con verduras"},
            ],
            tiempo_total=915, porciones=4, dificultad="Fácil", es_fabrica=True
        )

    # ==================== MASAS Y PANES ====================

    def _receta_pan(self) -> Receta:
        return Receta(
            nombre="Pan Casero",
            descripcion="Pan artesanal con corteza crujiente y miga tierna",
            ingredientes=[
                Ingrediente("harina de fuerza", 500, "g"),
                Ingrediente("agua tibia", 300, "ml"),
                Ingrediente("levadura fresca", 20, "g"),
                Ingrediente("sal", 10, "g"),
                Ingrediente("aceite de oliva", 30, "ml"),
            ],
            pasos=[
                {"tipo": "mecanica", "nombre": "Mezclar", "duracion": 30, "velocidad": 3, "descripcion": "Mezclar todos los ingredientes"},
                {"tipo": "mecanica", "nombre": "Amasar", "duracion": 600, "velocidad": 4, "descripcion": "Amasar hasta obtener masa elástica"},
            ],
            tiempo_total=630, porciones=8, dificultad="Media", es_fabrica=True
        )

    def _receta_masa_pizza(self) -> Receta:
        return Receta(
            nombre="Masa de Pizza",
            descripcion="Masa perfecta para pizza italiana fina y crujiente",
            ingredientes=[
                Ingrediente("harina", 400, "g"),
                Ingrediente("agua tibia", 250, "ml"),
                Ingrediente("levadura seca", 7, "g"),
                Ingrediente("sal", 8, "g"),
                Ingrediente("aceite de oliva", 30, "ml"),
                Ingrediente("azúcar", 5, "g"),
            ],
            pasos=[
                {"tipo": "mecanica", "nombre": "Mezclar", "duracion": 20, "velocidad": 2, "descripcion": "Mezclar ingredientes secos con líquidos"},
                {"tipo": "mecanica", "nombre": "Amasar", "duracion": 360, "velocidad": 5, "descripcion": "Amasar hasta masa suave y elástica"},
            ],
            tiempo_total=380, porciones=4, dificultad="Fácil", es_fabrica=True
        )

    def _receta_bizcocho(self) -> Receta:
        return Receta(
            nombre="Bizcocho Clásico",
            descripcion="Esponjoso bizcocho casero perfecto para el desayuno",
            ingredientes=[
                Ingrediente("harina", 250, "g"),
                Ingrediente("azúcar", 200, "g"),
                Ingrediente("huevos", 4, "unidad"),
                Ingrediente("aceite de girasol", 100, "ml"),
                Ingrediente("leche", 100, "ml"),
                Ingrediente("levadura química", 16, "g"),
                Ingrediente("ralladura de limón", 1, "unidad"),
            ],
            pasos=[
                {"tipo": "mecanica", "nombre": "Mezclar", "duracion": 60, "velocidad": 5, "descripcion": "Batir huevos con azúcar hasta blanquear"},
                {"tipo": "mecanica", "nombre": "Mezclar", "duracion": 60, "velocidad": 3, "descripcion": "Incorporar resto de ingredientes"},
            ],
            tiempo_total=120, porciones=8, dificultad="Fácil", es_fabrica=True
        )

    # ==================== GUARNICIONES ====================

    def _receta_pure_patatas(self) -> Receta:
        return Receta(
            nombre="Puré de Patatas",
            descripcion="Cremoso puré de patatas con mantequilla y nuez moscada",
            ingredientes=[
                Ingrediente("patatas", 1, "kg"),
                Ingrediente("leche", 200, "ml"),
                Ingrediente("mantequilla", 80, "g"),
                Ingrediente("nuez moscada", 1, "pizca"),
                Ingrediente("sal", 1, "cucharada"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 20, "velocidad": 5, "descripcion": "Pelar y trocear las patatas"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 1200, "temperatura": 100, "velocidad": 1, "descripcion": "Cocer las patatas hasta que estén tiernas"},
                {"tipo": "mecanica", "nombre": "Mezclar", "duracion": 60, "velocidad": 6, "descripcion": "Triturar con leche y mantequilla"},
            ],
            tiempo_total=1280, porciones=6, dificultad="Fácil", es_fabrica=True
        )

    def _receta_verduras_vapor(self) -> Receta:
        return Receta(
            nombre="Verduras al Vapor",
            descripcion="Mix de verduras cocinadas al vapor, sanas y coloridas",
            ingredientes=[
                Ingrediente("brócoli", 200, "g"),
                Ingrediente("coliflor", 200, "g"),
                Ingrediente("zanahoria", 2, "unidad"),
                Ingrediente("judías verdes", 150, "g"),
                Ingrediente("agua", 500, "ml"),
                Ingrediente("sal", 1, "pizca"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 20, "velocidad": 4, "descripcion": "Cortar las verduras en trozos similares"},
                {"tipo": "temperatura", "operacion": "vapor", "duracion": 720, "temperatura": 100, "velocidad": 1, "descripcion": "Cocinar al vapor hasta que estén tiernas"},
            ],
            tiempo_total=740, porciones=4, dificultad="Fácil", es_fabrica=True
        )

    def _receta_pisto(self) -> Receta:
        return Receta(
            nombre="Pisto Manchego",
            descripcion="Tradicional pisto con verduras de la huerta",
            ingredientes=[
                Ingrediente("calabacín", 2, "unidad"),
                Ingrediente("berenjena", 1, "unidad"),
                Ingrediente("pimiento rojo", 2, "unidad"),
                Ingrediente("pimiento verde", 2, "unidad"),
                Ingrediente("cebolla", 2, "unidad"),
                Ingrediente("tomate maduro", 500, "g"),
                Ingrediente("aceite de oliva", 100, "ml"),
                Ingrediente("sal y azúcar", 1, "al gusto"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 30, "velocidad": 5, "descripcion": "Trocear todas las verduras en cubos"},
                {"tipo": "temperatura", "operacion": "sofreir", "duracion": 1800, "temperatura": 100, "velocidad": 1, "descripcion": "Cocinar lentamente las verduras"},
            ],
            tiempo_total=1830, porciones=6, dificultad="Fácil", es_fabrica=True
        )

    # ==================== POSTRES ====================

    def _receta_natillas(self) -> Receta:
        return Receta(
            nombre="Natillas Caseras",
            descripcion="Cremosas natillas con canela y galleta",
            ingredientes=[
                Ingrediente("leche", 1, "l"),
                Ingrediente("yemas de huevo", 6, "unidad"),
                Ingrediente("azúcar", 150, "g"),
                Ingrediente("maicena", 40, "g"),
                Ingrediente("canela en rama", 1, "unidad"),
                Ingrediente("piel de limón", 1, "unidad"),
                Ingrediente("canela molida", 1, "cucharada"),
            ],
            pasos=[
                {"tipo": "mecanica", "nombre": "Mezclar", "duracion": 60, "velocidad": 5, "descripcion": "Batir yemas con azúcar y maicena"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 600, "temperatura": 90, "velocidad": 3, "descripcion": "Cocinar removiendo hasta espesar"},
            ],
            tiempo_total=660, porciones=6, dificultad="Media", es_fabrica=True
        )

    def _receta_compota_manzana(self) -> Receta:
        return Receta(
            nombre="Compota de Manzana",
            descripcion="Dulce compota casera perfecta para postres y meriendas",
            ingredientes=[
                Ingrediente("manzanas", 1, "kg"),
                Ingrediente("azúcar", 100, "g"),
                Ingrediente("canela en rama", 1, "unidad"),
                Ingrediente("limón", 1, "unidad"),
                Ingrediente("agua", 100, "ml"),
            ],
            pasos=[
                {"tipo": "corte", "operacion": "trocear", "duracion": 20, "velocidad": 5, "descripcion": "Pelar y trocear las manzanas"},
                {"tipo": "temperatura", "operacion": "hervir", "duracion": 900, "temperatura": 100, "velocidad": 1, "descripcion": "Cocinar con azúcar y canela"},
                {"tipo": "corte", "operacion": "picar", "duracion": 30, "velocidad": 6, "descripcion": "Triturar hasta obtener compota"},
            ],
            tiempo_total=950, porciones=6, dificultad="Fácil", es_fabrica=True
        )

    # ==================== CRUD ====================

    def get_all_recipes(self, incluir_fabrica: bool = True) -> List[Receta]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if incluir_fabrica:
                cursor.execute('SELECT * FROM recetas ORDER BY es_fabrica DESC, nombre')
            else:
                cursor.execute('SELECT * FROM recetas WHERE es_fabrica = 0 ORDER BY nombre')
            rows = cursor.fetchall()
            conn.close()
            return [Receta.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al obtener recetas: {e}")
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[Receta]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM recetas WHERE id = ?', (recipe_id,))
            row = cursor.fetchone()
            conn.close()
            return Receta.from_dict(dict(row)) if row else None
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al obtener receta: {e}")
    
    def add_recipe(self, receta: Receta, es_fabrica: bool = False) -> int:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            receta.es_fabrica = es_fabrica
            datos = receta.to_dict()
            cursor.execute('''
                INSERT INTO recetas (nombre, descripcion, ingredientes, pasos, tiempo_total, porciones, dificultad, es_fabrica)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (datos['nombre'], datos['descripcion'], datos['ingredientes'], datos['pasos'],
                  datos['tiempo_total'], datos['porciones'], datos['dificultad'], datos['es_fabrica']))
            recipe_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return recipe_id
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al añadir receta: {e}")
    
    def delete_user_recipe(self, recipe_id: int) -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM recetas WHERE id = ? AND es_fabrica = 0', (recipe_id,))
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            return affected > 0
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al eliminar receta: {e}")
    
    def get_recipe_count(self, solo_fabrica: bool = False) -> int:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if solo_fabrica:
                cursor.execute('SELECT COUNT(*) FROM recetas WHERE es_fabrica = 1')
            else:
                cursor.execute('SELECT COUNT(*) FROM recetas')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al contar recetas: {e}")

    # ==================== ACTUALIZAR RECETA ====================
    
    def update_recipe(self, receta: Receta) -> bool:
        """Actualiza una receta existente (solo recetas de usuario)."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            datos = receta.to_dict()
            cursor.execute('''
                UPDATE recetas SET 
                    nombre = ?, descripcion = ?, ingredientes = ?, pasos = ?,
                    tiempo_total = ?, porciones = ?, dificultad = ?
                WHERE id = ? AND es_fabrica = 0
            ''', (datos['nombre'], datos['descripcion'], datos['ingredientes'], datos['pasos'],
                  datos['tiempo_total'], datos['porciones'], datos['dificultad'], receta.id))
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            return affected > 0
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al actualizar receta: {e}")

    def duplicate_recipe(self, recipe_id: int, nuevo_nombre: str = None) -> int:
        """Duplica una receta (útil para clonar recetas de fábrica)."""
        try:
            receta_original = self.get_recipe_by_id(recipe_id)
            if not receta_original:
                raise DatabaseError("Receta no encontrada")
            
            nombre = nuevo_nombre or f"{receta_original.nombre} (copia)"
            nueva_receta = Receta(
                nombre=nombre,
                descripcion=receta_original.descripcion,
                ingredientes=receta_original.ingredientes.copy(),
                pasos=receta_original.pasos.copy(),
                tiempo_total=receta_original.tiempo_total,
                porciones=receta_original.porciones,
                dificultad=receta_original.dificultad,
                es_fabrica=False
            )
            return self.add_recipe(nueva_receta, es_fabrica=False)
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al duplicar receta: {e}")

    # ==================== FAVORITOS ====================
    
    def add_favorite(self, recipe_id: int) -> bool:
        """Añade una receta a favoritos."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO favoritos (receta_id) VALUES (?)', (recipe_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al añadir favorito: {e}")
    
    def remove_favorite(self, recipe_id: int) -> bool:
        """Elimina una receta de favoritos."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM favoritos WHERE receta_id = ?', (recipe_id,))
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            return affected > 0
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al eliminar favorito: {e}")
    
    def is_favorite(self, recipe_id: int) -> bool:
        """Comprueba si una receta está en favoritos."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM favoritos WHERE receta_id = ?', (recipe_id,))
            result = cursor.fetchone() is not None
            conn.close()
            return result
        except sqlite3.Error as e:
            return False
    
    def get_favorites(self) -> List[Receta]:
        """Obtiene todas las recetas favoritas."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.* FROM recetas r
                INNER JOIN favoritos f ON r.id = f.receta_id
                ORDER BY f.fecha_agregado DESC
            ''')
            rows = cursor.fetchall()
            conn.close()
            return [Receta.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al obtener favoritos: {e}")

    def get_favorite_ids(self) -> set:
        """Obtiene los IDs de las recetas favoritas."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT receta_id FROM favoritos')
            ids = {row[0] for row in cursor.fetchall()}
            conn.close()
            return ids
        except sqlite3.Error as e:
            return set()

    # ==================== HISTORIAL ====================
    
    def start_execution(self, receta: Receta, porciones: int = None) -> int:
        """Registra el inicio de una ejecución."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO historial (receta_id, receta_nombre, porciones_cocinadas)
                VALUES (?, ?, ?)
            ''', (receta.id, receta.nombre, porciones or receta.porciones))
            exec_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return exec_id
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al registrar ejecución: {e}")
    
    def finish_execution(self, exec_id: int, completada: bool = True, duracion_real: int = 0) -> bool:
        """Registra el fin de una ejecución."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE historial SET 
                    fecha_fin = CURRENT_TIMESTAMP,
                    duracion_real = ?,
                    completada = ?,
                    cancelada = ?
                WHERE id = ?
            ''', (duracion_real, 1 if completada else 0, 0 if completada else 1, exec_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al finalizar ejecución: {e}")
    
    def get_history(self, limit: int = 50) -> List[dict]:
        """Obtiene el historial de ejecuciones."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT h.*, r.dificultad, r.tiempo_total as tiempo_estimado
                FROM historial h
                LEFT JOIN recetas r ON h.receta_id = r.id
                ORDER BY h.fecha_inicio DESC
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al obtener historial: {e}")
    
    def get_stats(self) -> dict:
        """Obtiene estadísticas de uso."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Total de ejecuciones
            cursor.execute('SELECT COUNT(*) FROM historial')
            total_ejecuciones = cursor.fetchone()[0]
            
            # Completadas
            cursor.execute('SELECT COUNT(*) FROM historial WHERE completada = 1')
            completadas = cursor.fetchone()[0]
            
            # Canceladas
            cursor.execute('SELECT COUNT(*) FROM historial WHERE cancelada = 1')
            canceladas = cursor.fetchone()[0]
            
            # Receta más cocinada
            cursor.execute('''
                SELECT receta_nombre, COUNT(*) as veces
                FROM historial
                GROUP BY receta_nombre
                ORDER BY veces DESC
                LIMIT 1
            ''')
            row = cursor.fetchone()
            receta_favorita = dict(row) if row else None
            
            # Tiempo total cocinando
            cursor.execute('SELECT SUM(duracion_real) FROM historial WHERE completada = 1')
            tiempo_total = cursor.fetchone()[0] or 0
            
            # Recetas únicas cocinadas
            cursor.execute('SELECT COUNT(DISTINCT receta_nombre) FROM historial')
            recetas_unicas = cursor.fetchone()[0]
            
            conn.close()
            return {
                'total_ejecuciones': total_ejecuciones,
                'completadas': completadas,
                'canceladas': canceladas,
                'tasa_exito': round(completadas / total_ejecuciones * 100, 1) if total_ejecuciones > 0 else 0,
                'receta_favorita': receta_favorita,
                'tiempo_total_segundos': tiempo_total,
                'recetas_unicas': recetas_unicas
            }
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al obtener estadísticas: {e}")

    def clear_history(self) -> bool:
        """Limpia todo el historial."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM historial')
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al limpiar historial: {e}")

    # ==================== NOTAS DE RECETAS ====================
    
    def add_note(self, receta_id: int, nota: str) -> int:
        """Añade una nota a una receta."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO notas_recetas (receta_id, nota) VALUES (?, ?)', (receta_id, nota))
            note_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return note_id
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al añadir nota: {e}")
    
    def get_notes(self, receta_id: int) -> list:
        """Obtiene todas las notas de una receta."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM notas_recetas WHERE receta_id = ? ORDER BY fecha DESC', (receta_id,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            return []
    
    def delete_note(self, note_id: int) -> bool:
        """Elimina una nota."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM notas_recetas WHERE id = ?', (note_id,))
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            return affected > 0
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al eliminar nota: {e}")
