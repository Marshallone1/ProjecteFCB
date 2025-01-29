import sqlite3
import os

# Ruta absoluta para la base de datos en el directorio `~/ProjecteFCB`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(project_root, 'tickets.db')

def setup_database():
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tabla de oferta
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS oferta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            boca INTEGER NOT NULL,
            fila TEXT NOT NULL,
            asiento TEXT NOT NULL,
            processed INTEGER DEFAULT 0
        )
    ''')

    # Crear tabla de demanda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demanda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            boca INTEGER,
            fila INTEGER,
            asiento INTEGER,
            name TEXT,
            dni TEXT,
            pedido TEXT NOT NULL,
            processed INTEGER DEFAULT 0,
            match_names INTEGER DEFAULT 0
        )
    ''')

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

    print(f"Base de datos creada en: {db_path}")

if __name__ == "__main__":
    setup_database()