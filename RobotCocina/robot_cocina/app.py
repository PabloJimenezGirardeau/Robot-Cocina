"""
=================================================================
ROBOT DE COCINA - APLICACIÓN PRINCIPAL
=================================================================
Punto de entrada de la aplicación.

Tecnologías:
- NiceGUI: Framework de UI web con Python
- SQLite: Base de datos local
- AsyncIO: Programación asíncrona

Autor: Pablo Jimenez
=================================================================
"""

from nicegui import ui
from database.db_handler import DatabaseHandler
from ui.main_interface import MainInterface


def main():
    """
    Función principal.
    Inicializa la base de datos y lanza la interfaz.
    """
    print("=" * 60)
    print("  ROBOT DE COCINA PRO v4.0")
    print("  Sistema de Control Automatizado")
    print("=" * 60)
    
    # Inicializar base de datos
    print("[APP] Inicializando base de datos...")
    db = DatabaseHandler("data/robot_cocina.db")
    db.initialize_database()
    print(f"[APP] Base de datos lista. {db.get_recipe_count()} recetas disponibles.")
    
    # Crear interfaz
    print("[APP] Creando interfaz de usuario...")
    interface = MainInterface(db)
    
    # Página principal
    @ui.page('/')
    def index():
        interface.create_ui()
    
    # Configurar y lanzar servidor
    print("[APP] Iniciando servidor web...")
    print("[APP] Abre http://localhost:8080 en tu navegador")
    print("=" * 60)
    
    ui.run(
        title="Robot de Cocina Pro",
        favicon="🍳",
        port=8080,
        reload=False,
        show=True
    )


if __name__ == "__main__":
    main()
