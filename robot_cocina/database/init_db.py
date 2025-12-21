"""
Script de inicialización de base de datos.
Crea las tablas y carga recetas de fábrica.
"""

import sys
from pathlib import Path

# Añadir el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_handler import DatabaseHandler


def initialize():
    """Inicializa la base de datos con datos de fábrica."""
    print("\n" + "="*60)
    print("INICIALIZACIÓN DE BASE DE DATOS")
    print("="*60 + "\n")
    
    try:
        db = DatabaseHandler()
        
        print("1. Creando tablas...")
        db.initialize_database()
        print("   ✓ Tablas creadas correctamente")
        
        print("\n2. Cargando recetas de fábrica...")
        count = db.get_recipe_count(solo_fabrica=True)
        print(f"   ✓ {count} recetas de fábrica disponibles")
        
        print("\n3. Verificando integridad...")
        todas = db.get_all_recipes()
        print(f"   ✓ Total de recetas en BD: {len(todas)}")
        
        print("\nRecetas de fábrica disponibles:")
        print("-" * 60)
        for receta in [r for r in todas if r.es_fabrica]:
            print(f"  • {receta.nombre} ({receta.tiempo_str}) - {receta.dificultad}")
        
        print("\n" + "="*60)
        print("✓ BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    initialize()