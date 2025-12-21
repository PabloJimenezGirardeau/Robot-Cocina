"""
Modelo de datos para recetas.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import json


@dataclass
class Ingrediente:
    """Representa un ingrediente con su cantidad."""
    nombre: str
    cantidad: float
    unidad: str
    
    def __str__(self) -> str:
        return f"{self.cantidad} {self.unidad} de {self.nombre}"
    
    def to_dict(self) -> Dict:
        return {
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "unidad": self.unidad
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Ingrediente':
        return Ingrediente(
            nombre=data["nombre"],
            cantidad=data["cantidad"],
            unidad=data["unidad"]
        )


class Receta:
    """Representa una receta completa."""
    
    def __init__(
        self,
        nombre: str,
        descripcion: str,
        ingredientes: List[Ingrediente],
        pasos: List[Dict],
        tiempo_total: int,
        porciones: int = 4,
        dificultad: str = "Media",
        id: Optional[int] = None,
        es_fabrica: bool = False
    ):
        """
        Inicializa una receta.
        
        Args:
            nombre: Nombre de la receta
            descripcion: Descripción breve
            ingredientes: Lista de ingredientes
            pasos: Lista de pasos (cada paso es un dict con tarea)
            tiempo_total: Tiempo total en segundos
            porciones: Número de porciones
            dificultad: Fácil, Media o Difícil
            id: ID en la base de datos
            es_fabrica: Si es receta de fábrica (no borrable)
        """
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.ingredientes = ingredientes
        self.pasos = pasos
        self.tiempo_total = tiempo_total
        self.porciones = porciones
        self.dificultad = dificultad
        self.es_fabrica = es_fabrica
    
    @property
    def tiempo_str(self) -> str:
        """Retorna el tiempo en formato legible."""
        minutos = self.tiempo_total // 60
        if minutos < 60:
            return f"{minutos} min"
        else:
            horas = minutos // 60
            mins_restantes = minutos % 60
            if mins_restantes == 0:
                return f"{horas}h"
            return f"{horas}h {mins_restantes}min"
    
    @property
    def num_pasos(self) -> int:
        """Retorna el número de pasos."""
        return len(self.pasos)
    
    def to_dict(self) -> Dict:
        """Convierte la receta a diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "ingredientes": json.dumps([ing.to_dict() for ing in self.ingredientes]),
            "pasos": json.dumps(self.pasos),
            "tiempo_total": self.tiempo_total,
            "porciones": self.porciones,
            "dificultad": self.dificultad,
            "es_fabrica": 1 if self.es_fabrica else 0
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Receta':
        """Crea una receta desde un diccionario de BD."""
        ingredientes_data = json.loads(data["ingredientes"])
        ingredientes = [Ingrediente.from_dict(ing) for ing in ingredientes_data]
        
        return Receta(
            id=data.get("id"),
            nombre=data["nombre"],
            descripcion=data["descripcion"],
            ingredientes=ingredientes,
            pasos=json.loads(data["pasos"]),
            tiempo_total=data["tiempo_total"],
            porciones=data.get("porciones", 4),
            dificultad=data.get("dificultad", "Media"),
            es_fabrica=bool(data.get("es_fabrica", 0))
        )
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.tiempo_str}) - {self.num_pasos} pasos"
    
    def get_resumen(self) -> str:
        """Obtiene un resumen de la receta."""
        return (
            f"📖 {self.nombre}\n"
            f"⏱️ {self.tiempo_str} | "
            f"👥 {self.porciones} porciones | "
            f"📊 {self.dificultad}\n"
            f"{self.descripcion}"
        )