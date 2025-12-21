"""
Gestor de base de datos SQLite para el robot de cocina.
Maneja recetas de fábrica y de usuario.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
import json
from models.receta import Receta, Ingrediente
from models.tarea import TipoOperacion
from utils.exceptions import DatabaseError


class DatabaseHandler:
    """Maneja todas las operaciones de base de datos."""
    
    def __init__(self, db_path: str = "data/robot_cocina.db"):
        """Inicializa el manejador de BD."""
        self.db_path = db_path
        Path("data").mkdir(exist_ok=True)
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_database(self):
        """Crea las tablas necesarias si no existen."""
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
            
            conn.commit()
            conn.close()
            
            # Cargar recetas de fábrica si no existen
            if self.get_recipe_count(solo_fabrica=True) == 0:
                self.load_factory_recipes()
                
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al inicializar la base de datos: {e}")
    
    def load_factory_recipes(self):
        """Carga recetas de fábrica (no borrables)."""
        recetas_fabrica = [
            self._crear_receta_gazpacho(),
            self._crear_receta_pan(),
            self._crear_receta_sopa_verduras(),
            self._crear_receta_masa_pizza(),
            self._crear_receta_pure_patatas(),
            self._crear_receta_risotto(),
            self._crear_receta_crema_calabaza(),
            self._crear_receta_pollo_curry(),
        ]
        
        for receta in recetas_fabrica:
            self.add_recipe(receta, es_fabrica=True)
    
    # ==================== RECETAS DE FÁBRICA ====================
    
    def _crear_receta_gazpacho(self) -> Receta:
        """Receta: Gazpacho Andaluz."""
        ingredientes = [
            Ingrediente("tomates maduros", 1, "kg"),
            Ingrediente("pepino", 0.5, "unidad"),
            Ingrediente("pimiento verde", 0.5, "unidad"),
            Ingrediente("ajo", 1, "diente"),
            Ingrediente("aceite de oliva", 50, "ml"),
            Ingrediente("vinagre", 20, "ml"),
            Ingrediente("sal", 1, "pizca"),
        ]
        
        pasos = [
            {
                "tipo": "corte",
                "operacion": "trocear",
                "duracion": 15,
                "velocidad": 5,
                "descripcion": "Trocear todos los vegetales"
            },
            {
                "tipo": "corte",
                "operacion": "picar",
                "duracion": 30,
                "velocidad": 9,
                "descripcion": "Triturar hasta textura fina"
            },
        ]
        
        return Receta(
            nombre="Gazpacho Andaluz",
            descripcion="Refrescante sopa fría tradicional española",
            ingredientes=ingredientes,
            pasos=pasos,
            tiempo_total=45,
            porciones=4,
            dificultad="Fácil",
            es_fabrica=True
        )
    
    def _crear_receta_pan(self) -> Receta:
        """Receta: Pan Casero."""
        ingredientes = [
            Ingrediente("harina de fuerza", 500, "g"),
            Ingrediente("agua tibia", 300, "ml"),
            Ingrediente("levadura fresca", 20, "g"),
            Ingrediente("sal", 10, "g"),
            Ingrediente("aceite de oliva", 30, "ml"),
        ]
        
        pasos = [
            {
                "tipo": "mecanica",
                "nombre": "Mezclar",
                "duracion": 20,
                "velocidad": 3,
                "descripcion": "Mezclar todos los ingredientes"
            },
            {
                "tipo": "mecanica",
                "nombre": "Amasar",
                "duracion": 480,
                "velocidad": 4,
                "descripcion": "Amasar hasta masa elástica (reposo incluido)"
            },
        ]
        
        return Receta(
            nombre="Pan Casero",
            descripcion="Pan artesanal con corteza crujiente",
            ingredientes=ingredientes,
            pasos=pasos,
            tiempo_total=500,
            porciones=8,
            dificultad="Media",
            es_fabrica=True
        )
    
    def _crear_receta_sopa_verduras(self) -> Receta:
        """Receta: Sopa de Verduras."""
        ingredientes = [
            Ingrediente("zanahoria", 2, "unidades"),
            Ingrediente("calabacín", 1, "unidad"),
            Ingrediente("puerro", 1, "unidad"),
            Ingrediente("patata", 2, "unidades"),
            Ingrediente("caldo de verduras", 1, "litro"),
            Ingrediente("sal y pimienta", 1, "al gusto"),
        ]
        
        pasos = [
            {
                "tipo": "corte",
                "operacion": "trocear",
                "duracion": 20,
                "velocidad": 6,
                "descripcion": "Trocear todas las verduras"
            },
            {
                "tipo": "temperatura",
                "operacion": "sofreir",
                "duracion": 180,
                "temperatura": 120,
                "velocidad": 3,
                "descripcion": "Sofreír las verduras"
            },
            {
                "tipo": "temperatura",
                "operacion": "hervir",
                "duracion": 600,
                "temperatura": 100,
                "velocidad": 2,
                "descripcion": "Cocinar con el caldo"
            },
        ]
        
        return Receta(
            nombre="Sopa de Verduras",
            descripcion="Sopa casera nutritiva y reconfortante",
            ingredientes=ingredientes,
            pasos=pasos,
            tiempo_total=800,
            porciones=6,
            dificultad="Fácil",
            es_fabrica=True
        )
    
    def _crear_receta_masa_pizza(self) -> Receta:
        """Receta: Masa de Pizza."""
        ingredientes = [
            Ingrediente("harina", 400, "g"),
            Ingrediente("agua tibia", 250, "ml"),
            Ingrediente("levadura seca", 7, "g"),
            Ingrediente("sal", 8, "g"),
            Ingrediente("aceite de oliva", 30, "ml"),
            Ingrediente("azúcar", 5, "g"),
        ]
        
        pasos = [
            {
                "tipo": "mecanica",
                "nombre": "Mezclar",
                "duracion": 15,
                "velocidad": 2,
                "descripcion": "Mezclar ingredientes"
            },
            {
                "tipo": "mecanica",
                "nombre": "Amasar",
                "duracion": 300,
                "velocidad": 5,
                "descripcion": "Amasar hasta masa suave"
            },
        ]
        
        return Receta(
            nombre="Masa de Pizza",
            descripcion="Masa perfecta para pizza italiana",
            ingredientes=ingredientes,
            pasos=pasos,
            tiempo_total=315,
            porciones=4,
            dificultad="Fácil",
            es_fabrica=True
        )
    
    def _crear_receta_pure_patatas(self) -> Receta:
        """Receta: Puré de Patatas."""
        ingredientes = [
            Ingrediente("patatas", 1, "kg"),
            Ingrediente("leche", 150, "ml"),
            Ingrediente("mantequilla", 50, "g"),
            Ingrediente("sal", 1, "al gusto"),
            Ingrediente("nuez moscada", 1, "pizca"),
        ]
        
        pasos = [
            {
                "tipo": "corte",
                "operacion": "trocear",
                "duracion": 10,
                "velocidad": 4,
                "descripcion": "Trocear patatas"
            },
            {
                "tipo": "temperatura",
                "operacion": "hervir",
                "duracion": 900,
                "temperatura": 100,
                "velocidad": 1,
                "descripcion": "Hervir hasta blandas"
            },
            {
                "tipo": "corte",
                "operacion": "picar",
                "duracion": 40,
                "velocidad": 7,
                "descripcion": "Triturar con leche y mantequilla"
            },
        ]
        
        return Receta(
            nombre="Puré de Patatas",
            descripcion="Puré cremoso y suave",
            ingredientes=ingredientes,
            pasos=pasos,
            tiempo_total=950,
            porciones=4,
            dificultad="Fácil",
            es_fabrica=True
        )
    
    def _crear_receta_risotto(self) -> Receta:
        """Receta: Risotto de Champiñones."""
        ingredientes = [
            Ingrediente("arroz arborio", 300, "g"),
            Ingrediente("champiñones", 250, "g"),
            Ingrediente("caldo de pollo", 1, "litro"),
            Ingrediente("cebolla", 1, "unidad"),
            Ingrediente("vino blanco", 100, "ml"),
            Ingrediente("parmesano rallado", 50, "g"),
        ]
        
        pasos = [
            {
                "tipo": "corte",
                "operacion": "picar",
                "duracion": 15,
                "velocidad": 6,
                "descripcion": "Picar cebolla y champiñones"
            },
            {
                "tipo": "temperatura",
                "operacion": "sofreir",
                "duracion": 300,
                "temperatura": 130,
                "velocidad": 4,
                "descripcion": "Sofreír y cocinar con caldo"
            },
        ]
        
        return Receta(
            nombre="Risotto de Champiñones",
            descripcion="Risotto cremoso italiano",
            ingredientes=ingredientes,
            pasos=pasos,
            tiempo_total=315,
            porciones=4,
            dificultad="Media",
            es_fabrica=True
        )
    
    def _crear_receta_crema_calabaza(self) -> Receta:
        """Receta: Crema de Calabaza."""
        ingredientes = [
            Ingrediente("calabaza", 800, "g"),
            Ingrediente("cebolla", 1, "unidad"),
            Ingrediente("caldo de verduras", 500, "ml"),
            Ingrediente("nata líquida", 100, "ml"),
            Ingrediente("sal y pimienta", 1, "al gusto"),
        ]
        
        pasos = [
            {
                "tipo": "corte",
                "operacion": "trocear",
                "duracion": 15,
                "velocidad": 5,
                "descripcion": "Trocear calabaza y cebolla"
            },
            {
                "tipo": "temperatura",
                "operacion": "hervir",
                "duracion": 720,
                "temperatura": 100,
                "velocidad": 2,
                "descripcion": "Hervir hasta blanda"
            },
            {
                "tipo": "corte",
                "operacion": "picar",
                "duracion": 45,
                "velocidad": 8,
                "descripcion": "Triturar hasta cremoso"
            },
        ]
        
        return Receta(
            nombre="Crema de Calabaza",
            descripcion="Crema suave y aterciopelada",
            ingredientes=ingredientes,
            pasos=pasos,
            tiempo_total=780,
            porciones=4,
            dificultad="Fácil",
            es_fabrica=True
        )
    
    def _crear_receta_pollo_curry(self) -> Receta:
        """Receta: Pollo al Curry."""
        ingredientes = [
            Ingrediente("pechuga de pollo", 500, "g"),
            Ingrediente("cebolla", 1, "unidad"),
            Ingrediente("curry en polvo", 2, "cdas"),
            Ingrediente("leche de coco", 400, "ml"),
            Ingrediente("tomate triturado", 200, "g"),
            Ingrediente("jengibre", 1, "trozo"),
        ]
        
        pasos = [
            {
                "tipo": "corte",
                "operacion": "trocear",
                "duracion": 20,
                "velocidad": 6,
                "descripcion": "Trocear pollo y vegetales"
            },
            {
                "tipo": "temperatura",
                "operacion": "sofreir",
                "duracion": 900,
                "temperatura": 140,
                "velocidad": 3,
                "descripcion": "Cocinar con especias"
            },
        ]
        
        return Receta(
            nombre="Pollo al Curry",
            descripcion="Pollo especiado con leche de coco",
            ingredientes=ingredientes,
            pasos=pasos,
            tiempo_total=920,
            porciones=4,
            dificultad="Media",
            es_fabrica=True
        )
    
    # ==================== OPERACIONES CRUD ====================
    
    def get_all_recipes(self, incluir_fabrica: bool = True) -> List[Receta]:
        """
        Obtiene todas las recetas disponibles.
        
        Args:
            incluir_fabrica: Si incluir recetas de fábrica
        
        Returns:
            Lista de recetas
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if incluir_fabrica:
                cursor.execute('SELECT * FROM recetas ORDER BY es_fabrica DESC, nombre')
            else:
                cursor.execute('SELECT * FROM recetas WHERE es_fabrica = 0 ORDER BY nombre')
            
            rows = cursor.fetchall()
            conn.close()
            
            recetas = []
            for row in rows:
                receta_dict = dict(row)
                recetas.append(Receta.from_dict(receta_dict))
            
            return recetas
            
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al obtener recetas: {e}")
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[Receta]:
        """
        Obtiene una receta por su ID.
        
        Args:
            recipe_id: ID de la receta
        
        Returns:
            Receta o None si no existe
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM recetas WHERE id = ?', (recipe_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return Receta.from_dict(dict(row))
            return None
            
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al obtener receta: {e}")
    
    def add_recipe(self, receta: Receta, es_fabrica: bool = False) -> int:
        """
        Añade una receta a la base de datos.
        
        Args:
            receta: Receta a añadir
            es_fabrica: Si es receta de fábrica
        
        Returns:
            ID de la receta creada
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            receta.es_fabrica = es_fabrica
            datos = receta.to_dict()
            
            cursor.execute('''
                INSERT INTO recetas 
                (nombre, descripcion, ingredientes, pasos, tiempo_total, 
                 porciones, dificultad, es_fabrica)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos['nombre'],
                datos['descripcion'],
                datos['ingredientes'],
                datos['pasos'],
                datos['tiempo_total'],
                datos['porciones'],
                datos['dificultad'],
                datos['es_fabrica']
            ))
            
            recipe_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return recipe_id
            
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al añadir receta: {e}")
    
    def update_recipe(self, receta: Receta) -> bool:
        """
        Actualiza una receta existente.
        
        Args:
            receta: Receta con datos actualizados
        
        Returns:
            True si se actualizó correctamente
        """
        if receta.es_fabrica:
            raise DatabaseError("No se pueden modificar recetas de fábrica")
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            datos = receta.to_dict()
            
            cursor.execute('''
                UPDATE recetas 
                SET nombre = ?, descripcion = ?, ingredientes = ?, 
                    pasos = ?, tiempo_total = ?, porciones = ?, dificultad = ?
                WHERE id = ? AND es_fabrica = 0
            ''', (
                datos['nombre'],
                datos['descripcion'],
                datos['ingredientes'],
                datos['pasos'],
                datos['tiempo_total'],
                datos['porciones'],
                datos['dificultad'],
                receta.id
            ))
            
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            
            return rows_affected > 0
            
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al actualizar receta: {e}")
    
    def delete_user_recipe(self, recipe_id: int) -> bool:
        """
        Elimina una receta de usuario.
        
        Args:
            recipe_id: ID de la receta
        
        Returns:
            True si se eliminó correctamente
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Solo eliminar si no es de fábrica
            cursor.execute(
                'DELETE FROM recetas WHERE id = ? AND es_fabrica = 0',
                (recipe_id,)
            )
            
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            
            return rows_affected > 0
            
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al eliminar receta: {e}")
    
    def factory_reset(self) -> int:
        """
        Elimina todas las recetas de usuario, mantiene las de fábrica.
        
        Returns:
            Número de recetas eliminadas
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM recetas WHERE es_fabrica = 0')
            rows_deleted = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            return rows_deleted
            
        except sqlite3.Error as e:
            raise DatabaseError(f"Error en factory reset: {e}")
    
    def get_recipe_count(self, solo_fabrica: bool = False) -> int:
        """
        Obtiene el número de recetas.
        
        Args:
            solo_fabrica: Contar solo recetas de fábrica
        
        Returns:
            Número de recetas
        """
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