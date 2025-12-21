"""
Sistema de Control para Robot de Cocina
Punto de entrada principal de la aplicación
"""

from nicegui import ui
from database.db_handler import DatabaseHandler
from ui.main_interface import MainInterface
import sys


def main():
    """Función principal de la aplicación."""
    try:
        # Inicializar base de datos
        print("Inicializando base de datos...")
        db = DatabaseHandler()
        db.initialize_database()
        print(f"✓ Base de datos lista. Recetas disponibles: {db.get_recipe_count()}")
        
        # Crear interfaz principal
        print("Creando interfaz de usuario...")
        interface = MainInterface(db)
        interface.create_ui()
        print("✓ Interfaz creada")
        
        # Configuración del servidor
        print("\n" + "="*60)
        print("🤖 SISTEMA DE CONTROL PARA ROBOT DE COCINA")
        print("="*60)
        print("\nServidor iniciado en: http://localhost:8080")
        print("\nCaracterísticas:")
        print("  ✓ Modo Manual: Control directo de operaciones")
        print("  ✓ Cocina Guiada: Recetas paso a paso")
        print("  ✓ Gestión de Recetas: CRUD completo")
        print("  ✓ Factory Reset: Restaurar recetas de fábrica")
        print("\nPrincipos POO implementados:")
        print("  • Abstracción (Clase base Tarea)")
        print("  • Herencia (TareaCorte, TareaTemperatura, TareaMecanica)")
        print("  • Polimorfismo (método ejecutar() personalizado)")
        print("  • Encapsulamiento (propiedades privadas del Robot)")
        print("\nPresiona Ctrl+C para detener el servidor")
        print("="*60 + "\n")
        
        # Iniciar servidor NiceGUI
        ui.run(
            title="Control Robot de Cocina",
            port=8080,
            reload=False,
            show=True,
            favicon="🤖"
        )
        
    except KeyboardInterrupt:
        print("\n\n✓ Servidor detenido correctamente")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()