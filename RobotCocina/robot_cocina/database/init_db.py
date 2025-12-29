"""
Script para inicializar la base de datos.
"""

from database.db_handler import DatabaseHandler


def init_database():
    """Inicializa la base de datos con las recetas de fábrica."""
    print("Inicializando base de datos...")
    db = DatabaseHandler("data/robot_cocina.db")
    db.initialize_database()
    print(f"Base de datos inicializada con {db.get_recipe_count()} recetas.")


if __name__ == "__main__":
    init_database()
