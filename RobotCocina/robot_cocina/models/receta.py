"""
=================================================================
MODELOS DE RECETA E INGREDIENTE
=================================================================
Usa dataclasses para representación limpia de datos.
Demuestra encapsulamiento y serialización.
=================================================================
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json


@dataclass
class Ingrediente:
    """
    Representa un ingrediente de una receta.
    
    Usa @dataclass para:
    - Generación automática de __init__, __repr__, __eq__
    - Código más limpio y mantenible
    """
    nombre: str
    cantidad: float
    unidad: str
    
    def __str__(self) -> str:
        """Representación legible del ingrediente."""
        if self.cantidad == 0 or self.unidad == "al gusto":
            return f"{self.nombre} (al gusto)"
        
        # Formatear cantidad
        if self.cantidad == int(self.cantidad):
            cant_str = str(int(self.cantidad))
        else:
            cant_str = f"{self.cantidad:.1f}"
        
        return f"{cant_str} {self.unidad} de {self.nombre}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa a diccionario."""
        return {
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "unidad": self.unidad
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Ingrediente':
        """Deserializa desde diccionario."""
        return cls(
            nombre=data.get("nombre", ""),
            cantidad=float(data.get("cantidad", 0)),
            unidad=data.get("unidad", "unidad")
        )


@dataclass
class Receta:
    """
    Representa una receta completa.
    
    ENCAPSULAMIENTO:
    - Propiedades calculadas para datos derivados
    - Métodos de serialización para persistencia
    """
    nombre: str
    descripcion: str
    ingredientes: List[Ingrediente]
    pasos: List[Dict[str, Any]]
    tiempo_total: int  # segundos
    porciones: int = 4
    dificultad: str = "Media"
    es_fabrica: bool = False
    id: Optional[int] = None
    
    @property
    def tiempo_str(self) -> str:
        """Tiempo formateado como string."""
        minutos = self.tiempo_total // 60
        segundos = self.tiempo_total % 60
        
        if minutos >= 60:
            horas = minutos // 60
            minutos = minutos % 60
            return f"{horas}h {minutos}min"
        elif minutos > 0:
            return f"{minutos} min" if segundos == 0 else f"{minutos}m {segundos}s"
        else:
            return f"{segundos}s"
    
    @property
    def num_pasos(self) -> int:
        """Número de pasos de la receta."""
        return len(self.pasos)
    
    @property
    def num_ingredientes(self) -> int:
        """Número de ingredientes."""
        return len(self.ingredientes)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa la receta a diccionario para BD."""
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "ingredientes": json.dumps([i.to_dict() for i in self.ingredientes]),
            "pasos": json.dumps(self.pasos),
            "tiempo_total": self.tiempo_total,
            "porciones": self.porciones,
            "dificultad": self.dificultad,
            "es_fabrica": 1 if self.es_fabrica else 0,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Receta':
        """Deserializa desde diccionario de BD."""
        # Parsear ingredientes
        ingredientes_raw = data.get("ingredientes", "[]")
        if isinstance(ingredientes_raw, str):
            ingredientes_data = json.loads(ingredientes_raw)
        else:
            ingredientes_data = ingredientes_raw
        
        ingredientes = [Ingrediente.from_dict(i) for i in ingredientes_data]
        
        # Parsear pasos
        pasos_raw = data.get("pasos", "[]")
        if isinstance(pasos_raw, str):
            pasos = json.loads(pasos_raw)
        else:
            pasos = pasos_raw
        
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre", "Sin nombre"),
            descripcion=data.get("descripcion", ""),
            ingredientes=ingredientes,
            pasos=pasos,
            tiempo_total=int(data.get("tiempo_total", 0)),
            porciones=int(data.get("porciones", 4)),
            dificultad=data.get("dificultad", "Media"),
            es_fabrica=bool(data.get("es_fabrica", False)),
        )
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.tiempo_str}, {self.num_pasos} pasos)"
